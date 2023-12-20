#!/usr/bin/env python3

# from https://github.com/commaai/openpilot 31ab43ce41d6d0f88cb8a9b6df8e79f23b6309fe

#===== imports =====#
import cv2
import numpy as np
import onnxruntime as ort

import argparse
import time

#===== args =====#
parser = argparse.ArgumentParser()
parser.add_argument('video_path')
parser.add_argument('--fov', type=float, default=60)

#===== consts =====#
def index_function(idx, max_val=192, max_idx=32):
    return (max_val) * ((idx/max_idx)**2)

OUTPUT_SLICES = {
    'plan':                   slice(   0, 4955, None),
    'lane_lines':             slice(4955, 5483, None),
    'lane_lines_prob':        slice(5483, 5491, None),
    'road_edges':             slice(5491, 5755, None),
    'lead':                   slice(5755, 5857, None),
    'lead_prob':              slice(5857, 5860, None),
    'desire_state':           slice(5860, 5868, None),
    'meta':                   slice(5868, 5916, None),
    'desire_pred':            slice(5916, 5948, None),
    'pose':                   slice(5948, 5960, None),
    'wide_from_device_euler': slice(5960, 5966, None),
    'sim_pose':               slice(5966, 5978, None),
    'road_transform':         slice(5978, 5990, None),
    'lat_planner_solution':   slice(5990, 6254, None),
    'hidden_state':           slice(6254,   -2, None),
    'pad':                    slice(  -2, None, None),
}

DT_MDL = 0.05

IDX_N = 33
T_IDXS = [index_function(idx, max_val=10.0) for idx in range(IDX_N)]

HISTORY_BUFFER_LEN = 99
DESIRE_LEN = 8
NAV_FEATURE_LEN = 256
NAV_INSTRUCTION_LEN = 150
FEATURE_LEN = 512
LAT_PLANNER_STATE_LEN = 4

POSE_WIDTH = 6
WIDE_FROM_DEVICE_WIDTH = 3
LEAD_WIDTH = 4
LANE_LINES_WIDTH = 2
PLAN_WIDTH = 15
DESIRE_PRED_WIDTH = 8
LAT_PLANNER_SOLUTION_WIDTH = 4

NUM_LANE_LINES = 4
NUM_ROAD_EDGES = 2

LEAD_TRAJ_LEN = 6
DESIRE_PRED_LEN = 4

PLAN_MHP_N = 5
LEAD_MHP_N = 2
PLAN_MHP_SELECTION = 1
LEAD_MHP_SELECTION = 3

MODEL_WIDTH = 512
MODEL_HEIGHT = 256
MODEL_FRAME_SIZE = MODEL_WIDTH * MODEL_HEIGHT * 3 // 2

#===== globals =====#
sess = ort.InferenceSession('supercombo.onnx', providers=['CPUExecutionProvider'])

#===== helpers =====#
#----- math -----#
def sigmoid(x):
    return 1. / (1. + np.exp(-x))

def softmax(x, axis=-1):
    x -= np.max(x, axis=axis, keepdims=True)
    if x.dtype == np.float32 or x.dtype == np.float64:
        np.exp(x, out=x)
    else:
        x = np.exp(x)
    x /= np.sum(x, axis=axis, keepdims=True)
    return x

def interp(x, xp, fp):
    N = len(xp)

    def get_interp(xv):
        hi = 0
        while hi < N and xv > xp[hi]:
            hi += 1
        low = hi - 1
        return fp[-1] if hi == N and xv > xp[low] else (
            fp[0] if hi == 0 else
            (xv - xp[low]) * (fp[hi] - fp[low]) / (xp[hi] - xp[low]) + fp[low])

    return [get_interp(v) for v in x] if hasattr(x, '__iter__') else get_interp(x)

#----- graphics -----#
# ratio is final_width / original_width
# aspect is 2w:1h
def center_crop(im, ratio):
    assert ratio <= 1
    w_i = im.shape[1]
    h_i = im.shape[0]
    w_f = int(w_i * ratio)
    h_f = w_f // 2
    x_i = w_i // 2 - w_f // 2
    x_f = x_i + w_f
    y_i = h_i // 2 - h_f // 2
    y_f = y_i + h_f
    return im[y_i:y_f, x_i:x_f]

def transform(im):
    im = cv2.resize(im, (MODEL_WIDTH, MODEL_HEIGHT))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2YUV_I420)
    y = im[   :256]
    u = im[256:320].reshape((128, 256))
    v = im[320:384].reshape((128, 256))
    return np.array([  # see openpilot repo's selfdrive/modeld/transforms/loadyuv.cl loadys
        y[0::2, 0::2],  # even rows even cols
        y[1::2, 0::2],  # odd rows even cols
        y[0::2, 1::2],  # even rows odd cols
        y[1::2, 1::2],  # odd rows odd cols
        u,
        v,
    ])

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

