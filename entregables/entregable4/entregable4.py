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
        """
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
        """

        acumulado_izq = 0
        acumulado_izq_maximo = 0
        acumulado_drc = 0
        acumulado_drc_maximo = 0

        maximo_izq = 0
        punta_izq = -10

        maximo_drc = 0
        punta_drc = -1

        indice_izq = medio - 1
        indice_drc = medio

        lista_maximos = [0]

        lado_actual = "izq"
        while indice_izq >= start or indice_drc < end:
            if lado_actual == "izq":
                if indice_izq < start: # skipeamos si ya hemos terminado este lado
                    lado_actual = "drc"
                    continue
                # ir_izq

                if v[indice_izq] > maximo_izq and maximo_izq <= maximo_drc:
                    lista_maximos.append(maximo_izq)
                    maximo_izq = v[indice_izq]
                    punta_izq = indice_izq
                    acumulado_izq_maximo += acumulado_izq
                    acumulado_izq = 0
                    if maximo_izq > maximo_drc:
                        lado_actual = "drc"


                acumulado_izq += v[indice_izq]
                indice_izq -= 1


            if lado_actual == "drc":
                if indice_drc >= end: # skipeamos si ya hemos terminado este lado
                    break
                # ir_drc


                if v[indice_drc] > maximo_drc and maximo_drc <= maximo_izq:
                    lista_maximos.append(maximo_drc)
                    maximo_drc = v[indice_drc]
                    punta_drc = indice_drc
                    acumulado_drc_maximo += acumulado_drc
                    if maximo_drc > maximo_izq:
                        lado_actual = "izq"
                    acumulado_drc = 0

                acumulado_drc += v[indice_drc]
                indice_drc += 1




        acumulado = acumulado_izq_maximo + acumulado_drc_maximo
        coste = (punta_drc - punta_izq - 1) * min(maximo_izq,maximo_drc) - acumulado
        ctr = (punta_izq, punta_drc, coste)



        # comparar y devolver
        return max(izq, drc , ctr, key=lambda i: (i[2], -i[0], -i[1]))

    return solve(0, len(v))



def show_results(sol: Solution):
    print(sol[0], sol[1], sol[2])


if __name__ == "__main__":
    v = read_data(sys.stdin)
    sol = process(v)
    show_results(sol)
