from datetime import datetime
import os
import subprocess
import time

if not os.path.exists('fifo'):
    subprocess.run('mkfifo fifo'.split(), check=True)

with open('fifo', 'r') as fifo:
    while True:
        print(fifo.readline(), end='')
