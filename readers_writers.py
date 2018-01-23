# Writers aren't starving.
# At least one writer is guaranteed to enter the room before queued readers.
import sys
import time
import random
from sync_utils import Thread, Semaphore, Lightswitch, watch


ROOM_EMPTY = Semaphore(1)
LIGHTSWITCH = Lightswitch(ROOM_EMPTY)
TURNSTILE = Semaphore(1)


def job(name):
    sys.stdout.write('Start ' + name + '\n')
    time.sleep(random.random())
    sys.stdout.write('Stop ' + name + '\n')


def reader(n):
    sys.stdout.write('Reader ' + str(n) + ' arrived\n')
    TURNSTILE.wait()
    TURNSTILE.signal()
    LIGHTSWITCH.on()
    job("read {}".format(n))
    LIGHTSWITCH.off()


def writer(n):
    sys.stdout.write('Writer ' + str(n) + ' arrived\n')
    TURNSTILE.wait()
    ROOM_EMPTY.wait()
    job("write {}".format(n))
    ROOM_EMPTY.signal()
    TURNSTILE.signal()


def main():
    while True:
        time.sleep(0.25)
        target = writer if random.randint(1, 4) == 1 else reader
        Thread(target, random.randint(1, 100))

watch(main)
