#!/usr/bin/env python3

from traceback import print_tb
import glob
import sys

INSTANCE_DIR = "binpacking"
MODULES = ['binpacking_mq', 'binpacking_pqq', 'binpacking_pqqo']


def aviso(m: str, tb=None):
    mensaje("Aviso", m, tb)


def error(m: str, tb=None):
    mensaje("Error", m, tb)


def mensaje(type: str, m: str, tb):
    sys.stderr.write(f"{type}: {m}\n")
    if tb is not None:
        print_tb(tb, file=sys.stderr)
    sys.stderr.write("\n")


def load_modules():
    modules = []
    for name in MODULES:
        try:
            module = __import__(name)
        except ModuleNotFoundError:
            aviso(f"no se ha encontrado el módulo {name}")
            continue
        except Exception as e:
            tb = sys.exc_info()[2]
            aviso(f"no se ha cargado {name} por la excepción {e}", tb)
            continue
        modules.append((name, module))
    return modules


def is_ok_read_data(name, module, instance, ref) -> bool:
    try:
        with open(instance) as f:
            c, w = module.read_data(f)
    except Exception as e:
        tb = sys.exc_info()[2]
        aviso(f"no se ha cargado {instance} con read_data de {name} por la excepción {e}", tb)
        return False
    if (c, w) != ref:
        aviso(f"read_data de {name} no ha leído correctamente la instancia {instance}")
        return False
    return True


def is_ok_process(name, module, c, w) -> bool:
    # Utilizamos el process() del módulo
    nc = -1
    res = []
    try:
        res = module.process(c, w)
    except Exception as e:
        tb = sys.exc_info()[2]
        aviso(f"no se ha procesado {instance} con process de {name} por la excepción {e}", tb)
        return False

    error = None
    if not isinstance(res, list):
        error = "process no ha devuelto una lista"
    elif len(res) == 0:
        error = "process ha devuelto una lista vacía"
    else:
        nc = max(res) + 1
        sres = set(res)
        if len(res) != len(w):
            error = "process no devuelve una lista de la longitud adecuada"
        elif min(res) < 0:
            error = "process devuelve un contenedor de índice negativo"
        elif len(sres) != nc:
            for c in range(nc):
                if c not in sres:
                    error = f"process() devuelve, al menos, un contenedor vacío: {c}"
                    break
    # Mostramos el resultado del módulo
    if error is not None:
        print(f"  - {name + '.py':19}- {error}")
    else:
        print(f"  - {name + '.py':19}- Contenedores: {nc}")
    return error is None


def treat_instance(modules, instance: str, fails_read, fails_process):
    print(f"INSTANCIA '{instance}':")
    try:
        with open(instance) as f:
            ref = (int(f.readline()),
                   [int(l) for l in f.readlines()])
    except Exception as e:
        tb = sys.exc_info()[2]
        aviso(f"no se ha cargado {instance} por la excepción {e}", tb)
        return

    c, w = ref
    for name, module in modules:
        if name not in fails_read:
            if not is_ok_read_data(name, module, instance, ref):
                fails_read.add(name)
        if name not in fails_process:
            if not is_ok_process(name, module, c, w):
                fails_process.add(name)
    print(f"  - Como líquido       - Contenedores: {int((sum(w) + c - 1) / c)}")


if __name__ == "__main__":
    instances = glob.glob(f"{INSTANCE_DIR}/*.bpk")
    if len(instances) == 0:
        error(f"No se han encotrado ficheros de prueba en el directorio {INSTANCE_DIR}")
        sys.exit(1)
    modules = load_modules()
    fails_read = set()
    fails_process = set()
    for instance in instances:
        treat_instance(modules, instance, fails_read, fails_process)
