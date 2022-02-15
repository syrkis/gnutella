import networkx as nx
import random

G = nx.Graph()
n = 10 ** 4
e = 4 * 10 ** 4
p = 0.0008

for i in range(n):
    for j in range(i + 1, n):
        if random.random() < p:
            G.add_edge(i, j)

def compfrac(G):
    n = len(G.nodes)
    m = len(sorted(nx.strongly_connected_component(G))[-1])
    return m / n

def attack(G, p):
    
