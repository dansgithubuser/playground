#! /usr/bin/env python3

#===== imports =====#
import argparse
import datetime
import os
import re
import signal
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

def invoke(
    *args,
    quiet=False,
    env_add={},
    handle_sigint=True,
    popen=False,
    check=True,
    out=False,
    err=False,
    **kwargs,
):
    if len(args) == 1 and type(args) == str:
        args = args[0].split()
    if not quiet:
        print(blue('-'*40))
        print(timestamp())
        print(os.getcwd()+'$', end=' ')
        if any([re.search(r'\s', i) for i in args]):
            print()
            for i in args: print(f'\t{i} \\')
        else:
            for i, v in enumerate(args):
                if i != len(args)-1:
                    end = ' '
                else:
                    end = ';\n'
                print(v, end=end)
        if kwargs: print(kwargs)
        if popen: print('popen')
        print()
    if env_add:
        env = os.environ.copy()
        env.update(env_add)
        kwargs['env'] = env
    if out or err: kwargs['capture_output'] = True
    p = subprocess.Popen(args, **kwargs)
    if handle_sigint:
        signal.signal(signal.SIGINT, lambda *args: p.send_signal(signal.SIGINT))
    if popen:
        return p
    p.wait()
    if handle_sigint:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    if check and p.returncode:
        raise Exception(f'invocation {repr(args)} returned code {p.returncode}.')
    if out:
        stdout = p.stdout.decode('utf-8')
        if out != 'exact': stdout = stdout.strip()
        if not err: return stdout
    if err:
        stderr = p.stderr.decode('utf-8')
        if err != 'exact': stderr = stderr.strip()
        if not out: return stderr
    if out and err: return [stdout, stderr]
    return p

#===== main =====#
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
