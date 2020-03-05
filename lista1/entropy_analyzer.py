#!/usr/bin/python3
import math
import os
import sys
from collections import defaultdict
from typing import Dict


class EntropyAnalyzer:
    def __init__(self, filename: str):
        self.filename: str = filename
        size: int = os.stat(filename).st_size
        stats: Dict[int, int] = defaultdict(int)
        cond_stats: Dict[(int, int), int] = defaultdict(int)

        with open(filename, "br") as file:
            file_bytes = file.read()
            for i, c in enumerate(file_bytes):
                stats[c] += 1
                cond_stats[(c, file_bytes[i - 1] if i > 0 else 0)] += 1

        size_log = math.log2(size)

        self.entropy = (
            sum(-(math.log2(v) - size_log) * v for v in stats.values()) / size
        )

        self.cond_entropy = (
            sum(
                sum(
                    vv * -(math.log2(vv) - math.log2(v))
                    for kk, vv in cond_stats.items()
                    if kk[0] == k
                )
                for k, v in stats.items()
            )
            / size
        )

    def print(self) -> None:
        print(f"Results for {self.filename}")
        print(f"Entropy             = {self.entropy}")
        print(f"Conditional Entropy = {self.cond_entropy}")


if __name__ == "__main__":
    filename = sys.argv[1]

    analyzer = EntropyAnalyzer(filename)

    analyzer.print()
