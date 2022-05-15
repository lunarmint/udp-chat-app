import socket
import time
from threading import Event

import typer

from modules import utils
from modules.check_connection import CheckConnection
from modules.user import User
from modules.utils import xor_decode
from modules.send_message import sending
from packets.ack import Ack
from packets.information import Information
from packets.non_exist import NonExist
from packets.opcode import OpCode

app = typer.Typer()
MAX_LENGTH = 1024


@app.command()
def server(port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("", port))
        typer.echo(f"[STARTING] {socket.gethostname()} is listening on {port}/udp")
        dataset = {}
        active_users = []
        history = []
        running(sock, dataset, active_users, history)
    except socket.error as error:
        typer.echo(typer.style(f"[SERVER] Failed to create socket: {error}", fg=typer.colors.RED))
        sock.shutdown(socket.SOCK_DGRAM)
        sock.close()
    except KeyboardInterrupt:
        typer.echo(typer.style(f"[SERVER] Keyboard interruption. Terminating...", fg=typer.colors.RED))
        sock.shutdown(socket.SOCK_DGRAM)
        sock.close()
    finally:
        sock.close()


def running(sock: socket.socket, dataset: {}, active_users: [], history: []):
    # Create a thread to check the connection
    stopFlag = Event()
    connection_thread = CheckConnection(sock, dataset, active_users, stopFlag, 2)
    connection_thread.start()

    while True:
        data, address = sock.recvfrom(MAX_LENGTH)

        if address not in dataset:
            data = data.decode("utf-8")
            opcode = int(data[0])
            if opcode == OpCode.Auth.value:
                name = data[1:]

                # Send the Ack packet back to client
                key = utils.generate_key(8)
                ack_packet = Ack(key).construct_datagram()
                sock.sendto(ack_packet, address)

                # Add the new user to dataset
                user = User(address, name, key, round(time.time() * 1000))
                dataset.update({address: user})
                active_users.append(address)

                # Send notify
                message = f"{name} joined the conversation"
                sending(sock, dataset, active_users, address, message, type="green_notify")
                typer.echo(typer.style(message, fg=typer.colors.GREEN))
            elif opcode == OpCode.Exist.value:
                non_exist_packet = NonExist().construct_datagram()
                sock.sendto(non_exist_packet, address)
            elif opcode == OpCode.Error.value:
                typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            else:
                typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))

        else:
            main_user = dataset.get(address)
            if address not in active_users:
                active_users.append(address)
                user = dataset.get(address)
                user.update_heartbeat()
                data = data.decode("utf-8")

                # Send notify
                message = f"{user.name} has reconnected"
                sending(sock, dataset, active_users, address, message, type="green_notify")
                typer.echo(typer.style(user.name + " ", fg=typer.colors.GREEN))
            else:
                data = xor_decode(data, main_user.key, as_bytes=False)

            opcode = int(data[0])
            if opcode == OpCode.Msg.value:
                message = str(data[1:])
                sending(sock, dataset, active_users, address, message, type="message")
                history.append(message)
            elif opcode == OpCode.Heartbeat.value:
                main_user.update_heartbeat()
                if address not in active_users:
                    active_users.append(address)
            elif opcode == OpCode.Exist.value:
                info_packet = Information(main_user.name, main_user.key, history).construct_datagram()
                sock.sendto(info_packet, address)
            elif opcode == OpCode.Error.value:
                typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            else:
                typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))


if __name__ == "__main__":
    app()
