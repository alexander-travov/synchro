import sys
import time
import random
from sync_utils import Thread, Semaphore, Barrier, watch


EATING = WAITING = 0
MAX_EATING = 5
MAX_WAITING = 10
MUTEX = Semaphore(1)
PARTY_QUEUE = Semaphore(0)
PARTY = False


def print_state(action):
    global EATING
    global WAITING
    sys.stdout.write("{}\tE:{} W:{}\n".format(action, EATING, WAITING))


def visitor():
    global PARTY
    global EATING
    global WAITING
    global MAX_EATING

    MUTEX.acquire()
    if WAITING >= MAX_WAITING:
        print_state("Go away")
        MUTEX.release()
        return
    elif PARTY:
        WAITING += 1
        print_state("Wait")
        MUTEX.release()
        PARTY_QUEUE.wait()
        print_state("Sit")
    else:
        EATING += 1
        print_state("Sit")
        PARTY = EATING == MAX_EATING
        if PARTY:
            sys.stdout.write("Party starts.\n")
        MUTEX.release()

    # eat
    time.sleep(random.expovariate(1))

    MUTEX.acquire()
    EATING -= 1
    print_state("Done")
    if EATING == 0:
        n = min(WAITING, MAX_EATING)
        WAITING -= n
        EATING += n
        if PARTY:
            sys.stdout.write("Party ends.\n")
        PARTY = EATING == MAX_EATING
        if PARTY:
            sys.stdout.write("Party starts.\n")
        for _ in range(n):
            PARTY_QUEUE.signal()
    MUTEX.release()


def main():
    while True:
        time.sleep(random.expovariate(3))
        Thread(visitor)

watch(main)
