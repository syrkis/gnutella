# metrics.py
#   plotter class for gnutella analysis
# by: Noah Syrkis

"""
general purpose gnutella plotting
"""

# imports
import networkx as nx
from construct import S
from collections import Counter
import sys
from centrality import centrality
import pickle


# class
class Graph:

    data = {}

    def __init__(self, G, **kwargs):
        self.G = G
        for k, v in kwargs.items():
            exec(f"self.{k} = {v}")

    def construct(self):
        self._setup(self.G)
        return self.data

    def _setup(self, G):
        # degree distribution
        G_degs = self._degfreq(G)
        self.data['indeg'] = {'dict': G.in_degree, 'dist': G_degs[0]}
        self.data['outdeg'] = {'dict': G.out_degree, 'dist': G_degs[1]}
        # centrality measures and clustering
        self.data['centrality'] = centrality(G)
        self.data['clustering'] = self._clustering(G)
        # configuration metrics
        C = self._config(G)
        self.data['C'] = {'G': C, 'centrality': centrality(C), 'clustering': self._clustering(C)}

    def _degfreq(self, G):
        return Counter(dict(G.in_degree)).values(),  Counter(dict(G.out_degree)).values()

    def _clustering(self, G):
        cluster = Counter(dict(nx.clustering(G)).values())
        x = cluster.keys()
        y = cluster.values()
        return x, y

    def _config(self, G):
        d_in = [G.in_degree[node] for node in G.nodes]
        d_out = [G.out_degree[node] for node in G.nodes]
        return nx.directed_configuration_model(d_in, d_out)


# script
def main():
    data = None
    construct = True
    if construct:
        G = Graph(S[0])
        data = G.construct()
        with open(f'../data/dumps/pickle-{G.G.name}', 'wb') as data_file:
            pickle.dump(data, data_file)
    else:
        G = Graph(S[0], data=data)


if __name__ == "__main__":
    main()
