import os
import subprocess

DIR = os.path.dirname(os.path.realpath(__file__))

os.chdir(os.path.join(DIR, 'rs-server'))
subprocess.run(['cargo', 'build'], check=True)
server = subprocess.Popen(['cargo', 'run'])

try:
    os.chdir(os.path.join(DIR, 'rs-client'))
    subprocess.run(['cargo', 'run'], check=True)
finally:
    server.kill()
