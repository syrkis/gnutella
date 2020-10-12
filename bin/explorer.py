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
S = {idx : nx.read_edgelist(target,
    delimiter="\t", create_using=nx.DiGraph(name='test'))
    for idx, target in enumerate(targets)}
for idx, G in enumerate(S):
    S[G].name = targets[idx][-6:-4] + "-08-2002"



#########
# plots #
#########

def plotter(*args):
    n = len(args)
    for idx, arg in enumerate(args):
        plt.figure(figsize=(14, 8))

        plt.plot(list(arg[1].keys()), list(arg[1].values()), 'ob')
        plt.title(f"{arg[0]['kind']} {arg[0]['graph']} Linear"); plt.xlabel("x"); plt.ylabel("y")
        plt.savefig(f'../docs/plots/{"-".join(arg[0]["graph"].split("-")[::-1])}/{arg[0]["file"]}-lin')

        plt.title(f"{arg[0]['kind']} {arg[0]['graph']} LogLog"); plt.xlabel(arg[0]['xlab']); plt.ylabel(arg[0]['ylab']) 
        plt.loglog(list(arg[1].keys()), list(arg[1].values()), 'or')
        plt.savefig(f'../docs/plots/{"-".join(arg[0]["graph"].split("-")[::-1])}/{arg[0]["file"]}-log')
        plt.close()

def hister(*args):
    for idx, arg in enumerate(args):
        plt.figure(figsize=(14,8))
        x = arg[1].keys(); y = arg[1].values()
        plt.bar(x, y)
        plt.title(f"{arg[0]['kind']} {arg[0]['graph']} Linear"); plt.xlabel("x"); plt.ylabel("y") 
        plt.savefig(f"../docs/plots/{'-'.join(arg[0]['graph'].split('-')[::-1])}/{arg[0]['file']}-hist")
        plt.close()


############
# analysis #
############

def degrees():
    for idx, G in S.items():
        meta = {"file" : f"{G.name}-in-deg", "graph" : G.name, "kind" : "In Degree Distribution", "xlab" : "k", "ylab" : "p(k)"}
        tmp = [meta, Counter(dict(G.in_degree).values())]
        plotter(tmp)
        meta['file'] = f"{G.name}-out-degree"
        tmp = [meta, Counter(dict(G.out_degree).values())]
        plotter(tmp)


def clustering():
    for idx, G in S.items():
        meta = {"file" : f"{G.name}-clustering", "graph" : G.name, "kind" : "Clustering Distribution", "xlab" : "C", "ylab" : "P(C)"} 
        tmp = [meta, Counter(dict(nx.clustering(G)).values())]
        plotter(tmp)

def shortest_path(n = 10000):
    for idx, G in S.items():
        g = G.subgraph(sorted(nx.strongly_connected_components(G), key=len, reverse=True)[0])
        P = []
        for i in range(10000):
            nodes = random.sample(g.nodes(), 2)
            p = nx.shortest_path(g, source=nodes[0], target=nodes[1]) 
            P.append(p)
        P = [len(p) for p in P]
        P = Counter(P)
        meta = {"file" : f"{G.name}-shortest-paths", "graph" : G.name, "kind" : "Shortest Path Distribution", "xlab" : "Path length", "ylab" : "Frequency"}
        tmp = [meta, P]
        hister(tmp)


# call stack
def main():
    clustering()
    degrees()
    shortest_path()


if __name__ == "__main__":
    main()
