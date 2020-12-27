# robustness.py
#   simulates attacks of the gnutella network
# by: Noah Syrkis

# imports
from construct import S
import random
import networkx as nx
from operator import itemgetter
import numpy as np
import scipy.sparse
import scipy.sparse.csgraph
from tqdm import tqdm


class Robustness(object):
    """
    This class takes in a given when initialized.

    It has several attack methods, each outputting a subgraph consisting
    of what remains when removing p percent of the network
    with a given heuristic (i.e. random, by closeness, by degree, etc.)

    In addition to this there are several helper functions beginning with
    __.
    """
    def __init__(self, graph):
        self.graph = graph
        self.L = self.__component(self.graph)
        self.C = self.__closenss()
        #self.B = self.__betweenness()

    def random(self, p):
        G = self.L
        nodes = random.sample(G.nodes, int(float(len(G.nodes)) * (1-p)))
        S = nx.subgraph(G, nodes)
        return S

    def degrees(self, p):
        G = self.L
        degs = sorted(G.degree, key=itemgetter(1))[::-1]
        nodes = [entry[0] for entry in degs][int(len(degs) * p):]
        S = nx.subgraph(G, nodes)
        return S

    def eigen(self, p):
        G = self.L
        eiges = nx.eigenvector_centrality(G, max_iter=200)
        nodes = [(k, v) for k, v in eiges.items()]
        nodes = sorted(nodes, key=itemgetter(1))[::-1]
        nodes = [entry[0] for entry in nodes][int(len(nodes) * p):]
        S = nx.subgraph(G, nodes)
        return S

    def closeness(self, p):
        G = self.L
        nodes = self.C[int(len(self.C) * p):]
        nodes = [str(node) for node in nodes]
        S = nx.subgraph(G, nodes)
        return S

    def betweenness(self, p):
        G = self.L
        out = self.B
        nodes = [(k, v) for k, v in out.items()]
        nodes = sorted(nodes, key=itemgetter(1))[::-1]
        nodes = [entry[0] for entry in nodes][int(len(nodes) * p):]
        S = nx.subgraph(G, nodes)
        return S

    def pagerank(self, p):
        G = self.L
        eiges = nx.pagerank(G)
        nodes = [(k, v) for k, v in eiges.items()]
        nodes = sorted(nodes, key=itemgetter(1))[::-1]
        nodes = [entry[0] for entry in nodes][int(len(nodes) * p):]
        S = nx.subgraph(G, nodes)
        return S

    def __component(self, G):
        """
        Takes in graph and returns largest strongly connected component
        therein
        """
        components = sorted(nx.strongly_connected_components(G), key=len)[::-1]
        L = G.subgraph(components[0])
        return L

    def __betweenness(self):
        G = self.L
        return nx.betweenness_centrality(G)

    def __closenss(self):
        """
        Linear algebra trick to calculate closeness for the entire
        network in less than a year.
        """
        ccs = {}
        G = self.L
        if G.is_multigraph():
            G = nx.DiGraph(G)
        A = nx.adjacency_matrix(G).tolil()
        D = scipy.sparse.csgraph.floyd_warshall(A,
                                                directed=False,
                                                unweighted=False)

        n = D.shape[0]
        for r in range(n):
            cc = 0.0
            possible_paths = list(enumerate(D[r, :]))
            shortest_paths = dict(filter(\
                lambda x: not x[1] == np.inf, possible_paths))
            total = sum(shortest_paths.values())
            n_shortest_paths = len(shortest_paths) - 1.0

            if total > 0.0 and n > 1:
                s = n_shortest_paths / (n - 1)
                cc = (n_shortest_paths / total) * s
            ccs[r] = cc

        nodes_sorted_by_closeness = sorted(ccs, key=ccs.__getitem__, reverse=True)
        return nodes_sorted_by_closeness



def main():
    G = list(S.values())[-2]
    robustness = Robustness(G)
    #attack.random(0.1)
    robustness.betweenness(0.1)


if __name__ == "__main__":
    main()
