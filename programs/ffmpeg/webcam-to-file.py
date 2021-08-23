#! /usr/bin/env python3

import argparse
import datetime
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('device', nargs='?', default='/dev/video0', help='default: /dev/video0')
args = parser.parse_args()

def timestamp():
    return '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())

print('q to end recording')
subprocess.run(f'ffmpeg -i {args.device} rec-{timestamp()}.mkv'.split())
