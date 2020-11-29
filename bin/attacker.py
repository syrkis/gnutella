# attacker.py
#   simulates attacks of the gnutella network
# by: Noah Syrkis

# imports
from construct import S
import random
import networkx as nx
from operator import itemgetter


class Attack(object):

    def __init__(self, graph):
        self.graph = graph
        self.L = self.__component(self.graph)

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
        if G.is_multigraph():
            G = nx.DiGraph(G)
        eiges = nx.eigenvector_centrality(G, max_iter=200)
        nodes = [(k, v) for k, v in eiges.items()]
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
        components = sorted(nx.strongly_connected_components(G), key=len)[::-1]
        L = G.subgraph(components[0])
        return L


def main():
    G = list(S.values())[-2]
    attack = Attack(G)
    #attack.random(0.1)
    attack.degrees(0.1)


if __name__ == "__main__":
    main()
