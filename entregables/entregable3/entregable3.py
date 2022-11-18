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
        brick: Brick
        camino: Solution

    class KnapsackDS(ScoredDecisionSequence):
        def is_solution(self) -> bool:  # dice si estamos en una soludcion
            return self.extra.brick.b1 == board.target_pos() == self.extra.brick.b2

        def successors(self) -> Iterator[KnapsackDS]:  # añade las dos posibles decisiones
            newBrick: Brick = self.extra.brick.move(Direction.Right)
            if board.has_tile(newBrick.b1) and board.has_tile(newBrick.b2):
                caminoActual = self.extra.camino + tuple([Direction.Right])
                yield self.add_decision(Direction.Right, Extra(newBrick, caminoActual))

            newBrick: Brick = self.extra.brick.move(Direction.Up)
            if board.has_tile(newBrick.b1) and board.has_tile(newBrick.b2):
                caminoActual = self.extra.camino + tuple([Direction.Up])
                yield self.add_decision(Direction.Up, Extra(newBrick, caminoActual))

            newBrick: Brick = self.extra.brick.move(Direction.Down)
            if board.has_tile(newBrick.b1) and board.has_tile(newBrick.b2):
                caminoActual = self.extra.camino + tuple([Direction.Down])
                yield self.add_decision(Direction.Down, Extra(newBrick, caminoActual))

            newBrick: Brick = self.extra.brick.move(Direction.Left)
            if board.has_tile(newBrick.b1) and board.has_tile(newBrick.b2):
                caminoActual = self.extra.camino + tuple([Direction.Left])
                yield self.add_decision(Direction.Left, Extra(newBrick, caminoActual))

        def solution(self):
            return self.extra.camino

        def state(self):  # cuando dos nodos tienen el mismo futuro (repesentan el mismo problema)
            return self.extra.brick

        def score(self):
            return len(self.extra.camino)

    initial_ds = KnapsackDS(Extra(Brick(board.start_pos(), board.start_pos()), tuple([])))
    lista = list(bt_min_solve(initial_ds))
    longitud = len(lista)
    if longitud == 0:
        return None
    best_sol = lista[-1]
    return best_sol


def show_results(solution: Optional[Solution]):
    if solution == None:
        print("INSTANCE WITHOUT SOLUTION")
    else:
        print(directions2string(solution))


# Programa principal --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    board0 = read_data(sys.stdin)
    solution0 = process(board0)
    show_results(solution0)
