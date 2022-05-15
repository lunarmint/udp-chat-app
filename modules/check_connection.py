import socket
import time
from threading import Thread, Event
from modules.send_message import sending
import typer


class CheckConnection(Thread):
    def __init__(self, sock: socket.socket, dataset: {}, active_users: [], event: Event, delay: int):
        Thread.__init__(self)
        self.sock = sock
        self.dataset = dataset
        self.active_users = active_users
        self.stopped = event
        self.delay = delay

    def run(self):
        while not self.stopped.wait(self.delay):
            for addr in self.active_users:
                user = self.dataset.get(addr)
                current_time = round(time.time() * 1000)
                if (current_time - user.last_heartbeat) > 3000:
                    self.active_users.remove(addr)
                    message = f"{user.name} left"
                    sending(self.sock, self.dataset, self.active_users, addr, message, type="yellow_notify")
                    typer.echo(typer.style(message, fg=typer.colors.YELLOW))