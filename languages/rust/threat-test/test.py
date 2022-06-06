import subprocess
import time

p = subprocess.Popen(['cargo', 'run'])
time.sleep(1)
subprocess.run(['ps', 'H', '-o', 'pid tid cmd comm pcpu'])
