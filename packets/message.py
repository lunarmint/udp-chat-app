from packets.opcode import OpCode
from modules.utils import xor_encode


class Message:
    def __init__(self, content: str, key: str):
        self.opcode = OpCode.Msg.value
        self.content = content
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.content
        return xor_encode(packet, self.key)
