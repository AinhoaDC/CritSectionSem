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
def is_anybody_inside(critical, tid):
    found = False
    i = 0
    while i<len(critical) and not found:
        found = tid!=i and critical[i]==1
        i += 1
    return found
def task(common, tid, critical, turn, semaforo):
    a = 0
    for i in range(100):
        print(f'{tid}−{i}: Non−critical Section')
        a += 1
        print(f'{tid}−{i}: End of non−critical Section')
        semaforo.acquire()
        critical[tid] = 1
        while is_anybody_inside(critical, tid):
            critical[tid] = 0
            print(f'{tid}−{i}: Giving up')
            while turn.value==tid:
                pass
            critical[tid] = 1
        print(f'{tid}−{i}: Critical section')
        v = common.value + 1
        print(f'{tid}−{i}: Inside critical section')
        common.value = v
        print(f'{tid}−{i}: End of critical section')
        semaforo.release()
        critical[tid] = 0
        turn.value = tid
def main():
    lp = []
    semaforo = Lock()
    common = Value('i', 0)
    critical = Array('i', [0]*N)
    turn = Value('i', 0)
    for tid in range(N):
        lp.append(Process(target=task, args=(common, tid, critical, turn, semaforo)))
    print (f"Valor inicial del contador {common.value}")
    for p in lp:
        p.start()
    for p in lp:
        p.join()
    print (f"Valor final del contador {common.value}")
    print ("fin")
if __name__ == "__main__":
    main()