from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass
class Pixel:
    red: int
    green: int
    blue: int

    def __add__(self, other: Pixel) -> Pixel:
        return Pixel(
            red=self.red + other.red,
            green=self.green + other.green,
            blue=self.blue + other.blue,
        )

    def __sub__(self, other: Pixel) -> Pixel:
        return Pixel(
            red=self.red - other.red,
            green=self.green - other.green,
            blue=self.blue - other.blue,
        )

    def __mul__(self, number: int) -> Pixel:
        return Pixel(self.red * number, self.green * number, self.blue * number)

    def __floordiv__(self, other: int) -> Pixel:
        return Pixel(
            red=self.red // other, green=self.green // other, blue=self.blue // other
        )

    def __iter__(self):
        yield from (self.red, self.green, self.blue)

    def quantify(self, step: int) -> Pixel:
        return Pixel(
            self.red // step * step, self.green // step * step, self.blue // step * step
        )

    def normalize(self) -> None:
        def _normalize(component: int) -> int:
            if component < 0:
                return 0
            if component > 255:
                return 255
            return component

        self.red = _normalize(self.red)
        self.green = _normalize(self.green)
        self.blue = _normalize(self.blue)


@dataclass
class BitMap:
    pixels: List[List[Pixel]]
    width: int
    height: int

    def __getitem__(self, pos: Tuple[int, int]) -> Pixel:
        x, y = pos

        x = min(self.width - 1, max(0, x))

        y = min(self.height - 1, max(0, y))

        return self.pixels[y][x]


class TGAParser:
    def __init__(self, file: str):
        with open(file, "rb") as f:
            tga = f.read()
        self._header = tga[:18]
        self.width = tga[13] * 256 + tga[12]
        self.height = tga[15] * 256 + tga[14]
        self.image_size = self.width * self.height * 3
        self.bitmap = tga[18 : self.image_size + 18]
        self._footer = tga[self.image_size + 18 :]

    @staticmethod
    def _get_pixels(
        bitmap_bytes: Sequence[int], width: int, height: int
    ) -> List[List[Pixel]]:
        pixels = [[] for _ in range(height)]

        for i in range(height):
            row_loc = width * i
            for j in range(width):
                pixel_loc = (row_loc + j) * 3
                pixels[i].append(
                    Pixel(
                        blue=bitmap_bytes[pixel_loc],
                        green=bitmap_bytes[pixel_loc + 1],
                        red=bitmap_bytes[pixel_loc + 2],
                    )
                )

        return pixels

    @classmethod
    def sequence_to_bitmap(
        cls, bitmap_bytes: Sequence[int], width: int, height: int
    ) -> BitMap:
        pixels = cls._get_pixels(bitmap_bytes, width, height)

        return BitMap(pixels, width, height)

    def get_bitmap(self) -> BitMap:
        pixels = self._get_pixels(self.bitmap, self.width, self.height)

        return BitMap(list(reversed(pixels)), self.width, self.height)

    @staticmethod
    def bitmap_to_array(bitmap: BitMap) -> List[int]:
        payload = []
        for row in bitmap.pixels:
            for pixel in row:
                payload += [pixel.blue, pixel.green, pixel.red]
        return payload

    def new_tga(self, bitmap: BitMap, filename: str) -> None:
        with open(filename, "wb") as f:
            f.write(self._header + bytes(self.bitmap_to_array(bitmap)) + self._footer)

    def new_tga_from_bytes(self, encoded: bytes, filename: str) -> None:
        with open(filename, "wb") as f:
            f.write(self._header + encoded + self._footer)
