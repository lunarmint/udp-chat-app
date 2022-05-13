import time


class User:
    def __init__(self, address: (str, int), name: str, key: str, last_heartbeat: int):
        self.address = address
        self.name = name
        self.key = key
        self.last_heartbeat = last_heartbeat

    def update_heartbeat(self):
        self.last_heartbeat = round(time.time() * 1000)