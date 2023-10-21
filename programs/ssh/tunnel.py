#!/usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--local-port', default=8000)
parser.add_argument('--jump-server-port', default=22)
parser.add_argument('--remote-port', default=22)
parser.add_argument('remote_hostname')
parser.add_argument('jump_server_user_at_hostname')
args = parser.parse_args()

invocation = f'ssh -N -L {args.local_port}:{args.remote_hostname}:{args.remote_port} -p {args.jump_server_port} {args.jump_server_user_at_hostname}'
print(invocation)
subprocess.run(invocation.split(), check=True)
