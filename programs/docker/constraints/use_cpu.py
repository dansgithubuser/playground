#! /usr/bin/env python3

import os
import time

import psutil

def sample_usage(f):
    now = time.time()
    total = 0
    samples = 0
    while time.time() - now < 1:
        f()
        total += psutil.cpu_percent()
        samples += 1
    return total / samples * psutil.cpu_count()

baseline = sample_usage(lambda: time.sleep(0.1))
elevated = sample_usage(lambda: [i for i in range(200_000)])

print(f'usage: {elevated - baseline:.2f}%')
