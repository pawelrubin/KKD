from typing import Optional

from bin_utils import to_bitstring, to_bytes

hamming_codes = [
    "00000000",
    "11010010",
    "01010101",
    "10000111",
    "10011001",
    "01001011",
    "11001100",
    "00011110",
    "11100001",
    "00110011",
    "10110100",
    "01100110",
    "01111000",
    "10101010",
    "00101101",
    "11111111",
]


def from_hamming(byte: str) -> Optional[str]:
    for code in hamming_codes:
        errors = 0
        for p, q in zip(byte, code):
            if p != q:
                errors += 1

        if errors == 0:
            return byte[2] + byte[4] + byte[5] + byte[6]

        if errors == 1:
            return code[2] + code[4] + code[5] + code[6]

    return None


def decode(source: bytes):
    bitstring = to_bitstring(source)
    decoded = ""
    errors = 0

    while len(bitstring) >= 8:
        nibble = from_hamming(bitstring[0:8])
        decoded += nibble or "0000"
        errors += nibble is None
        bitstring = bitstring[8:]

    print(f"Number of blocks with more than 1 error: {errors}")

    return to_bytes(decoded)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("output_file", type=str)

    args = parser.parse_args()

    with open(args.input_file, "rb") as in_file, open(
        args.output_file, "wb"
    ) as out_file:
        out_file.write(decode(in_file.read()))


if __name__ == "__main__":
    main()
