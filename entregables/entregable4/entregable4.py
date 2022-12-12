from typing import TextIO
import sys


Solution = tuple[int, int, int]  # l, r, coste


def read_data(f: TextIO) -> list[int]:
    raise NotImplementedError("read_data")


def process(v: list[int]) -> Solution:
    raise NotImplementedError("process")


def show_results(sol: Solution):
    raise NotImplementedError("show_results")


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)
