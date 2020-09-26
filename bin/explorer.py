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
S = {"G" + str(idx) : nx.read_edgelist(target, delimiter="\t", create_using=nx.Graph(name='test'))for idx, target in enumerate(targets)}

# plotting


# call stack
def main():
    for G in S:
        print(nx.info(S[G]))
    return 0

if __name__ == "__main__":
    main()
