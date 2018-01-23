import sys
import time
import random
from threading import Thread, Semaphore
from watcher import watch


SANTA = Semaphore(0)

NUM_DEERS = 0
DEER_MUTEX = Semaphore(1)
SLEDGE = Semaphore(0)

NUM_ELVES = 0
ELF_MUTEX = Semaphore(1)
ELF_MULTIPLEX = Semaphore(3)
HELP = Semaphore(0)


def raindeer():
    global NUM_DEERS
    time.sleep(5 + 3*random.random())
    DEER_MUTEX.acquire()
    NUM_DEERS += 1
    sys.stdout.write("Deer arrives.\n")
    if NUM_DEERS == 9:
        sys.stdout.write("Deers wake Santa.\n")
        SANTA.release()
    DEER_MUTEX.release()

    SLEDGE.acquire()
    sys.stdout.write("Deer gets hitched.\n")
    # get hitched


def santa():
    global NUM_DEERS
    global NUM_ELVES
    while True:
        SANTA.acquire()
        DEER_MUTEX.acquire()
        if NUM_DEERS == 9:
            DEER_MUTEX.release()
            # prepare sledge
            sys.stdout.write("Santa prepares sledges.\n")
            for _ in range(9):
                SLEDGE.release()
            break
        else:
            DEER_MUTEX.release()

        # help elves

        sys.stdout.write("Santa helps elves.\n")
        for _ in range(3):
            HELP.release()

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
        SANTA.release()
        ELF_MUTEX.release()
    else:
        ELF_MUTEX.release()
    HELP.acquire()
    # get help
    sys.stdout.write("Elf gets help.\n")


def main():
    THREADS = [Thread(target=raindeer) for _ in range(9)] + [Thread(target=santa)]
    for t in THREADS:
        t.start()
    while True:
        time.sleep(random.random())
        Thread(target=elf).start()

watch(main)
