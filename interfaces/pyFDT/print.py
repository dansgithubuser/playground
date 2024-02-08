import fdt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dtb')
args = parser.parse_args()

with open(args.dtb, 'rb') as f:
    dt = fdt.parse_dtb(f.read())

def print_(node, depth=0):
    print('  ' * depth, end='')
    print(node.name)
    for child in node.nodes:
        print_(child, depth+1)

print_(dt.root)
