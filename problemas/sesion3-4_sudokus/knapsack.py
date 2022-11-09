from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TextIO, Iterator
from auxiliares3_4.sudoku_lib import *
from algoritmia.schemes.bt_scheme import ScoredDecisionSequence, bt_max_solve

Weight = int
Value = int
Decision = int
Decisions = tuple[Decision, ...]


def read_data(f: TextIO) -> tuple[Weight,list[Value], list[Weight]]:
    capacidad = int(f.readline())
    values: list[Value] = []
    weights: list[Weight] = []
    for linea in f:
        v_txt, w_txt = linea.split()
        values.append(int(v_txt))
        weights.append(int(w_txt))
    return capacidad, values, weights




def process(capacidad: Weight, valorObjetos: list[Value],
            pesoObjetos: list[Weight]) -> tuple[Value, Weight, Decisions]:
    @dataclass
    class Extra:
        current_weight: Weight
        current_value: Value

    class KnapsackDS(ScoredDecisionSequence):
        def is_solution(self) -> bool: # dice si estamos en una soludcion
            return len(self) == len(valorObjetos)
            pass

        def successors(self) -> Iterator[KnapsackDS]:  # añade las dos posibles decisiones
            n = len(self)
            if n < len(valorObjetos):
                if self.extra.current_weight + pesoObjetos[n] <= capacidad:
                    current_weight2 = self.extra.current_weight + pesoObjetos[n]
                    current_value2 = self.extra.current_value + valorObjetos[n]
                    yield self.add_decision(1, Extra(current_weight2, current_value2))
                yield self.add_decision(0, self.extra)  # no metemos objeto en mochila, lo metemos despues, asi llega antes a los 1 y por lo tanto añade mas elementos

        def solution(self):
            return self.extra.current_value, self.extra.current_weight, self.decisions()

        def state(self):  # cuando dos nodos tienen el mismo futuro (repesentan el mismo problema)
            return len(self), self.extra.current_weight

        def score(self):
            return self.extra.current_value

    initial_ds = KnapsackDS(Extra(0,0))
    best_sol = list(bt_max_solve(initial_ds))[-1]
    return best_sol


def show_results(value: Value, weight:Weight, decisions:Decisions):
    print(value)
    print(weight)
    #print(" ".join([ str(d) for d in decisions ]))
    for d in decisions:
        print(d)


if __name__ == "__main__":
    pesoMochila, valores, pesos = read_data(sys.stdin)
    valorTotal, pesoTotal, decisciones = process(pesoMochila, valores, pesos)
    show_results(valorTotal, pesoTotal, decisciones)
