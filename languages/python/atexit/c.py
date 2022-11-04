import atexit
import subprocess

atexit.register(lambda: subprocess.run(['systemctl', 'restart', 'ModemManager.service'], check=True))

raise Exception('exception')
