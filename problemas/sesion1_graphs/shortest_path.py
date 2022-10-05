from algoritmia.datastructures.graphs import UndirectedGraph
from typing import TextIO

from algoritmia.datastructures.queues import Fifo

import labyrinth
import sys

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]
Path = list[Vertex]


def bf_search(g: UndirectedGraph[Vertex], source: Vertex, target: Vertex) -> list[Edge]:
    queue = Fifo()
    seen = set()
    queue.push((source, source))
    seen.add(source)
    res = []
    while len(queue) > 0:
        u, v = queue.pop()
#        yield u, v
        res.append((u, v))
        if v == target:
            return res
        for suc in g.succs(v):
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)
    return []


def path_recover(edges: list[Edge], target: Vertex) -> Path:
    # construir diccionario bp (back pointer)
    bp = {}
    for e in edges:
        u, v = e
        bp[v] = u  # el padre de v es u

    # Recuperar camino desde target (while)
    path = [target]
    v = target
    while True:
        padre = bp[v]
        path.append(padre)
        if padre == v:
            break
        v = padre

    # reverse path
    path.reverse()
    return path


def read_data(f: TextIO) -> tuple[int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    return rows, cols


def process(nrows: int, ncols: int) -> tuple[UndirectedGraph[Vertex], Path]:
    laberinto: UndirectedGraph[Vertex] = labyrinth.create_labyrinth(nrows, ncols)

    source: Vertex = (0,0)
    target: Vertex = (nrows-1, ncols -1)
    edges: list[Edge] = bf_search(laberinto, source, target)  # aristas de un recorrido en anchura

    camino: Path = path_recover(edges, target)  # camino mas corto por path recover

    return laberinto, camino


def show_results(path: Path):
    for v in path:
        print(v)


if __name__ == "__main__":
    rows0, cols0 = read_data(sys.stdin)
    graph0, path0 = process(rows0, cols0)
    show_results(path0)

