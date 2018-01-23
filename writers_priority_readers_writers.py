# Writers have priority over readers.
import sys
import time
import random
from sync_utils import Thread, Semaphore, Lightswitch, watch


ROOM_EMPTY = Semaphore(1)
ROOM_LIGHTSWITCH = Lightswitch(ROOM_EMPTY)
NO_WRITERS = Semaphore(1)
WRITERS_LIGHTSWITCH = Lightswitch(NO_WRITERS)


def job(name):
    sys.stdout.write('Start ' + name + '\n')
    time.sleep(random.random())
    sys.stdout.write('Stop ' + name + '\n')


def reader(n):
    sys.stdout.write('Reader ' + str(n) + ' arrived\n')
    NO_WRITERS.wait()
    ROOM_LIGHTSWITCH.on()
    NO_WRITERS.signal()
    job("read {}".format(n))
    ROOM_LIGHTSWITCH.off()


def writer(n):
    sys.stdout.write('Writer ' + str(n) + ' arrived\n')
    WRITERS_LIGHTSWITCH.on()
    ROOM_EMPTY.wait()
    job("write {}".format(n))
    WRITERS_LIGHTSWITCH.off()
    ROOM_EMPTY.signal()



def main():
    while True:
        time.sleep(0.25)
        target = writer if random.randint(1, 4) == 1 else reader
        Thread(target, random.randint(1, 100))

watch(main)
