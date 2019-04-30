print('__main__.py start')
try:
	from . import common
	print('from . import common succeeded')
except: pass
try:
	import common
	print('import common succeeded')
except: pass
common.run()
print('__main__.py end')
