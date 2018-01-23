import sys
import time
import random
from sync_utils import Thread, Semaphore, Barrier, watch


H = 0
O = 0
MUTEX = Semaphore(1)
FUSE_H = Semaphore(0)
FUSE_O = Semaphore(0)
FUSE_BARRIER = Barrier(3)


def try_fuse():
    global H
    global O
    if H >= 2 and O >= 1:
        H -= 2
        O -= 1
        sys.stdout.write("Fuse start.\n")
        FUSE_H.signal()
        FUSE_H.signal()
        FUSE_O.signal()
    else:
        MUTEX.release()


def hydrogen():
    global H
    global O
    MUTEX.acquire()
    H += 1
    sys.stdout.write("H arrived. H:{} O:{}\n".format(H, O))
    try_fuse()
    FUSE_H.wait()
    sys.stdout.write("H fusing.\n")
    FUSE_BARRIER.wait()


def oxygen():
    global H
    global O
    MUTEX.acquire()
    O += 1
    sys.stdout.write("O arrived. H:{} O:{}\n".format(H, O))
    try_fuse()
    FUSE_O.wait()
    sys.stdout.write("O fusing.\n")
    FUSE_BARRIER.wait()
    MUTEX.release()


def main():
    while True:
        time.sleep(0.25)
        atom = oxygen if random.randint(1, 3) == 1 else hydrogen
        Thread(atom)

watch(main)
