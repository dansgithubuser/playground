#!/usr/bin/env python3

import cv2

import argparse
import datetime
import os
import shutil
import time
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--period', '-p', default=1, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--extension', '-e', default='png')
parser.add_argument('--skip-similar', metavar='threshold [attention span] [max time between images]')
parser.add_argument('--rm-thresh-gb', type=float, default=1, help='Remove old images when this much disk or less remains, in gigabytes.')
parser.add_argument('--rm-amount-gb', type=float, default=0.1, help='Remove this many gigabytes of images when threshold reached.')
parser.add_argument('--preview', action='store_true')
args = parser.parse_args()

class SimilarChecker:
    def __init__(self, threshold, attention_span=60, max_time_between_images=300):
        self.threshold = threshold
        self.attention_span = attention_span
        self.max_time_between_images = max_time_between_images
        self.frame = None
        self.t_frame = 0
        self.t_attention = 0

    def is_similar(self, frame):
        assert frame.dtype.name == 'uint8'
        # first frame and attention span
        if self.frame is None or time.time() - self.t_attention < self.attention_span:
            self.frame = frame
            self.t_frame = time.time()
            return False
        # calculate difference
        d = cv2.norm(self.frame, frame, cv2.NORM_L1) / (frame.shape[0] * frame.shape[1] * frame.shape[2] * 256)
        # compare to threshold
        if d > self.threshold:
            self.frame = frame
            self.t_frame = time.time()
            self.t_attention = time.time()
            print(f'{datetime.datetime.now().isoformat()} {d} ❕')
            return False
        # max time between images
        if time.time() - self.t_frame > self.max_time_between_images:
            self.frame = frame
            self.t_frame = time.time()
            print(f'{datetime.datetime.now().isoformat()} {d} ⌚')
            return False
        # otherwise similar
        print(f'{datetime.datetime.now().isoformat()} {d:.3f}', end='\r')
        return True

if args.skip_similar:
    similar_checker = SimilarChecker(*[float(i) for i in args.skip_similar.split()])

def rm_old():
    if shutil.disk_usage('.').free / 1e9 > args.rm_thresh_gb: return
    for path in sorted(os.listdir('.')):
        os.remove(path)
        if shutil.disk_usage('.').free / 1e9> args.rm_thresh_gb + args.rm_amount_gb: return

def main():
    cap = cv2.VideoCapture(args.camera_index)
    if args.width: cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    if args.height: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    while True:
        ret, frame = cap.read()
        if args.preview:
            cv2.imshow('preview', frame)
            cv2.waitKey(1)
        if not args.skip_similar or not similar_checker.is_similar(frame):
            file_name = (
                '{:%Y-%m-%b-%d_%H-%M-%S}.{}'
                .format(
                    datetime.datetime.now(),
                    args.extension,
                )
                .lower()
            )
            cv2.imwrite(file_name, frame)
        time.sleep(args.period)
        rm_old()

while True:
    try:
        main()
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()
    time.sleep(1)
