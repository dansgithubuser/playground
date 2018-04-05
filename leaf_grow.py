#!/usr/bin/env python

from __future__ import print_function
import argparse

class Stem:
	def __init__(self, locality):
		self.food=[1]*360
		self.curr_leaf=None
		self.prev_leaf=None
		self.locality=locality

	def grow(self):
		self.prev_leaf=self.curr_leaf
		self.curr_leaf=max(enumerate(self.food), key=lambda x: x[1])[0]
		for i in range(len(self.food)):
			angle=(i-self.curr_leaf+360)%360
			distance=min(angle, 360-angle)
			self.food[i]*=1-2**(-(self.locality*distance/180.0)**2)
			self.food[i]+=1

	def show(self):
		hi=max(self.food)
		lo=min(self.food)
		print(hi)
		for h in range(5):
			for i in range(60):
				def level(l): return l/5.0*(hi-lo)
				c=' '
				if level(5-h)>=self.food[i*6]-lo>=level(4-h): c='x'
				print(c, end='')
			print()
		print(lo)

	def angle(self):
		if self.curr_leaf is None: return None
		if self.prev_leaf is None: return None
		return (self.curr_leaf-self.prev_leaf+360)%360

	def characterize(self):
		for i in range(40): self.grow()
		angle=self.angle()
		for i in range(10):
			self.grow()
			if abs(self.angle()-angle)>5: return None
		return self.angle()

parser=argparse.ArgumentParser()
parser.add_argument('--show', '-s', action='store_true')
parser.add_argument('--characterize', '-c', action='store_true')
args=parser.parse_args()

if args.show:
	stem=Stem(4)
	for i in range(20):
		stem.grow()
		print('grew at {}, angle: {}'.format(stem.curr_leaf, stem.angle()))
		stem.show()

if args.characterize:
	for i in range(1, 100):
		locality=i/10.0
		print(locality, Stem(locality).characterize())
