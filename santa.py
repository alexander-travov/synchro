import sys
import time
import random
from sync_utils import Thread, Semaphore, Barrier, watch


SANTA = Semaphore(0)

NUM_DEERS = 0
DEER_MUTEX = Semaphore(1)
SLEDGE = Semaphore(0)
SLEDGE_READY = Semaphore(0)
BARRIER = Barrier(9)

NUM_ELVES = 0
ELF_MUTEX = Semaphore(1)
ELF_MULTIPLEX = Semaphore(3)
HELP = Semaphore(0)


def raindeer():
    global NUM_DEERS
    while True:
        time.sleep(5 + 3*random.random())
        rudolf = False
        DEER_MUTEX.acquire()
        NUM_DEERS += 1
        sys.stdout.write("Deer arrives.\n")
        if NUM_DEERS == 9:
            rudolf = True
            sys.stdout.write("Deers wake Santa.\n")
            SANTA.signal()
        DEER_MUTEX.release()

        SLEDGE.wait()
        sys.stdout.write("Deer gets hitched.\n")
        BARRIER.wait()
        if rudolf:
            SLEDGE_READY.signal()



def santa():
    global NUM_DEERS
    global NUM_ELVES
    while True:
        SANTA.wait()
        DEER_MUTEX.acquire()
        if NUM_DEERS == 9:
            NUM_DEERS = 0
            DEER_MUTEX.release()
            # prepare sledge
            sys.stdout.write("Santa prepares sledges.\n")
            for _ in range(9):
                SLEDGE.release()
            SLEDGE_READY.wait()
            sys.stdout.write("Ho-ho-ho.\n")
            continue
        else:
            DEER_MUTEX.release()

        # help elves

        sys.stdout.write("Santa helps elves.\n")
        for _ in range(3):
            HELP.signal()

        ELF_MUTEX.acquire()
        NUM_ELVES = 0
        ELF_MUTEX.release()

        for _ in range(3):
            ELF_MULTIPLEX.release()


def elf():
    global NUM_ELVES
    ELF_MULTIPLEX.acquire()
    sys.stdout.write("Elf wants help.\n")

    ELF_MUTEX.acquire()
    NUM_ELVES += 1
    if NUM_ELVES == 3:
        sys.stdout.write("Elves wake Santa.\n")
        SANTA.signal()
        ELF_MUTEX.release()
    else:
        ELF_MUTEX.release()
    HELP.wait()
    # get help
    sys.stdout.write("Elf gets help.\n")


def main():
    Thread(target=santa)
    for i in range(9):
        Thread(raindeer)
    while True:
        time.sleep(random.random())
        Thread(elf)

watch(main)
