import sys
import time
import random
from sync_utils import Thread, Semaphore, watch


NUM_SEATS = 4
QUEUE = []
MUTEX = Semaphore(1)

CLIENT = Semaphore(0)
BARBER_SEAT = Semaphore(0)

CLIENT_DONE = Semaphore(0)
BARBER_DONE = Semaphore(0)


def client(n):
    global NUM_SEATS
    global QUEUE
    MUTEX.acquire()
    if len(QUEUE) == NUM_SEATS:
        # go away
        sys.stdout.write("Client {}: No seats. Going away.\n".format(n))
        MUTEX.release()
    else:
        # take a seat
        s = Semaphore(0)
        QUEUE.append(s)
        MUTEX.release()
        sys.stdout.write("Client {}: Sitting.\n".format(n))
        CLIENT.signal()
        s.acquire()
        BARBER_SEAT.acquire()
        # get haircut
        sys.stdout.write("Client {}: Getting haircut.\n".format(n))
        CLIENT_DONE.signal()
        BARBER_DONE.wait()


def barber():
    global QUEUE
    while True:
        CLIENT.wait()
        MUTEX.acquire()
        s = QUEUE.pop(0)
        MUTEX.release()
        s.release()
        BARBER_SEAT.release()
        # make haircut
        time.sleep(2 * random.random())
        sys.stdout.write("Barber: Making haircut.\n")
        CLIENT_DONE.wait()
        BARBER_DONE.signal()


def main():
    Thread(barber)
    while True:
        time.sleep(random.random())
        Thread(client, random.randint(1, 100))

watch(main)
