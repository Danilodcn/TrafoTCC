from collections import namedtuple
from multiprocessing import Pool, Process, managers
from os import getpid, getppid
from pprint import pprint
from random import random
from threading import Thread
from time import sleep, time

dstate = namedtuple("State", "name tempo PID")
DADO = {}


def info(*args):
    try:
        name, d = args
    except:
        name, d = args[0]

    d[str(random())] = random()
    print(dstate(name, getpid(), getppid()))
    return (name, getpid(), getppid())


def tempo(*args):
    try:
        name, t = args
    except:
        name, t = args[0]
    t = random()
    sleep(t)
    print(dstate(name, "{0:.4} ms".format(t * 1000), getpid()))

    return name, t, getpid()


if __name__ == "__main__":
    server = managers.SyncManager()
    server.start()

    d = server.dict()

    p = Pool(10)
    arg = [(f"Pocess {i + 1}", 0.1) for i in range(300)]
    # print(arg)
    t0 = time()
    r = p.map_async(tempo, (*arg,))
    r.wait()

    r = r.get()
    t1 = time()

    print("\nResultados")
    pprint(r)
    soma = 0
    for i, j, k in r:
        soma += j
    print(f"Tempo total: {soma}")
    print(f"Tempo real: {t1 - t0}")
