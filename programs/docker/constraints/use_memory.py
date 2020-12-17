#! /usr/bin/env python3

from print_styled import print_styled

import psutil

import time

x = []

for _ in range(50):
    info = psutil.Process().memory_full_info()
    print(f'using {info.rss / 1_000_000:7.3f} MB, {info.swap / 1_000_000:7.3f} MB swap')
    if info.rss + info.swap > 50_000_000:
        break
    for _ in range(200_000):
        x.append(time.time())

print_styled('<yellow>all done')
