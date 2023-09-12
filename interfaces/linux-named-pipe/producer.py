from datetime import datetime
import os
import subprocess
import time

if not os.path.exists('fifo'):
    subprocess.run('mkfifo fifo'.split(), check=True)

with open('fifo', 'a') as fifo:
    while True:
        fifo.write(f'{datetime.now().isoformat()}\n')
        fifo.flush()
        time.sleep(1)
