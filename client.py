import socket
from threading import Event

import typer

from modules.heart_beat_task import HeartBeatTask
from modules.receive_message_task import ReceiveMsgTask
from packets.auth import Auth
from packets.exist import Exist
from packets.message import Message
from packets.opcode import OpCode

app = typer.Typer()
MAX_LENGTH = 1024


@app.command()
def client(client_port: int, host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", client_port))
    address = (host, port)

    # Check if it is the first time to connect to server
    exist_packet = Exist().construct_datagram()
    sock.sendto(exist_packet, address)

    key = None
    user_name = None
    history = None
    while True:
        data, _ = sock.recvfrom(MAX_LENGTH)
        data = data.decode("utf-8")
        opcode = int(data[0])
        if opcode == OpCode.Information.value:
            infor = str(data[1:]).split("\t")
            user_name, key, history = infor[0], infor[1], infor[2]
            break
        elif opcode == OpCode.NonExist.value:
            break
        elif opcode == OpCode.Error.value:
            typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            break
        else:
            typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))
            break

    if key:
        typer.echo("Reconnected! Welcome Back...")
        typer.echo(history)
    else:
        # Send Auth
        user_name = str(input("Enter your name: "))
        name_packet = Auth(user_name).construct_datagram()
        sock.sendto(name_packet, address)

        # Receive ACK packet
        while True:
            data, _ = sock.recvfrom(MAX_LENGTH)
            data = data.decode("utf-8")
            opcode = int(data[0])
            if opcode == OpCode.Ack.value:
                key = data[1:]
                typer.echo("Successfully connected to server")
                break
            elif opcode == OpCode.Error.value:
                typer.echo(typer.style(data[1:], fg=typer.colors.RED))
                break
            else:
                typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))
                break

    # Running
    running(sock, address, user_name, key)


def running(sock: socket.socket, address: (str, int), name: str, key: str):
    # Create a thread to check the heartbeat
    connected = Event()
    heartbeat_thread = HeartBeatTask(sock, address, connected, 2, key)
    heartbeat_thread.start()

    # Create a thread to receive message
    receive_msg_thread = ReceiveMsgTask(sock, connected, 0, key)
    receive_msg_thread.start()

    # Send message
    while True:
        message = input()
        if message != "":
            if message == "exit":
                connected.set()
                typer.echo(typer.style("DISCONNECTED!", fg=typer.colors.RED))
                break
            message = f"{name}: {message}"
            msg_packet = Message(message, key).construct_datagram()
            sock.sendto(msg_packet, address)

    sock.shutdown(socket.SOCK_DGRAM)
    sock.close()


if __name__ == "__main__":
    app()
