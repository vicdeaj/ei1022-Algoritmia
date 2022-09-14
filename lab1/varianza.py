import sys
from typing import TextIO


def read_data(f: TextIO) -> list[int]:
    lines: list[str] = f.readlines()
    return [int(line) for line in lines]


def average(nums: list[int]) -> float:
    return sum(nums)/len(nums)


def process(nums: list[int]) -> float:
    s = 0
    avg = average(nums)
    for num in nums:
        s += (num - avg) ** 2
    return s/len(nums)


def show_results(v: float):
    print(v)


if __name__ == "__main__":
    nums = read_data(sys.stdin)
    v = process(nums)
    show_results(v)