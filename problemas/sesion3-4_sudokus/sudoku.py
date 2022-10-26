from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TextIO, Iterator
from auxiliares3_4.sudoku_lib import *

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solve


# Position = tuple[int, int]
# Sudoku = list[list[int]]


def read_data(f: TextIO) -> Sudoku:
    return desde_cadenas(f.readlines())

def process_fast(s:Sudoku) -> Iterator[Sudoku]:
    @dataclass
    class Extra:
        sudoku: Sudoku
        vacias: set[Position]

    class SudokuDS(DecisionSequence):
        def is_solution(self) -> bool:
            return len(self.extra.vacias) == 0

        def successors(self) -> Iterator[SudokuDS]:
            pos = primera_vacia(self.extra.sudoku)
            if pos is not None:
                row, col = pos
                for num in posibles_en(self.extra.sudoku, pos):
                    sudoku2 = [ linea[:] for linea in self.extra.sudoku ]
                    sudoku2[row][col] = num
                    vacias2 = set(self.extra.vacias)

                    yield self.add_decision(num, Extra(sudoku2, vacias2))

        def solution(self) -> Sudoku:
            return self.extra.sudoku

    initial_ds = SudokuDS(Extra(s))
    return bt_solve(initial_ds)


def process_naive(s: Sudoku) -> Iterator[Sudoku]:
    @dataclass
    class Extra:
        sudoku: Sudoku

    class SudokuDS(DecisionSequence):
        def is_solution(self) -> bool:
            return primera_vacia(self.extra.sudoku) is None

        def successors(self) -> Iterator[SudokuDS]:
            best_posibles = None
            best_pos = (-1,-1)

            for pos_v in self.extra.vacias:
                aux = posibles_en(self.extra.sudoku, pos_v)
                if best_posibles is None or len(aux) - len(best_posibles):
                    best_posibles = aux
                    best_pos = pos_v

            pos =   best_pos

            if pos is not None:
                row, col = pos
                for num in posibles_en(self.extra.sudoku, pos):
                    sudoku2 = [ linea[:] for linea in self.extra.sudoku ]
                    sudoku2[row][col] = num
                    vacias2 = set(self.extra.vacias)
                    vacias2.remove(pos)
                    yield self.add_decision(num, Extra(sudoku2))

        def solution(self) -> Sudoku:
            return self.extra.sudoku

    initial_ds = SudokuDS(Extra(s))
    return bt_solve(initial_ds)


def show_results(solution: Iterator[Sudoku]):
    for s in solution:
        pretty_print(s)


process = process_fast # select algorithm fast / naive

if __name__ == "__main__":
    s: Sudoku = read_data(sys.stdin)
    solutionS = process(s)
    show_results(solutionS)
