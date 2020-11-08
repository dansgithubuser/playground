import cv2

import argparse
import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--period', '-p', default=1, type=int)
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera_index)

while True:
    ret, frame = cap.read()
    file_name = '{:%Y-%m-%b-%d_%H-%M-%S}.png'.format(datetime.datetime.now()).lower()
    cv2.imwrite(file_name, frame)
    time.sleep(args.period)
