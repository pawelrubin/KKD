from functools import reduce
from typing import Iterable

from bin_utils import to_bitstring, to_bytes


def calc_parity(bitstring: str, indices: Iterable[int]) -> str:
    return str(
        reduce(lambda acc, index: acc + (bitstring[index] == "1"), indices, 0) % 2
    )


def to_hamming(bits: str) -> str:
    p1 = calc_parity(bits, [0, 1, 3])
    p2 = calc_parity(bits, [0, 2, 3])
    p3 = calc_parity(bits, [1, 2, 3])

    code_word = p1 + p2 + bits[0] + p3 + bits[1:]
    parity = calc_parity(code_word, range(7))

    return code_word + parity


def encode(source: bytes) -> bytes:
    bitstring = to_bitstring(source)

    result = ""
    while len(bitstring) >= 4:
        result += to_hamming(bitstring[0:4])
        bitstring = bitstring[4:]

    return to_bytes(result)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("output_file", type=str)

    args = parser.parse_args()

    with open(args.input_file, "rb") as in_file, open(
        args.output_file, "wb"
    ) as out_file:
        out_file.write(encode(in_file.read()))


if __name__ == "__main__":
    main()
