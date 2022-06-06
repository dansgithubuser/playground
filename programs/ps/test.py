import pyprctl

import subprocess
import threading
import time

quit = False

def loop(thread_name):
    pyprctl.set_name(thread_name)
    while not quit:
        time.sleep(0.1)

threads = [
    threading.Thread(target=loop, args=(f'PS TEST {i}',))
    for i in range(5)
]
for thread in threads: thread.start()
subprocess.run(['ps', 'H', '-o', 'pid tid cmd comm pcpu'])
quit = True
