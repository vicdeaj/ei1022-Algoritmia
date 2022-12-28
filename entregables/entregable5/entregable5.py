import sys
from typing import TextIO

Score = int     # Puntos
Decision = int  # Índice en el vector de tablones


def read_data(f: TextIO) -> tuple[int, int, list[Score]]:
    K, M = (int(e) for e in f.readline().strip().split())
    T = [int(line) for line in f]
    return K, M, T


def process(K: int, M: int, T: list[Score]) -> tuple[Score, list[Decision]]:
    # IMPLEMENTAR
    raise NotImplementedError()


def show_results(score: Score, decisions: list[Decision]):
    print(score)
    for d in decisions:
        print(d)


if __name__ == '__main__':
    K0, M0, T0 = read_data(sys.stdin)
    score0, decisions0 = process(K0, M0, T0)
    show_results(score0, decisions0)
