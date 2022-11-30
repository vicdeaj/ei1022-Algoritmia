from typing import TextIO
import sys


def read_data(f: TextIO) -> list[int]:
    res = []
    for line in f:
        res.append(int(line))
    return res


def show_results(suma: int, b: int, e:int):
    print(suma)
    print(b)
    print(e)

Solution = tuple[int,int, int] # suma start end


def process_rec(v:list[int]) -> Solution:
    def div_solve(start: int, end:int) -> Solution:
        if end - start == 1:
            return v[start], start, end # vector de talla 1
        # divide
        h = (start + end) // 2
        # recursividad
        best_left = div_solve(start, h)
        best_right = div_solve(h, end)
        best_center = (0, 0, 0)


        # idea feliz
        acc = v[h]
        v_right_max = v[h]
        i_right_max = h
        for i in range(h+1, end):
            acc += v[i]
            if acc > v_right_max:
                v_right_max = acc
                i_right_max = i

        acc2 = v[h]
        v_left_max = v[h]
        i_left_max = h
        for i2 in range(h-1,start - 1, -1):
            acc2 += v[i2]
            if acc2 > v_left_max:
                v_left_max = acc2
                i_left_max = i2
        best_center = (v_right_max + v_left_max - v[h], i_left_max, i_right_max + 1)

        # return combine
        return max(best_left, best_center, best_right)

    return div_solve(0, len(v))


process = process_rec

if __name__ == "__main__":
    lista = read_data(sys.stdin)
    suma, begin, end = process(lista)
    show_results(suma, begin, end)