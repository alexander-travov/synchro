# Queue problem

import sys
import time
import random
from sync_utils import Thread, Semaphore, watch

LEADERS_QUEUE = Semaphore(0)
FOLLOWERS_QUEUE = Semaphore(0)


def leader():
    FOLLOWERS_QUEUE.signal()
    LEADERS_QUEUE.wait()
    sys.stdout.write("Leader dances.\n")


def follower():
    LEADERS_QUEUE.signal()
    FOLLOWERS_QUEUE.wait()
    sys.stdout.write("Follower dances.\n")


def main():
    while True:
        time.sleep(0.25)
        person = leader if random.randint(0, 1) else follower
        Thread(person)

watch(main)
