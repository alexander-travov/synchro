import sys
import time
import random
from threading import Thread, Semaphore


class Lightswitch:
    def __init__(self, semaphore):
        self.n = 0
        self.mutex = Semaphore(1)
        self.semaphore = semaphore

    def lock(self):
        self.mutex.acquire()
        self.n += 1
        if self.n == 1:
            self.semaphore.acquire()
        self.mutex.release()

    def unlock(self):
        self.mutex.acquire()
        self.n -= 1
        if self.n == 0:
            self.semaphore.release()
        self.mutex.release()


ROOM_EMPTY = Semaphore(1)
LIGHTSWITCH = Lightswitch(ROOM_EMPTY)


def job(name):
    sys.stdout.write('Start ' + name + '\n')
    time.sleep(0.1)
    sys.stdout.write('Stop ' + name + '\n')


def reader(n):
    LIGHTSWITCH.lock()
    job("read {}".format(n))
    LIGHTSWITCH.unlock()


def writer(n):
    ROOM_EMPTY.acquire()
    job("write {}".format(n))
    ROOM_EMPTY.release()


WRITERS = [Thread(target=writer, args=(i,)) for i in range(5)]
READERS = [Thread(target=reader, args=(i,)) for i in range(10)]
THREADS = WRITERS + READERS
random.shuffle(THREADS)


for t in THREADS:
    t.start()

for t in THREADS:
    t.join()
