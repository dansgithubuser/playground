#! /usr/bin/env python3

#===== imports =====#
import argparse
import datetime
import os
import subprocess
import sys

#===== args =====#
parser = argparse.ArgumentParser()
args = parser.parse_args()

#===== consts =====#
DIR = os.path.dirname(os.path.realpath(__file__))

#===== setup =====#
os.chdir(DIR)

#===== helpers =====#
def timestamp():
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def invoke(*args, popen=False, **kwargs):
    print('-'*40)
    print(timestamp())
    print(args, kwargs, 'popen' if popen else '')
    print()
    if popen:
        return subprocess.Popen(args, **kwargs)
    else:
        if 'check' not in kwargs: kwargs['check'] = True
        return subprocess.run(args, **kwargs)

#===== main =====#
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
