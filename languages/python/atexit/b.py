import atexit

atexit.register(lambda: print('exit'))

raise Exception('exception')
