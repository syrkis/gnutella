# explorer.py
#   preliminary exploration of the gnutelle network
# by: Noah Syrkis

# imports
import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import Counter
import os

# construct
path = '../data/'
targets = [path + target for target in os.listdir(path)]
S = {"G" + str(idx) : nx.read_edgelist(target,
    delimiter="\t", create_using=nx.DiGraph(name='test'))
    for idx, target in enumerate(targets)}
for idx, G in enumerate(S):
    S[G].name = "2002-08-" + targets[idx][-6:-4]

# plotting
def plotter(*args):
    n = len(args)
    for idx, arg in enumerate(args):
        plt.figure(figsize=(14, 8))

        plt.plot(list(arg.keys()), list(arg.values()), 'ob')
        plt.title(f"Linear plot"); plt.xlabel("x"); plt.ylabel("y")
        plt.savefig(f'../docs/plots/lin')

        plt.title(f"Log plot"); plt.xlabel("x"); plt.ylabel("y") 
        plt.loglog(list(arg.keys()), list(arg.values()), 'or')
        plt.savefig(f'../docs/plots/log')

# call stack
def main():
    tmp = Counter(dict(S['G0'].degree).values())
    plotter(tmp)

if __name__ == "__main__":
    main()
