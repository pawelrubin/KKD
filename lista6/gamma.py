from typing import List


def encode(num: int) -> str:
    """Encodes given int."""
    bitstring = format(num, "b")
    return "0" * (len(bitstring) - 1) + bitstring


def decode(bitstring: str) -> List[int]:
    """Decodes given bitstring."""
    codes = []
    padding_count = 0
    index = 0
    while index < len(bitstring):
        if bitstring[index] == "0":
            padding_count += 1
            index += 1
        else:
            codes.append(int(bitstring[index : index + padding_count + 1], 2))
            index += padding_count + 1
            padding_count = 0
    return codes
