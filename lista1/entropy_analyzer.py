#!/usr/local/bin/python3.8
import math
import os
import sys
from collections import defaultdict
from typing import Dict, Tuple


class EntropyAnalyzer:
    def __init__(self, filename: str):
        self.filename: str = filename
        size: int = os.stat(filename).st_size
        stats: Dict[int, int] = defaultdict(int)
        cond_stats: Dict[Tuple[int, int], int] = defaultdict(int)

        with open(filename, "br") as file:
            for i, c in enumerate(file_bytes := file.read()):
                stats[c] += 1
                cond_stats[(c, file_bytes[i - 1] if i > 0 else 0)] += 1

        size_log = math.log2(size)
        self.entropy = 0.0
        self.cond_entropy = 0.0

        for curr_byte, curr_byte_count in stats.items():
            cb_log = math.log2(curr_byte_count)
            self.entropy += (size_log - cb_log) * curr_byte_count
            for bytes_pair, bytes_pair_count in cond_stats.items():
                if bytes_pair[0] == curr_byte:
                    self.cond_entropy += bytes_pair_count * (
                        cb_log - math.log2(bytes_pair_count)
                    )

        self.entropy /= size
        self.cond_entropy /= size

    def print(self) -> None:
        print(f"Results for {self.filename}")
        print(f"Entropy             = {self.entropy}")
        print(f"Conditional Entropy = {self.cond_entropy}")


if __name__ == "__main__":
    filename = sys.argv[1]

    analyzer = EntropyAnalyzer(filename)

    analyzer.print()
