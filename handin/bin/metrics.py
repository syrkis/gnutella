# metrics.py
#   plotter class for gnutella analysis
# by: Group D

"""
Class to precompute various network metrics for quick plotting and analysis.
Main purpose is to take in graph and save data into .json file.
"""

# imports
import networkx as nx
from construct import S
from collections import Counter
from centrality import centrality
from tqdm import tqdm
from robustness import Robustness
import os
import json
import random


# class
class Metric:

    def __init__(self, G, data={}):
        """
        Calls setup and and precomputes data
        """
        self.G = G
        self.U = nx.Graph(G)
        self.name = G.name
        self.data = data
        self.__setup(self.G)

    def save(self):
        """
        Saves data
        """
        json_data = json.dumps(self.data, indent=4)
        with open(f'../data/dumps/{self.name}.json', 'w') as json_file:
            json_file.write(json_data)

    def __setup(self, G):
        """
        Computes all data by by using other classes and functions
        """
        # degree distribution
        G_degs = self.__degfreq(G)
        self.data['degs'] = {'in': G_degs[0], 'out': G_degs[1]}
        # centrality measures, clustering
        self.data['robustness'] = self.__robustness(G)
        self.data['centrality'] = centrality(G)
        self.data['clustering'] = self.__clustering(G)
        self.data['shortest'] = self.__shortest(self.__component(G))

        # configuration metrics
        C = self.__config(G)
        self.data['C'] = {'robustness': self.__robustness(C), 'centrality': centrality(C),
                          'clustering': self.__clustering(C), 'shortest': self.__shortest(self.__component(C))}

    def __robustness(self, G):
        """
        Returns list of lists of fractions of nodes still in largest component when removing node by different
        rules (randomly, by degree and by betweenness centrality). The fraction of nodes removed is represented
        by p. p varies from 0.05 to 1.0.
        """
        A = Robustness(G)
        ps = [0.05 * i for i in range(0, 20)]
        rands, degs, betws, eigs, links = [], [], [], [], []
        for p in ps:
            r = A.random(p)
            d = A.degrees(p)
            b = A.betweenness(p)
            e = A.eigen(p)
            l = A.random_edge(p)
            rands.append(self.__connectivity(r))
            degs.append(self.__connectivity(d))
            betws.append(self.__connectivity(b))
            eigs.append(self.__connectivity(e))
            links.append(self.__connectivity(l))
        return rands, degs, betws, eigs, links, ps        # random, degree, closeness, betweenness, eigen, portions

    def __shortest(self, G):
        """
        Returns average shortest path of network.
        """
        lens = []
        for i in range(10000):
            nodes = random.sample(G.nodes(), 2)
            l = nx.shortest_path_length(G, source=nodes[0], target=nodes[1])
            lens.append(l)
        return sum(lens) / len(lens)

    def __degfreq(self, G):
        """
        runs lists with degrees and frequencies for network.
        """
        in_freq = Counter(dict(G.in_degree).values())
        in_x = list(in_freq.keys())
        in_y = list(in_freq.values())
        out_freq = Counter(dict(G.out_degree).values())
        out_x = list(out_freq.keys())
        out_y = list(out_freq.values())
        return [in_x, in_y], [out_x, out_y]

    def __clustering(self, G):
        """
        runs clustering coeficinets and frequencies for network.
        """
        if G.is_multigraph():
            G = nx.DiGraph(G)
        cluster = Counter(dict(nx.clustering(G)).values())
        x = list(cluster.keys())
        y = list(cluster.values())
        return x, y

    def __config(self, G):
        """
        Takes in graph and returns directed configuration model
        """
        d_in = [G.in_degree[node] for node in G.nodes]
        d_out = [G.out_degree[node] for node in G.nodes]
        C = nx.directed_configuration_model(d_in, d_out)
        C = nx.DiGraph(C)
        return C

    def __connectivity(self, G):
        """
        Determines fraction of ndoes till on largest component (used for robustness tests)
        """
        L = self.__component(G)
        return len(L.nodes) / len(G.nodes)

    def __component(self, G):
        """
        takes in graph and returns largest strongly connected component of the network
        """
        components = sorted(nx.strongly_connected_components(G), key=len)[::-1]
        L = G.subgraph(components[0])
        return L

# script
def main():
    construct = True        # if True we reconstruct the graph analysis data.
    for G in tqdm(S.values()):
        if not construct and f"{G.name}.json" in os.listdir('../data/dumps/'):
            with open(f"../data/dumps/{G.name}.json", 'r') as data_file:
                data = json.load(data_file)
            D = Metric(G, data=data)
        else:               # read graph analysis data from file
            D = Metric(G)
            D.save()


if __name__ == "__main__":
    main()
