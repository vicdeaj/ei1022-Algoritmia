from typing import Optional
import sys


def read_data(f) -> tuple[int, list[int], list[int]]:
    W = int(f.readline())
    v = []
    w = []
    for line in f.readlines():
        p = line.strip().split()
        v.append(int(p[0]))
        w.append(int(p[1]))
    return W, v, w


Score = int
Decision = int
Solution = tuple[Score, Optional[list[Decision]]]

SParams = tuple[int, int]

Mem = dict[SParams, Score]
MemPath = dict[SParams, tuple[Score, SParams, Decision]]

def process(impl: int, C: int, v: list[int], w: list[int]) -> Solution:
    if impl == 0:
        return knapsack_direct(w, v, C)
    elif impl == 1:
        return knapsack_memo(w, v, C)
    elif impl == 2:
        return knapsack_memo_path(w, v, C)
    elif impl == 3:
        return knapsack_iter(w, v, C)
    elif impl == 4:
        return knapsack_iter_red(w, v, C)


def show_results(sol: Solution):
    tv, decisions = sol
    print(tv)
    if decisions is not None:
        for d in decisions:
            print(d)


def knapsack_direct(w: list[int], v: list[int], C: int) -> Solution:
    def S(c,n):
        if n==0:
            return 0
        if n > 0 and w[n-1] <= c:
            return max(S(c,n-1),
                       S(c -w[n-1], n-1) + v[n-1])
        if n > 0 and w[n-1] > c:
            return S(c,n-1)

    return S(C, len(w)), None


def knapsack_memo(w: list[int], v: list[int], C: int) -> Solution:
    def S(c, n):
        if n == 0:
            return 0
        if (c,n) not in mem:
            if n > 0 and w[n - 1] <= c:
                mem[c, n] = max(S(c, n - 1),
                           S(c - w[n - 1], n - 1) + v[n - 1])
            if n > 0 and w[n - 1] > c:
                mem[c,n]= S(c, n - 1)
        return mem[c,n]

    mem: Mem = {}
    return S(C, len(w)), None


def knapsack_memo_path(w: list[int], v: list[int], C: int) -> Solution:
    def S(c, n):
        if n == 0:
            return 0
        if (c, n) not in mem:
            if n > 0 and w[n - 1] <= c:
                mem[c, n] = max((S(c, n - 1), (c, n - 1), 0),
                                (S(c - w[n - 1], n - 1) + v[n - 1],
                                 (c - w[n - 1], n - 1), 1))
            if n > 0 and w[n - 1] > c:
                mem[c, n] = (S(c, n - 1), (c, n - 1), 0)
        return mem[c, n][0]

    mem: MemPath = {}
    score = S(C, len(w))
    path = []
    c,n = C, len(w)
    while n>0:
        _, (c,n), d= mem[c,n]
        path.append(d)
    path.reverse()
    return score, path

def knapsack_iter(w: list[int], v: list[int], C: int) -> Solution:
    mem: MemPath = {}

    for n in range:
        def S(c, n):
            if n == 0:
                return 0
            if (c, n) not in mem:
                if n > 0 and w[n - 1] <= c:
                    mem[c, n] = max((S(c, n - 1), (c, n - 1), 0),
                                    (S(c - w[n - 1], n - 1) + v[n - 1],
                                     (c - w[n - 1], n - 1), 1))
                if n > 0 and w[n - 1] > c:
                    mem[c, n] = (S(c, n - 1), (c, n - 1), 0)
            return mem[c, n][0]


    score = S(C, len(w))
    path = []
    c,n = C, len(w)
    while n>0:
        _, (c,n), d= mem[c,n]
        path.append(d)
    path.reverse()
    return score, path


def knapsack_iter_red(w: list[int], v: list[int], C: int) -> Solution:
    raise NotImplementedError()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        impl = 0
    else:
        impl = int(sys.argv[1])
    C, v, w = read_data(sys.stdin)
    res = process(impl, C, v, w)
    show_results(res)
