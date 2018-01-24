import sys
import os
import signal
import threading


if sys.version_info.major == 2:
    _Semaphore = threading._Semaphore
else:
    _Semaphore = threading.Semaphore


class Semaphore(_Semaphore):
    def release(self, n=1):
        for _ in range(n):
            _Semaphore.release(self)

    signal = release
    wait = _Semaphore.acquire



class Thread(threading.Thread):
    def __init__(self, target, *args):
        threading.Thread.__init__(self, target=target, args=args)
        self.start()


class Lightswitch:
    def __init__(self, semaphore):
        self.n = 0
        self.mutex = Semaphore(1)
        self.semaphore = semaphore

    def on(self):
        self.mutex.acquire()
        self.n += 1
        if self.n == 1:
            self.semaphore.acquire()
        self.mutex.release()

    def off(self):
        self.mutex.acquire()
        self.n -= 1
        if self.n == 0:
            self.semaphore.release()
        self.mutex.release()


class Barrier:
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count = 0
        self.mutex = Semaphore(1)
        self.turnstiles = (Semaphore(0), Semaphore(0))
        self.t = 0 # current active turnstile index

    def wait(self):
        turnstile = self.turnstiles[self.t]

        self.mutex.acquire()
        self.count += 1
        if self.count == self.num_threads:
            self.count = 0
            self.t = 1 - self.t # alternate turnstile index
            turnstile.release(self.num_threads)
        self.mutex.release()

        turnstile.acquire()


def watch(run, *args, **kwargs):
    try:
        run(*args, **kwargs)
        signal.pause()
    except KeyboardInterrupt:
        os.kill(os.getpid(), signal.SIGTERM)
