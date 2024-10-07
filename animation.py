import itertools
import time
import sys
import threading

def long_process():
    time.sleep(5)

def animate():
    thread = threading.Thread(target=long_process)
    thread.start()
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
        if not thread.is_alive():
            break
    sys.stdout.write('\rDone!     ')