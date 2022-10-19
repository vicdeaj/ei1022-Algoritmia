import sys
from typing import TextIO


def read_data(f: TextIO) -> (int, list[int]):
    capacidad = int(f.readline())
    objetos = []
    for l in f:
        objetos.append(int(l))
    return capacidad, objetos


def process(C: int, w: list[int]) -> list[int]:
    x = [-1] * len(w)
    contenedor_actual = 0
    peso_actual = 0
    for i in range(len(w)):
        if peso_actual + w[i] <= C:
            x[i] = contenedor_actual
            peso_actual += w[i]
        else:
            contenedor_actual += 1
            x[i] = contenedor_actual
            peso_actual = w[i]

    return x

def show_results(solution: list[int]):
    for x_i in solution:
        print(x_i)


if __name__ == "__main__":
    C0, w0 = read_data(sys.stdin)
    solution = process(C0, w0)
    show_results(solution)