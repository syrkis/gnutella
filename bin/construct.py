# construct.py
#   preliminary exploration of the gnutelle network
# by: Noah Syrkis


# imports
import networkx as nx
import os


# construct
path = '../data/'
targets = [path + target for target in os.listdir(path)]
S = {idx: nx.read_edgelist(target, delimiter="\t", create_using=nx.DiGraph(name='test')) \
     for idx, target in enumerate(targets)}
for idx, G in enumerate(S):
    S[G].name = targets[idx][-6:-4] + '-08-2002'


def main():
    for idx, G in S.items():
        print(G.info)


if __name__ == "__main__":
    main()
