import os
from typing import List, Union

from predictors import PredictionPixel

BitMap = List[List[PredictionPixel]]


class TGAParser:
    def __init__(self, file: Union[str, bytes, int]):
        with open(file, "rb") as f:
            tga = f.read()

        self._width = tga[13] * 256 + tga[12]
        self._height = tga[15] * 256 + tga[14]

        self._bitmap = tga[18:-26]

    def get_pixels(self) -> BitMap:
        pixels: BitMap = [[] for _ in range(self._height)]

        for i in range(self._height):
            row_loc = self._width * i
            for j in range(self._width):
                pixel_loc = (row_loc + j) * 3
                pixels[i].append(
                    PredictionPixel(
                        blue=self._bitmap[pixel_loc],
                        green=self._bitmap[pixel_loc + 1],
                        red=self._bitmap[pixel_loc + 2],
                    )
                )

        return list(reversed(pixels))
