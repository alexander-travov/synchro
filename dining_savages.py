import sys
import time
import random
from threading import Thread, Semaphore


PORTIONS = POT_CAPACITY = 10
MUTEX = Semaphore(1)
COOK = Semaphore(0)
FULL = Semaphore(0)


def savage():
    global PORTIONS
    global POT_CAPACITY

    while True:
        MUTEX.acquire()
        if not PORTIONS:
            # wake up the cook
            sys.stdout.write("Waking for cook.\n")
            COOK.release()
            FULL.acquire()
            PORTIONS = POT_CAPACITY
        # eat
        PORTIONS -= 1
        sys.stdout.write("Got portion. {} left.\n".format(PORTIONS))
        MUTEX.release()

        time.sleep(random.random())
        sys.stdout.write("Eating.\n")
        time.sleep(random.random())


def cook():
    while True:
        COOK.acquire()
        sys.stdout.write("Cooking.\n")
        FULL.release()
    

THREADS = [Thread(target=savage) for _ in range(4)] + [Thread(target=cook)]

for t in THREADS:
    t.deamon = True
    t.start()

for t in THREADS:
    t.join()
