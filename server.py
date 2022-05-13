import socket
import time
from threading import Event

import typer

from modules import utils
from modules.check_connection import CheckConnection
from modules.user import User
from modules.utils import xor_decode
from packets.ack import Ack
from packets.message import Message
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
        running(sock, dataset, active_users)
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


def running(sock: socket.socket, dataset: {}, active_users: []):
    # Create a thread to check the connection
    stopFlag = Event()
    connection_thread = CheckConnection(dataset, active_users, stopFlag, 2)
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
            elif opcode == OpCode.Error.value:
                typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            else:
                typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))
        else:
            user = dataset.get(address)
            data = xor_decode(data, user.key, as_bytes=False)
            opcode = int(data[0])

            if opcode == OpCode.Msg.value:
                message = str(data[1:]).split("\t")
                user_name, msg = message[0], message[1]
                for user in active_users:
                    msg_packet = Message(user_name, msg, user.key).construct_datagram()
                    sock.sendto(msg_packet, user.address)
            elif opcode == OpCode.Heartbeat.value:
                user = dataset.get(address)
                user.update_heartbeat()
                if user not in active_users:
                    active_users.append(user)
            elif opcode == OpCode.Error.value:
                typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            else:
                typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))

        stopFlag.set()


if __name__ == "__main__":
    app()
