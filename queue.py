# Queue problem

import sys
import random
from threading import Thread, Semaphore

LEADERS_QUEUE = Semaphore(0)
FOLLOWERS_QUEUE = Semaphore(0)


def leader():
    FOLLOWERS_QUEUE.release()
    LEADERS_QUEUE.acquire()
    sys.stdout.write("Leader dances.\n")


def follower():
    LEADERS_QUEUE.release()
    FOLLOWERS_QUEUE.acquire()
    sys.stdout.write("Follower dances.\n")


N = 20
THREADS = [Thread(target=leader) for _ in range(N)] + [Thread(target=follower) for _ in range(N)] 
random.shuffle(THREADS)

for t in THREADS:
    t.start()
for t in THREADS:
    t.join()
sys.stdout.write("All passed.\n")
