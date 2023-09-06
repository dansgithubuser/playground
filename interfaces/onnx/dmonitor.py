'''
Python script that takes input from stdin, puts into ONNX model, and prints the output.
'''

import numpy as np
import onnxruntime as ort

import json
import pprint
import sys

ort_sess = ort.InferenceSession('openpilot-dmonitor.onnx')
buf = bytearray()
while True:
    b = sys.stdin.buffer.read(1)[0]
    if b != 0:
        buf.append(b)
    else:
        pprint.pprint(ort_sess.run(None, {
            'input_img': np.array([json.loads(buf)], dtype=np.float32),
            'calib': np.zeros((1, 3), dtype=np.float32),
        }))
        buf.clear()
