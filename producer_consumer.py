import sys
import random
import time
from sync_utils import Thread, Semaphore, watch


BUFFER = []
BUFFER_MAX_SIZE = 5

MUTEX = Semaphore(1)
QUEUE = Semaphore(0)
SPOTS = Semaphore(BUFFER_MAX_SIZE)


def producer(n):
    while True:
        # producing
        time.sleep(random.expovariate(1))
        data = random.randint(1, 1000)

        SPOTS.acquire()
        MUTEX.acquire()
        BUFFER.append(data)
        sys.stdout.write("P{} added: {}\n".format(n, data))
        MUTEX.release()
        QUEUE.signal()


def consumer(n):
    while True:
        QUEUE.wait()
        MUTEX.acquire()
        data = BUFFER.pop(0)
        sys.stdout.write("C{} popped: {}\n".format(n, data))
        MUTEX.release()
        SPOTS.release()

        # consuming
        time.sleep(random.expovariate(1))


def main():
    for i in range(3):
        Thread(producer, i)
        Thread(consumer, i)

watch(main)
