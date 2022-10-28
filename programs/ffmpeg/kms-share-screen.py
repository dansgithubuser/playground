#!/usr/bin/env python3

# appropriate in Ubuntu 22 with Wayland
# requires rtsp-server.py running

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('server', nargs='?', default='localhost')
args = parser.parse_args()

def invoke(invocation):
    subprocess.run(invocation, shell=True, check=True)

invoke(f'''sudo ffmpeg -f kmsgrab -i - -vf 'hwmap=derive_device=vaapi,hwdownload,format=bgr0' -f rtsp -muxdelay 0.1 rtsp://{args.server}:8554/screen''')
