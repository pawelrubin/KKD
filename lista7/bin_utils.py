def to_bitstring(data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in data)


def to_bytes(bitstring: str) -> bytes:
    return bytes(int(bitstring[i : i + 8], 2) for i in range(0, len(bitstring), 8))
