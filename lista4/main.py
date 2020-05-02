from collections import defaultdict
from math import log2, log
from pprint import pprint
from sys import argv
from typing import Dict

from tga import TGAParser, BitMap
from predictors import predictors, PredictionPixel, PredictionNeighboring
from encoder import encode


def bitmap_entropy(
    pixels: BitMap, component=None,
):
    stats: Dict[int, int] = defaultdict(int)
    size = 0
    for row in pixels:
        for pixel in row:
            if component is not None:
                stats[getattr(pixel, component)] += 1
                size += 1
            else:
                stats[pixel.red] += 1
                stats[pixel.green] += 1
                stats[pixel.blue] += 1
                size += 3

    size_log = log2(size)
    entropy = sum((size_log - log2(count)) * count for count in stats.values())

    return entropy / size


def get_entropies(pixels: BitMap):
    return {
        "general": bitmap_entropy(pixels, None),
        "red": bitmap_entropy(pixels, "red"),
        "green": bitmap_entropy(pixels, "green"),
        "blue": bitmap_entropy(pixels, "blue"),
    }


def main():
    file = argv[1]
    pixels = TGAParser(file).get_pixels()
    predictors_entropies = {}

    print("Entropies for tga image.")
    pprint(get_entropies(pixels))
    print(31 * "-")
    print("Entropies for encoded image, per predictor.")
    for predictor in predictors:
        encoded = encode(pixels, predictor)
        entropies = get_entropies(encoded)
        predictors_entropies[predictor.__name__] = entropies
        print("\033[32m" + predictor.__name__ + "\033[0m")
        pprint(entropies)
        print(31 * "-")

    best_predictor = lambda stat: min(
        predictors_entropies.items(), key=lambda predictor: predictor[1][stat]
    )

    print("--------Best predictors--------")
    print(f"general: {best_predictor('general')}")
    print(f"red: {best_predictor('red')}")
    print(f"green: {best_predictor('green')}")
    print(f"blue: {best_predictor('blue')}")


if __name__ == "__main__":
    main()
