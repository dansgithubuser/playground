#!/usr/bin/env python3

# Linux CPU usage monitor

import time

class State:
    def __init__(self, stat):
        line = stat.readline()
        stat.seek(0)
        jiffies = [int(i) for i in line.split()[1:]]
        self.user = jiffies[0]
        self.system = jiffies[2]
        self.idle = jiffies[3]
        self.other = jiffies[1] + sum(jiffies[4:])
        self.total = sum(jiffies)

    def compare(self, other):
        total = self.total - other.total
        return (
            100 * (self.user   - other.user  ) / total,
            100 * (self.system - other.system) / total,
            100 * (self.idle   - other.idle  ) / total,
            100 * (self.other  - other.other ) / total,
        )

stat = open('/proc/stat', 'r')
state_prev = None
while True:
    state = State(stat)
    if state_prev:
        user, system, idle, other = state.compare(state_prev)
        print(f'usr {user:5.1f}, sys {system:5.1f}, idl {idle:5.1f}, oth {other:5.1f}')
    state_prev = state
    time.sleep(0.25)
