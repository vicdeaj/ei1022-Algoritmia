from typing import TextIO
import sys


def read_data(f: TextIO) -> list[int]:
    res = []
    for line in f:
        res.append(int(line))
    return res

def show_results(pos_pic: int):
    print(pos_pic)


def process_rec(v:list[int]) -> int:
    def tail_dec_solve(start: int, end:int) -> int:
        if end - start == 1: # is simple 1
            return start
        elif end - start == 2: # is simple 2
            return start if v[start] > v[start+1] else start + 1
        # decrease
        h = (start + end ) // 2
        if v[h-1] < v[h]:
            start = h
        else:
            end = h
        # recursividad
        return tail_dec_solve(start,end)

    def div_solve(start: int, end: int) -> Solution:
        # if problem.is_simple():
        #     return problem.trivial_solution
        # else:
        #     subproblemas = problem.divide()
        #     solutions = recursividad(...) for p in subproblemas
        #     return problem.combine(solutions)
        if end - start == 1:                    # is simple
            return v[start], start, start + 1   # trivial sol
        # divide
        h = (start + end) // 2
        # recursividad
        best_left = div_solve(start, h)
        best_right = div_solve(h, end)

        acumulado_l = 0
        i_max_l = h
        v_max_l = v[h]
        for i in range(h - 1, start - 1, - 1):
            acumulado_l = acumulado_l + v[i]
            if acumulado_l > v_max_l:
                i_max_l = i
                v_max_l = acumulado_l

        acumulado_r = 0
        i_max_r = h
        v_max_r = v[h]
        for i in range(h + 1, end):
            acumulado_r = acumulado_r + v[i]
            if acumulado_r > v_max_r:
                i_max_r = i
                v_max_r = acumulado_r

        best_center = (v_max_l + v_max_r - v[h], i_max_l, i_max_r)
        # combine & return
        return max(best_left, best_right, best_center)

    return div_solve(0, len(v))
    return tail_dec_solve(0, len(v))


process = process_rec

if __name__ == "__main__":
    lista = read_data(sys.stdin)
    pos_pico = process(lista)
    show_results(pos_pico)