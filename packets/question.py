from opcode import OpCode


class Question:
    def __init__(self):
        self.opcode = OpCode.question.value

    def construct_datagram(self, data) -> bytes:
        packet = (str(self.opcode) + data).encode("utf-8")
        return bytearray(packet)
