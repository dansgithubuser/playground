import os
import subprocess
from pprint import pprint

import numpy as np

import dmonitor

IM_SIZE = 1440 * 960
GST_PIPELINE = '''\
libcamerasrc \
! videoconvert \
! video/x-raw, format=GRAY8 \
! videoscale \
! video/x-raw, width=1440, height=960 \
! filesink location=fifo-gst \
'''

if not os.path.exists('fifo-gst'):
    subprocess.run('mkfifo fifo-gst'.split())
p_gst = subprocess.Popen(f'gst-launch-1.0 {GST_PIPELINE}'.split())
fifo_gst = open('fifo-gst', 'rb')
while True:
    buf = fifo_gst.read(IM_SIZE)
    assert len(buf) == IM_SIZE
    im = np.array(list(buf), dtype=np.float32).reshape((1, -1)) / 255
    out = dmonitor.ort_sess.run(
        None,
        {
            'input_img': im,
            'calib': np.zeros((1, 3), dtype=np.float32),
        },
    )
    pprint(out)
