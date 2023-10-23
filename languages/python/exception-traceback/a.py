import b

import traceback

e = b.hello()
if e:
    traceback.print_exception(e)
    print('\n'.join(traceback.format_exception(e)))
