#!/usr/bin/env python3
import sys
from typing import TextIO


def read_data(f: TextIO) -> int:
    return None


def process(data: int) -> int:
    return None


def show_results(result: int):
    return None


# Escribir los resultados
if __name__ == "__main__":
    data = read_data(sys.stdin)
    results = process(data)
    show_results(results)