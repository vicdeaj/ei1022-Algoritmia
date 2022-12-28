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
    def S(m, n, k) -> Score:
        # Check if the result has already been calculated
        if (m, n, k) in memo:
            return memo[(m, n, k)]

        if n == len(T):
            return 0
        if m < M and k < K:

            opcion1 = S(m, n+1, k +1)
            opcion2 = S(m+1, n+1, 1) + T[n]

            if opcion1 > opcion2:
                result = opcion1
            else:
                result = opcion2

           # return max(S(m, n+1, k +1, caminito), (S(m+1, n+1, 1, anyadir)[0] + T[n]))

        elif m < M and k == K:
            result = S(m+1, n+1, 1) + T[n]

        elif m == M and k < K:
            result = S(m, n+1, k+1)

        elif k == K and m == M:
            result = -infinity

        # Store the result in the memoization dictionary
        memo[(m, n, k)] = result
        return result

    # Initialize the memoization dictionary
    memo = {}
    aux = S(1, 1, 1)
    lista_decisiones = aux[1]
    lista_decisiones.sort()
    lista_decisiones = [0] + lista_decisiones
    return aux[0] + T[0], lista_decisiones



def show_results(score: Score, decisions: list[Decision]):
    print(score)
    for d in decisions:
        print(d)


if __name__ == '__main__':
    K0, M0, T0 = read_data(sys.stdin)
    score0, decisions0 = process(K0, M0, T0)
    show_results(score0, decisions0)
