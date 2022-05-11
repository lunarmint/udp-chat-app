from opcode import OpCode
from utils import xor_encode


class Ack:
    def __init__(self, data: str, key: str):
        self.opcode = OpCode.Ack.value
        self.data = data
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.data
        return xor_encode(packet, self.key)
