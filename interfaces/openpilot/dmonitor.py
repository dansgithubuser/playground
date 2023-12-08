#!/usr/bin/env python3

# from https://github.com/commaai/openpilot 31ab43ce41d6d0f88cb8a9b6df8e79f23b6309fe

#===== imports =====#
import cv2
import numpy as np
import onnxruntime as ort

import math
import os
import time

#===== consts =====#
REG_SCALE = 0.25
DRAW_LEFT_FACE = int(os.environ.get('DMON_DRAW_LEFT_FACE', '1'))
LEFT_FACE_X_OFFSET = int(os.environ.get('DMON_LEFT_FACE_X_OFFSET', '0'))
LEFT_FACE_Y_OFFSET = int(os.environ.get('DMON_LEFT_FACE_Y_OFFSET', '0'))
LEFT_FACE_YAW_OFFSET = int(os.environ.get('DMON_LEFT_FACE_YAW_OFFSET', '0'))
LEFT_FACE_PITCH_OFFSET = int(os.environ.get('DMON_LEFT_FACE_PITCH_OFFSET', '0'))
DRAW_RIGHT_FACE = int(os.environ.get('DMON_DRAW_RIGHT_FACE', '1'))
RIGHT_FACE_X_OFFSET = int(os.environ.get('DMON_RIGHT_FACE_X_OFFSET', '0'))
RIGHT_FACE_Y_OFFSET = int(os.environ.get('DMON_RIGHT_FACE_Y_OFFSET', '0'))
RIGHT_FACE_YAW_OFFSET = int(os.environ.get('DMON_RIGHT_FACE_YAW_OFFSET', '0'))
RIGHT_FACE_PITCH_OFFSET = int(os.environ.get('DMON_RIGHT_FACE_PITCH_OFFSET', '0'))
DRAW_STATS = int(os.environ.get('DMON_DRAW_STATS', '1'))

#===== types =====#
class DriverData:
    def __init__(self, model_output_driver):
        mod = model_output_driver
        self.faceOrientation    = [float(i) * REG_SCALE for i in mod[0:3]]
        self.facePosition       = [float(i) * REG_SCALE for i in mod[3:5]]
        self.faceSize           = float(mod[5])
        self.faceOrientationStd = [math.exp(i) for i in mod[6:9]]
        self.facePositionStd    = [math.exp(i) for i in mod[9:11]]
        self.faceSizeStd        = math.exp(mod[11])
        self.faceProb           = sigmoid(mod[12])

        self.eyes               = [float(i) for i in mod[13:31]]
        self.leftEyeProb        = sigmoid(mod[21])  # one of these four has gotta be wrong?
        self.rightEyeProb       = sigmoid(mod[30])
        self.leftBlinkProb      = sigmoid(mod[31])
        self.rightBlinkProb     = sigmoid(mod[32])

        self.sunglassesProb     = sigmoid(mod[33])
        self.occludedProb       = sigmoid(mod[34])
        self.readyProb          = [sigmoid(i) for i in mod[35:39]]  # touching wheel, paying attention, deprecated distracted 1, deprecated distracted 2
        self.notReadyProb       = [sigmoid(i) for i in mod[39:41]]  # using phone, distracted

    def face_pitch(self):
        return self.faceOrientation[0]

    def face_yaw(self):
        return self.faceOrientation[1]

    def touching_wheel(self):
        return self.readyProb[0]

    def paying_attention(self):
        return self.readyProb[1]

    def deprecated_1(self):
        return self.readyProb[2]

    def deprecated_2(self):
        return self.readyProb[2]

    def using_phone(self):
        return self.notReadyProb[0]

    def distracted(self):
        return self.notReadyProb[1]

class DriverState:
    def __init__(self, model_output):
        mo = model_output
        self.leftDriverData = DriverData(mo[0][0][0:41])
        self.rightDriverData = DriverData(mo[0][0][41:82])
        self.poorVisionProb = sigmoid(mo[0][0][82])
        self.wheelOnRightProb = sigmoid(mo[0][0][83])

    def driver_data(self):
        return [self.leftDriverData, self.rightDriverData]

    def driver_data_active(self):
        if self.wheelOnRightProb < 0.5:
            return self.leftDriverData
        else:
            return self.rightDriverData

#===== globals =====#
sess = ort.InferenceSession('dmonitor.onnx', providers=['CPUExecutionProvider'])

#===== helpers =====#
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def put_text(
    im,
    lines,
    x,
    y,
    float_fmt='{:>7.3f}',
    size=0.5,
    fg_color=(255, 255, 255),
    bg_color=(0, 0, 0),
):
    for line in lines:
        if type(line) == float:
            line = float_fmt.format(line)
        elif type(line) == list and len(line) and type(line[0]) == float:
            line = ' '.join([float_fmt.format(i) for i in line])
        else:
            line = str(line)
        cv2.putText(im, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, bg_color, 2)
        cv2.putText(im, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, fg_color, 1)
        y += 24 * size

