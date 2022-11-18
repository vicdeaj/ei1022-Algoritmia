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
        # TODO: IMPLEMENTAR
        raise NotImplementedError()

    # IMPORTANTE: Puedes añadir métodos adicionales a la clase Brick
