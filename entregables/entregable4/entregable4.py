from typing import TextIO
import sys


Solution = tuple[int, int, int]  # l, r, coste


def read_data(f: TextIO) -> list[int]:
    res = []
    for l in f:
        res.append(int(l))

    return res


def process(v: list[int]) -> Solution:
    raise NotImplementedError("process")


def show_results(sol: Solution):
    print(sol[0], sol[1], sol[2])


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)
