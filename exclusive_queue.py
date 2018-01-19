# Exclusive Queue problem

import sys
import random
from threading import Thread, Semaphore

NUM_LEADERS = 0
NUM_FOLLOWERS = 0

LEADERS_QUEUE = Semaphore(0)
FOLLOWERS_QUEUE = Semaphore(0)
MUTEX = Semaphore(1)
RENDEZVOUS = Semaphore(0)


def print_queue():
    sys.stdout.write("\tL: {} F: {}\n".format(NUM_LEADERS, NUM_FOLLOWERS))


def leader():
    global NUM_LEADERS
    global NUM_FOLLOWERS

    MUTEX.acquire()
    sys.stdout.write("Leader arrived.")
    if NUM_FOLLOWERS:
        NUM_FOLLOWERS -= 1
        sys.stdout.write(" Pair passes.")
        print_queue()
        FOLLOWERS_QUEUE.release()
    else:
        NUM_LEADERS += 1
        sys.stdout.write(" Waiting.")
        print_queue()
        MUTEX.release()
        LEADERS_QUEUE.acquire()

    sys.stdout.write("Leader dances.\n")
    RENDEZVOUS.acquire()
    MUTEX.release()



def follower():
    global NUM_LEADERS
    global NUM_FOLLOWERS

    MUTEX.acquire()
    sys.stdout.write("Follower arrived.")
    if NUM_LEADERS:
        NUM_LEADERS -= 1
        sys.stdout.write(" Pair passes.")
        print_queue()
        LEADERS_QUEUE.release()
    else:
        NUM_FOLLOWERS += 1
        sys.stdout.write(" Waiting.")
        print_queue()
        MUTEX.release()
        FOLLOWERS_QUEUE.acquire()

    sys.stdout.write("Follower dances.\n")
    RENDEZVOUS.release()


N = 20
THREADS = [Thread(target=leader) for _ in range(N)] + [Thread(target=follower) for _ in range(N)] 
random.shuffle(THREADS)

for t in THREADS:
    t.start()
for t in THREADS:
    t.join()
sys.stdout.write("All passed.\n")
