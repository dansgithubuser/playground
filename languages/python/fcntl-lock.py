import argparse
import datetime
import fcntl
import random
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('id', nargs='?', default='main')
args = parser.parse_args()

def timestamp():
    return datetime.datetime.now().isoformat(' ', 'milliseconds')

def tprint(s):
    print(timestamp(), s)

if args.id == 'main':
    procs = []
    for i in range(10):
        p = subprocess.Popen(['python3', 'fcntl-lock.py', str(i)])
        procs.append(p)
    for p in procs:
        p.wait()
else:
    indent = '\t' * int(args.id)
    for i in range(10):
        lock = open('lock', 'w')
        tprint(f'process {args.id}, iteration {i}, {indent}waiting')
        fcntl.lockf(lock, fcntl.LOCK_EX)
        tprint(f'process {args.id}, iteration {i}, {indent}locked')
        time.sleep(random.random() / 10)
        tprint(f'process {args.id}, iteration {i}, {indent}unlocking')
        lock.close()
