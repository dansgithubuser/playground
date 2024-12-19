from netCDF4 import Dataset

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()

ds = Dataset(args.path)
print(ds)
