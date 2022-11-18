#!/usr/bin/env python3

import io
import platform
import sys
from contextlib import redirect_stdout
from enum import Enum
from glob import glob
from time import process_time
from traceback import print_tb
from typing import Optional

from board import Board
from brick import Brick, RowCol
from entregable3 import read_data, process, show_results, Solution, INSTANCE_WITHOUT_SOLUTION
from direction import Direction

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


def check_brick_implementation():
    def check_brick_moves(brick_old: Brick, dic_expected: dict[Direction: Brick]):
        for d in dic_expected:
            brick_new = brick_old
            try:
                brick_new = brick_old.move(d)
            except Exception as e:
                tb = sys.exc_info()[2]
                error_e(f"Tu método 'move()' de Brick ha lanzado una excepción", e, tb)
            if dic_expected[d] != brick_new:
                msg = f"Error en tu implementación del método 'move()' de la clase 'Brick'\n"
                msg += f"\t Al mover el bloque {brick_old} en la dirección '{d.value}':\n"
                msg += f"\t   - Esperado: {dic_expected[d]}\n"
                msg += f"\t   - Obtenido: {brick_new}"
                error(msg)

    for ir in [0, 1, 2, 3]:
        for ic in [0, 1, 2, 3]:
            brick = Brick(RowCol(2 + ir, 2 + ic), RowCol(2 + ir, 2 + ic))
            expected = {Direction.Left: Brick(RowCol(2 + ir, 0 + ic), RowCol(2 + ir, 1 + ic)),
                        Direction.Right: Brick(RowCol(2 + ir, 3 + ic), RowCol(2 + ir, 4 + ic)),
                        Direction.Up: Brick(RowCol(0 + ir, 2 + ic), RowCol(1 + ir, 2 + ic)),
                        Direction.Down: Brick(RowCol(3 + ir, 2 + ic), RowCol(4 + ir, 2 + ic))}
            check_brick_moves(brick, expected)
            brick = Brick(RowCol(2 + ir, 1 + ic), RowCol(2 + ir, 2 + ic))
            expected = {Direction.Left: Brick(RowCol(2 + ir, 0 + ic), RowCol(2 + ir, 0 + ic)),
                        Direction.Right: Brick(RowCol(2 + ir, 3 + ic), RowCol(2 + ir, 3 + ic)),
                        Direction.Up: Brick(RowCol(1 + ir, 1 + ic), RowCol(1 + ir, 2 + ic)),
                        Direction.Down: Brick(RowCol(3 + ir, 1 + ic), RowCol(3 + ir, 2 + ic))}
            check_brick_moves(brick, expected)
            brick = Brick(RowCol(1 + ir, 2 + ic), RowCol(2 + ir, 2 + ic))
            expected = {Direction.Left: Brick(RowCol(1 + ir, 1 + ic), RowCol(2 + ir, 1 + ic)),
                        Direction.Right: Brick(RowCol(1 + ir, 3 + ic), RowCol(2 + ir, 3 + ic)),
                        Direction.Up: Brick(RowCol(0 + ir, 2 + ic), RowCol(0 + ir, 2 + ic)),
                        Direction.Down: Brick(RowCol(3 + ir, 2 + ic), RowCol(3 + ir, 2 + ic))}
            check_brick_moves(brick, expected)


def check_read_data_implementation():
    lines = ['ooo-------', 'oSoooo----', 'oooo-oooo-', '-ooo-ooooo', '-----ooToo', '------ooo-']
    puzle_str = '\n'.join(lines)
    print(f'Testing with instance:\n{puzle_str}')
    f = io.StringIO(puzle_str)
    board: Optional[Board] = None
    try:
        board = read_data(f)
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Tu función 'read_data()' ha lanzado una excepción", e, tb)
    if not isinstance(board, Board):
        error(f"Tu 'read_data()' no ha devuelto un objeto de tipo Board")
    if board.start_pos() != RowCol(1, 1):
        error(f"Tu 'read_data()' ha devuelto un objeto Board cuyo método start_pos() no funciona correctamente")
    if board.target_pos() != RowCol(4, 7):
        error(f"Tu 'read_data()' ha devuelto un objeto Board cuyo método target_pos() no funciona correctamente")
    for r in range(board.rows):
        for c in range(board.cols):
            if board.has_tile(RowCol(r, c)) != (lines[r][c] != '-'):
                error(f"Tu 'read_data()' ha devuelto un objeto Board cuyo método has_tile({RowCol(r,c)}) no funciona correctamente")


def check_show_results_implementation(solution: Optional[Solution], expected_output: str):
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            show_results(solution)
            lines: list[str] = f.getvalue().strip().split('\n')
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Tu función 'show_results()' ha lanzado una excepción", e, tb)

    print_debug(f"Comprobando la salida de 'show_results()'...")
    if len(lines) != 1:
        error(f"Tu 'show_results()' debe mostrar exactamente una linea por la salida estándar")

    if lines[0].strip() != expected_output:
        msg = f"show_results(({','.join('Direction.'+s.name for s in solution)})) no muestra lo que debe:"
        error(f"{msg}\n\tEsperado: {expected_output}\n\tDevuelto: {lines[0]}")


