#!/usr/bin/env python3

import cv2
import numpy as np

import argparse
import math

parser = argparse.ArgumentParser(description='Draw the likelihood each pixel of an image came from similar source as subset of the image.')
parser.add_argument('image_path')
parser.add_argument('mask_xi', type=int)
parser.add_argument('mask_yi', type=int)
parser.add_argument('mask_xf', type=int)
parser.add_argument('mask_yf', type=int)
args = parser.parse_args()

HIST_SIZE = 16

class Mask:
    def __init__(self, xi, yi, xf, yf):
        self.xi = xi
        self.yi = yi
        self.xf = xf
        self.yf = yf

    def as_image(self, shape):
        image = np.zeros(shape, dtype='uint8')
        cv2.rectangle(image, (self.xi, self.yi), (self.xf, self.yf), 255, -1)
        return image

    def size(self):
        return (self.xf - self.xi) * (self.yf - self.yi)

    def outline(self, image, color):
        cv2.rectangle(image, (self.xi, self.yi), (self.xf, self.yf), color)

def get_hist(image, mask):
    return cv2.calcHist(
        images=[image],
        channels=[0, 1, 2],
        mask=mask.as_image(image.shape[:2]),
        histSize=[HIST_SIZE] * 3,
        ranges=[0, 256] * 3,
    ) / mask.size()

log_prob = np.vectorize(lambda x: 1 + math.log10(x + 1e-6) / 2)

def get_prob(image, mask):
    hist = get_hist(image, mask)
    prob = np.zeros(image.shape[:2])
    for x in range(0, 640):
        for y in range(0, 480):
            h = hist
            for c in image[y][x]:
                h = h[c // (256 // HIST_SIZE)]
            prob[y][x] = h
    return log_prob(prob)

image = cv2.imread(args.image_path)
mask = Mask(args.mask_xi, args.mask_yi, args.mask_xf, args.mask_yf)
prob = get_prob(image, mask)

mask.outline(image, (255, 255, 255))
cv2.imshow('image', image)
cv2.imshow('prob', prob)
cv2.moveWindow('image', 0, 0)
cv2.moveWindow('prob', image.shape[1], 0)
print('Press escape key to close windows.')
while cv2.waitKey() != 27: pass
