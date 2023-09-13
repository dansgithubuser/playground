'''
example usage: python3 cam-cv2.py | python3 dmonitor.py
'''

import cv2
import numpy as np

import struct
import sys

IM_SIZE = 1440 * 960

def resize(im):
    w_f = 1440
    h_f = 960
    aspect_f = w_f / h_f
    w_i = im.shape[1]
    h_i = im.shape[0]
    aspect_i = w_i / h_i
    if abs(aspect_i - aspect_f) < 0.01:  # close enough
        im = cv2.resize(im, (w_f, h_f))
    elif aspect_i > aspect_f:  # too wide
        scale = h_f / h_i
        im = cv2.resize(im, (
            round(w_i * scale),
            h_f,
        ))
        center = im.shape[1] // 2
        left = center - w_f // 2
        right = left + w_f
        im = im[:, left:right]
    else:  # too tall
        scale = w_f / w_i
        im = cv2.resize(im, (
            w_f,
            round(h_i * scale),
        ))
        center = im.shape[0] // 2
        top = center - h_f // 2
        bottom = top + h_f
        im = im[top:bottom, :]
    return im

def preprocess(im):
    im = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
    im = cv2.split(im)[0]
    im = np.float32(im) / 255
    im = im.reshape(-1)
    return im

def pack(im):
    return struct.pack(f'{IM_SIZE}f', *im)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
while True:
    ret, im = cap.read()
    if not ret: break
    sys.stdout.buffer.write(pack(preprocess(resize(im))))
    sys.stdout.flush()
