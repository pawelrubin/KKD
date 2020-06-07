from math import ceil
from typing import Tuple

from bin_utils import to_bitstring


def diff(file1: bytes, file2: bytes) -> Tuple[bool, int]:
    bits1 = to_bitstring(file1)
    bits2 = to_bitstring(file2)

    diffs = ceil(abs(len(bits1) - len(bits2)) / 4)
    for i in range(0, len(bits1), 4):
        if bits1[i : i + 4] != bits2[i : i + 4]:
            diffs += 1

    return diffs != 0, diffs


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file1", type=str)
    parser.add_argument("file2", type=str)

    args = parser.parse_args()

    with open(args.file1, "rb") as f1, open(args.file2, "rb") as f2:
        differ, diffs = diff(f1.read(), f2.read())
        if differ:
            print(f"Files differ in {diffs} 4-bits blocks.")


if __name__ == "__main__":
    main()
