#! /usr/bin/env python3

from print_styled import print_styled

import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--build', '-b', action='store_true')
parser.add_argument('--memory', '--mem', '-m', action='store_true')
parser.add_argument('--cpu', '-c', action='store_true')
args = parser.parse_args()

if len(sys.argv) == 1:
    args.build = True
    args.memory = True
    args.cpu = True

def invoke(invocation, check=True):
    invocation = print_styled(invocation)
    subprocess.run(invocation.split(), check=check)

if args.build:
    invoke('docker build -t dans_playground_use_memory -f mem.dockerfile .')
    invoke('docker build -t dans_playground_use_cpu -f cpu.dockerfile .')

if args.memory:
    invoke('docker run dans_playground_use_memory')
    invoke('docker run -m <green>20m</green> dans_playground_use_memory .', check=False)
    invoke('docker run -m <green>20m</green> --memory-swap <green> 0m</green> dans_playground_use_memory', check=False)
    invoke('docker run -m <green>20m</green> --memory-swap <green>20m</green> dans_playground_use_memory', check=False)
    invoke('docker run -m <green>20m</green> --memory-swap <green>40m</green> dans_playground_use_memory', check=False)
    invoke('docker run -m <green>20m</green> --memory-swap <green>60m</green> dans_playground_use_memory', check=False)
    invoke('docker run -m <green>40m</green> --memory-swap <green>40m</green> dans_playground_use_memory', check=False)
    invoke('docker run -m <green>60m</green> --memory-swap <green>20m</green> dans_playground_use_memory', check=False)
    invoke('docker run -m <green>60m</green> --memory-swap <green> 0m</green> dans_playground_use_memory', check=False)

if args.cpu:
    invoke('docker run dans_playground_use_cpu')
    invoke('docker run --cpus <green>1</green> dans_playground_use_cpu')
    invoke('docker run --cpus <green>0.5</green> dans_playground_use_cpu')
    invoke('docker run --cpus <green>0.2</green> dans_playground_use_cpu')
    invoke('docker run --cpus <green>0.1</green> dans_playground_use_cpu')
