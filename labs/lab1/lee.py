import sys
from typing import TextIO


def read_data(fichero: TextIO) -> list[int]:
    # En l tenemos una cadena por línea:
    lines: list[str] = fichero.readlines()

    # Transformamos cada línea en un entero:
    return [int(line) for line in lines]


def show_results(nums: list[int]):
    for num in nums:
        print(num)


# Escribir los resultados
if __name__ == "__main__":
    nums = read_data(sys.stdin)
    show_results(nums)