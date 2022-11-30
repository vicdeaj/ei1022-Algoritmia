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

    return tail_dec_solve(0, len(v))


process = process_rec

if __name__ == "__main__":
    lista = read_data(sys.stdin)
    pos_pico = process(lista)
    show_results(pos_pico)