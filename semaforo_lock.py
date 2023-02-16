#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 12:13:01 2023

@author: prpa
"""

from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import Semaphore, Lock
N = 8
def task(common, tid,  semaforo):
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        semaforo.acquire()

        print(f'{tid}−{i}: Critical section')
        v = common.value + 1
        print(f'{tid}−{i}: Inside critical section')
        common.value = v
        print(f'{tid}−{i}: End of critical section')
        semaforo.release()
        
def main():
    lp = []
    semaforo = Lock()
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    turn = Value('i', 0)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, semaforo)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")
if __name__ == "__main__":
    main()