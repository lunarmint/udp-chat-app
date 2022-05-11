from opcode import OpCode
from utils import xor_encode


class Heartbeat:
    def __init__(self, index: int, key: str):
        self.opcode = OpCode.heartbeat.value
        self.index = index
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + str(self.index)
        return xor_encode(packet, self.key)
