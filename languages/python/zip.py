#!/usr/bin/env python3

import argparse
import glob
from pathlib import Path
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--zip', metavar='glob')
parser.add_argument('--list', metavar='zip_path')
parser.add_argument('--unzip', metavar='zip_path')
parser.add_argument('--unzip-one', nargs=2, metavar=('zip_path', 'member'))

def zip_glob(member_glob):
    with zipfile.ZipFile(Path(member_glob).parts[0] + '.zip', 'w') as zf:
        for path in glob.glob(member_glob):
            zf.write(path)

def zip_list(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        return zf.namelist()

def unzip(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall()

def unzip_one(zip_path, member):
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(member) as f:
            contents = f.read()
    Path(member).parent.mkdir(parents=True, exist_ok=True)
    with open(member, 'wb') as f:
        f.write(contents)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.zip:
        zip_glob(args.zip)
    if args.list:
        print(zip_list(args.list))
    if args.unzip:
        unzip(args.unzip)
    if args.unzip_one:
        unzip_one(*args.unzip_one)
