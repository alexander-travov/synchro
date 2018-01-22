# Reusable Barrier problem

import sys
from threading import Thread, Semaphore
from watcher import watch


class Barrier:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count = 0
        self.mutex = Semaphore(1)
        self.turnstiles = (Semaphore(0), Semaphore(0))
        self.t = 0 # current active turnstile index

    def wait(self):
        turnstile = self.turnstiles[self.t]

        self.mutex.acquire()
        self.count += 1
        if self.count == self.num_threads:
            self.count = 0
            self.t = 1 - self.t # alternate turnstile index
            for _ in range(self.num_threads):
                turnstile.release()
        self.mutex.release()

        turnstile.acquire()


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
    THREADS = [Thread(target=run, args=(i,)) for i in range(NUM_THREADS)]
    for t in THREADS:
        t.start()

watch(main)
