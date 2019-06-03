#!/usr/bin/python

import os, re, subprocess, sys

def invoke(invocation):
	subprocess.check_call(invocation, shell=True)

src=next(i for i in os.listdir('.') if re.match(sys.argv[1], i))
invoke('g++ -Wall -Wextra -pedantic -std=c++11 -pthread {} -lbluetooth'.format(src))
invoke('sudo ./a.out')
