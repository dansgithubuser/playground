#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'bin_sets',
    metavar='name, price, quantity, depth, width, height',
    nargs='+',
    help='Depth is how far into the shelf the bin goes. Height is how far you can put an item into the bin.',
)
args = parser.parse_args()

class BinSet:
    def __init__(self, *args):
        self.name = args[0]
        self.price = float(args[1])
        self.quantity = int(args[2])
        self.depth = float(args[3])
        self.width = float(args[4])
        self.height = float(args[5])

    def print_properties(self):
        print(f'name: {self.name}')
        print(f'quantity: {self.quantity}')
        print(f'price: {self.price}')
        print(f'unit price: {self.price / self.quantity:.2f} $/bin')
        print(f'volume: {self.width:.1f} x {self.depth:.1f} = {self.width * self.depth * self.height:.2f}')
        print(f'total volume: {self.width * self.depth * self.height * self.quantity:.2f}')
        print(f'footprint: {self.width:.1f} x {self.depth:.1f} = {self.width * self.depth:.1f}')
        print(f'total footprint: {self.width * self.depth * self.quantity:.2f}')

for i in range(0, len(args.bin_sets), 6):
    BinSet(*args.bin_sets[i:]).print_properties()
    print()
