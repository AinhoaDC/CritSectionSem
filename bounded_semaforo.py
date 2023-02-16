#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 13:12:13 2023

@author: prpa
"""

from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value, Array
from multiprocessing import BoundedSemaphore, Lock
import time 
import random 
N = 8
def task(common, tid,  semaforo):
    for i in range(10):
        print(f'{tid}−{i}: Non−critical Section', flush = True)
        time.sleep(random.random())
        print(f'{tid}−{i}: End of non−critical Section',flush = True)
        semaforo.acquire()

        print(f'{tid}−{i}: Critical section',flush = True)
        v = common.value + 1
        time.sleep(random.random())
        print(f'{tid}−{i}: Inside critical section',flush = True)
        common.value = v
        print(f'{tid}−{i}: End of critical section',flush = True)
        semaforo.release()
        
def main():
    lp = []
    semaforo = BoundedSemaphore(1)
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