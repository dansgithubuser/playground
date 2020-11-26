import atexit
import subprocess
import time

p = subprocess.Popen(
    ['python', '-u', 'timer.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

def clean_up():
    p.kill()
    p.communicate()
    print(p.returncode)
atexit.register(clean_up)

while True:
    out = bytearray(1)
    p.stdout.readinto(out)
    print(out)
    if out == b'\x00': break
