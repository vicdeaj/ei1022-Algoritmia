from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet

from random import shuffle


Vertex = tuple[int, int]


def create_labyrinth(rows: int, cols: int, n:int=0) -> UndirectedGraph[Vertex]:
    vertices: list[Vertex] = [(row, col) for row in range(rows) for col in range(cols)]
    mfs: MergeFindSet[Vertex] = MergeFindSet()
    for v in vertices:
        mfs.add(v)
    edges = [((row, col), (row + 1, col)) for row in range(rows - 1) for col in range(cols)]
    edges.extend([((row, col), (row, col + 1)) for row in range(rows) for col in range(cols - 1)])
    shuffle(edges)
    corridors = []
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        elif n > 0:
            n -= 1
            corridors.append((u, v))
    return UndirectedGraph(E=corridors)

