#!/usr/bin/env python

import numpy as np
import pyopencl as cl

import time

a_np = np.random.rand(100_000_000).astype(np.float32)
b_np = np.random.rand(100_000_000).astype(np.float32)

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_np)
b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_np)

prg = cl.Program(ctx, """
__kernel void sum(
    __global const float *a_g, __global const float *b_g, __global float *res_g)
{
  int gid = get_global_id(0);
  res_g[gid] = sqrt(a_g[gid] + b_g[gid]);
}
""").build()

t_i = time.time()

res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a_np.nbytes)
knl = prg.sum  # Use this Kernel object for repeated calls
knl(queue, a_np.shape, None, a_g, b_g, res_g)

res_np = np.empty_like(a_np)
cl.enqueue_copy(queue, res_np, res_g)

dur_cl = time.time() - t_i

# Check on CPU with Numpy:
print(res_np)
t_i = time.time()
expected = np.sqrt(a_np + b_np)
dur_np = time.time() - t_i
print(expected)

print(f'cl time: {dur_cl * 1e3:9.1f} ms')
print(f'np time: {dur_np * 1e3:9.1f} ms')

assert np.allclose(res_np, expected)
