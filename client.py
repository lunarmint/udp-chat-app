import socket

import typer

import utils
from utils import xor_encode, xor_decode
from packets.auth import Auth
from packets.opcode import OpCode

app = typer.Typer()


@app.command()
async def client(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    key = utils.generate_key(8)
    auth_packet = Auth.construct_datagram(key)
    sock.sendto(auth_packet, (host, port))

    data, address = sock.recvfrom(1024)
    if xor_decode(data, key)[1] != OpCode.ack.value:
        return typer.echo(typer.style("Failed to connect to server: No response received", fg=typer.colors.RED))

    data, address = sock.recvfrom(1024)
    if not xor_decode(data, key)[1] == OpCode.info.value:
        return typer.echo()
