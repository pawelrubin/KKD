import math
from typing import List

from lgb import generate, euclid_squared, Vector


def MSE(bitmap1: list, bitmap2: list) -> float:
    return (1 / len(bitmap1)) * sum(
        [euclid_squared(bitmap1[i], bitmap2[i]) ** 2 for i in range(len(bitmap1))]
    )


def SNR(xs: List[Vector], mse: float) -> float:
    def square_sum(xs: list) -> float:
        return sum(i ** 2 for i in xs)

    x_len = len(xs)
    return sum(map(square_sum, xs)) / (mse * x_len)


def quantify(bitmap: List[Vector], colors: int) -> List[Vector]:
    codebook = generate(bitmap, colors)
    new_bitmap = []
    for pixel in bitmap:
        diffs = [euclid_squared(pixel, x) for x in codebook]
        new_bitmap.append(codebook[diffs.index(min(diffs))])
    return new_bitmap