def to_top_view(vec):
    x = vec[0]
    y = vec[1]
    return int(y * 10 + 320), int(x * -10 + 240)

def to_right_view(vec):
    x = vec[0]
    z = vec[2]
    return int(x * 10 + 960), int(z * -10 + 720)

#----- model output parsing -----#
def parse_categorical_crossentropy(name, outs, out_shape=None):
    raw = outs[name]
    if out_shape is not None:
        raw = raw.reshape((raw.shape[0],) + out_shape)
    outs[name] = softmax(raw, axis=-1)

def parse_binary_crossentropy(name, outs):
    raw = outs[name]
    outs[name] = sigmoid(raw)

def parse_mdn(name, outs, in_N=0, out_N=1, out_shape=None):
    raw = outs[name]
    raw = raw.reshape((raw.shape[0], max(in_N, 1), -1))

    pred_mu = raw[:,:,:(raw.shape[2] - out_N)//2]
    n_values = (raw.shape[2] - out_N)//2
    pred_mu = raw[:,:,:n_values]
    pred_std = np.exp(raw[:,:,n_values: 2*n_values])

    if in_N > 1:
        weights = np.zeros((raw.shape[0], in_N, out_N), dtype=raw.dtype)
        for i in range(out_N):
            weights[:,:,i - out_N] = softmax(raw[:,:,i - out_N], axis=-1)

        if out_N == 1:
            for fidx in range(weights.shape[0]):
                idxs = np.argsort(weights[fidx][:,0])[::-1]
                weights[fidx] = weights[fidx][idxs]
                pred_mu[fidx] = pred_mu[fidx][idxs]
                pred_std[fidx] = pred_std[fidx][idxs]
        full_shape = tuple([raw.shape[0], in_N] + list(out_shape))
        outs[name + '_weights'] = weights
        outs[name + '_hypotheses'] = pred_mu.reshape(full_shape)
        outs[name + '_stds_hypotheses'] = pred_std.reshape(full_shape)

        pred_mu_final = np.zeros((raw.shape[0], out_N, n_values), dtype=raw.dtype)
        pred_std_final = np.zeros((raw.shape[0], out_N, n_values), dtype=raw.dtype)
        for fidx in range(weights.shape[0]):
            for hidx in range(out_N):
                idxs = np.argsort(weights[fidx,:,hidx])[::-1]
                pred_mu_final[fidx, hidx] = pred_mu[fidx, idxs[0]]
                pred_std_final[fidx, hidx] = pred_std[fidx, idxs[0]]
    else:
        pred_mu_final = pred_mu
        pred_std_final = pred_std

    if out_N > 1:
        final_shape = tuple([raw.shape[0], out_N] + list(out_shape))
    else:
        final_shape = tuple([raw.shape[0],] + list(out_shape))
    outs[name] = pred_mu_final.reshape(final_shape)
    outs[name + '_stds'] = pred_std_final.reshape(final_shape)

def slice_outputs(model_outputs):
    return {k: model_outputs[np.newaxis, v] for k, v in OUTPUT_SLICES.items()}

def parse_outputs(outs):
    parse_mdn('plan',                              outs, in_N=PLAN_MHP_N, out_N=PLAN_MHP_SELECTION, out_shape=(IDX_N, PLAN_WIDTH))
    parse_mdn('lane_lines',                        outs, in_N=0,          out_N=0,                  out_shape=(NUM_LANE_LINES, IDX_N, LANE_LINES_WIDTH))
    parse_mdn('road_edges',                        outs, in_N=0,          out_N=0,                  out_shape=(NUM_ROAD_EDGES, IDX_N, LANE_LINES_WIDTH))
    parse_mdn('pose',                              outs, in_N=0,          out_N=0,                  out_shape=(POSE_WIDTH,))
    parse_mdn('road_transform',                    outs, in_N=0,          out_N=0,                  out_shape=(POSE_WIDTH,))
    parse_mdn('sim_pose',                          outs, in_N=0,          out_N=0,                  out_shape=(POSE_WIDTH,))
    parse_mdn('wide_from_device_euler',            outs, in_N=0,          out_N=0,                  out_shape=(WIDE_FROM_DEVICE_WIDTH,))
    parse_mdn('lead',                              outs, in_N=LEAD_MHP_N, out_N=LEAD_MHP_SELECTION, out_shape=(LEAD_TRAJ_LEN, LEAD_WIDTH))
    parse_mdn('lat_planner_solution',              outs, in_N=0,          out_N=0,                  out_shape=(IDX_N, LAT_PLANNER_SOLUTION_WIDTH))
    parse_binary_crossentropy('lead_prob',         outs)
    parse_binary_crossentropy('lane_lines_prob',   outs)
    parse_binary_crossentropy('meta',              outs)
    parse_categorical_crossentropy('desire_state', outs,                                            out_shape=(DESIRE_PRED_WIDTH,))
    parse_categorical_crossentropy('desire_pred',  outs,                                            out_shape=(DESIRE_PRED_LEN, DESIRE_PRED_WIDTH))
    return outs

def parse_output_more(output):
    return {
        'plan': [
            {
                'position': plan_element[0:3],
                'velocity': plan_element[3:6],
                'acceleration': plan_element[6:9],
                'rotation': plan_element[9:12],
                'rotation_rate': plan_element[12:15],
            }
            for plan_element in output['plan'][0]
        ],
        'lane_lines': output['lane_lines'][0],
    }

#----- high-level -----#
def preprocess(im, fov):
    preprocess.input_imgs[:, :6] = preprocess.input_imgs[:, 6:]
    preprocess.big_input_imgs[:, :6] = preprocess.big_input_imgs[:, 6:]
    preprocess.input_imgs[:, 6:] = transform(center_crop(im, 30 / fov))
    preprocess.big_input_imgs[:, 6:] = transform(center_crop(im, 60 / fov))
    return preprocess.input_imgs, preprocess.big_input_imgs
preprocess.input_imgs = np.zeros((1, 12, 128, 256), dtype=np.float16)
preprocess.big_input_imgs = np.zeros((1, 12, 128, 256), dtype=np.float16)

def predict(input_imgs, big_input_imgs):
    start = time.time()
    output = sess.run(
        None,
        {
            'input_imgs': input_imgs,
            'big_input_imgs': big_input_imgs,
            'desire': np.zeros((1, HISTORY_BUFFER_LEN + 1, DESIRE_LEN), dtype=np.float16),  # no desire
            'traffic_convention': np.array([[0, 1]], dtype=np.float16),  # driver is on right from inward-facing dashcam's perspective
            'lat_planner_state': predict.lat_planner_state,
            'nav_features': np.zeros((1, NAV_FEATURE_LEN), dtype=np.float16),  # experimental, not using
            'nav_instructions': np.zeros((1, NAV_INSTRUCTION_LEN), dtype=np.float16),  # experimental, not using
            'features_buffer': predict.features_buffer,
        },
    )
    duration = time.time() - start
    output = parse_outputs(slice_outputs(output[0].flatten()))
    predict.features_buffer[:-FEATURE_LEN] = predict.features_buffer[FEATURE_LEN:]
    predict.features_buffer[-FEATURE_LEN:] = output['hidden_state'][0, :]
    predict.lat_planner_state[0, 2] = interp(DT_MDL, T_IDXS, output['lat_planner_solution'][0, :, 2])
    predict.lat_planner_state[0, 3] = interp(DT_MDL, T_IDXS, output['lat_planner_solution'][0, :, 3])
    return output, duration
predict.lat_planner_state = np.zeros((1, LAT_PLANNER_STATE_LEN), dtype=np.float16)
predict.features_buffer = np.zeros((1, HISTORY_BUFFER_LEN, FEATURE_LEN), dtype=np.float16)

def postprocess_im(output, im):
    output, duration = output
    output = parse_output_more(output)
    im = cv2.copyMakeBorder(im, 480, 0, 0, 640, cv2.BORDER_CONSTANT)
    # plan
    thickness = 2
    for i, (a, b) in enumerate(zip(output['plan'], output['plan'][1:])):
        color = (255 - i * 6, 255 - i * 6, 255 - i * 6)
        cv2.line(im, to_top_view(a['position'])  , to_top_view(b['position'])  , color, thickness)
        cv2.line(im, to_right_view(a['position']), to_right_view(b['position']), color, thickness)
    # lane lines
    thickness = 2
    color = (0, 255, 255)
    for lane_line in output['lane_lines']:
        for a, b in zip(lane_line, lane_line[1:]):
            cv2.line(im, to_top_view(a), to_top_view(b), color, thickness)
    return im

#===== main =====#
if __name__ == '__main__':
    args = parser.parse_args()
    cap = cv2.VideoCapture(args.video_path)
    while True:
        ret, im = cap.read()
        if not ret:
            break
        output = predict(*preprocess(im, args.fov))
        im = postprocess_im(output, im)
        cv2.imshow('supercombo', im)
        c = cv2.waitKey()
        if c == 27:
            break
