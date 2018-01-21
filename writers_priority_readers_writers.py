# Writers have priority over readers.
import sys
import time
import random
from threading import Thread, Semaphore


class Lightswitch:
    def __init__(self, semaphore):
        self.n = 0
        self.mutex = Semaphore(1)
        self.semaphore = semaphore

    def on(self):
        self.mutex.acquire()
        self.n += 1
        if self.n == 1:
            self.semaphore.acquire()
        self.mutex.release()

    def off(self):
        self.mutex.acquire()
        self.n -= 1
        if self.n == 0:
            self.semaphore.release()
        self.mutex.release()


ROOM_EMPTY = Semaphore(1)
ROOM_LIGHTSWITCH = Lightswitch(ROOM_EMPTY)
NO_WRITERS = Semaphore(1)
WRITERS_LIGHTSWITCH = Lightswitch(NO_WRITERS)


def job(name):
    sys.stdout.write('Start ' + name + '\n')
    time.sleep(random.random())
    sys.stdout.write('Stop ' + name + '\n')


def reader(n):
    time.sleep(5 * random.random())
    sys.stdout.write('Reader ' + str(n) + ' arrived\n')
    NO_WRITERS.acquire()
    ROOM_LIGHTSWITCH.on()
    NO_WRITERS.release()
    job("read {}".format(n))
    ROOM_LIGHTSWITCH.off()


def writer(n):
    time.sleep(5 * random.random())
    sys.stdout.write('Writer ' + str(n) + ' arrived\n')
    WRITERS_LIGHTSWITCH.on()
    ROOM_EMPTY.acquire()
    job("write {}".format(n))
    WRITERS_LIGHTSWITCH.off()
    ROOM_EMPTY.release()


WRITERS = [Thread(target=writer, args=(i,)) for i in range(5)]
READERS = [Thread(target=reader, args=(i,)) for i in range(10)]
THREADS = WRITERS + READERS


for t in THREADS:
    t.start()

for t in THREADS:
    t.join()
