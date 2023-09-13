import time

x = [i % 256 for i in range(1_000_000)]

t0 = time.time()
y = [i / 256 for i in x]
tf = time.time()
print(tf - t0, 's')
