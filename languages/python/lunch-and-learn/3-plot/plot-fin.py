#===== imports =====#
import matplotlib.pyplot as plt

import argparse
import math

#===== argument parsing =====#
parser = argparse.ArgumentParser()
args = parser.parse_args()

#===== main =====#
lines = [
    'yonge-university-spadina-NAD83.csv',
    'bloor-danforth-NAD83.csv',
]
x = []
y = []
for line in lines:
    with open('assets/'+line) as file:
        lines = file.read().splitlines()
    for line in lines:
        lat, lon, station = line.split(',')
        lat = float(lat)
        lon = float(lon)
        x.append(lon)
        y.append(lat)
plt.scatter(x, y)
plt.savefig('ttc.png')
# we let matplotlib choose our aspect ratio -- so while this plot _looks_ spatially accurate, it is a coincidence
