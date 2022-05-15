from socket import socket

import typer

from packets.green_notify import GreenNotify
from packets.message import Message
from packets.yellow_notify import YellowNotify


def sending(sock: socket, dataset: {}, active_users: [], address: (str, int), message: str, type: str):
    global packet
    for key in active_users:
        if key == address:
            continue
        user = dataset.get(key)
        if type == "message":
            packet = Message(message, user.key).construct_datagram()
        elif type == "green_notify":
            packet = GreenNotify(message, user.key).construct_datagram()
        elif type == "yellow_notify":
            packet = YellowNotify(message, user.key).construct_datagram()

        try:
            sock.sendto(packet, user.address)
        except NameError:
            typer.echo(typer.style(NameError, fg=typer.colors.RED))