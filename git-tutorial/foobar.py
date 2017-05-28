#link to post

try: input=raw_input
except: pass

import subprocess, os

HOME=os.path.split(os.path.realpath(__file__))[0]
GIT_CORPUS=os.path.join(HOME, '..', 'git-corpus.py')

def section(name):
	y=10
	x=len(name)+2*y
	print('+'+'-'*x           +'+')
	print('|'+' '*y+name+' '*y+'|')
	print('+'+'-'*x           +'+')

def pause():
	print(r'\---/press enter to continue')
	input()

def invoke(*args):
	for arg in args:
		f=subprocess.check_call
		if type(arg)==list: arg=arg[0]; f=subprocess.call
		print(r'/---\about to invoke '+arg)
		pause()
		if arg.split()[0]=='cd': os.chdir(arg.split()[1])
		else: f(arg, shell=True)

def write_file(name, contents):
	print(r'/---\about to write to '+name)
	print(contents)
	pause()
	with open(name, 'w') as file:
		file.write(contents)
	print('resulting in git diff')
	print(subprocess.check_output('git diff', shell=True).decode())

section('1st commit')
invoke('mkdir foo', 'cd foo', 'git init')
write_file('math.py', 
'''def launch_the_missiles(x):
	print('{0} times 4 is {1}'.format(x, x*4))

print('running tests')

print('running test 1')

launch_the_missiles(3)
launch_the_missiles(4)

print('done')''')
invoke('git add math.py', 'git commit -m "multiply some numbers by 4"')

section('2nd commit')
write_file('math.py',
'''def launch_the_missiles(x):
	print('{0} times 4 plus 2 is {1}'.format(x, x*4+2))

print('running tests')

print('running test 1')

launch_the_missiles(3)
launch_the_missiles(4)

print('done')''')
invoke('git add math.py', 'git commit -m "add two for good measure"')

section('nomenclature branch')
invoke('git checkout -b nomenclature')
write_file('math.py',
'''def operate_and_print(x):
	print('{0} times 4 plus 2 is {1}'.format(x, x*4+2))

print('running tests')

print('running test 1')

operate_and_print(3)
operate_and_print(4)

print('done')''')
invoke('git add math.py', 'git commit -m "nomenclature -- launching missiles never actually supported"')

section('commit in bar')
invoke(
	'cd ..', 'mkdir bar', 'cd bar', 'git init', 'git config receive.denyCurrentBranch ignore',
	'cd ../foo', 'git remote add origin ../bar',
	'git push -u origin master',
	'cd ../bar',
	'git reset --hard HEAD'
)
write_file('math.py',
'''def launch_the_missiles(x, y=4):
	print('{0} times {1} plus 2 is {2}'.format(x, y, x*y+2))

print('running tests')

print('running test 0')

launch_the_missiles(1, 0)
launch_the_missiles(2, 0)

print('running test 1')

launch_the_missiles(3)
launch_the_missiles(4)

print('done')''')
invoke('git add math.py', 'git commit -m "allow multiplication by numbers other than 4"')

section('merge nomenclature into master')
invoke(
	'cd ../foo', 'git fetch',
	'git checkout master'
)
write_file('math.py',
'''def launch_the_missiles(x):
	print('{0} times 4 plus 2 is {1}'.format(x, x*4+2))

print('running tests')

print('running test 1')

launch_the_missiles(3)
print('done launching 3 missiles')
print('about to launch 4 missiles')
launch_the_missiles(4)

print('done')''')
invoke(
	'git stash', 'git reset --hard origin/master', 'git stash pop',
	'git reset --hard HEAD', ['git merge nomenclature']
)
write_file('math.py',
'''def operate_and_print(x, y=4):
	print('{0} times {1} plus 2 is {2}'.format(x, y, x*y+2))

print('running tests')

print('running test 0')

launch_the_missiles(1, 0)
launch_the_missiles(2, 0)

print('running test 1')

operate_and_print(3)
operate_and_print(4)

print('done')''')
invoke(
	'git add math.py', 'git commit',
	'git reset --hard origin/master',
)

section('foo\'s corpus of commits before rebase')
invoke('python {} git-tutorial-pre-rebase'.format(GIT_CORPUS))

section('rebase')
invoke('git checkout nomenclature', ['git rebase master'])
write_file('math.py',
'''def operate_and_print(x, y=4):
	print('{0} times {1} plus 2 is {2}'.format(x, y, x*y+2))

print('running tests')

print('running test 0')

operate_and_print(1, 0)
operate_and_print(2, 0)

print('running test 1')

operate_and_print(3)
operate_and_print(4)

print('done')''')
invoke('git add math.py', 'git rebase --continue', 'python {} git-tutorial-post-rebase'.format(GIT_CORPUS))
