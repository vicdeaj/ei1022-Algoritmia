from __future__ import annotations

import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional, TextIO

from algoritmia.schemes.bt_scheme import bt_min_solve, ScoredDecisionSequence

from board import Board, RowCol
from brick import Brick
from direction import Direction, directions2string

# Variable global con la salida de show_results() si no hay solución
INSTANCE_WITHOUT_SOLUTION = "INSTANCE WITHOUT SOLUTION"

# Tipos que utilizarás en el process() al aplicar el esquema de backtracking
Decision = Direction  # Cuatro valores posibles: Directions.Right, Direction.Left, Direction.Up, Direction.Down
Solution = tuple[Decision, ...]  # Utilizad la función auxiliar 'directions2string' de direction.py para convertir
                                 # una solución en una cadena del tipo 'RRUUULLDR...'


# ---------------------------------------------------------------------------------------------------------------------

def read_data(f: TextIO) -> Board:
    board: Board = Board(f.readlines())
    return board



def process(board: Board) -> Optional[Solution]:
    @dataclass
    class Extra:
        brick: Brick = Brick(board.start_pos(), board.start_pos())

    class KnapsackDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:  # dice si estamos en una soludcion
            return self.extra. == board.target_pos()

        def successors(self) -> Iterator[KnapsackDS]:  # añade las dos posibles decisiones
            n = len(self)
            if n < len(valorObjetos):
                if self.extra.current_weight + pesoObjetos[n] <= capacidad:
                    current_weight2 = self.extra.current_weight + pesoObjetos[n]
                    current_value2 = self.extra.current_value + valorObjetos[n]
                    yield self.add_decision(1, Extra(current_weight2, current_value2))
                yield self.add_decision(0,
                                        self.extra)  # no metemos objeto en mochila, lo metemos despues, asi llega antes a los 1 y por lo tanto añade mas elementos

        def solution(self):
            return self.extra.current_value, self.extra.current_weight, self.decisions()

        def state(self):  # cuando dos nodos tienen el mismo futuro (repesentan el mismo problema)
            return len(self), self.extra.current_weight

        def score(self):
            return self.extra.current_value

    initial_ds = KnapsackDS(Extra(0, 0))
    best_sol = list(bt_max_solve(initial_ds))[-1]
    return best_sol


def show_results(solution: Optional[Solution]):
    if solution == None:
        print("INSTANCE WITHOUT SOLUTION")
    else:
        directions2string(solution)


# Programa principal --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    board0 = read_data(sys.stdin)
    solution0 = process(board0)
    show_results(solution0)
