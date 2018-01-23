import sys
import time
import random
from sync_utils import Thread, Semaphore, watch


PORTIONS = POT_CAPACITY = 10
MUTEX = Semaphore(1)
EMPTY = Semaphore(0)
FULL = Semaphore(0)


def savage():
    global PORTIONS
    global POT_CAPACITY

    while True:
        MUTEX.acquire()
        if not PORTIONS:
            # wake up the cook
            sys.stdout.write("Waking cook.\n")
            EMPTY.signal()
            FULL.wait()
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
        EMPTY.wait()
        sys.stdout.write("Cooking.\n")
        FULL.signal()
    

def main():
    Thread(cook)
    for _ in range(4):
        Thread(target=savage)

watch(main)
