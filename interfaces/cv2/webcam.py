import cv2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera_index)

while True:
    ret, frame = cap.read()
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break
