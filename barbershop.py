import sys
import time
import random
from threading import Thread, Semaphore
from watcher import watch


NUM_SEATS = 4
MUTEX = Semaphore(1)

BARBER = Semaphore(0)
BARBER_SEAT = Semaphore(0)

CLIENT_DONE = Semaphore(0)
BARBER_DONE = Semaphore(0)


def client(n):
    global NUM_SEATS
    MUTEX.acquire()
    if NUM_SEATS == 0:
        # go away
        sys.stdout.write("Client {}: No seats. Going away.\n".format(n))
        MUTEX.release()
    else:
        NUM_SEATS -= 1 # take a seat
        MUTEX.release()
        sys.stdout.write("Client {}: Sitting.\n".format(n))
        BARBER.release() # signaling barber
        BARBER_SEAT.acquire() # waiting for him to get of his chair
        MUTEX.acquire()
        NUM_SEATS += 1 # leave the waiting room
        MUTEX.release()
        # get haircut
        sys.stdout.write("Client {}: Getting haircut.\n".format(n))
        CLIENT_DONE.release()
        BARBER_DONE.acquire()


def barber():
    while True:
        BARBER.acquire()
        BARBER_SEAT.release()
        # make haircut
        time.sleep(2 * random.random())
        sys.stdout.write("Barber: Making haircut.\n")
        CLIENT_DONE.acquire()
        BARBER_DONE.release()


def main():
    Thread(target=barber).start()
    while True:
        time.sleep(random.random())
        Thread(target=client, args=(random.randint(1, 100),)).start()

watch(main)
