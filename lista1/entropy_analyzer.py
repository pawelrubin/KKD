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
            for line in file:
                for i, c in enumerate(line):
                    stats[c] += 1
                    cond_stats[(c, line[i - 1] if i > 0 else 0)] += 1

        self.entropy = sum(-math.log2(v / size) * (v / size) for v in stats.values())

        self.cond_entropy = sum(
            v
            / size
            * sum(
                vv / v * -math.log2(vv / v)
                for kk, vv in cond_stats.items()
                if kk[0] == k
            )
            for k, v in stats.items()
        )

    def print(self) -> None:
        print(f"Results for {self.filename}")
        print(f"Entropy             = {self.entropy}")
        print(f"Conditional Entropy = {self.cond_entropy}")


if __name__ == "__main__":
    filename = sys.argv[1]

    analyzer = EntropyAnalyzer(filename)

    analyzer.print()
