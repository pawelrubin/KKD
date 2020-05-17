import math
from collections import defaultdict
from functools import reduce
from typing import List, Tuple, Union


_size_data = 0
_dim = 0


Vector = Union[List[float], List[int]]
CodeBook = List[Vector]


def generate(
    data: List[Vector], size_codebook: int, epsilon: float = 0.001
) -> CodeBook:
    data_size = len(data)

    codebook = []

    c0 = _avg_vec_of_vecs(data)
    codebook.append(c0)

    avg_dist = _avg_distortion_c0(c0, data, data_size)

    while len(codebook) < size_codebook:
        codebook, avg_dist = _split(data, codebook, epsilon, avg_dist)

    return [list(map(math.floor, vector)) for vector in codebook]


def _split(
    data: list, codebook: CodeBook, epsilon: float, initial_avg_dist: float
) -> Tuple[CodeBook, float]:
    data_size = len(data)

    new_codevectors: List[Vector] = []
    for c in codebook:
        new_codevectors.append(_new_codevector(c, epsilon))
        new_codevectors.append(_new_codevector(c, -epsilon))

    codebook = new_codevectors
    len_codebook = len(codebook)

    print(f"current codebook size: {len_codebook}")

    avg_dist = 0.0
    err = epsilon + 1
    while err > epsilon:
        closest_c_list: List[Vector] = [None] * data_size
        vecs_near_c = defaultdict(list)
        vec_idxs_near_c = defaultdict(list)
        for i, vec in enumerate(data):
            min_dist = None
            closest_c_index = None
            for i_c, c in enumerate(codebook):
                d = euclid_squared(vec, c)
                if min_dist is None or d < min_dist:
                    min_dist = d
                    closest_c_list[i] = c
                    closest_c_index = i_c
            vecs_near_c[closest_c_index].append(vec)
            vec_idxs_near_c[closest_c_index].append(i)

        for i_c in range(len_codebook):
            vecs = vecs_near_c.get(i_c) or []
            num_vecs_near_c = len(vecs)
            if num_vecs_near_c > 0:
                new_c = _avg_vec_of_vecs(vecs)
                codebook[i_c] = new_c
                for i in vec_idxs_near_c[i_c]:
                    closest_c_list[i] = new_c

        prev_avg_dist = avg_dist if avg_dist > 0 else initial_avg_dist
        avg_dist = _avg_distortion_c_list(closest_c_list, data, data_size)

        err = (prev_avg_dist - avg_dist) / prev_avg_dist

    return codebook, avg_dist


def _avg_vec_of_vecs(vecs: List[Vector]) -> Vector:
    size = len(vecs)
    avg_vec = [0.0] * 3
    for vec in vecs:
        for i, x in enumerate(vec):
            avg_vec[i] += x / size

    return avg_vec


def _new_codevector(c: Vector, e: float) -> Vector:
    return [x * (1.0 + e) for x in c]


def _avg_distortion_c0(c0: Vector, data: List[Vector], size: int) -> float:
    return reduce(
        lambda s, d: s + d / size, (euclid_squared(c0, vec) for vec in data), 0.0
    )


def _avg_distortion_c_list(c_list: List[Vector], data: list, size: int) -> float:
    return reduce(
        lambda s, d: s + d / size,
        (euclid_squared(c_i, data[i]) for i, c_i in enumerate(c_list)),
        0.0,
    )


def euclid_squared(xsa: Vector, xsb: Vector) -> float:
    return sum((x_a - x_b) ** 2 for x_a, x_b in zip(xsa, xsb))
