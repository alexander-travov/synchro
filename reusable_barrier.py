# Reusable Barrier problem

import sys
from sync_utils import Thread, Semaphore, Barrier, watch


NUM_THREADS = 5
BARRIER = Barrier(NUM_THREADS)


def run(n):
    i = 1
    while True:
        sys.stdout.write('cycle {}: before barrier {}\n'.format(i, n))
        BARRIER.wait()
        sys.stdout.write('cycle {}: between barriers {}\n'.format(i, n))
        BARRIER.wait()
        sys.stdout.write('cycle {}: after barrier {}\n'.format(i, n))
        BARRIER.wait()
        i += 1


def main():
    for i in range(NUM_THREADS):
        Thread(run, i)

watch(main)
