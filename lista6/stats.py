from functools import singledispatch
from itertools import chain
from typing import Iterable, List, Literal, TypeVar

from tga import Pixel, BitMap

T = TypeVar("T")


def _flatten(lst: Iterable[Iterable[T]]) -> List[T]:
    return list(chain.from_iterable(lst))


def _euclid_squared(a: int, b: int) -> int:
    return (a - b) ** 2


def MSE(origin: List[int], new: List[int]) -> float:
    return (1 / len(origin)) * sum(_euclid_squared(a, b) for a, b in zip(origin, new))


def SNR(pixels: List[int], mse: float):
    return (1 / len(pixels)) * sum(_euclid_squared(p, 0) for p in pixels) / mse


def get_colors(
    pixels: List[Pixel], color: Literal["red", "green", "blue"]
) -> List[int]:
    return [getattr(pixel, color) for pixel in pixels]


def print_stats(origin: BitMap, new: BitMap) -> None:
    origin_flat = _flatten(origin.pixels)
    new_flat = _flatten(new.pixels)
    mse = MSE(_flatten(origin_flat), _flatten(new_flat))
    print(f"MSE       = {mse}")
    print(
        f"MSE red   = {MSE(get_colors(origin_flat, 'red'), get_colors(new_flat, 'red'))}"
    )
    print(
        f"MSE green = {MSE(get_colors(origin_flat, 'green'), get_colors(new_flat, 'green'))}"
    )
    print(
        f"MSE blue  = {MSE(get_colors(origin_flat, 'blue'), get_colors(new_flat, 'blue'))}"
    )
    print(f"SNR       = {SNR(_flatten(origin_flat), mse)}")
