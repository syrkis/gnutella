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
class Centrality(object):

    def __init__(self, G):
        self.G = G
        self.data = {}

    def extract(self):
        """
        Outputs dictionary of centrality measures
        """
        self.__setup(self.G)
        return self.data

    def __setup(self, G):
        """
        Call to calculate all centrality measures
        """
        if G.is_multigraph():
            G = nx.DiGraph(G)
        self.data['betweenness'] = self.__centrality(nx.betweenness_centrality(G, k=1000))
        self.data['eigenvector'] = self.__centrality(nx.eigenvector_centrality(G, max_iter=200))
        self.data['degree'] = self.__centrality(nx.degree_centrality(G))
        self.data['in_degree'] = self.__centrality(nx.in_degree_centrality(G))
        self.data['out_degree'] = self.__centrality(nx.out_degree_centrality(G))
        self.data['closeness'] = self.__closeness(G)

    def __centrality(self, data):
        """
        Outputs binned centrality measures
        """
        w = np.ones_like(list(data.values())) / (len(data.values()))
        n, x, _ = plt.hist(list(data.values()), bins=20, weights=w)
        plt.close()
        bin_centers = 0.5 * (x[1:] + x[:-1])
        return list(bin_centers), list(n)

    def __closeness(self, G):
        """
        Outputs closeness centrality
        """
        data = {}
        L = self.__component(G)
        for node in random.sample(L.nodes(), 1000):
            data[node] = nx.closeness_centrality(L, u=node)
        x, y = self.__centrality(data)
        return list(x), list(y)

    def __component(self, G):
        """
        returns largest components of graph
        """
        components = sorted(nx.strongly_connected_components(G), key=len)[::-1]
        L = G.subgraph(components[0])
        return L


def centrality(G):
    C = Centrality(G).extract()
    return C


def main():
    from construct import S
    G = S[7]
    C = Centrality(G)
    out = C.closeness(G)
    print(out)


if __name__ == '__main__':
    main()
