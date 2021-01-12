#!/usr/bin/env python3

import subprocess
import sys

subprocess.run(['cargo', 'build'], check=True)

names = [
    'alice',
    'bob',
    'charlie',
    'denise',
    'emily',
    'frank',
    'gary',
    'harry',
    'ingrid',
    'jerry',
]

procs = [
    subprocess.Popen(['target/debug/rusqlite', name])
    for name in names
]
r = 0
for proc in procs: r |= proc.wait()
sys.exit(r)
