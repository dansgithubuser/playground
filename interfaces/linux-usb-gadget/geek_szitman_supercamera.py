#!/usr/bin/env python3

#===== imports =====#
import os
from pathlib import Path
import subprocess

#===== helpers =====#
def invoke(*args, **kwargs):
    if len(args) == 1:
        args = args[0].split()
    kwargs.setdefault('check', True)
    return subprocess.run(args, **kwargs)

def symlink(wd, p1, p2=''):
    cwd = os.getcwd()
    os.chdir(wd)
    invoke(f'ln -s {str(p1)} {str(p2)}')
    os.chdir(cwd)

#===== g_webcam =====#
def check_g_webcam():
    return 'g_webcam' in invoke('lsmod', capture_output=True).stdout.decode()
if not check_g_webcam():
    invoke('modprobe g_webcam')
    assert check_g_webcam()

#===== config =====#
config_path = Path('/sys/kernel/config/usb_gadget/geek_szitman_supercamera')
config_path.mkdir(exist_ok=True)

with (config_path / 'idVendor').open('w') as f:
    f.write('0x2ce3')
with (config_path / 'idProduct').open('w') as f:
    f.write('0x3828')

config1_rel_path = Path('configs') / 'c.1'
config1_path = config_path / config1_rel_path
config1_path.mkdir(parents=True, exist_ok=True)

function_rel_path = Path('functions') / 'uvc.geek_szitman_supercamera'
function_path = config_path / function_rel_path
function_path.mkdir(parents=True, exist_ok=True)

resolution_path = function_path / 'streaming' / 'uncompressed' / 'u' / '1080p'
resolution_path.mkdir(parents=True, exist_ok=True)
frame_intervals = [666666, 1000000, 5000000]
with (resolution_path / 'dwFrameInterval').open('w') as f:
    for frame_interval in frame_intervals:
        f.write(f'{frame_interval}\n')

h_path = function_path / 'streaming' / 'header' / 'h'
h_path.mkdir(exist_ok=True)
symlink(h_path, '../../uncompressed/u')
symlink(function_path / 'streaming' / 'class' / 'fs', '../../header/h')
symlink(function_path / 'streaming' / 'class' / 'hs', '../../header/h')
symlink(function_path / 'streaming' / 'class' / 'ss', '../../header/h')
(function_path / 'control' / 'header' / 'h').mkdir(exist_ok=True)
symlink(function_path / 'control', 'header/h', 'class/fs')
symlink(function_path / 'control', 'header/h', 'class/ss')

symlink(config_path, function_rel_path, config1_rel_path)
