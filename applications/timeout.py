#!/usr/bin/python

#run a command with a timeout

#say git is hanging on you
#rename this to git and put it before git on your path,
#and edit the command in this script to the original git binary
#now you have a git that times out

import timestamp
import os, subprocess, sys, time

t=time.time()
p=subprocess.Popen(['/usr/bin/git']+sys.argv[1:])
def unique_open(pid):
	for i in range(1000):
		p='{}-{}'.format(os.path.join(os.path.expanduser('~'), 'timeout', str(pid)), i)
		if not os.path.exists(p): break
		i+=1
	return open(p, 'a')
file=unique_open(p.pid)
file.write(timestamp.timestamp()+' '+' '.join(sys.argv)+'\n')
d=0.001
while time.time()<t+300:
	if p.poll()!=None:
		file.write('returncode {}\n'.format(p.returncode))
		file.close()
		import sys
		sys.exit(p.returncode)
	time.sleep(d)
	d=min(d*2, 60)
with open(os.path.join(os.path.expanduser('~'), 'timeout.txt'), 'a') as file:
	file.write(timestamp.timestamp()+'\n')
	file.write('command has timed out\n')
	file.write(' '.join(sys.argv)+'\n')
	file.write('pid: {}\n'.format(p.pid))
p.kill()
sys.stderr.write('timeout\n')
file.close()
sys.exit(1)
