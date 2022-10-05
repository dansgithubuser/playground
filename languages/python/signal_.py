import datetime
import pdb
import signal
import sys
import time

def handle(sig, frame):
    print('handling', sig, frame)
    if sig == signal.SIGINT:
        sys.exit()
    elif sig == signal.SIGQUIT:
        pdb.set_trace()

for sig in signal.valid_signals():
    print(sig)
    try:
        signal.signal(sig, handle)
    except Exception as e:
        print(e)

done = False
while not done:
    time.sleep(1)
    print(datetime.datetime.now())
