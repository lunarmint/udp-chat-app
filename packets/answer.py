from opcode import OpCode


class Answer:
    def __init__(self):
        self.opcode = OpCode.answer.value

    def construct_datagram(self, data) -> bytes:
        packet = (str(self.opcode) + data).encode("utf-8")
        return bytearray(packet)
