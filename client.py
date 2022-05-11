import socket
import msvcrt
import time
import sys
import typer
import utils
from packets.answer import Answer
from packets.information import Information
from packets.auth import Auth
from packets.opcode import OpCode
from utils import xor_encode, xor_decode

app = typer.Typer()
MAX_LENGTH = 1024


@app.command()
async def client(host: str, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (host, port)

    # Send key
    key = utils.generate_key(8)
    auth_packet = Auth(key).construct_datagram()
    sock.sendto(auth_packet, address)

    # Receive the first ack packet
    data, _ = sock.recvfrom(MAX_LENGTH)
    data = xor_decode(data, key, as_bytes=False)
    if data[0] != OpCode.ack.value:
        return typer.echo(typer.style("Failed to connect to server: No response received", fg=typer.colors.RED))

    # Send the chosen name
    name = str(input("Enter your name!"))
    name_packet = Information(name, key).construct_datagram()
    sock.sendto(name_packet, address)

    # Receive the first notify packet
    notify, _ = sock.recvfrom(MAX_LENGTH)
    notify = xor_decode(notify, key, as_bytes=False)
    if notify[0] != OpCode.notify.value:
        return typer.echo(typer.style("Server has not received your name yet", fg=typer.colors.RED))
    typer.echo(notify[1:])

    # Start the game
    while True:
        # Receive the question packet
        question, _ = sock.recvfrom(MAX_LENGTH)
        question = xor_decode(question, key, as_bytes=False)

        if question[0] == OpCode.question.value:
            typer.echo(question[1:])

        # Get/send answer
        try:
            answer = input_with_timeout("running", 5)
        except TimeoutExpired:
            answer = None
            typer.echo(typer.style('Sorry, times up', fg=typer.colors.RED))

        answer_packet = Answer(answer, key).construct_datagram()
        sock.sendto(answer_packet, address)

        # Check the ack packet to ensure that the server has received the answer
        ack, _ = sock.recvfrom(MAX_LENGTH)
        if xor_decode(ack, key, as_bytes=False)[0] != OpCode.ack.value:
            return typer.echo(typer.style("Server has not received your answer yet", fg=typer.colors.RED))

        # Receive notify packet, then check the winner
        notify, _ = sock.recvfrom(MAX_LENGTH)
        notify = xor_decode(notify, key, as_bytes=False)
        typer.echo(notify[1:])


class TimeoutExpired(Exception):
    pass


def input_with_timeout(prompt, timeout, timer=time.monotonic):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche())  # XXX can it block on multibyte characters?
            if result[-1] == '\r':
                return ''.join(result[:-1])
        time.sleep(0.04)  # just to yield to other processes/threads
    raise TimeoutExpired
