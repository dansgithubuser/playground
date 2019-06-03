import argparse
parser=argparse.ArgumentParser(description='do a bunch of commands concurrently across specified directories')
parser.add_argument('glob', help='glob to determine which directories within current directory to operate on')
parser.add_argument('command', help='what command to invoke in specified directories')
args=parser.parse_args()

import os, subprocess
if args.glob=='.':
	while True:
		print(os.getcwd())
		try: subprocess.call(args.command, shell=True)
		except: pass
else:
	print('press enter to quit')
	import glob
	processes=[]
	for i in glob.glob(args.glob):
		start=os.getcwd()
		os.chdir(i)
		processes.append(subprocess.Popen(
			['python', os.path.realpath(__file__), '.', args.command]
		))
		os.chdir(start)

try: input=raw_input
except: pass

input()
for i in processes: i.kill()
