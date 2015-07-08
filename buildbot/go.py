#!/usr/bin/python

import subprocess, os, argparse

parser=argparse.ArgumentParser()
parser.add_argument('command', help='create, start, restart, or stop')
args=parser.parse_args()

if args.command=='create':
	subprocess.check_call('buildbot create-master -r play-master-basedir', shell=True)
	subprocess.check_call('buildslave create-slave -r play-slave-basedir localhost:9989 play-slave password', shell=True)

if args.command=='start':
	subprocess.check_call('buildbot start play-master-basedir', shell=True)
	subprocess.check_call('buildslave start play-slave-basedir', shell=True)

if args.command=='restart':
	subprocess.check_call('buildbot restart play-master-basedir', shell=True)
	subprocess.check_call('buildslave restart play-slave-basedir', shell=True)

if args.command=='stop':
	print(subprocess.call('buildbot stop play-master-basedir', shell=True))
	print(subprocess.call('buildslave stop play-slave-basedir', shell=True))
