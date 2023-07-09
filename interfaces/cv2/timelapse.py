#!/usr/bin/env python3

import cv2

import argparse
import datetime
import math
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
parser.add_argument('--skip-similar', nargs='?', const=True,
    metavar='[threshold_cushion=1.05] [attention_span=60] [max_consecutive_attention=3] [max_time_between_images=300]',
    help=(
        'threshold_cushion: how much dissimilarity should exceed average to give attention, '
        'attention_span: images to take before stopping attention, '
        'max_consecutive_attention: reduce threshold by threshold_cushion after this number of consecutive attentions, '
        'max_time_between_images: in seconds'
    )
)
parser.add_argument('--rm-thresh-gb', type=float, default=1, help='Remove old images when this much disk or less remains, in gigabytes.')
parser.add_argument('--rm-amount-gb', type=float, default=0.1, help='Remove this many gigabytes of images when threshold reached.')
parser.add_argument('--preview', action='store_true')
args = parser.parse_args()

class SimilarChecker:
    def __init__(self, threshold_cushion=1.05, attention_span=60, max_consecutive_attention=3, max_time_between_images=300):
        self.threshold_cushion = threshold_cushion
        self.attention_span = attention_span
        self.max_consecutive_attention = max_consecutive_attention
        self.max_time_between_images = max_time_between_images
        self.frame = None
        self.d_hist = []
        self.threshold = math.inf
        self.t_frame = 0
        self.t_attention = 0
        self.consecutive_attention = 0

    def set_frame(self, frame):
        self.frame = frame
        self.t_frame = time.time()

    def is_similar(self, frame):
        assert frame.dtype.name == 'uint8'
        # first frame
        if self.frame is None or time.time() - self.t_attention < self.attention_span:
            self.set_frame(frame)
            return False
        # calculate difference
        d = cv2.norm(self.frame, frame, cv2.NORM_L1) / (frame.size * 256)
        self.d_hist.append(d)
        if len(self.d_hist) > self.max_time_between_images:
            del self.d_hist[0]
        # attention span
        if time.time() - self.t_attention < self.attention_span:
            self.set_frame(frame)
            return False
        # compare to threshold (check if should pay attention)
        if d > self.threshold:
            self.set_frame(frame)
            self.t_attention = time.time()
            self.consecutive_attention += 1
            if self.consecutive_attention > self.max_consecutive_attention:
                self.threshold / self.threshold_cushion
            print(f'{datetime.datetime.now().isoformat()} dissimilarity: {d:.5} threshold: {self.threshold:.5} ❕')
            return False
        self.consecutive_attention = 0
        # max time between images
        if time.time() - self.t_frame > self.max_time_between_images:
            self.set_frame(frame)
            self.threshold = max(self.d_hist) * self.threshold_cushion
            print(f'{datetime.datetime.now().isoformat()} dissimilarity: {d:.5} threshold: {self.threshold:.5} ⌚')
            return False
        # otherwise similar
        print(f'{datetime.datetime.now().isoformat()} dissimilarity: {d:.5} threshold: {self.threshold:.5} ', end='\r')
        return True

if args.skip_similar == True:
    similar_checker = SimilarChecker()
elif args.skip_similar:
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