def resize(im):
    w_f = 1440
    h_f = 960
    aspect_f = w_f / h_f
    w_i = im.shape[1]
    h_i = im.shape[0]
    aspect_i = w_i / h_i
    if w_i == w_f and h_i == h_f:  # equal
        return im
    if abs(aspect_i - aspect_f) < 0.01:  # close enough
        im = cv2.resize(im, (w_f, h_f))
    elif aspect_i > aspect_f:  # too wide
        scale = h_f / h_i
        im = cv2.resize(im, (
            round(w_i * scale),
            h_f,
        ))
        center = im.shape[1] // 2
        left = center - w_f // 2
        right = left + w_f
        im = im[:, left:right]
    else:  # too tall
        scale = w_f / w_i
        im = cv2.resize(im, (
            w_f,
            round(h_i * scale),
        ))
        center = im.shape[0] // 2
        top = center - h_f // 2
        bottom = top + h_f
        im = im[top:bottom, :]
    assert im.shape[0] == h_f
    assert im.shape[1] == w_f
    return im

def draw_eye(im, center, blink, color, thickness):
    if blink:
        end = 180
    else:
        end = 360
    cv2.ellipse(im, center, (20, 10), 0, 0, end, color, thickness)

def preprocess(im):
    im = resize(im)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2YUV)
    im = cv2.split(im)[0]
    im = np.float32(im) / 255
    im = im.reshape(1, -1)
    return im

def predict(im):
    im = preprocess(im)
    calib = np.zeros((1, 3), dtype=np.float32)
    start = time.time()
    output = sess.run(None, {'input_img': im, 'calib': calib})
    duration = time.time() - start
    return output, duration

def postprocess(output):
    output, _ = output
    return DriverState(output)

def postprocess_im(output, im):
    _, latency = output
    driver_state = postprocess(output)
    im_w = im.shape[1]
    im_h = im.shape[0]
    if DRAW_STATS:
        put_text(
            im,
            [
                'poor vis',
                'wheel right',
                'latency',
            ],
            8,
            600,
        )
        put_text(
            im,
            [
                driver_state.poorVisionProb,
                driver_state.wheelOnRightProb,
                latency,
            ],
            120,
            600,
        )
    for dd_i, dd in enumerate(driver_state.driver_data()):
        if dd_i == 0 and not DRAW_LEFT_FACE:
            continue
        if dd_i == 1 and not DRAW_RIGHT_FACE:
            continue
        if dd_i == 0:
            x_offset = LEFT_FACE_X_OFFSET
            y_offset = LEFT_FACE_Y_OFFSET
            yaw_offset = LEFT_FACE_YAW_OFFSET
            pitch_offset = LEFT_FACE_PITCH_OFFSET
        elif dd_i == 1:
            x_offset = RIGHT_FACE_X_OFFSET
            y_offset = RIGHT_FACE_Y_OFFSET
            yaw_offset = RIGHT_FACE_YAW_OFFSET
            pitch_offset = RIGHT_FACE_PITCH_OFFSET
        color = [(255, 255, 0), (0, 255, 0)][dd_i]
        if DRAW_STATS:
            put_text(
                im,
                [
                    'face prob',
                    'face position',
                    'eye prob',
                    'blink prob',
                    'sunglasses',
                ],
                8 + im_w // 2 * (1 - dd_i),
                480,
                fg_color=color,
            )
            put_text(
                im,
                [
                    dd.faceProb,
                    dd.facePosition,
                    [dd.leftEyeProb, dd.rightEyeProb],
                    [dd.leftBlinkProb, dd.rightBlinkProb],
                    dd.sunglassesProb,
                ],
                120 + im_w // 2 * (1 - dd_i),
                480,
                fg_color=color,
            )
        dx, dy = dd.facePosition
        x = int((dx + 1/2) * im_w) + x_offset
        y = int((dy + 1/6) * im_h) + y_offset
        face_size = 80
        eye_space = 30
        if dd.faceProb > 0.5:
            cv2.circle(im, (x, y), face_size, color, 2)
            nose_x = int(math.sin(dd.face_yaw()   + yaw_offset) * face_size)
            nose_y = int(math.sin(dd.face_pitch() + pitch_offset) * face_size)
            cv2.ellipse(im, (x, y), (abs(nose_x), face_size), 0 if nose_x > 0 else 180, 90, 270, color, 2)
            cv2.ellipse(im, (x, y), (face_size, abs(nose_y)), 0 if nose_y < 0 else 180,  0, 180, color, 2)
            if dd.leftEyeProb > 0.1:
                draw_eye(im, (x - eye_space, y - eye_space), dd.leftBlinkProb > 0.25, color, 2)
            if dd.rightEyeProb > 0.1:
                draw_eye(im, (x + eye_space, y - eye_space), dd.rightBlinkProb > 0.25, color, 2)
        if (dd_i == 1) == (driver_state.wheelOnRightProb > 0.5):
            cv2.circle(im, (x, y), face_size + 5, color, 2)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    while True:
        ret, im = cap.read()
        if not ret:
            break
        output = predict(im)
        postprocess_im(output, im)
        cv2.imshow('dmonitor', im)
        c = cv2.waitKey(1)
        if c == 27:
            break
