import subprocess
import time

p = subprocess.Popen(['python3', 'echo.py'], stdin=subprocess.PIPE)
for i in range(4):
    p.stdin.write(f'{i}\n'.encode())
    p.stdin.flush()
    time.sleep(1)
p.kill()
