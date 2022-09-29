import subprocess
import time

p = subprocess.Popen(
    ['python3', '-u', 'timer2.py'],
    stdout=subprocess.PIPE,
)

while p.poll() == None:
    out = bytearray(1)
    p.stdout.readinto(out)
    print(out)

print('---------')

for i in range(10):
    time.sleep(0.1)
    p.stdout.readinto(out)
    print(out)
