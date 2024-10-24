#!/usr/bin/env python3

import subprocess
import time

server = subprocess.Popen('python3 server'.split())
try:
    time.sleep(1)
    subprocess.run('python3 client'.split(), check=True)
    time.sleep(1)
finally:
    server.kill()
