import sys
import traceback

def print_exception(*exc_info):
    print(''.join(traceback.format_exception(*exc_info)))

sys.excepthook = lambda *exc_info: print_exception(*exc_info)

raise Exception('hello')
