#!/usr/bin/env python3

import random

with open('toy1.csv', 'w') as f:
    f.write('x, equal, zero, small, random, noisy\n')
    for x in range(100):
        f.write(f'{x}, {x}, 0, {x / 100}, {random.random()}, {x + random.random() * 300}\n')

with open('toy2.csv', 'w') as f:
    f.write('out, in1, in2, in3, in4, in5\n')
    for _ in range(1000):
        in1 = random.random()
        in2 = random.random()
        in3 = random.random()
        in4 = random.random()
        in5 = random.random()
        effect1 = in1
        effect2 = 0
        effect3 = in3 / 8
        effect4 = random.random()
        effect5 = in5 + random.random()
        out = effect1 + effect2 + effect3 + effect4 + effect5
        f.write(f'{out}, {in1}, {in2}, {in3}, {in4}, {in5}\n')
