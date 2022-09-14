import sys
from typing import TextIO


def read_data(fichero: TextIO) -> list[int]:
    # En l tenemos una cadena por línea:
    lines: list[str] = fichero.readlines()

    # Transformamos cada línea en un entero:
    return [int(line) for line in lines]


def process(nums: list[int]) -> int:
    m = nums[0]
    for num in nums:
        if num < m:
            m = num
        return m


def show_results(num: int):
    print(num)


# Escribir los resultados
if __name__ == "__main__":
    nums = read_data(sys.stdin)
    result = process(nums)
    show_results(result)