import math
from collections import defaultdict


def entropy(freq, num_of_symbols):
    return sum(
        f / num_of_symbols * -math.log(f / num_of_symbols, 2) for f in freq.values()
    )


def get_frequencies(file_bytes):
    freq = defaultdict(int)
    for symbol in file_bytes:
        freq[symbol] += 1
    return freq


def stats(uncompressed: bytes, compressed: bytes):
    freq = get_frequencies(uncompressed)
    com_freq = get_frequencies(compressed)

    _len = len(uncompressed)
    com_len = len(compressed)

    print(f"Entropy:                    {entropy(freq, _len)}")
    print(f"Entropy after compression:  {entropy(com_freq, com_len)}")
    print(f"Size:                       {_len} bytes")
    print(f"Size after compression:     {com_len} bytes")
    print(f"Compression ratio:          {com_len / _len}")
