from socket import socket
from threading import Thread, Event
import typer
from packets.heartbeat import Heartbeat


class HeartBeatTask(Thread):
    def __init__(self, sock: socket, address: str, event: Event, delay: int, key: str):
        Thread.__init__(self)
        self.sock = sock
        self.address = address
        self.stopped = event
        self.delay = delay
        self.key = key

    def run(self):
        index = 1
        while not self.stopped.wait(self.delay):
            heartbeat_packet = Heartbeat(index, self.key).construct_datagram()
            self.sock.sendto(heartbeat_packet, self.address)
            index += 1
        typer.echo(typer.style("DISCONNECTED!", fg=typer.colors.RED))
