from dataclasses import dataclass


@dataclass
class PredictionPixel:
    red: int
    green: int
    blue: int

    def __add__(self, other):
        return PredictionPixel(
            red=self.red + other.red,
            green=self.green + other.green,
            blue=self.blue + other.blue,
        )

    def __sub__(self, other):
        return PredictionPixel(
            red=self.red - other.red,
            green=self.green - other.green,
            blue=self.blue - other.blue,
        )

    def __floordiv__(self, other):
        return PredictionPixel(
            red=self.red // other, green=self.green // other, blue=self.blue // other
        )

    def __mod__(self, other):
        return PredictionPixel(
            red=self.red % other, green=self.green % other, blue=self.blue % other
        )


@dataclass
class PredictionNeighboring:
    """
    Standard neighboring model for predictors.

    [c][a]
    [b][x] <- current pixel
    """

    a: PredictionPixel
    b: PredictionPixel
    c: PredictionPixel


def _1(n: PredictionNeighboring):
    return n.b


def _2(n: PredictionNeighboring):
    return n.a


def _3(n: PredictionNeighboring):
    return n.c


def _4(n: PredictionNeighboring):
    return n.b + n.a - n.c


def _5(n: PredictionNeighboring):
    return n.b + (n.a - n.c) // 2


def _6(n: PredictionNeighboring):
    return n.a + (n.b - n.c) // 2


def _7(n: PredictionNeighboring):
    return (n.b + n.a) // 2


def LOCO_I(n: PredictionNeighboring):
    """
    LOCO-I predictor.
    Calculated for every color component separately.

    https://www.hpl.hp.com/loco/dcc96copy.pdf*

    *note that the pixels [a][b] in the paper are swapped.
    """

    def for_component(a, b, c):
        if c >= max(a, b):
            return min(a, b)
        if c <= min(a, b):
            return max(a, b)
        return a + b - c

    return PredictionPixel(
        red=for_component(n.a.red, n.b.red, n.c.red),
        green=for_component(n.a.green, n.b.green, n.c.green),
        blue=for_component(n.a.blue, n.b.blue, n.c.blue),
    )


predictors = [_1, _2, _3, _4, _5, _6, _7, LOCO_I]
