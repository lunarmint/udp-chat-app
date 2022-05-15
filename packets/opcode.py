from enum import Enum


class OpCode(Enum):
    Ack = 0
    Auth = 1
    Msg = 2
    Heartbeat = 3
    Error = 4
    Exist = 5
    NonExist = 6
    Information = 7
    Green = 8
    Yellow = 9
