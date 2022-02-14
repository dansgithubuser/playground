import argparse
import glob
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('cmd_fmt')
parser.add_argument('glob')
args = parser.parse_args()

def read(file_path):
    with open(file_path, 'rb') as f: return f.read()

def write(file_path, content):
    with open(file_path, 'wb') as f: f.write(content)

for file_path in glob.glob(args.glob):
    cmd = args.cmd_fmt.format(file_path)
    curr = subprocess.run(cmd, shell=True, capture_output=True).stdout
    state_file_path = file_path.replace('/', '__')
    if os.path.exists(state_file_path):
        prev = read(state_file_path)
        if curr != prev:
            msg = [
                '=====',
                'Change detected!',
                'cmd:', cmd,
                'prev:', prev,
                'curr:', curr,
            ]
            print('\n'.join(msg))
    write(state_file_path, curr)
