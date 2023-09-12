'''
example usage: python3 cam-gst.py & cat fifo-dmon | python3 dmonitor.py

camera        gstreamer     fifo-gst      us            fifo-dmon
.             .             .             .             .             
raw video---->.             .             .             .             
.             .             .             .             .             
.             [preprocess]  .             .             .             
.             .             .             .             .             
.             ------------->.             .             .             
.             .             .             .             .             
.             .             ------------->.             .             
.             .             .             .             .             
.             .             .             [pack]        .             
.             .             .             .             .             
.             .             .             ------------->.             
.             .             .             .             .             
'''

import json
import os
import subprocess
import sys

IM_SIZE = 1440 * 960
GST_PIPELINE = '''\
v4l2src \
! videoconvert \
! video/x-raw, format=GRAY8 \
! videoscale \
! video/x-raw, width=1440, height=960 \
! filesink location=fifo-gst \
'''

def pack(im):
    return json.dumps(im)

if not os.path.exists('fifo-gst'):
    subprocess.run('mkfifo fifo-gst'.split())
if not os.path.exists('fifo-dmon'):
    subprocess.run('mkfifo fifo-dmon'.split())
p_gst = subprocess.Popen(f'gst-launch-1.0 {GST_PIPELINE}'.split())
fifo_gst = open('fifo-gst', 'rb')
fifo_dmon = open('fifo-dmon', 'wb')
while True:
    buf = fifo_gst.read(IM_SIZE)
    assert len(buf) == IM_SIZE
    im = [i / 255 for i in buf]
    fifo_dmon.write(pack(im).encode())
    fifo_dmon.write(b'\0')
    fifo_dmon.flush()
