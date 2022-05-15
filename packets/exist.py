from packets.opcode import OpCode


class Exist:
    def __init__(self):
        self.opcode = OpCode.Exist.value

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode)
        return bytearray(packet.encode("utf-8"))