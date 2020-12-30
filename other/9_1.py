import networkx as nx
import sys
sys.path.append('bin')
sys.path.append('../bin')
import backboning as bb
import network_map2 as nm

G = nx.read_edgelist('../data/other/southernwomen.txt', create_using=nx.Graph())
jac = nm.jaccard(G, nodes)
ycn = nm.ycn(G, nodes)
