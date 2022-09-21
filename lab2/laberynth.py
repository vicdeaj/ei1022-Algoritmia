import sys
import random
from typing import TextIO
from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet


Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

def read_data(f: TextIO) -> tuple[int, int]:
    rows2 = int(f.readline())
    cols2 = int(f.readline())
    return rows2, cols2


def process(rows2: int, cols2: int) -> UndirectedGraph:
    # paso 1: crear vertices
    vertices: [Vertex] = []
    for r in range(rows2):
        for c in range(cols2):
            vertices.append((r, c))

    # paso 2: crear mfs
    mfs: MergeFindSet = MergeFindSet()
    for v in vertices:
        mfs.add(v)

    # paso 3: crear aristas
    aristas: [Edge] = []
    """
    for r in range(rows2):
        for c in range(cols2):
            if r == (rows2 - 1) and c == (cols2 - 1):
                continue

            if r == (rows2 - 1):
                a: Edge = ((r, c), (r, c + 1))
                aristas.append(a)
            elif c == (cols2 -1):
                a: Edge = ((r, c), (r + 1, c))
                aristas.append(a)
            else:
                a1: Edge = ((r, c), (r, c+1))
                a2: Edge = ((r, c), (r+1, c))
                aristas.append(a1)
                aristas.append(a2)
    """

    for r, c in vertices:
        if r == 0 and c == 0:
            continue
        elif r == 0:
            a: Edge = ((r, c), (r, c - 1))
            aristas.append(a)
        elif c == 0:
            a: Edge = ((r, c), (r - 1, c))
            aristas.append(a)
        else:
            a1: Edge = ((r, c), (r, c - 1))
            a2: Edge = ((r, c), (r - 1, c))
            aristas.append(a1)
            aristas.append(a2)

    random.seed(42)
    random.shuffle(aristas)

    # paso4: crear corridors
    corridors: list[Edge] = []
    for e in aristas:
        u, v = e
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u,v)
            corridors.append(e)


    # paso6:
    return UndirectedGraph(E = corridors)




def show_results(labyrinth2: UndirectedGraph):
    print(labyrinth2)


if __name__ == "__main__":
    rows, cols = read_data(sys.stdin)
    labyrinth = process(rows, cols)
    show_results(labyrinth)
