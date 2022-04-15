#!/usr/bin/env python3

import cv2

import argparse
import datetime
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--file', '-f', action='store_true')
parser.add_argument('--list', '-l', action='store_true')
parser.add_argument('--list-formats', '--lf', action='store_true')
parser.add_argument('--pixel-format')
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--dim', '-d', help='<width>x<height>')
parser.add_argument('--fps', type=int)
args = parser.parse_args()

if args.dim:
    w, h = args.dim.split('x')
    args.width = int(w)
    args.height = int(h)

def timestamp():
    return '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())

if args.list:
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f'{i} {w} x {h} @ {fps}')
        cap.release()
    try: subprocess.run(['uvcdynctrl', '-l'])
    except: pass
    sys.exit()

if args.list_formats:
    subprocess.run([
        'v4l2-ctl',
        '-d', f'/dev/video{args.camera_index}',
        '--list-formats-ext',
    ])
    sys.exit()

cap = cv2.VideoCapture(args.camera_index)
if args.pixel_format: cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*args.pixel_format))
if args.width: cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
if args.height: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
if args.fps: cap.set(cv2.CAP_PROP_FPS, args.fps)
if args.file:
    cod = cv2.VideoWriter_fourcc(*'H264')
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()
    writer = cv2.VideoWriter(f'rec-{timestamp()}.mp4', cod, fps, frame.shape[:2])
print('Hit escape to exit.')
while True:
    ret, frame = cap.read()
    cv2.imshow('Input', frame)
    if args.file: writer.write(frame)
    c = cv2.waitKey(1)
    if c == 27:
        break
if args.file: writer.release()
