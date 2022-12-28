import sys
from typing import TextIO
from algoritmia.utils import infinity

Score = int     # Puntos
Decision = int  # Índice en el vector de tablones


def read_data(f: TextIO) -> tuple[int, int, list[Score]]:
    K, M = (int(e) for e in f.readline().strip().split())
    T = [int(line) for line in f]
    return K, M, T

def process(K: int, M: int, T: list[Score]) -> tuple[Score, list[Decision]]:
    # IMPLEMENTAR
    def S(m, n, k, puntuacion: Score, caminito: list[Decision]) -> tuple[Score, list[Decision]]:
        caminito = list(caminito)
        if n == len(T):
            return puntuacion, caminito
        if m < M and k < K:
            anyadir = list(caminito)
            anyadir.append(n)
            anyadir_pto = puntuacion + T[n]

            opcion1 = S(m, n+1, k +1, puntuacion, caminito)
            opcion2 = S(m+1, n+1, 1, anyadir_pto, anyadir)

            if opcion1[0] > opcion2[0]:
                return opcion1
            else:
                return opcion2

           # return max(S(m, n+1, k +1, caminito), (S(m+1, n+1, 1, anyadir)[0] + T[n]))

        if m < M and k == K:
            caminito.append(n)
            return S(m+1, n+1, 1, puntuacion + T[n], caminito)


        if m == M and k < K:
            return S(m, n+1, k+1, puntuacion, caminito)


        if k == K and m == M:
            return -infinity, caminito

    return S(0, 1, 1, T[0], [0])


def show_results(score: Score, decisions: list[Decision]):
    print(score)
    for d in decisions:
        print(d)


if __name__ == '__main__':
    K0, M0, T0 = read_data(sys.stdin)
    score0, decisions0 = process(K0, M0, T0)
    show_results(score0, decisions0)
