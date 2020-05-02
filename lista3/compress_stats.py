from math import log2
from collections import defaultdict


def entropy(symbols):
    stats = defaultdict(int)
    size = 0

    for symbol in symbols:
        stats[symbol] += 1
        size += 1

    size_log = log2(size)
    entropy = sum((size_log - log2(count)) * count for count in stats.values())

    return entropy / size


def stats(uncompressed: bytes, compressed: bytes):
    _len = len(uncompressed)
    com_len = len(compressed)

    print(f"Entropy:                    {entropy(uncompressed)}")
    print(f"Entropy after compression:  {entropy(compressed)}")
    print(f"Size:                       {_len} bytes")
    print(f"Size after compression:     {com_len} bytes")
    print(f"Compression ratio:          {_len / com_len}")
