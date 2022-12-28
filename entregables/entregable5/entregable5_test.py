#!/usr/bin/env python3

import platform
import sys
from enum import Enum
from glob import glob
from time import process_time
from traceback import print_tb

from entregable5 import read_data, process, Score, Decision

MAX_SECONDS = 1


class Result(Enum):
    OK = 1
    ERROR_SOLUTION_LENGTH = 2
    ERROR_TIMEOUT = 3
    ERROR_INVALID_SOLUTION = 4
    ERROR_EXCEPTION_LAUNCHED = 5
    ERROR_CHECK_FAILED = 6


def error(msg: str):
    print(f"RESULT: {Result.ERROR_CHECK_FAILED}")
    print(f"  ERROR: {msg}")
    sys.exit(Result.ERROR_CHECK_FAILED.value)


def error_e(msg: str, e: Exception, tb):
    print(f"RESULT: {Result.ERROR_EXCEPTION_LAUNCHED.name}")
    print(f"  ERROR: {msg}")
    print(f'         {e}\n')
    sys.stderr.write(f'{"-" * 20}\n')
    print_tb(tb, file=sys.stderr)
    sys.stderr.write(f'{"-" * 60}\n')
    sys.exit(Result.ERROR_EXCEPTION_LAUNCHED.value)


def print_debug(msg: str):
    # sys.stderr.write(msg + '\n')  # Descomentar para depuración
    return


def get_process_output_and_time(K: int, M: int, T: list[int]) -> tuple[tuple[Score, list[Decision]], float]:
    print_debug(f"Ejecutando tu 'process()'...")
    elapsed_time: float = 0
    score: int = -1
    decisions: list[Decision] = []
    try:
        t0 = process_time()
        score, decisions = process(K, M, T)
        t1 = process_time()
        elapsed_time = t1 - t0
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Tu función 'process()' ha lanzado una excepción", e, tb)
    return (score, decisions), elapsed_time


def check_solution(K: int, M: int, T: list[int], score: Score, decisions: list[Decision]) -> str:
    print_debug(f"Comprobando la solución obtenida de tu 'process()'...")
    if len(decisions) == 0:
        return f"La lista de decisiones está vacía."
    if decisions[0] != 0:
        return f"El primer índice de la solución debe ser el 0"
    if decisions[-1] + K < len(T):
        return f"El último índice de la solución no permite salir del puente en un salto"
    s = decisions[0]
    observed = T[s]
    for pos, t in enumerate(decisions[1:]):
        pos += 1
        observed += T[t]
        M -= 1
        if M < 0:
            return f"Has efectuado más saltos que el máximo de la instancia"
        if t < 0:
            return f"Los índices de la solución no pueden ser negativos: el índice en la posición {pos} es {t}"
        if t >= len(T):
            return f"Los índices no pueden salirse del vector: el índice en la posición {pos} es {t} y el último índice es {len(T) - 1}."
        if t <= s:
            return f"Los índices de la solución deben ser crecientes: los índices en las posiciones {pos} y {pos + 1} son {s} y {t}"
        jump = t - s
        if not (1 <= jump <= K):
            return f"El movimiento {(s, t)} no es válido. Tiene que saltar de 1 a {K} posiciones y salta {jump}"
        s = t

    if observed != score:
        return f"La puntuación calculada a partir de las decisiones que devuelve process() es {observed} y no coincide al que devuelve ({score})"
    return ''


def check_instance(filename) -> Result:
    print(f"INSTANCE: {filename}")
    expected_score = int(filename[:-2].split('_')[-1])

    with open(filename) as f:
        K0, S0, T0 = read_data(f)  # Puede lanzar excepción

    (score, decisions), elapsed_time = get_process_output_and_time(K0, S0, T0)  # Puede lanzar excepción

    # Comprobar la solución devuelta por tu process()
    primer_error = check_solution(K0, S0, T0, score, decisions)  # Puede lanzar excepción

    if primer_error == '':
        if elapsed_time <= MAX_SECONDS and score == expected_score:
            print(f"RESULT: {Result.OK.name}")
            print(f"  SCORE:    OK - {expected_score} points")
            print(f"  USEDTIME: OK - {elapsed_time:.2f} sec (<= {MAX_SECONDS} sec)")
            return Result.OK
        elif score < expected_score:
            print(f"RESULT: {Result.ERROR_SOLUTION_LENGTH.name}")
            print(f"  SCORE:    ERROR - {score} points (< {expected_score})")
            if elapsed_time <= MAX_SECONDS:
                print(f"  USEDTIME:    OK - {elapsed_time:.2f} sec (<= {MAX_SECONDS} sec)")
            else:
                print(f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {MAX_SECONDS} sec)")
        else:
            print(f"RESULT: {Result.ERROR_TIMEOUT.name}")
            print(f"  SCORE:    OK - {score} points")
            print(f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {MAX_SECONDS} sec)")
            return Result.ERROR_TIMEOUT
    else:
        print(f"RESULT: {Result.ERROR_INVALID_SOLUTION.name}")
        print(f"  {primer_error}")
        return Result.ERROR_INVALID_SOLUTION


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ejemplo de uso: python3.10 entregable5_test.py <instance1.i> <instance2.i> ... ")
        sys.exit(1)

    print('-' * 60)
    if platform.system() != "Windows":
        files = sys.argv[1:]
    else:
        files = [fn for arg in sys.argv[1:] for fn in sorted(glob(arg))]
    for fn in files:
        check_instance(fn)
        print('-' * 60)
