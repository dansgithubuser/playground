#!/usr/bin/env python

import argparse
parser=argparse.ArgumentParser()
parser.add_argument('legion', help='any other node, or . if this is the first')
parser.add_argument('--test', '-t', action='store_true')
args=parser.parse_args()

import socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip=s.getsockname()[0]
s.close()

if args.legion!='.':
	import os
	os.environ['LEGION']=args.legion

invocation='iex --name legion@{} --cookie legion-cookie-value -S mix'.format(ip)
if args.test: invocation+=' test'
import subprocess
subprocess.check_call(invocation, shell=True)
