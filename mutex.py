# Incrementing counter N concurrently using mutex.

from __future__ import print_function
from threading import Thread, Semaphore


N = 0
MAX = 1000
MUTEX = Semaphore(1)


def inc():
    global N
    global S
    for _ in range(MAX):
        # critical section
        MUTEX.acquire()
        N += 1
        MUTEX.release()


NUM_THREADS = 10
THREADS = [Thread(target=inc) for _ in range(NUM_THREADS)]

for t in THREADS:
    t.start()

for t in THREADS:
    t.join()

print('Expected value:', MAX * NUM_THREADS)
print('Actual value:', N)