def get_read_data(filename: str) -> Board:
    print_debug(f"Ejecutando tu 'read_data()'...")

    board_ok = None
    try:
        with open(filename) as f:
            lines = f.readlines()
        try:
            board_ok = Board(lines)
        except Exception:
            error(f"El archivo '{filename}' no tiene el formato adecuado")
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Al abrir el archivo '{filename}' se ha lanzado una excepción", e, tb)

    board = None
    with open(filename) as f:
        try:
            board = read_data(f)
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e(f"Tu función 'read_data()' ha lanzado una excepción", e, tb)

    for r in range(board_ok.rows):
        for c in range(board_ok.cols):
            rc = RowCol(r, c)
            if board.has_tile(rc) != board_ok.has_tile(rc):
                error(f"El Board devuelto por tu 'read_data()' tiene en error en {rc}")

    if board_ok.start_pos() != board.start_pos():
        error(f"El Board devuelto por tu 'read_data()' tiene mal la posición inicial")
    if board_ok.target_pos() != board.target_pos():
        error(f"El Board devuelto por tu 'read_data()' tiene mal la posición objetivo")
    return board


def get_process_output_and_time(board: Board) -> tuple[Optional[Solution], float]:
    print_debug(f"Ejecutando tu 'process()'...")
    solution: Optional[Direction] = None
    elapsed_time: float = 0
    try:
        t0 = process_time()
        solution = process(board)
        t1 = process_time()
        elapsed_time = t1 - t0
    except Exception as e:
        tb = sys.exc_info()[2]
        error_e(f"Tu función 'process()' ha lanzado una excepción", e, tb)
    return solution, elapsed_time


def check_solution(board: Board, solution: Optional[Solution], expected_length: int) -> str:
    print_debug(f"Comprobando la solución obtenida de tu 'process()'...")
    if expected_length == 0:
        if solution is not None:
            return "Tu 'process()' debería haber devuelto 'None' para esta instancia (no tiene solución)"
        return ''

    if solution is None:
        return f"Tu 'process()' ha devuelto 'None' en vez de una solución de longitud {expected_length}"

    source = board.start_pos()
    brick = Brick(source, source)
    for i, d in enumerate(solution):
        try:
            brick = brick.move(d)
        except Exception as e:
            tb = sys.exc_info()[2]
            error_e(f"Tu método 'move()' de Brick ha lanzado una excepción", e, tb)
        if not board.has_tile(brick.b1) or not board.has_tile(brick.b2):
            return f'El bloque se sale del tablero: {solution[:i]}·{solution[i:]}'
    if brick.b1 != brick.b2 or brick.b1 != board.target_pos():
        return f'Tu process() ha devuelto una solución que no termina con el bloque en la posición objetivo'
    return ''


def check_instance(filename) -> Result:
    print(f"INSTANCE: {filename}")
    expected_length = int(filename[:-2].split('_')[-1])

    board = get_read_data(filename)  # Puede lanzar excepción

    your_solution, elapsed_time = get_process_output_and_time(board)  # Puede lanzar excepción
    np = len(your_solution) if your_solution is not None else 0

    # Comprobar la solución devuelta por tu process()
    primer_error = check_solution(board, your_solution, expected_length)  # Puede lanzar excepción

    if primer_error == '':
        if elapsed_time <= MAX_SECONDS and np == expected_length:
            print(f"RESULT: {Result.OK.name}")
            print(f"  LENGTH:   OK - {np} movements")
            print(f"  USEDTIME: OK - {elapsed_time:.2f} sec (<= {MAX_SECONDS} sec)")
            return Result.OK
        elif np > expected_length:
            print(f"RESULT: {Result.ERROR_SOLUTION_LENGTH.name}")
            print(f"  LENGTH:   ERROR - {np} movements (> {expected_length})")
            if elapsed_time <= MAX_SECONDS:
                print(f"  USEDTIME:    OK - {elapsed_time:.2f} sec (<= {MAX_SECONDS} sec)")
            else:
                print(f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {MAX_SECONDS} sec)")
        else:
            print(f"RESULT: {Result.ERROR_TIMEOUT.name}")
            print(f"  LENGTH:      OK - {np} movements")
            print(f"  USEDTIME: ERROR - {elapsed_time:.2f} sec (> {MAX_SECONDS} sec)")
            return Result.ERROR_TIMEOUT
    else:
        print(f"RESULT: {Result.ERROR_INVALID_SOLUTION.name}")
        print(f"  {primer_error}")
        return Result.ERROR_INVALID_SOLUTION


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Ejemplo de uso: python3.10 entregable3_test.py <instance1.i> <instance2.i> ... ")
        sys.exit(1)

    print("Comprobando tu implementación del método 'move()' de la clase 'Brick'...")
    check_brick_implementation()
    print("Comprobación finalizada: Tu implementación de 'move()' pasa las pruebas.\n")

    print("Comprobando tu implementación del método 'read_data()'...")
    check_read_data_implementation()
    print("Comprobación finalizada: Tu implementación de 'read_data()' pasa las pruebas.\n")

    print("Comprobando tu implementación del método 'show_results()'...")
    check_show_results_implementation(None, INSTANCE_WITHOUT_SOLUTION)
    check_show_results_implementation((Direction.Left, Direction.Right, Direction.Down, Direction.Up), 'LRDU')
    print("Comprobación finalizada: Tu implementación de 'show_results()' pasa las pruebas.\n")

    print('-' * 60)
    if platform.system() != "Windows":
        files = sys.argv[1:]
    else:
        files = [fn for arg in sys.argv[1:] for fn in sorted(glob(arg))]
    for fn in files:
        check_instance(fn)
        print('-' * 60)
