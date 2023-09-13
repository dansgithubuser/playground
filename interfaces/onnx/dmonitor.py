'''
Python script that takes input from stdin, puts into ONNX model, and prints the output.
'''

import numpy as np
import onnxruntime as ort

import pprint
import struct
import sys

IM_SIZE = 1440 * 960

ort_sess = ort.InferenceSession('openpilot-dmonitor.onnx')
while True:
    buf = sys.stdin.buffer.read(IM_SIZE * 4)
    im = struct.unpack(f'{IM_SIZE}f', buf)
    out = ort_sess.run(
        None,
        {
            'input_img': np.array([im], dtype=np.float32),
            'calib': np.zeros((1, 3), dtype=np.float32),
        },
    )
    pprint.pprint(out)
