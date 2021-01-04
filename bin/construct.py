# construct.py
#   preliminary exploration of the gnutelle network
# by: Noah Syrkis


# imports
import networkx as nx
import os


# construct
path = '../data/graphs/'
targets = sorted([path + target for target in os.listdir(path) if target[-1] == 't'])
S = {idx: nx.read_edgelist(target, delimiter="\t", create_using=nx.DiGraph(name='test'), nodetype=int) \
     for idx, target in enumerate(targets)}
for idx, G in enumerate(S):
    S[G].name = targets[idx][-6:-4] + '-08-2002'


def main():
    for idx, G in S.items():
        print(G.info)


if __name__ == "__main__":
    main()
