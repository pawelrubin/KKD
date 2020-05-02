from typing import Callable
from predictors import PredictionPixel, PredictionNeighboring
from tga import BitMap

EMPTY_PIXEL = PredictionPixel(0, 0, 0)


def encode(
    pixels: BitMap, predictor: Callable[[PredictionNeighboring], PredictionPixel],
):
    result: BitMap = [[] for _ in range(len(pixels))]
    for i, row in enumerate(pixels):
        for j, pixel in enumerate(row):
            if i != 0:
                a = pixels[i - 1][j]
            else:
                a = EMPTY_PIXEL

            if j != 0:
                b = pixels[i][j - 1]
            else:
                b = EMPTY_PIXEL

            if i != 0 and j != 0:
                c = pixels[i - 1][j - 1]
            else:
                c = EMPTY_PIXEL

            neighboring = PredictionNeighboring(a, b, c)
            encoded_pixel = (pixel - predictor(neighboring)) % 256
            result[i].append(encoded_pixel)

    return result
