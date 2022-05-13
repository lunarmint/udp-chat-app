from packets.opcode import OpCode


class Ack:
    def __init__(self, key: str):
        self.opcode = OpCode.Ack.value
        self.key = key

    def construct_datagram(self) -> bytes:
        packet = str(self.opcode) + self.key
        return bytearray(packet.encode("utf-8"))
