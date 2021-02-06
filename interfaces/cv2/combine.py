import argparse
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--frame-rate', '--fr', type=int, default=30)
parser.add_argument('--output', '-o', default='combined.mp4')
parser.add_argument('--frames', '-f', type=int)
args = parser.parse_args()

file_names = sorted([i for i in os.listdir('.') if i.endswith('.png')])
if args.frames: file_names = file_names[:args.frames]
for i, file_name in enumerate(file_names):
    shutil.copyfile(file_name, f'frame-{i:06}.png')

subprocess.run([
    'ffmpeg',
    '-i', 'frame-%06d.png',
    '-framerate', str(args.frame_rate),
    args.output,
])
