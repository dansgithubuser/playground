template='''#this file created with the following invocation:
#{invocation}
'scopeName': 'text.{name}'
'name': '{name}'
'patterns': [
	{{
		'match': '{keyword_regex}'
		'name': 'keyword.{name}'
	}}
	{{
		'match': '{italic_regex}'
		'name': 'markup.italic.{name}'
	}}
	{{
		'match': '{bold_regex}'
		'name': 'markup.bold.{name}'
	}}
]
'''

import argparse
parser=argparse.ArgumentParser(description='create a custom syntax highlighting package')
parser.add_argument('atom_home', help='path to atom folder -- something like ~/.atom -- contains packages folder')
parser.add_argument('name', help='name of syntax')
parser.add_argument('-k', default='', help='keyword regex')
parser.add_argument('-i', default='', help='italic regex')
parser.add_argument('-b', default='', help='bold regex')
args=parser.parse_args()

import os
os.chdir(os.path.join(args.atom_home, 'packages'))
path=os.path.join(args.name, 'grammars')
try: os.makedirs(path)
except: pass
os.chdir(path)

import sys
with open(args.name+'.cson', 'w') as file:
	file.write(template.format(
		invocation=str(sys.argv),
		name=args.name,
		keyword_regex=args.k,
		italic_regex=args.i,
		bold_regex=args.b
	))
