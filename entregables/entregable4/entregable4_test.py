#!/usr/bin/env python3

import io
import sys
import os.path
from contextlib import redirect_stdout
from enum import Enum
from time import process_time
from traceback import print_tb

from entregable4 import read_data, process, show_results, Solution

MAX_SECONDS = 1
BAR = 60*"-"


class Result(Enum):
    OK = 0
    ERROR_TIMEOUT = 1
    ERROR_INVALID_SOLUTION = 2
    ERROR_EXCEPTION_LAUNCHED = 3
    ERROR_CHECK_FAILED = 4


def error(msg: str):
    print(f"RESULT: {Result.ERROR_CHECK_FAILED}")
    print(f"  ERROR: {msg}")
    sys.exit(Result.ERROR_CHECK_FAILED.value)


def error_e(msg: str, e: Exception, tb):
    print(f"RESULT: {Result.ERROR_EXCEPTION_LAUNCHED.name}")
    print(f"  ERROR: {msg}")
    print(f'         {type(e).__name__}\n')
    sys.stderr.write(BAR + "\n")
    print_tb(tb, file=sys.stderr)
    sys.stderr.write(BAR + "\n")
    sys.exit(Result.ERROR_EXCEPTION_LAUNCHED.value)


def print_debug(msg: str):
    # sys.stderr.write(msg + '\n')  # Descomentar para depuración
    return


def check_read_data():
    numbers = [1, 3, 4, 0, 5]
    as_string = '\n'.join(str(n) for n in numbers)
    f = io.StringIO(as_string)
    try:
        result = read_data(f)
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e("Tu función 'read_data()' ha lanzado una excepción", e, tb)
    if result != numbers:
        error(f"Tu función 'read_data()' ante la entrada:\n{as_string} ha devuelto {result} en lugar de {numbers}")


def check_show_results():
    solution = [1, 2, 3]
    expected_output = " ".join(str(n) for n in solution)

    f = io.StringIO()
    try:
        with redirect_stdout(f):
            show_results(solution)
            lines: list[str] = f.getvalue().strip().split('\n')
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e("Tu función 'show_results()' ha lanzado una excepción", e, tb)

    print_debug("Comprobando la salida de 'show_results()'...")
    if len(lines) != 1:
        error("Tu 'show_results()' debe mostrar exactamente una linea por la salida estándar")

    if lines[0].strip() != expected_output:
        msg = f"show_results({solution}) no muestra lo que debe:"
        error(f"{msg}\n\tEsperado: {expected_output}\n\tMostrado: {lines[0]}")


def use_read_data(filename: str) -> list[int]:
    print_debug("Ejecutando tu 'read_data()'...")
    v = None
    try:
        with open(filename) as f:
            try:
                v = read_data(f)
            except Exception as e:
                tb = sys.exc_info()[2]
                error_e(f"Tu función 'read_data()' ha lanzado una excepción", e, tb)
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Al abrir el archivo '{filename}' se ha lanzado una excepción", e, tb)

    if not isinstance(v, list):
        error(f"Tu función 'read_data()' ha devuelto {v} en lugar de una lista de enteros")
        for i, n in enumerate(v):
            if not isinstance(n, int):
                error(f"Tu función 'read_data()' ha devuelto {repr(n)} en lugar de un entero")

    return v


def use_process_output(v: list[int]) -> tuple[Solution, float]:
    print_debug(f"Ejecutando tu 'process()'...")
    solution: Solution = None
    elapsed_time: float = 0
    try:
        t0 = process_time()
        solution = process(v)
        t1 = process_time()
        elapsed_time = t1 - t0
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Tu función 'process()' ha lanzado una excepción", e, tb)
    return solution, elapsed_time


def check_solution(expected: Solution, found: Solution) -> str:
    if expected != found:
        return f"Tu función 'process()' ha devuelto {found} en lugar de {expected}."
    return ''


def check_instance(filename):
    print(f"INSTANCIA: {filename}")

    level = use_read_data(filename)  # Puede lanzar excepción
    expected = tuple(int(n) for n in
                os.path.splitext(os.path.basename(filename))[0]
                .split("_")[-3:])

    found, elapsed_time = use_process_output(level)
    error = check_solution(expected, found)

    if error != '':
        result = Result.ERROR_INVALID_SOLUTION
        message = "  " + error
    elif elapsed_time <= MAX_SECONDS:
        result = Result.OK
        message = f"  USEDTIME: OK - {elapsed_time:.2f} sec (<= {MAX_SECONDS} sec)"
    else:
        result = Result.ERROR_TIMEOUT
        message = f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {MAX_SECONDS} sec)"
    print(f"RESULT: {result.name}")
    print(message)
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ejemplo de uso: python3.10 entregable4_test.py <instance1.vec> <instance2.vec> ... ")
        sys.exit(0)

    print("Comprobando el método 'read_data()'...")
    check_read_data()

    print("Comprobando el método 'show_results()'...")
    check_show_results()

    print(BAR)
    for fn in sys.argv[1:]:
        check_instance(fn)
        print(BAR)
