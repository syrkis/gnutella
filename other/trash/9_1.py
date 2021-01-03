import networkx as nx
import sys
sys.path.append('bin')
import network_map2 as nm

with open('../data/other/women.txt', 'r') as datafile:
    data = datafile.readlines()

nodes1 = list(set([int(n) for edge in data for n in edge.split()]))
nodes2 = [i + max(nodes1) + 1 for i in range(len(data))]

G = nx.Graph()
G.add_nodes_from(nodes1)
G.add_nodes_from(nodes2)

for i in range(len(data)):
    n1, n2 = list(map(int, data[i].strip().split()))
    G.add_edges_from([(n1, nodes2[i]), (n2, nodes2[i])])


nodes = nx.algorithms.bipartite.basic.sets(G)
n1s = sorted(list(nodes[0]))
n2s = sorted(list(nodes[1]))

G_sw = nm.jaccard(G, n2s)
G_rw = nm.ycn(G, n1s)

