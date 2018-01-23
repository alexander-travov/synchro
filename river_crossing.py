import sys
import time
import random
from threading import Thread, Semaphore
from watcher import watch
from reusable_barrier import Barrier

H = 0
S = 0
MUTEX = Semaphore(1)

HACKER_QUEUE = Semaphore(0)
SERF_QUEUE = Semaphore(0)

BARRIER = Barrier(4)


def hacker():
    global H
    global S
    is_captain = False
    MUTEX.acquire()
    H += 1
    sys.stdout.write("Hacker arrives.\tH:{} S:{}\n".format(H, S))
    if H == 4:
        is_captain = True
        H -= 4
        HACKER_QUEUE.release()
        HACKER_QUEUE.release()
        HACKER_QUEUE.release()
        HACKER_QUEUE.release()
    elif H == 2 and S >= 2:
        is_captain = True
        H -= 2
        S -= 2
        HACKER_QUEUE.release()
        HACKER_QUEUE.release()
        SERF_QUEUE.release()
        SERF_QUEUE.release()
    else:
        MUTEX.release()
    HACKER_QUEUE.acquire()
    sys.stdout.write("Hacker gets on board.\n")
    BARRIER.wait()
    if is_captain:
        sys.stdout.write("Boat flees.\n")
        MUTEX.release()


def serf():
    global H
    global S
    is_captain = False
    MUTEX.acquire()
    S += 1
    sys.stdout.write("Serf arrives.\tH:{} S:{}\n".format(H, S))
    if S == 4:
        is_captain = True
        S -= 4
        SERF_QUEUE.release()
        SERF_QUEUE.release()
        SERF_QUEUE.release()
        SERF_QUEUE.release()
    elif S == 2 and H >= 2:
        is_captain = True
        S -= 2
        H -= 2
        SERF_QUEUE.release()
        SERF_QUEUE.release()
        HACKER_QUEUE.release()
        HACKER_QUEUE.release()
    else:
        MUTEX.release()
    SERF_QUEUE.acquire()
    sys.stdout.write("Serf gets on board.\n")
    BARRIER.wait()
    if is_captain:
        sys.stdout.write("Boat flees.\n")
        MUTEX.release()


def main():
    while True:
        time.sleep(0.1)
        person = hacker if random.randint(0, 1) else serf
        Thread(target=person).start()

watch(main)
