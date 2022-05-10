from opcode import OpCode


class Heartbeat:
    def __init__(self, index):
        self.opcode = OpCode.heartbeat.value
        self.index = index

    def construct_datagram(self) -> bytes:
        string = str(self.opcode) + str(self.index)
        return bytearray(string.encode("utf-8"))
