import os

home=os.path.split(os.path.realpath(__file__))[0]

template='''#this file created with the following invocation:
#{invocation}
'scopeName': 'text.{name}'
'name': '{name}'
'patterns': [{patterns}]
'''

template_pattern='''
	{{
		'match': '{regex}'
		'name': '{name}'
	}}
'''

def generate_syntax_package(atom_home):
	import shutil
	dst=os.path.join(atom_home, 'packages', 'highlight-syntax')
	shutil.rmtree(dst)
	shutil.copytree(os.path.join(home, 'highlight-syntax'), dst)

def generate_grammar_package(atom_home, name, patterns):
	path=os.path.join(atom_home, 'packages', name, 'grammars')
	try: os.makedirs(path)
	except: pass
	import sys
	with open(os.path.join(path, name+'.cson'), 'w') as file:
		file.write(template.format(
			invocation=str(sys.argv),
			name=name,
			patterns=''.join([template_pattern.format(regex=regex, name=name) for name, regex in patterns]),
		))

if __name__=='__main__':
	import argparse
	parser=argparse.ArgumentParser(description='create a custom syntax highlighting package')
	parser.add_argument('atom_home', help='path to atom folder -- something like ~/.atom -- contains packages folder')
	parser.add_argument('name', help='name of syntax')
	parser.add_argument('-k', default='', help='keyword regex')
	parser.add_argument('-i', default='', help='italic regex')
	parser.add_argument('-b', default='', help='bold regex')
	args=parser.parse_args()

	if os.path.exists(os.path.join(args.atom_home, 'packages', 'highlight-syntax')):
		print('found highlight-syntax package, it better be mine!')
	else:
		print('no highlight-syntax package, creating -- switch your syntax to take full advantage of your custom grammar')
		generate_syntax_package(args.atom_home)

	generate_grammar_package(args.atom_home, args.name, [
		('keyword.'      +args.name, args.k),
		('markup.italic.'+args.name, args.i),
		('markup.bold.'  +args.name, args.b),
	])
