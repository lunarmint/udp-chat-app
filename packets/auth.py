from packets.opcode import OpCode


class Auth:
    def __init__(self, name: str):
        self.opcode = OpCode.Auth.value
        self.name = name

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.name
        return bytearray(packet.encode("utf-8"))