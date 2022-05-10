from opcode import OpCode


class Notify:
    def __init__(self, name: str):
        self.opcode = OpCode.notify.value
        self.name = name

    def construct_datagram(self) -> bytes:
        string = str(self.opcode) + self.name
        return bytearray(string.encode("utf-8"))
