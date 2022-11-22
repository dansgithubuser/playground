#!/usr/bin/env python3

# requires rtsp-server.py running

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('server', nargs='?', default='localhost')
args = parser.parse_args()

def invoke(invocation):
    subprocess.run(invocation, shell=True, check=True)

invoke(f'ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i /dev/video0 -f rtsp rtsp://{args.server}:8554/webcam')
