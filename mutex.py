# Incrementing counter N concurrently using mutex.

from __future__ import print_function
from sync_utils import Thread, Semaphore


N = 0
MAX = 1000
MUTEX = Semaphore(1)


def inc():
    global N
    global S
    for _ in range(MAX):
        MUTEX.acquire()
        # critical section
        N += 1
        MUTEX.release()


NUM_THREADS = 10
THREADS = [Thread(inc) for _ in range(NUM_THREADS)]

for t in THREADS:
    t.join()

print('Expected value:', MAX * NUM_THREADS)
print('Actual value:', N)
