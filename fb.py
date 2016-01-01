import argparse
parser=argparse.ArgumentParser(description='tools for working with downloaded copies of Facebook data')
parser.add_argument('path', help='path to root of facebook data download (unzipped)')
parser.add_argument('--word-frequency', '--wf', action='store_true', help='count word frequency in messages')
parser.add_argument('--word-frequency-user', '--wfu', help='user to get word frequency for, default all users')
args=parser.parse_args()

if args.word_frequency:
	import re
	from html.parser import HTMLParser
	class MessageParser(HTMLParser):
		def __init__(self, desired_user):
			super().__init__()
			self.desired_user=desired_user
			self.stack=[]
			self.user=None
			self.meta=None
			from collections import defaultdict
			self.wordcount=defaultdict(int)

		def handle_starttag(self, tag, attrs):
			self.stack.append((tag, attrs))

		def handle_endtag(self, tag):
			assert tag==self.stack[-1][0]
			self.stack=self.stack[:-1]

		def handle_data(self, data):
			if   self.stack[-1]==('span', [('class', 'user')]):
				self.user=data
			elif self.stack[-1]==('span', [('class', 'meta')]):
				self.meta=data
			elif (self.desired_user and self.user==self.desired_user) or ((not self.desired_user) and self.user):
				for word in data.split():
					self.wordcount[re.sub(r'[^a-z\-\']', '', word.lower())]+=1

	parser=MessageParser(args.word_frequency_user)
	import os
	with open(os.path.join(args.path, 'html', 'messages.htm'), encoding='utf8') as file: parser.feed(file.read())
	wordcount=list(parser.wordcount.items())
	wordcount.sort(key=lambda x: x[1])
	with open('wc.txt', 'w', encoding='utf8') as file:
		for word, count in wordcount: file.write(word+' '+str(count)+'\n')

print('all requests processed; call with -h for help')
