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
def blue(text):
    return '\x1b[34m' + text + '\x1b[0m'

def timestamp():
    return '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())

def invoke(*args, popen=False, no_split=False, **kwargs):
    if len(args) == 1 and not no_split:
        args = args[0].split()
    print(blue('-'*40))
    print(timestamp())
    print(os.getcwd()+'$', end=' ')
    for i, v in enumerate(args):
        if re.search(r'\s', v):
            v = v.replace("'", """ '"'"' """.strip())
            v = f"'{v}'"
        if i != len(args)-1:
            end = ' '
        else:
            end = ';\n'
        print(v, end=end)
    if kwargs: print(kwargs)
    if popen: print('popen')
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
