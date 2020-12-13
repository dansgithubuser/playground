import cv2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--file', action='store_true')
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera_index)
if args.file:
    cod = cv2.VideoWriter_fourcc(*'H264')
    fps = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()
    writer = cv2.VideoWriter('rec.mp4', cod, fps, frame.shape[:2])

while True:
    ret, frame = cap.read()
    cv2.imshow('Input', frame)

    if args.file:
        writer.write(frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

writer.release()
