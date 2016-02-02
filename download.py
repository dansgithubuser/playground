import argparse
parser=argparse.ArgumentParser(description='python script to download from links on a webpage')
parser.add_argument('url', help='webpage url')
parser.add_argument('pattern', help='regex to filter which links to download from')
parser.add_argument('path', help='where to download to')
args=parser.parse_args()

import os, re, sys

if sys.version_info[0]==2:
	import urllib2
	request=urllib2.urlopen
else:
	import urllib.request
	request=urllib.request.urlopen

for line in request(args.url):
	match=re.search('<a href="([^"]*)"', line.decode())
	if not match: continue
	file_name=match.group(1)
	if re.search(args.pattern, file_name):
		response=request(args.url+'/'+file_name)
		with open(os.path.join(args.path, file_name), 'wb') as file: file.write(response.read())
