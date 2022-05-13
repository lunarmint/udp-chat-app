import typer
import socket
from threading import Event
from packets.auth import Auth
from packets.opcode import OpCode
from packets.message import Message
from modules.heart_beat_task import HeartBeatTask
from modules.receive_message_task import ReceiveMsgTask

app = typer.Typer()
MAX_LENGTH = 1024


@app.command()
async def client(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (host, port)

    # Send Auth
    name = str(input("Enter your name: "))
    name_packet = Auth(name).construct_datagram()
    sock.sendto(name_packet, address)

    # Receive ACK packet
    key = None
    while True:
        data, _ = sock.recvfrom(MAX_LENGTH)
        data = data.decode("utf-8")
        opcode = int(data[0])
        if opcode == OpCode.Ack.value:
            key = data[1:]
            break
        elif opcode == OpCode.Error.value:
            typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            break
        else:
            typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))
            break

    # Running
    if key:
        typer.echo("Successfully connected to server")
        running(sock, address, name, key)
    else:
        typer.echo("Unable to connect to server")


def running(sock: socket.socket, address: (str, int), name: str, key: str):
    # Create a thread to check the heartbeat
    stopFlag = Event()
    heartbeat_thread = HeartBeatTask(sock, address, stopFlag, 2, key)
    heartbeat_thread.start()

    # Create a thread to receive message
    connected = Event()
    receive_msg_thread = ReceiveMsgTask(sock, connected, key)
    receive_msg_thread.start()

    # Send message
    while True:
        message = input(name + ": ")
        if message == "STOP":
            stopFlag.set()
            connected.set()
            break
        msg_packet = Message(name, message, key)
        sock.sendto(msg_packet, address)