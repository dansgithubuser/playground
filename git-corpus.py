import glob, os, pprint, subprocess

commits={}

for folder in glob.glob(os.path.join('.git', 'objects', '*')):
	if os.path.split(folder)[-1] in ['info', 'pack']: continue
	print(folder)
	for file in glob.glob(os.path.join(folder, '*')):
		hash=''.join(file.split(os.path.sep)[-2:])
		if subprocess.check_output('git cat-file -t '+hash, shell=True).decode().strip()=='commit':
			commits[hash]=subprocess.check_output('git log --pretty=%P -n 1 '+hash, shell=True).decode().strip().split()

pprint.pprint(commits)

import graphviz
graph=graphviz.Digraph()
for commit in commits:
	hash=commit[:8]
	subject=subprocess.check_output('git log --pretty=format:%s -n 1 '+commit, shell=True).decode().strip()
	graph.node(commit, hash+'\n'+subject)
for commit, parents in commits.items():
	for parent in parents: graph.edge(commit, parent)
graph.render('git-corpus.gv', view=True)
