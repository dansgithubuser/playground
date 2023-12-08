'''
Python script that takes input from stdin, puts into ONNX model, and prints the output.
'''

import numpy as np
import onnxruntime as ort

import os
import pprint
import struct
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
IM_SIZE = 1440 * 960

print(f'dmonitor.py PID is {os.getpid()}')
ort_sess = ort.InferenceSession(os.path.join(DIR, '../openpilot/dmonitor.onnx'))
while True:
    buf = sys.stdin.buffer.read(IM_SIZE * 4)
    im = np.frombuffer(buf, dtype=np.float32).reshape((1, -1))
    out = ort_sess.run(
        None,
        {
            'input_img': im,
            'calib': np.zeros((1, 3), dtype=np.float32),
        },
    )
    pprint.pprint(out)
