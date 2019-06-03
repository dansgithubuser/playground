def major_section(name): print('\n'+'='*20+' {} '.format(name)+'='*20)
def minor_section(): print('-'*20)

class Decorator(object):
	def __init__(self, function):
		print('Decorator.__init__ entered, function is {}'.format(function.__name__))
		self.function=function
		print('Decorator.__init__ returning')

	def __call__(self, *args, **kwargs):
		print('Decorator.__call__ entered, args are {}'.format((args, kwargs)))
		result=self.function(*args, **kwargs)
		print('Decorator.__call__ returning')
		return result

class Descriptor(Decorator):
	def __get__(self, object, type):
		print('Descriptor.__get__ entered, object is {}, type is {}'.format(object, type.__name__))
		got_function=self.function.__get__(object, type)
		print('got_function is {}'.format(got_function))
		result=self.__class__(got_function)#create a new instance of myself with bound method
		print('Descriptor.__get__ returning')
		return result

class Property(Decorator):
	def __get__(self, object, type):
		print('Property.__get__ entered, object is {}, type is {}'.format(object, type.__name__))
		got_function=self.function.__get__(object, type)
		print('got_function is {}'.format(got_function))
		result=got_function()
		print('Property.__get__ returning')
		return result

#========================================#
major_section('function decorator')

@Descriptor
def function(x):
	print('function entered, x is {}'.format(x))
	print('function returning')

minor_section()

try: function(1)
except Exception as e: print(e)

#========================================#
major_section('method decorator')

class Class(object):
	@Decorator
	def function(self, x):
		print('Class.function entered, x is {}'.format(x))
		print('Class.function returning')

minor_section()

c=Class()
try: c.function(2)
except Exception as e: print(e)

#========================================#
major_section('method descriptor')

class Class(object):
	@Descriptor
	def function(self, x):
		print('Class.function entered, x is {}'.format(x))
		print('Class.function returning')

minor_section()

c=Class()
try: c.function(3)
except Exception as e: print(e)

#========================================#
major_section('property')

class Class(object):
	@Property
	def function(self): return 4

minor_section()

c=Class()
try: print(c.function)
except Exception as e: print(e)
