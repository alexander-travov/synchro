import sys
import time
from threading import Thread, Semaphore
from watcher import watch
from reusable_barrier import Barrier


NUM_PASSENGERS = 0
CAR_CAPACITY = 10
MUTEX = Semaphore(1)
CAR = Semaphore(0)
BOARD_QUEUE = Semaphore(0)
UNBOARD_QUEUE = Semaphore(0)
BARRIER = Barrier(CAR_CAPACITY)
ALL_ON_BOARD = Semaphore(0)
ALL_OFF_BOARD = Semaphore(0)

def passenger():
    global NUM_PASSENGERS
    MUTEX.acquire()
    NUM_PASSENGERS += 1
    sys.stdout.write("Passenger arrives.\n")
    leader = False
    if NUM_PASSENGERS == CAR_CAPACITY:
        leader = True
        CAR.release()
    else:
        MUTEX.release()
    BOARD_QUEUE.acquire()
    sys.stdout.write("Passenger boards.\n")
    BARRIER.wait()
    if leader:
        ALL_ON_BOARD.release()
        sys.stdout.write("All onboard.\n")
    UNBOARD_QUEUE.acquire()
    sys.stdout.write("Passenger unboards.\n")
    BARRIER.wait()
    if leader:
        ALL_OFF_BOARD.release()
        sys.stdout.write("All offboard.\n")
        NUM_PASSENGERS = 0
        MUTEX.release()


def car():
    while True:
        CAR.acquire()
        sys.stdout.write("Car loads.\n")
        for _ in range(CAR_CAPACITY):
            BOARD_QUEUE.release()
        ALL_ON_BOARD.acquire()
        sys.stdout.write("Car runs.\n")
        sys.stdout.write("Car unloads.\n")
        for _ in range(CAR_CAPACITY):
            UNBOARD_QUEUE.release()
        ALL_OFF_BOARD.acquire()


def main():
    Thread(target=car).start()
    while True:
        time.sleep(0.1)
        Thread(target=passenger).start()

watch(main)
