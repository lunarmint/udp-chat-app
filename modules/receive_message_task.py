from socket import socket
from threading import Thread, Event
import typer
from packets.opcode import OpCode
from modules.utils import xor_decode

MAX_LENGTH = 1024


class ReceiveMsgTask(Thread):
    def __init__(self, sock: socket, event: Event, delay: int, key: str):
        Thread.__init__(self)
        self.sock = sock
        self.stopped = event
        self.delay = delay
        self.key = key

    def run(self):
        while not self.stopped.wait(self.delay):
            try:
                data, _ = self.sock.recvfrom(MAX_LENGTH)
                data = xor_decode(data, self.key, as_bytes=False)
                opcode = int(data[0])
                if opcode == OpCode.Msg.value:
                    message = str(data[1:])
                    typer.echo(message)
                elif opcode == OpCode.Green.value:
                    message = str(data[1:])
                    typer.echo(typer.style(message, fg=typer.colors.GREEN))
                elif opcode == OpCode.Yellow.value:
                    message = str(data[1:])
                    typer.echo(typer.style(message, fg=typer.colors.YELLOW))
                elif opcode == OpCode.Error.value:
                    typer.echo(typer.style(data[1:], fg=typer.colors.RED))
                else:
                    typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))
            except:
                break