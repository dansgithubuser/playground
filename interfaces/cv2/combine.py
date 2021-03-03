import argparse
import glob
import os
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
parser.add_argument('extension', nargs='?', default='.png')
parser.add_argument('--frame-rate', '--fr', type=int, default=30)
parser.add_argument('--output', '-o', default='combined.mp4')
parser.add_argument('--frames', '-f', type=int)
args = parser.parse_args()

DIR = os.path.dirname(os.path.realpath(__file__))

file_glob = os.path.join(
    os.path.expanduser(args.path),
    f'*{args.extension}',
)
file_paths = sorted(glob.glob(file_glob))
if not file_paths:
    print(f'no files match glob {file_glob}')
if args.frames: file_paths = file_paths[:args.frames]
for i, file_path in enumerate(file_paths):
    shutil.copyfile(file_path, os.path.join(DIR, f'frame-{i:06}{args.extension}'))

subprocess.run([
    'ffmpeg',
    '-i', os.path.join(DIR, f'frame-%06d{args.extension}'),
    '-framerate', str(args.frame_rate),
    args.output,
])
