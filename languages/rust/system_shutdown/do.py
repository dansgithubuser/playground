import subprocess

subprocess.run(['docker', 'build', '-t', 'rust-system-shutdown', '.'])
subprocess.run(['docker', 'run', '-it', 'rust-system-shutdown', '/bin/bash'])
