# Rendezvous problem

from __future__ import print_function
from sync_utils import Thread, Semaphore


a1done = Semaphore(0)
b1done = Semaphore(0)


def run_a():
    print('a1')
    a1done.signal()
    b1done.wait()
    print('a2')


def run_b():
    print('b1')
    b1done.signal()
    a1done.wait()
    print('b2')


Thread(run_a)
Thread(run_b)
