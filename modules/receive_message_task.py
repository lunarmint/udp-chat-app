from socket import socket
from threading import Thread, Event
import typer
from packets.opcode import OpCode
from modules.utils import xor_decode

MAX_LENGTH = 1024


class ReceiveMsgTask(Thread):
    def __init__(self, sock: socket, event: Event, key: str):
        Thread.__init__(self)
        self.sock = sock
        self.stopped = event
        self.key = key

    def run(self):
        while not self.stopped.wait(0):
            data, _ = self.sock.recvfrom(MAX_LENGTH)
            data = xor_decode(data, self.key, as_bytes=False)
            opcode = int(data[0])
            if opcode == OpCode.Msg.value:
                message = str(data[1:]).split("\t")
                user_name, msg = message[0], message[1]
                typer.echo(user_name + ": " + msg)
            elif opcode == OpCode.Error.value:
                typer.echo(typer.style(data[1:], fg=typer.colors.RED))
            else:
                typer.echo(typer.style("Receive unknown data: " + data, fg=typer.colors.RED))