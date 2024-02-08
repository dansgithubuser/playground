import fdt
import graphviz

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dtb')
args = parser.parse_args()

with open(args.dtb, 'rb') as f:
    dt = fdt.parse_dtb(f.read())

dot = graphviz.Digraph()

def graph(node):
    dot.node(node.name, node.name)
    for child in node.nodes:
        graph(child)
        dot.edge(node.name, child.name)

graph(dt.root)

print(dot.render('dt.gv'))
