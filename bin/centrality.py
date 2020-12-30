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
import gc; gc.enable()


# class
class Centrality(object):

    def __init__(self, G):
        self.G = G
        self.data = {}

    def extract(self):
        self.__setup(self.G)
        return self.data

    def __setup(self, G):
        if G.is_multigraph():
            G = nx.DiGraph(G)
        self.data['betweenness'] = self.__centrality(nx.betweenness_centrality(G, k=1000))
        self.data['eigenvector'] = self.__centrality(nx.eigenvector_centrality(G, max_iter=200))
        self.data['in_degree'] = self.__centrality(nx.in_degree_centrality(G))
        self.data['out_degree'] = self.__centrality(nx.out_degree_centrality(G))
        self.data['closeness'] = self.__closeness(G)

    def __centrality(self, data):
        w = np.ones_like(list(data.values())) / (len(data.values()))
        n, x, _ = plt.hist(list(data.values()), bins=20, weights=w)
        plt.close()
        bin_centers = 0.5*(x[1:]+x[:-1])
        return list(bin_centers), list(n)

    def __closeness(self, G):
        data = {}
        L = self.__component(G)
        for node in random.sample(L.nodes(), 1000):
            data[node] = nx.closeness_centrality(L, u=node)
        x, y = self.__centrality(data)
        return list(x), list(y)

    def __component(self, G):
        components = sorted(nx.strongly_connected_components(G), key=len)[::-1]
        L = G.subgraph(components[0])
        return L


def centrality(G):
    C = Centrality(G).extract()
    return C

