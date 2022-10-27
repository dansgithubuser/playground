#!/usr/bin/env python3

import os
import subprocess

def invoke(invocation):
    subprocess.run(invocation, shell=True, check=True)

if not os.path.exists('rtsp-simple-server'):
    invoke('curl -o tmp.tar.gz --location https://github.com/aler9/rtsp-simple-server/releases/download/v0.20.1/rtsp-simple-server_v0.20.1_linux_amd64.tar.gz')
    invoke('tar -xf tmp.tar.gz')

invoke('./rtsp-simple-server')
