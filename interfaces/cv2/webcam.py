#!/usr/bin/env python3

import cv2

import argparse
import datetime
import subprocess
import sys
import traceback
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--file', '-f', action='store_true')
parser.add_argument('--file-ext', default='avi')
parser.add_argument('--list', '-l', action='store_true')
parser.add_argument('--list-formats', '--lf', action='store_true')
parser.add_argument('--pixel-format')
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--dim', '-d', help='<width>x<height>')
parser.add_argument('--fps', type=int)
parser.add_argument('--rotate', choices=['90', '180', '270'])
args = parser.parse_args()

if args.dim:
    w, h = args.dim.split('x')
    args.width = int(w)
    args.height = int(h)

def timestamp():
    return '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())

def open_camera():
    cap = cv2.VideoCapture(args.camera_index)
    if args.pixel_format: cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*args.pixel_format))
    if args.width: cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    if args.height: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    if args.fps: cap.set(cv2.CAP_PROP_FPS, args.fps)
    return cap

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
        'v4l2-ctl',  # apt install v4l-utils
        '-d', f'/dev/video{args.camera_index}',
        '--list-formats-ext',
    ])
    sys.exit()

print('Hit escape to exit.')
writer = None
done = False
while not done:
    try:
        cap = open_camera()
        if args.file and not writer:
            shape = cap.read()[1].shape
            writer = cv2.VideoWriter(
                f'rec-{timestamp()}.{args.file_ext}',
                cv2.VideoWriter_fourcc(*args.pixel_format),
                cap.get(cv2.CAP_PROP_FPS),
                (shape[1], shape[0]),
            )
    except:
        traceback.print_exc()
        time.sleep(2)
        continue
    while True:
        try:
            ret, frame = cap.read()
            if args.rotate:
                frame = cv2.rotate(
                    frame,
                    {
                        '90': cv2.ROTATE_90_CLOCKWISE,
                        '180': cv2.ROTATE_180,
                        '270': cv2.ROTATE_90_COUNTERCLOCKWISE,
                    }[args.rotate],
                )
            cv2.imshow('Input', frame)
            if args.file: writer.write(frame)
        except:
            traceback.print_exc()
            break
        c = cv2.waitKey(1)
        if c == 27:
            done = True
            break
if args.file: writer.release()
