from dataclasses import dataclass
from typing import List, Union


class TGAParser:
    def __init__(self, file: str):
        with open(file, "rb") as f:
            tga = f.read()
        self._header = tga[:18]
        self._footer = tga[:-26]
        self._width = tga[13] * 256 + tga[12]
        self._height = tga[15] * 256 + tga[14]
        self._bitmap = tga[18:-26]

    def get_bitmap(self) -> List[List[int]]:
        pixels = []

        for i in range(self._height * self._width):
            pixel_loc = i * 3
            pixels.append(
                [
                    self._bitmap[pixel_loc],
                    self._bitmap[pixel_loc + 1],
                    self._bitmap[pixel_loc + 2],
                ]
            )

        return pixels

    def bitmap_to_bytes(self, bitmap: List[List[int]]) -> bytes:
        payload = []
        for x in bitmap:
            for i in x:
                payload.append(i)
        return bytes(payload)

    def new_tga(self, bitmap: List[List[int]], filename: str) -> None:
        with open(filename, "wb") as f:
            f.write(self._header + self.bitmap_to_bytes(bitmap) + self._footer)
