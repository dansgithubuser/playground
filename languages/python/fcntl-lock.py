import argparse
import fcntl
import random
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('id', nargs='?', default='main')
args = parser.parse_args()

if args.id == 'main':
    procs = []
    for i in range(10):
        p = subprocess.Popen(['python3', 'fcntl-lock.py', str(i)])
        procs.append(p)
    for p in procs:
        p.wait()
else:
    for i in range(10):
        lock = open('lock', 'w')
        fcntl.lockf(lock, fcntl.LOCK_EX)
        print(f'process {args.id}, iteration {i}, locked')
        time.sleep(random.random())
        print(f'process {args.id}, iteration {i}, unlocking')
        lock.close()
