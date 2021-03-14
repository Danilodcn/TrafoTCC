from typing import Dict
from multiprocessing import Pool
from os import getpid
from time import sleep, time
from pprint import pprint




def funcao(n):
    sleep(n/100)
    return n, getpid()

workers = Pool(3)


t0 = time()
response = workers.map(funcao, range(100))
t1 = time()
pprint(response)
print("{.2f} s".format((t1 - t0) / 1000))