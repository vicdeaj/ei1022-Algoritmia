import sys
from typing import TextIO


def read_data(fichero: TextIO) -> list[int]:
    lines: list[str] = fichero.readlines()
    return [int(line) for line in lines]


def process(data: list[int]) -> bool:
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if data[i] == data[j]:
                return True
    return False


def show_results(num: bool):
    print("No hay repetidos" if not result else "Hay repetidos")


# Escribir los resultados
if __name__ == "__main__":
    nums = read_data(sys.stdin)
    result = process(nums)
    show_results(result)