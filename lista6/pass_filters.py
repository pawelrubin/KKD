from tga import BitMap, Pixel

LOW_FILTER = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
HIGH_FILTER = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]


def _filter_pixel(bitmap: BitMap, x: int, y: int, high: bool = False) -> Pixel:
    pass_filter = HIGH_FILTER if high else LOW_FILTER

    result = Pixel(0, 0, 0)
    for i in range(-1, 2):
        for j in range(-1, 2):
            result += bitmap[x + i, y + j] * pass_filter[i + 1][j + 1]

    weights_sum = sum([sum(row) for row in pass_filter])

    result = result // (weights_sum or 1)

    result.normalize()

    return result


def filter_bitmap(bitmap: BitMap, high: bool = False) -> BitMap:
    pixels = [
        [_filter_pixel(bitmap, x, y, high) for x in range(bitmap.width)]
        for y in range(bitmap.height)
    ]
    return BitMap(list(reversed(pixels)), bitmap.width, bitmap.height)
