from packets.opcode import OpCode
from modules.utils import xor_encode


class Message:
    def __init__(self, user_name: str, content: str, key: str):
        self.opcode = OpCode.Msg.value
        self.user_name = user_name
        self.content = content
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.user_name + "\t" + self.content
        return xor_encode(packet, self.key)
