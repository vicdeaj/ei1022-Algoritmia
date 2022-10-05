import sys
from typing import TextIO

from algoritmia.algorithms.traversers import bf_vertex_traverser
from algoritmia.datastructures.graphs import UndirectedGraph

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]
Path = list[Vertex]


def knight_graph(rows: int, cols: int) -> UndirectedGraph[Vertex]:
    vertices: list[Vertex] = []
    for r in range(rows):
        for c in range(cols):
            vertices.append((r, c))

    edges: list[Edge] = []
    for r, c in vertices:
        for ir, ic in [(1, -2), (2, -1), (2, 1), (1, 2)]:
            r2 = r + ir
            c2 = c + ic
            if 0 <= r2 < rows and 0 <= c2 < cols:
                edges.append(((r,c), (r2, c2)))

    return UndirectedGraph(E=edges)


def read_data(f: TextIO) -> tuple[int, int, int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    firstrow = int(f.readline())
    firstcol = int(f.readline())
    return rows, cols, firstrow, firstcol


def process(rows: int, cols: int, first_row: int, first_col: int) -> tuple[UndirectedGraph[Vertex], int]:
    g = knight_graph(rows, cols)
    vertices: list[Vertex] = list(bf_vertex_traverser(g, (first_row, first_col)))
    return g, len(vertices)


def show_results(num: int):
    print(num)


if __name__ == "__main__":
    rows0, cols0, first_row0, first_col0 = read_data(sys.stdin)
    graph0, num0 = process(rows0, cols0, first_row0, first_col0)
    show_results(num0)

