import sys
import random
from threading import Thread, Semaphore


BUFFER = []
BUFFER_SIZE = 5

MUTEX = Semaphore(1)
QUEUE = Semaphore(0)
ITEMS = Semaphore(BUFFER_SIZE)
TOTAL = 50


def producer(n):
    # producing
    event = random.randint(1, 1000)
    sys.stdout.write("P{} produced: {}\n".format(n, event))

    ITEMS.acquire()

    MUTEX.acquire()
    BUFFER.append(event)
    sys.stdout.write("P{} added: {}\n".format(n, event))
    MUTEX.release()

    QUEUE.release()


def consumer(n):
    QUEUE.acquire()
    MUTEX.acquire()
    event = BUFFER.pop()
    MUTEX.release()
    ITEMS.release()
    # consuming
    sys.stdout.write("C{} consumed: {}\n".format(n, event))


PRODUCERS = [Thread(target=producer, args=(i,)) for i in range(TOTAL)]
CONSUMERS = [Thread(target=consumer, args=(i,)) for i in range(TOTAL)]
THREADS = PRODUCERS + CONSUMERS
random.shuffle(THREADS)

for t in THREADS:
    t.start()

for t in THREADS:
    t.join()
