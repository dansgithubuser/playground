import argparse

main_parser=argparse.ArgumentParser(description='check if a change is whitespace-only')
main_parser.add_argument('--invariants', default='[](){};', help='characters that mean the same with or without neighboring whitespace')
subparsers=main_parser.add_subparsers()
parser=subparsers.add_parser('files')
parser.add_argument('old')
parser.add_argument('new')
parser=subparsers.add_parser('git')
parser.add_argument('commit')
parser.add_argument('file')
args=main_parser.parse_args()

if hasattr(args, 'old'):
	with open(args.old) as file: old=file.read()
	with open(args.new) as file: new=file.read()
elif hasattr(args, 'commit'):
	import subprocess
	old=subprocess.check_output('git show {}~1:{}'.format(args.commit, args.file), shell=True).decode('utf-8')
	new=subprocess.check_output('git show {}~0:{}'.format(args.commit, args.file), shell=True).decode('utf-8')
else:
	parser.print_help()
	import sys
	sys.exit(0)

def reduce(text):
	result=[]
	x=None
	line=0
	for i in text:
		if i=='\n':
			x='\n'
			line+=1
		elif i in ' \t\r':
			if x!='\n': x=' '
		elif i in args.invariants:
			if x=='\n':
				result.append(('\n', line))
			else:
				result.append((' ', line))
			result.append((i, line))
			x=' '
		else:
			if x:
				result.append((x, line))
				x=None
			result.append((i, line))
	return result

old_reduced=reduce(old)
new_reduced=reduce(new)
old_lines=old.split('\n')
new_lines=new.split('\n')

def same(a, b):
	if a!=b:
		if not(a in ' \n' and b in ' \n'):
			return False
	return True

def similar(a, b):
	i=0
	variant=False
	while i<len(a) and i<len(b):
		if not same(a[i][0], b[i][0]):
			return False
		if a[i][0] not in args.invariants+' \n': variant=True
		if a[i][0]=='\n' and variant: break
		i+=1
	return True

old_i=0
new_i=0
while old_i<len(old_reduced) and new_i<len(new_reduced):
	if not same(old_reduced[old_i][0], new_reduced[new_i][0]):
		print('difference on line {} (old), {} (new):'.format(old_reduced[old_i][1]+1, new_reduced[new_i][1]+1))
		print('	old: {}'.format(old_lines[old_reduced[old_i][1]]))
		print('	new: {}'.format(new_lines[new_reduced[new_i][1]]))
		done=False
		for d in range(len(old_reduced)+len(new_reduced)):
			for old_j in range(old_i, len(old_reduced)):
				new_j=new_i+d-old_j
				if new_j>=len(new_reduced): continue
				if new_j<new_i: break
				if old_reduced[old_j][0]!='\n': continue
				if new_reduced[new_j][0]!='\n': continue
				if similar(old_reduced[old_j:], new_reduced[new_j:]):
					old_i=old_j
					new_i=new_j
					print('resynched on line {} (old), {} (new)'.format(old_reduced[old_i][1]+1, new_reduced[new_i][1]+1))
					done=True
					break
			if done: break
	else:
		old_i+=1
		new_i+=1
if old_i!=len(old_reduced): print('old is longer than new')
if new_i!=len(new_reduced): print('new is longer than old')
