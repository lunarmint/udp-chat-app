from packets.opcode import OpCode


class Information:
    def __init__(self, name: str, key: str, history: []):
        self.opcode = OpCode.Information.value
        self.name = name
        self.key = key
        self.history = '\n'.join(history)

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.name + "\t" + self.key + "\t" + self.history
        return bytearray(packet.encode("utf-8"))