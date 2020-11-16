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
from centrality import centrality
from tqdm import tqdm
import os
import json


# class
class Metric:

    def __init__(self, G, data={}):
        self.G = G
        self.name = G.name
        self.data = data

    def build(self):
        self._setup(self.G)

    def save(self):
        json_data = json.dumps(self.data, indent=4)
        with open(f'../data/dumps/{self.name}.json', 'w') as json_file:
            json_file.write(json_data)

    def _setup(self, G):
        # degree distribution
        G_degs = self._degfreq(G)
        self.data['indeg'] = {'dict': list(G.in_degree), 'dist': G_degs[0]}
        self.data['outdeg'] = {'dict': list(G.out_degree), 'dist': G_degs[1]}
        # centrality measures and clustering
        self.data['centrality'] = centrality(G)
        self.data['clustering'] = self._clustering(G)
        # configuration metrics
        C = self._config(G)
        self.data['C'] = {'centrality': centrality(C), 'clustering': self._clustering(C)}

    def _degfreq(self, G):
        return list(Counter(dict(G.in_degree)).values()), list(Counter(dict(G.out_degree)).values())

    def _clustering(self, G):
        if G.is_multigraph():
            G = nx.DiGraph(G)
        cluster = Counter(dict(nx.clustering(G)).values())
        x = list(cluster.keys())
        y = list(cluster.values())
        return x, y

    def _config(self, G):
        d_in = [G.in_degree[node] for node in G.nodes]
        d_out = [G.out_degree[node] for node in G.nodes]
        return nx.directed_configuration_model(d_in, d_out)


# script
def main():
    construct = False        # if True we reconstruct the graph analysis data.
    for G in tqdm(S.values()):
        if not construct and f"{G.name}.json" in os.listdir('../data/dumps/'):
            with open(f"../data/dumps/{G.name}.json", 'r') as data_file:
                data = json.load(data_file)
            D = Metric(S[0], data=data)
        else:               # read graph analysis data from file
            D = Metric(G)
            D.build()
            D.save()


if __name__ == "__main__":
    main()
