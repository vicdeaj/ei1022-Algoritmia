#!/usr/bin/env python3
import sys
from random import shuffle, seed
from typing import TextIO, Optional

from algoritmia.algorithms.traversers import bf_vertex_traverser
from algoritmia.datastructures.graphs import UndirectedGraph, IGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet

from algoritmia.algorithms.shortest_path import shortest_path_unweighted_graph, Path, path_recover
from algoritmia.datastructures.queues import Fifo

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

NO_VALID_WALL = 'NO VALID WALL'

# Función ya implementada
# Esta función utiliza un MFSet para crear un laberinto, pero le añade n aristas
# adicionales que provocan que el laberinto tenga ciclos.
def create_labyrinth(rows: int, cols: int, n: int, s: int) -> UndirectedGraph[Vertex]:
    vertices: list[Vertex] = [(r, c) for r in range(rows) for c in range(cols)]
    mfs: MergeFindSet[Vertex] = MergeFindSet((v,) for v in vertices)
    edges: list[Edge] = [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    edges.extend([((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)])
    seed(s)
    shuffle(edges)
    corridors: list[Edge] = []
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        elif n > 0:
            n -= 1
            corridors.append((u, v))
    return UndirectedGraph(E=corridors)


def read_data(f: TextIO) -> tuple[UndirectedGraph[Vertex], int, int]:
    rows = int(f.readline())
    cols = int(f.readline())
    removeN = int(f.readline())
    seed = int(f.readline())

    graph = create_labyrinth(rows, cols, removeN, seed)

    return graph, rows, cols


def precalculateDistanceBetter(g: IGraph[Vertex], v_initial: Vertex, dictresults: dict[Vertex, int]):
    profundidad = 0
    # edge traverse
    queue = Fifo()
    seen = set()
    queue.push((v_initial, v_initial))
    seen.add(v_initial)
    while len(queue) > 0:
        level_size = len(queue)
        while (level_size != 0):

            level_size -= 1
            u, v = queue.pop()
            # guardamos profundidad de cad nodo
            dictresults[v] = profundidad

            for suc in g.succs(v):
                if suc not in seen:
                    queue.push((v, suc))
                    seen.add(suc)
        profundidad += 1


def precalculardist(lab: UndirectedGraph[Vertex], inicio: Vertex, dictresults: dict[Vertex, int]):

    for v in lab.V:
        distancia = len(shortest_path_unweighted_graph(lab, inicio, v))
        dictresults[v] = distancia




def process(lab: UndirectedGraph[Vertex], rows: int, cols: int) -> tuple[Optional[Edge], int, int]:
    v_source = (0,0)
    v_dest = (rows - 1, cols - 1)



    dictInit2Cell: dict[Vertex, int] = {}  # diccionario que guarda las distancias desde el inicio a cada posible coordenada del grafo
    dictCell2End: dict[Vertex, int] = {}  # diccionario que guarda las distancias desde el final a cada posible coordenada del grafo

    wallToDelete = ((999999,999999),(999999,999999))


    # precalcular de 0 a todas las celdas n

    precalculateDistanceBetter(lab, v_source, dictInit2Cell)

    # precalcular de todas las celdas a la  salida n

    precalculateDistanceBetter(lab, v_dest, dictCell2End)

    length_before = dictInit2Cell[v_dest]
    length_after = length_before

    # recorremos TODAS las aristas y si no estan en el laberinto y son mas corta (el camino por ahí es mas corto) que la actual guardamos la pared n
    for r, c in lab.V:

        if r == 0 and c == 0:
            continue
        elif r == 0:
            a: Edge = ((r, c), (r, c - 1))
            if a[0] > a[1]:
                a = (a[1], a[0])

            coste = min(dictInit2Cell[a[0]] + dictCell2End[a[1]], dictCell2End[a[0]] + dictInit2Cell[a[1]])
            if coste < length_after or (coste == length_after and a < wallToDelete):
                length_after = coste
                wallToDelete = a

        elif c == 0:
            a: Edge = ((r, c), (r - 1, c))
            if a[0] > a[1]:
                a = (a[1], a[0])



            coste = min(dictInit2Cell[a[0]] + dictCell2End[a[1]], dictCell2End[a[0]] + dictInit2Cell[a[1]])
            if coste < length_after or (coste == length_after and a < wallToDelete):
                length_after = coste
                wallToDelete = a
        else:
            a1: Edge = ((r, c), (r, c - 1))
            if a1[0] > a1[1]:
                a1 = (a1[1], a1[0])

            a2: Edge = ((r, c), (r - 1, c))
            if a2[0] > a2[1]:
                a2 = (a2[1], a2[0])


            coste = min(dictInit2Cell[a1[0]] + dictCell2End[a1[1]], dictCell2End[a1[0]] + dictInit2Cell[a1[1]])
            if coste < length_after or (coste == length_after and a1 < wallToDelete):
                length_after = coste
                wallToDelete = a1


            coste = min(dictInit2Cell[a2[0]] + dictCell2End[a2[1]], dictCell2End[a2[0]] + dictInit2Cell[a2[1]])
            if coste < length_after or (coste == length_after and a2 < wallToDelete):
                length_after = coste
                wallToDelete = a2

    if wallToDelete in lab.E:
        wallToDelete = None

    return wallToDelete, length_before, length_after + 1


def show_results(edge_to_add: Optional[Edge], length_before: int, length_after: int):

    if edge_to_add is None:
        print(NO_VALID_WALL)
    else:
        print(edge_to_add[0][0], edge_to_add[0][1], edge_to_add[1][0], edge_to_add[1][1])

    print(length_before)
    print(length_after)


if __name__ == '__main__':
    graph0, rows0, cols0 = read_data(sys.stdin)
    edge_to_add0, length_before0, length_after0 = process(graph0, rows0, cols0)
    show_results(edge_to_add0, length_before0, length_after0)
