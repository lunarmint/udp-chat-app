from opcode import OpCode


class Ack:
    def __init__(self):
        self.opcode = OpCode.Ack.value

    def construct_datagram(self, data) -> bytes:
        packet = (str(self.opcode) + data).encode("utf-8")
        return bytearray(packet)
