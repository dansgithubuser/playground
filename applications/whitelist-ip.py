import sys
import time

HOSTS_ALLOW = '/etc/hosts.allow'
UNIQUIFIER = 'AAoASp4kAyKW1Aw7yWZ5FXMQ36ZcqnIN'

with open(HOSTS_ALLOW, 'a') as f:
    f.write(f'{sys.argv[1]} # temporary line added by {__file__} {UNIQUIFIER}\n')

time.sleep(60)

with open(HOSTS_ALLOW, 'r') as f:
    old = f.read()
new = []
for line in old.splitlines():
    if UNIQUIFIER not in line:
        new.append(line+'\n')
with open(HOSTS_ALLOW, 'w') as f:
    f.write(''.join(new))
