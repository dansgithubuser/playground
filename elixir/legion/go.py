#!/usr/bin/env python

import socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip=s.getsockname()[0]
s.close()

invocation='iex --name legion@{} --cookie legion-cookie-value -S mix'.format(ip)
import subprocess
subprocess.check_call(invocation, shell=True)
