import sys
import time
import random
from sync_utils import Thread, Semaphore, watch


NUM_LEADERS = 0
NUM_FOLLOWERS = 0

LEADERS_QUEUE = Semaphore(0)
FOLLOWERS_QUEUE = Semaphore(0)
MUTEX = Semaphore(1)
RENDEZVOUS = Semaphore(0)


def print_queue():
    global NUM_LEADERS
    global NUM_FOLLOWERS
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
        FOLLOWERS_QUEUE.signal()
    else:
        NUM_LEADERS += 1
        sys.stdout.write(" Waiting.")
        print_queue()
        MUTEX.release()
        LEADERS_QUEUE.wait()

    sys.stdout.write("Leader dances.\n")
    RENDEZVOUS.wait()
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
        LEADERS_QUEUE.signal()
    else:
        NUM_FOLLOWERS += 1
        sys.stdout.write(" Waiting.")
        print_queue()
        MUTEX.release()
        FOLLOWERS_QUEUE.wait()

    sys.stdout.write("Follower dances.\n")
    RENDEZVOUS.signal()


def main():
    while True:
        time.sleep(0.25)
        person = leader if random.randint(0, 1) else follower
        Thread(person)

watch(main)
