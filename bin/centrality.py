# centrality.py
#   centraility analysis of gnutella
# by: Noah Syrkis

"""
This scripts focuses on various centrality measures of the Gnutella network. For now it both performs both calculation and plotting. Soon I will create a seperate plotter.
"""

# imports
import sys
import random
import networkx as nx
import numps as np
import pandas as pd
from builder import S
from collections import Counter
from matplotlib import pyplot as plt


# analysis
def centrality(G):
    betw = nx.betweenness_centrality(G, k = 1000)
    ideg = nx.in_degree_centrality(G)
    odeg = nx.out_degree_centrality(G)


# helpers
def largecomp(G):
    sotred_comps = sorted(nx.strongly_connected_components(G), key = len, reverse = True)
    return G.subgraph(sorted_comps[0])

# call stack
def main():
    for G in S.values():
        centrality(G)

if __name__ == "__main__":
    main()
