from opcode import OpCode


class Information:
    def __init__(self, name: str):
        self.opcode = OpCode.info.value
        self.name = name

    def construct_datagram(self) -> bytes:
        string = str(self.opcode) + self.name
        return bytearray(string.encode("utf-8"))
