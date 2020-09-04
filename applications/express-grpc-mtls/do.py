#! /usr/bin/env python3

#===== imports =====#
import argparse
import copy
import datetime
import os
import re
import subprocess
import sys
import time

#===== args =====#
parser = argparse.ArgumentParser()
parser.add_argument('--server', '-s', action='store_true')
parser.add_argument('--client-new-creds', '--cn', action='store_true')
parser.add_argument('--client', '-c', action='store_true')
parser.add_argument('--verbose', '-v', action='store_true')
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
    popen=False,
    no_split=False,
    stdout=False,
    quiet=False,
    **kwargs,
):
    if len(args) == 1 and not no_split:
        args = args[0].split()
    if not quiet:
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
    if kwargs.get('env'):
        env = copy.copy(os.environ)
        env.update(kwargs['env'])
        kwargs['env'] = env
    if popen:
        return subprocess.Popen(args, **kwargs)
    else:
        if 'check' not in kwargs: kwargs['check'] = True
        if stdout: kwargs['capture_stdout'] = True
        result = subprocess.run(args, **kwargs)
        if stdout:
            result = result.stdout.decode('utf-8').strip()
        return result

def ensure_creds():
    if os.path.exists('client.crt'): return
    print('Creating crypto material for mutual TLS.')
    #----- CA -----#
    invoke('openssl genrsa -out ca.key 2048')  # create ca.key
    invoke('openssl req -x509 -key ca.key -out ca.pem -subj /CN=dans-playground-express-grpc-mtls')  # create ca.pem from ca.key
    #----- server -----#
    invoke('openssl genrsa -out server.key 2048')  # create server.key
    # create server.pem from server.key, sign with ca.key
    invoke('openssl req -new -key server.key -out server.csr -subj /CN=dans-playground-express-grpc-mtls')
    with open('server.ext', 'w') as server_ext:
        server_ext.write(
            'keyUsage = digitalSignature\n'
            'subjectAltName = DNS:localhost\n'
        )
    invoke('openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -out server.crt -extfile server.ext')
    #----- client -----#
    new_client_creds()

def new_client_creds():
    invoke('openssl genrsa -out client.key 2048')  # create client.key
    # create client.pem from client.key, sign with ca.key
    invoke('openssl req -new -key client.key -out client.csr -subj  /CN=dans-playground-express-grpc-mtls')
    with open('client.ext', 'w') as client_ext:
        client_ext.write('keyUsage = digitalSignature\n')
    invoke('openssl x509 -req -in client.csr -CA ca.pem -CAkey ca.key -out client.crt -extfile client.ext')

#===== main =====#
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

ensure_creds()
if args.verbose:
    os.environ['GRPC_TRACE'] = 'all'
    os.environ['GRPC_VERBOSITY'] = 'DEBUG'

if args.server:
    invoke('node server.js')

if args.client_new_creds:
    new_client_creds()

if args.client:
    invoke('node client.js')
