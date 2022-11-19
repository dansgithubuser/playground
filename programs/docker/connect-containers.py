import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('network_name')
parser.add_argument('container_name', nargs='*')
args = parser.parse_args()

def invoke(cmd, **kwargs):
    print(cmd)
    return subprocess.run(cmd.split(), **kwargs)

if invoke(f'docker network inspect {args.network_name}').returncode:
    invoke(f'docker network create --driver bridge {args.network_name}', check=True)

for container_name in args.container_name:
    invoke(f'docker network connect {args.network_name} {container_name}', check=True)
