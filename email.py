import collections, glob, pprint

try: input=raw_input()
except: pass

import argparse
parser=argparse.ArgumentParser(
	description='process a series of emails exported as plain text by ImportExportTools addon for Thunderbird'
)
parser.add_argument('glob', nargs='+', help='glob of email files')
parser.add_argument('--start', help='regex of start of interesting section')
parser.add_argument('--end', help='regex of end of interesting section')
parser.add_argument('--split', help='what to split lines with', default=' ')
parser.add_argument('--output', default='out.txt')
parser.add_argument('--keygen', action='store_true', help='prompt when unkeyed item is encountered')
parser.add_argument('--key', default='key.txt', help='file associated with keygen')
args=parser.parse_args()

print('globs: '+str(args.glob))
if args.start: print('start: ('+args.start+')')
if args.end: print('end: ('+args.end+')')
print('split: ('+args.split+')')

key=collections.defaultdict(list)
if args.key:
	try:
		with open(args.key) as file: key.update(eval(file.read()))
	except FileNotFoundError: pass

total=0
for g in args.glob: total+=len(glob.glob(g))

def write_key():
	with open(args.key, 'w') as file: file.write(pprint.pformat(dict(key)))

history=collections.defaultdict(dict)
i=0
for g in args.glob:
	for filename in glob.glob(g):
		i+=1
		print('{}/{} {}'.format(i, total, filename))
		with open(filename, encoding='utf-8') as file: lines=file.readlines()
		date=None
		interested=False
		items=collections.defaultdict(lambda: collections.defaultdict(list))
		if not args.start: interested=True
		import re
		for line in lines:
			if not date:
				if line.startswith('Date: '):
					match=re.match('Date: ([0-9]+)/([0-9]+)/([0-9:]+)', line)
					date='{}-{:0>2}-{:0>2}'.format(match.group(3), match.group(1), match.group(2))
			elif not interested:
				if re.search(args.start, line):
					interested=True
			else:
				if args.end and re.search(args.end, line): break
				for item in line.split(args.split):
					item=item.lower().strip()
					if not item: continue
					keywords=[]
					#key
					for keyword, regexes in key.items():
						for regex in regexes:
							if re.search(regex, item):
								keywords.append(keyword)
								break
					#keygen
					if not keywords and args.keygen:
						print('unkeyed item encountered: {}'.format(item.encode()))
						#regex
						while True:
							print('regex? ')
							regex=input()
							if not regex: regex=re.sub(r'(\?|\.|\+|\(|\))', r'\\\1', item)
							if re.search(regex, item): break
							else: print('regex does not match')
						#new key
						while True:
							print('keyword? ')
							keyword=input()
							if keyword: break
							else: import pdb; pdb.set_trace()
						key[keyword].append(regex)
						write_key()
						keywords.append(keyword)
					#update items
					if not keywords: keywords.append(None)
					for keyword in keywords: items[keyword][item].append(line.strip())
		history[date].update(items)
write_key()
with open(args.output, 'w', encoding='utf-8') as file: file.write(pprint.pformat(history))
heatFilename='heat.'+args.output
with open(heatFilename, 'w', encoding='utf-8') as file:
	file.write('begin\n')
	index=[]
	for date, items in sorted(history.items(), key=lambda x: x[0]):
		for item, lines in sorted(items.items(), key=lambda x: x[0] if x[0] else ''):
			if item not in index: index.append(item)
	index=dict([(index[i], i) for i in range(len(index))])
	for item, i in index.items():
		import synesthesia
		r, g, b, a=synesthesia.color(str(item))
		file.write('ycolor {} {} {} {} 255\n'.format(i, r, g, b))
	def to_days(date):
		from datetime import datetime
		return (datetime.strptime(date, '%Y-%m-%d')-datetime.utcfromtimestamp(0)).days
	for date, items in history.items():
		for item, lines in items.items():
			file.write('hover {} {} {}\n'.format(to_days(date), index[item], '{}\n{}\n'.format(item, '\n'.join(lines))))
	file.write('end\n')
	for date, items in history.items():
		for item, lines in items.items():
			file.write('{} {}\n'.format(to_days(date), index[item]))
import subprocess
subprocess.call('python ../plotstuff/go.py --type heat '+heatFilename, shell=True)
