import random
import string
from itertools import cycle
from typing import Union


def xor_encode(data: Union[bytes, str], key: str) -> bytes:
    if isinstance(data, str):
        data = bytes(data, "utf-8")

    key = bytes(key, "utf-8")
    encrypted = [x ^ y for (x, y) in zip(data, cycle(key))]
    return bytes(encrypted)


def xor_decode(data: bytes, key: str, as_bytes: bool = True) -> Union[bytes, str]:
    key = bytes(key, "utf-8")
    decrypted = [x ^ y for (x, y) in zip(data, cycle(key))]
    decrypted_bytes = bytes(decrypted)
    if not as_bytes:
        return decrypted_bytes.decode()
    return decrypted_bytes


def generate_key(length: int):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
