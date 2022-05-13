import time
from threading import Thread, Event


class CheckConnection(Thread):
    def __init__(self, dataset: {}, active_users: [], event: Event, delay: int):
        Thread.__init__(self)
        self.dataset = dataset
        self.active_users = active_users
        self.stopped = event
        self.delay = delay

    def run(self):
        while not self.stopped.wait(self.delay):
            for key in self.dataset:
                user = self.dataset.get(key)
                current_time = round(time.time() * 1000)
                if (current_time - user.last_heartbeat) > 60000:
                    self.dataset.pop(key)
                    self.active_users.remove(user)