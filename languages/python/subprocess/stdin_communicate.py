import subprocess

p = subprocess.Popen('cat', stdin=subprocess.PIPE)
p.stdin.write(b'asdf')
p.communicate()
