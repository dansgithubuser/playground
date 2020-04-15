import os
import subprocess

DIR = os.path.dirname(os.path.realpath(__file__))

os.chdir(os.path.join(DIR, 'rs-server'))
server = subprocess.Popen(['cargo', 'run'])

os.chdir(os.path.join(DIR, 'rs-client'))
subprocess.run(['cargo', 'run'])

server.kill()
