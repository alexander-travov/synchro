import sys
import time
import random
from threading import Thread, Semaphore
from watcher import watch

def left(i):
    return i

def right(i):
    return (i + 1) % 5

FORKS = [Semaphore(1) for _ in range(5)]
MULTIPLEX = Semaphore(4)

def philosopher(i):
    while True:
        # think
        sys.stdout.write("{} thinking...\n".format(i))
        time.sleep(random.random())
        # get forks
        MULTIPLEX.acquire()
        r, l = right(i), left(i)
        FORKS[r].acquire()
        time.sleep(random.random())
        sys.stdout.write("{} got right fork {}\n".format(i, r))
        FORKS[l].acquire()
        sys.stdout.write("{} got left fork {}\n".format(i, l))
        # eat
        sys.stdout.write("{} eating...\n".format(i))
        time.sleep(random.random())
        # put forks
        FORKS[r].release()
        sys.stdout.write("{} put right fork {}\n".format(i, r))
        FORKS[l].release()
        sys.stdout.write("{} put left fork {}\n".format(i, l))
        MULTIPLEX.release()

def main():
    PHILOSOPHERS = [Thread(target=philosopher, args=(i,)) for i in range(5)]
    for p in PHILOSOPHERS:
        p.start()

watch(main)
