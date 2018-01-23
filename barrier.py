# Barrier problem

import sys
from sync_utils import Thread, Semaphore


NUM_THREADS = 5
COUNT = 0 # Number of threads arrived at barrier

MUTEX = Semaphore(1)
BARRIER = Semaphore(0)


def run(n):
    global COUNT
    global NUM_THREADS

    sys.stdout.write('before barrier {}\n'.format(n))

    MUTEX.acquire()
    COUNT += 1
    if COUNT == NUM_THREADS:
        for _ in range(NUM_THREADS):
            BARRIER.signal()
    MUTEX.release()

    # critical point
    BARRIER.wait()

    sys.stdout.write('after barrier {}\n'.format(n))


THREADS = [Thread(run, i) for i in range(NUM_THREADS)]
for t in THREADS:
    t.join()
