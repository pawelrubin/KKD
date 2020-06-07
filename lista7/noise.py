from random import random

from bin_utils import to_bitstring, to_bytes


def flip(bit: str):
    return str(int(bit) ^ 1)


def add_noise(source: bytes, p: float) -> bytes:
    bitstring = to_bitstring(source)
    result = ""
    for bit in bitstring:
        result += flip(bit) if p < random() else bit
    return to_bytes(bitstring)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("p", type=float)
    parser.add_argument("input_file", type=str)
    parser.add_argument("output_file", type=str)

    args = parser.parse_args()

    with open(args.input_file, "rb") as in_file, open(
        args.output_file, "wb"
    ) as out_file:
        out_file.write(add_noise(in_file.read(), args.p))


if __name__ == "__main__":
    main()
