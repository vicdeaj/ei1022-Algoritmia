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
    pesos_contenedores = [0]
    for i in range(len(w)):
        for nc in range(len(pesos_contenedores)):
            if pesos_contenedores[nc] + w[i] <= C:
                pesos_contenedores[nc] += w[i]
                x[i] = nc
                break

        else: # no ha cabido en ningun contenedor
            pesos_contenedores.append(w[i])
            x[i] = len(pesos_contenedores) - 1

    return x


def show_results(solution: list[int]):
    for x_i in solution:
        print(x_i)


if __name__ == "__main__":
    C0, w0 = read_data(sys.stdin)
    solution = process(C0, w0)
    show_results(solution)