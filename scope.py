#!/usr/bin/python

x=1

def f(y):
	global x
	if y==3: x=2
	print(x)

f(4)
print('good so far')

def f(y):
	if y==3: x=2
	print(x)

f(4)
