#!/usr/bin/env python3

import argparse
import socket
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--consumer-hostname', default='localhost')
parser.add_argument('--producer-hostname', default='localhost')
args = parser.parse_args()

def run_on_host(cmd, hostname):
    if hostname != 'localhost':
        cmd = ['ssh', '-X', hostname, cmd]
    else:
        cmd = cmd.split()
    return subprocess.Popen(cmd)

if args.consumer_hostname == 'localhost':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 8888))
    consumer_ip = s.getsockname()[0]
else:
    consumer_ip = args.consumer_hostname

consumer = run_on_host(
    f'ffplay -hide_banner -loglevel warning -rtsp_flags listen rtsp://0.0.0.0:8888/live.sdp?tcp',
    args.consumer_hostname,
)
producer = run_on_host(
    f'ffmpeg -hide_banner -loglevel warning -i /dev/video0 -f rtsp -rtsp_transport tcp rtsp://{consumer_ip}:8888/live.sdp?tcp',
    args.producer_hostname,
)

try:
    while True:
        time.sleep(1)
except:
    pass
consumer.kill()
producer.kill()
