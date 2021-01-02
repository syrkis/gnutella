# robustness.py
#   simulates attacks of the gnutella network
# by: Noah Syrkis

# imports
import random
import networkx as nx
from operator import itemgetter
import numpy as np
import scipy.sparse
import scipy.sparse.csgraph
import gc; gc.enable()


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
        self.L = self.__component(graph)
        self.B = self.__betweenness()

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

    def closeness(self, p):
        G = self.L
        nodes = self.C[int(len(self.C) * p):]
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




def main():
    from construct import S
    G = list(S.values())[-2]
    robustness = Robustness(G)
    #attack.random(0.1)
    S = robustness.closeness(0.1)
    print(nx.info(S))


if __name__ == "__main__":
    main()
