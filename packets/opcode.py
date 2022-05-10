from enum import Enum


class OpCode(Enum):
    auth = 0
    ack = 1
    info = 2
    question = 3
    answer = 4
    notify = 5
    heartbeat = 6
    error = 7
