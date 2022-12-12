from typing import TextIO
import sys


Solution = tuple[int, int, int]  # l, r, coste


def read_data(f: TextIO) -> list[int]:
    res = []
    for l in f:
        res.append(int(l))

    return res


def process(v: list[int]) -> Solution:
    def solve(start: int, end: int) -> Solution:
        if start == end:
            return start, end, 0
        if end - start == 1:
            return start, end, 0

        medio = (start + end) // 2
        izq: Solution = solve(start, medio)
        drc: Solution = solve(medio, end)
        # calculamos el del medio
        acumulado_izq = 0
        acumulado_maximo_izq = 0

        maximo_izq = 0
        indice_max_izq = -1
        for i in range(medio, start, -1):
            acumulado_izq += v[i]
            if v[i] >= maximo_izq:
                indice_max_izq = i
                acumulado_maximo_izq = acumulado_izq


        for ii in range(medio, end):





        ctr: Solution = (0,0,0)
        # comparar y devolver
        return max(izq, drc , ctr, key=lambda i: (i[2], i[0], i[1]))

    return solve(0, len(v))



def show_results(sol: Solution):
    print(sol[0], sol[1], sol[2])


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)
