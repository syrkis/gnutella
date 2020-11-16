# centrality.py
#   calculate centrality measure of given graph
# by: Noah Syrkis

"""
class for returning the centrality measure of a graph G
"""

# imports
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import random


# class
class Centrality:

    def __init__(self, G):
        self.G = G
        self.data = {}

    def extract(self):
        self._setup(self.G)
        return self.data

    def _setup(self, G):
        if G.is_multigraph():
            G = nx.DiGraph(G)
        self.data['betweenness'] = self._centrality(nx.betweenness_centrality(G, k=1000))
        self.data['eigenvector'] = self._centrality(nx.eigenvector_centrality(G, max_iter=200))
        self.data['in_degree'] = self._centrality(nx.in_degree_centrality(G))
        self.data['out_degree'] = self._centrality(nx.out_degree_centrality(G))
        self.data['closeness'] = self._closeness(G)

    def _centrality(self, data):
        w = np.ones_like(list(data.values())) / (len(data.values()))
        n, x, _ = plt.hist(list(data.values()), bins=20, weights=w)
        plt.close()
        bin_centers = 0.5*(x[1:]+x[:-1])
        return list(bin_centers), list(n)

    def _closeness(self, G):
        data = {}
        L = self._component(G)
        for node in random.sample(L.nodes(), 1000):
            data[node] = nx.closeness_centrality(L, u=node)
        x, y = self._centrality(data)
        return list(x), list(y)

    def _component(self, G):
        components = sorted(nx.strongly_connected_components(G), key=len)[::-1]
        L = G.subgraph(components[0])
        return L


def centrality(G):
    C = Centrality(G).extract()
    return C

