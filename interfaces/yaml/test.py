#!/usr/bin/env python3

import glob
from pprint import pprint

import yaml

for file_name in sorted(glob.glob("*.yaml")):
    print('\n=================================\n')
    with open(file_name) as file:
        for i, line in enumerate(file.readlines()):
            print(f'{i+1:02}', line.rstrip())
        print()
        file.seek(0)
        try:
            pprint(yaml.safe_load(file))
        except Exception as e:
            print(e)
