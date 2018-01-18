# Rendezvous problem

from __future__ import print_function
from threading import Thread, Semaphore


a1done = Semaphore(0)
b1done = Semaphore(0)


def run_a():
    print('a1')
    a1done.release()
    b1done.acquire()
    print('a2')


def run_b():
    print('b1')
    b1done.release()
    a1done.acquire()
    print('b2')


thread_a = Thread(target=run_a)
thread_b = Thread(target=run_b)

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()
