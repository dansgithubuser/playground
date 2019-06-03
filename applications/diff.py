def cantor(sum):
	for i in range(sum):
		for j in range(i+1):
			yield (j, i-j)

def print_section(name, ords):
	print('='*10+name+'='*10)
	print(''.join([chr(i) for i in ords]))

def join(separator, lists):
	result=[]
	for i, list in enumerate(lists):
		result+=list
		if i<len(lists)-1: result+=separator
	return result

def ordify(x):
	if type(x)==str: return ord(x)
	return x

class Char:
	def __init__(self, ord):
		self.ord=ord
		self.ignored=False

	def __eq__(self, other): return self.ord==other.ord

	def __str__(self): return chr(self.ord)

	def __repr__(self): return 'c'+str(self.ord)

class File:
	def __init__(self, ords, ignore_whitespace):
		for i in ords: assert type(i)==int
		self.chars=[Char(i) for i in ords]
		self.ignore_whitespace=ignore_whitespace
		if self.ignore_whitespace:
			for i in range(len(self.chars)):
				if self.chars[i].ord in [ord(i) for i in ' \t\n\r']:
					self.chars[i].ignored=True
		self.unignored=[i for i, char in enumerate(self.chars) if not char.ignored]

	def __getitem__(self, i):
		if isinstance(i, slice):
			start, stop, step=i.indices(len(self.unignored))
			assert step==1
			x=self.unignored[stop] if stop<len(self.unignored) else -1
			chars=self.chars[self.unignored[start]:x]
			return File([j.ord for j in chars], self.ignore_whitespace)
		return self.chars[self.unignored[i]]

	def __len__(self):
		return len(self.unignored)

	def __eq__(self, other):
		return [self.chars[i] for i in self.unignored]==[other.chars[i] for i in other.unignored]

	def __str__(self): return 'File '+''.join([str(i) for i in self.chars])

	def __repr__(self): return 'File '+repr([i.ord for i in self.chars])

	def ords(self): return [i.ord for i in self.chars]

	def ords_unignored(self): return [self.chars[i].ord for i in self.unignored]

	def ords_from_unignored(self, start, end):
		x=self.unignored[end] if end<len(self.unignored) else -1
		return [i.ord for i in self.chars[self.unignored[start]:x]]

	def get_lines(self):
		lines=[]
		ords=[]
		for i in self.chars:
			if i.ord==ord('\n'):
				lines.append(File(ords, self.ignore_whitespace))
				ords=[]
			else: ords.append(i.ord)
		lines.append(File(ords, self.ignore_whitespace))
		return lines

def file_from_file(path, ignore_whitespace):
	with open(path, 'rb') as file: return File([ordify(i) for i in file.read()], ignore_whitespace)

class Differ:
	def __init__(self, file_a, file_b, ignore_whitespace):
		self.a=file_from_file(file_a, ignore_whitespace)
		self.b=file_from_file(file_b, ignore_whitespace)

	def go(self, print_equal):
		reconcile=Differ.reconcile
		self.i_a=0
		self.i_b=0
		start_of_equality=0
		while self.i_a<len(self.a) and self.i_b<len(self.b):
			if self.a[self.i_a]==self.b[self.i_b]:
				self.i_a+=1
				self.i_b+=1
			else:
				if print_equal:
					print_section('equal', self.a.ords_from_unignored(start_of_equality, self.i_a))
				start_of_equality=None
				if not reconcile(self): break
				start_of_equality=self.i_a
		if print_equal and start_of_equality!=None and start_of_equality!=self.i_a:
			print_section('equal', self.a.ords_from_unignored(start_of_equality, self.i_a))
		if self.i_a<len(self.a): print_section('remaining a', self.a[self.i_a:].ords())
		if self.i_b<len(self.b): print_section('remaining b', self.b[self.i_b:].ords())
		print_section('', [])

	def reconcile(self):
		lines_a=self.a[self.i_a:].get_lines()
		lines_b=self.b[self.i_b:].get_lines()
		for l_a, l_b in cantor(len(lines_a)+len(lines_b)):
			if l_a>=len(lines_a): continue
			if l_b>=len(lines_b): continue
			if len(lines_a[l_a]) and len(lines_b[l_b]) and lines_a[l_a]==lines_b[l_b]: break
		else: return False
		d_a=lines_a[:l_a]
		d_b=lines_b[:l_b]
		print_section('diff a', join([ord('\n')], [i.ords() for i in d_a]))
		print_section('diff b', join([ord('\n')], [i.ords() for i in d_b]))
		self.i_a+=sum([len(i.ords_unignored()) for i in d_a])
		self.i_b+=sum([len(i.ords_unignored()) for i in d_b])
		return True

if __name__=='__main__':
	import argparse
	parser=argparse.ArgumentParser(description='collection of diff methods')
	parser.add_argument('file_a')
	parser.add_argument('file_b')
	parser.add_argument('--ignore-whitespace', action='store_true')
	parser.add_argument('--print-equal', action='store_true')
	args=parser.parse_args()
	Differ(args.file_a, args.file_b, args.ignore_whitespace).go(args.print_equal)
