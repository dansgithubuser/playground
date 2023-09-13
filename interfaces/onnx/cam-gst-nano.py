'''
for Jetson Nano
example usage: python3 cam-gst-nano.py & cat fifo-dmon | python3 dmonitor.py

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

import os
import struct
import subprocess
import sys

IM_SIZE = 1440 * 960
I420_SIZE = IM_SIZE * 3 // 2
GST_PIPELINE = '''\
nvarguscamerasrc \
! nvvidconv \
! video/x-raw, format=I420 \
! videoscale \
! video/x-raw, width=1440, height=960 \
! filesink location=fifo-gst \
'''

def pack(im):
    return struct.pack(f'{IM_SIZE}f', *im)

if not os.path.exists('fifo-gst'):
    subprocess.run('mkfifo fifo-gst'.split())
if not os.path.exists('fifo-dmon'):
    subprocess.run('mkfifo fifo-dmon'.split())
p_gst = subprocess.Popen(f'gst-launch-1.0 {GST_PIPELINE}'.split())
fifo_gst = open('fifo-gst', 'rb')
fifo_dmon = open('fifo-dmon', 'wb')
while True:
    buf = fifo_gst.read(I420_SIZE)
    assert len(buf) == I420_SIZE
    im = [i / 255 for i in buf[:IM_SIZE]]
    fifo_dmon.write(pack(im))
    fifo_dmon.flush()
