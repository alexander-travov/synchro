import os
import signal


def watch(run, *args, **kwargs):
    try:
        run(*args, **kwargs)
        signal.pause()
    except KeyboardInterrupt:
        os.kill(os.getpid(), signal.SIGTERM)
