#!/usr/bin/env python

class Fibonacci:
	def __init__(self, initial, generator):
		self.initial=initial
		self.generator=generator

	def show(self):
		state=self.initial
		for i in range(20):
			old_state=state
			state=state[1:]+[self.generator(*state)]
			print('{} {}'.format(old_state, 1.0*state[-1]/old_state[-1]))

Fibonacci([1, 1], lambda x, y: x+y).show()
Fibonacci([1, 1, 1], lambda x, y, z: x+y+z).show()
