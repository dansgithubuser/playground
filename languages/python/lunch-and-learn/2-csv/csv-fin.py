#===== imports =====#
import argparse

#===== argument parsing =====#
parser = argparse.ArgumentParser()
parser.add_argument('file_path')
args = parser.parse_args()

#===== main =====#
with open(args.file_path) as file:
    lines = file.read().splitlines()
for line in lines:
    name, rating = line.split(',')
    print(f'name: {name:8}, rating: {rating}')
