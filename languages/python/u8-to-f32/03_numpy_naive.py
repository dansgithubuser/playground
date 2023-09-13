import numpy as np

import time

x = [i % 256 for i in range(1_000_000)]

t0 = time.time()
y = np.array(x, dtype=np.float32)
y /= 255
tf = time.time()
print(tf - t0, 's')
