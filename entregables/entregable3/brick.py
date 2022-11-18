from __future__ import annotations

from dataclasses import dataclass

from board import RowCol
from direction import Direction


# dataclass: Brick
# Esta dataclass se encarga de gestionar los movimientos del bloque (prisma rectangular, ladrillo o brick)
#
# - Contine dos atributos del tipo RowCol, b1 y b2, con las posiciones de los dos cubos que forman
#   el bloque.
# - Para simplificar la implementación añadimos dos restriciones obligatorias:
#     - Cuando el bloque esté tumbado sobre una fila, b1 deberá ser el bloque de menor columna.
#     - Cuando el bloque esté tumbado sobre una columna, b1 deberá ser el bloque de menor fila.
# - Con estas dos restricciones un bloque debe cumplir una de estas tres condiciones:
#     b1.row == b2.row and b1.col == b2.col       # El boque está de pie
#     b1.row == b2.row and b1.col == b2.col - 1   # El boque está tumbado en una fila
#     b1.row == b2.row - 1 and b1.col == b2.col   # El boque está tumbado en una columna
# - Los objetos de esta clase son inmutables, por lo tanto, el método move() devuelve un nuevo bloque.
#
@dataclass(frozen=True)
class Brick:
    b1: RowCol
    b2: RowCol

    # El método __post_init__() es una ayuda para detectar bugs, se llama automáticamnte despues del constructor.
    # Comprueba que cada bloque que se construya cumpla una de las tres condiciones válidas
    def __post_init__(self):
        is_valid = self.b1.row == self.b2.row and self.b1.col == self.b2.col or \
                   self.b1.row == self.b2.row and self.b1.col == self.b2.col - 1 or \
                   self.b1.row == self.b2.row - 1 and self.b1.col == self.b2.col
        if not is_valid:
            raise RuntimeError(f"Built an invalid Brick (see restrictions): {self}")

    # Funcion para mover el bloque, como el bloque es inmutable el 'move' devuelve otro bloque
    def move(self, d: Direction) -> Brick:
        b1: RowCol = self.b1
        b2: RowCol = self.b2
        if self.b1.row == self.b2.row and self.b1.col == self.b2.col:  # estamos de pie
            if d == Direction.Up:
                b1 = RowCol(b1.row-2, b1.col)
                b2 = RowCol(b2.row-1, b2.col)

            elif d == Direction.Down:
                b1 = RowCol(b1.row + 1, b1.col)
                b2 = RowCol(b2.row + 2, b2.col)

            elif d == Direction.Left:
                b1 = RowCol(b1.row, b1.col - 2)
                b2 = RowCol(b2.row, b2.col - 1)

            elif d == Direction.Right:
                b1 = RowCol(b1.row, b1.col + 1)
                b2 = RowCol(b2.row, b2.col + 2)

            else:
                raise RuntimeError("Move: Invalid argument")

        elif self.b1.row == self.b2.row and self.b1.col == self.b2.col - 1:  # estamos tumbados en una fila
            if d == Direction.Up:
                b1 = RowCol(b1.row - 1, b1.col)
                b2 = RowCol(b2.row - 1, b2.col)

            elif d == Direction.Down:
                b1 = RowCol(b1.row + 1, b1.col)
                b2 = RowCol(b2.row + 1, b2.col)

            elif d == Direction.Left:
                b1 = RowCol(b1.row, b1.col - 1)
                b2 = RowCol(b2.row, b2.col -2)

            elif d == Direction.Right:
                b1 = RowCol(b1.row, b1.col + 2)
                b2 = RowCol(b2.row , b2.col + 1)
            else:
                raise RuntimeError("Move: Invalid argument")

        elif self.b1.row == self.b2.row - 1 and self.b1.col == self.b2.col:  # estamos tumbados en una columna
            if d == Direction.Up:
                b1 = RowCol(b1.row - 1, b1.col)
                b2 = RowCol(b2.row - 2, b2.col)

            elif d == Direction.Down:
                b1 = RowCol(b1.row + 2, b1.col)
                b2 = RowCol(b2.row + 1, b2.col)

            elif d == Direction.Left:
                b1 = RowCol(b1.row , b1.col-1)
                b2 = RowCol(b2.row , b2.col-1)

            elif d == Direction.Right:
                b1 = RowCol(b1.row, b1.col +1)
                b2 = RowCol(b2.row, b2.col+1)

            else:
                raise RuntimeError("Move: Invalid argument")
        else:
            raise RuntimeError("Move: imposible state reached")

        return Brick(b1,b2)
        # TODO: IMPLEMENTAR

    # IMPORTANTE: Puedes añadir métodos adicionales a la clase Brick
