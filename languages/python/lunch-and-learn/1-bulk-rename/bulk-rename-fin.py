#===== imports =====#
import argparse
import os

#===== argument parsing =====#
parser = argparse.ArgumentParser()
parser.add_argument('transform')
args = parser.parse_args()

#===== main =====#
transform = eval(args.transform)
for cur_name in os.listdir('.'):
    new_name = transform(cur_name)
    if new_name:
        print(f'renaming {cur_name} to {new_name}')
        os.rename(cur_name, new_name)
