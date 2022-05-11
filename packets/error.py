from enum import Enum
from opcode import OpCode
from utils import xor_encode


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
    def __init__(self, error: int, key: str):
        self.opcode = OpCode.error.value
        self.error = error
        self.key = key

    def construct_datagram(self) -> bytes:
        error_name = "error" + str(self.error)
        error_value = ErrorCode[error_name].value
        packet = str(self.opcode) + error_value
        return xor_encode(packet, self.key)
