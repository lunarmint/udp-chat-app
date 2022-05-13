from enum import Enum
from packets.opcode import OpCode


class ErrorCode(Enum):
    error0 = "Not defined, see error message (if any)."
    error1 = "File not found."
    error2 = "Access violation."
    error3 = "Disk full or allocation exceeded."
    error4 = "Illegal TFTP operation."
    error5 = "Unknown transfer ID."
    error6 = "File already exists."
    error7 = "No such user."
    error8 = "Transfer terminated due to option negotiation."


class Error:
    def __init__(self, error: int):
        self.opcode = OpCode.Error.value
        self.error = error

    def construct_datagram(self) -> bytes:
        error_code = "error" + str(self.error)
        error_content = ErrorCode[error_code].value
        packet = str(self.opcode) + error_content
        return bytearray(packet.encode("utf-8"))
