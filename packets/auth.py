from opcode import OpCode


class Auth:
    def __init__(self, key: str):
        self.opcode = OpCode.auth.value
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.key
        return bytearray(packet.encode("utf-8"))
