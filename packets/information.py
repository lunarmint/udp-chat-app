from opcode import OpCode
from utils import xor_encode


class Information:
    def __init__(self, name: str, key: str):
        self.opcode = OpCode.info.value
        self.name = name
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.name
        return xor_encode(packet, self.key)