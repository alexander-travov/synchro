import sys
import random
import time
from threading import Thread, Semaphore
from watcher import watch


BUFFER = []
BUFFER_MAX_SIZE = 5

MUTEX = Semaphore(1)
QUEUE = Semaphore(0)
ITEMS = Semaphore(BUFFER_MAX_SIZE)


def producer(n):
    while True:
        # producing
        time.sleep(random.random())
        event = random.randint(1, 1000)

        ITEMS.acquire()
        MUTEX.acquire()
        BUFFER.append(event)
        sys.stdout.write("P{} added: {}\n".format(n, event))
        MUTEX.release()
        QUEUE.release()


def consumer(n):
    while True:
        QUEUE.acquire()
        MUTEX.acquire()
        event = BUFFER.pop(0)
        sys.stdout.write("C{} popped: {}\n".format(n, event))
        MUTEX.release()
        ITEMS.release()

        # consuming
        time.sleep(random.random())


def main():
    PRODUCERS = [Thread(target=producer, args=(i,)) for i in range(10)]
    CONSUMERS = [Thread(target=consumer, args=(i,)) for i in range(3)]
    THREADS = PRODUCERS + CONSUMERS
    for t in THREADS:
        t.start()

watch(main)
