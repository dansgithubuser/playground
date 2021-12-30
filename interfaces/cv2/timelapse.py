import cv2

import argparse
import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--period', '-p', default=1, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--extension', '-e', default='png')
args = parser.parse_args()

def main():
    cap = cv2.VideoCapture(args.camera_index)
    if args.width: cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    if args.height: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    while True:
        ret, frame = cap.read()
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

while True:
    try:
        main()
    except Exception as e:
        print(e)
    time.sleep(1)
