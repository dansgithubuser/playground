import cv2

import os
import re

paths = sorted([
    path
    for path in os.listdir('.')
    if re.search('(png|jpg)$', path)
])
i = 0
done = False
while not done:
    im = cv2.imread(paths[i])
    cv2.imshow('timelapse-preview', im)
    k = -1
    while k == -1:
        k = cv2.waitKey(100)
        if cv2.getWindowProperty('timelapse-preview', cv2.WND_PROP_VISIBLE) < 1:
            done = True
            break
    if k in [
        108,  # j
        106,  # l
         83,  # right
         84,  # down
         13,  # enter
         32,  # space
    ]:
        if i < len(paths) - 1:
            i += 1
    elif k in [
        104,  # h
        107,  # k
         81,  # left
         82,  # up
    ]:
        if i > 0:
            i -= 1
