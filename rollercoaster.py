import sys
import time
from sync_utils import *


NUM_PASSENGERS = 0
CAR_CAPACITY = 10
MUTEX = Semaphore(1)
BOARD_QUEUE = Semaphore(0)
UNBOARD_QUEUE = Semaphore(0)
BARRIER = Barrier(CAR_CAPACITY)
ALL_ON_BOARD = Semaphore(0)
ALL_OFF_BOARD = Semaphore(0)


def passenger():
    global NUM_PASSENGERS
    leader = False
    BOARD_QUEUE.wait()
    MUTEX.acquire()
    NUM_PASSENGERS += 1
    sys.stdout.write("Passenger boards.\n")
    if NUM_PASSENGERS == CAR_CAPACITY:
        leader = True
    else:
        MUTEX.release()
    BARRIER.wait()
    if leader:
        ALL_ON_BOARD.signal()
        sys.stdout.write("All onboard.\n")
    UNBOARD_QUEUE.wait()
    sys.stdout.write("Passenger unboards.\n")
    BARRIER.wait()
    if leader:
        NUM_PASSENGERS = 0
        sys.stdout.write("All offboard.\n")
        ALL_OFF_BOARD.signal()
        MUTEX.release()


def car():
    while True:
        sys.stdout.write("Car starts loading.\n")
        for _ in range(CAR_CAPACITY):
            BOARD_QUEUE.signal()
        ALL_ON_BOARD.wait()
        sys.stdout.write("Car runs.\n")
        sys.stdout.write("Car starts unloading.\n")
        for _ in range(CAR_CAPACITY):
            UNBOARD_QUEUE.signal()
        ALL_OFF_BOARD.wait()


def main():
    Thread(car)
    while True:
        time.sleep(0.1)
        Thread(passenger)

watch(main)
