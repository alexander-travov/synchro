# Writers aren't starving.
# At least one writer is guaranteed to enter the room before queued readers.
import sys
import time
import random
from threading import Thread, Semaphore
from watcher import watch


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
LIGHTSWITCH = Lightswitch(ROOM_EMPTY)
TURNSTILE = Semaphore(1)


def job(name):
    sys.stdout.write('Start ' + name + '\n')
    time.sleep(random.random())
    sys.stdout.write('Stop ' + name + '\n')


def reader(n):
    while True:
        time.sleep(5 * random.random())
        sys.stdout.write('Reader ' + str(n) + ' arrived\n')
        TURNSTILE.acquire()
        TURNSTILE.release()
        LIGHTSWITCH.on()
        job("read {}".format(n))
        LIGHTSWITCH.off()


def writer(n):
    while True:
        time.sleep(5 * random.random())
        sys.stdout.write('Writer ' + str(n) + ' arrived\n')
        TURNSTILE.acquire()
        ROOM_EMPTY.acquire()
        job("write {}".format(n))
        ROOM_EMPTY.release()
        TURNSTILE.release()


def main():
    WRITERS = [Thread(target=writer, args=(i,)) for i in range(5)]
    READERS = [Thread(target=reader, args=(i,)) for i in range(10)]
    for t in WRITERS + READERS:
        t.start()

watch(main)
