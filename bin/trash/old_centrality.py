# centrality.py
#   centraility analysis of gnutella
# by: Noah Syrkis

"""
This scripts focuses on various centrality measures of the Gnutella network. For now it both performs both calculation and plotting. Soon I will create a seperate plotter.
"""

# imports
import random
import plotting
import networkx as nx
from constructor import S



# analysis
def centrality(G):
    # betweenness
    betw = nx.betweenness_centrality(G, k=1000)
    in_meta = {"title": f"{G.name}, betweenness centrality",
               "folder": "-".join(G.name.split("-")[::-1]),
               "file": f"betw-cent-{G.name}",
               "xlab": "C_b", "ylab": "P(C_b)"}
    plotting.scatter(betw, in_meta)

    #ideg = nx.in_degree_centrality(G)

    #odeg = nx.out_degree_centrality(G)
    # cloeseness
    clos = {nx.closeness_centrality(component(G), u=n) for n in sampler(component(G))}
    in_meta = {"title": f"{G.name}, closeness centrality",
               "folder": "-".join(G.name.split("-")[::-1]),
               "file": f"clos-cent-{G.name}",
               "xlab": "C_b", "ylab": "P(C_b)"}
    plotting.scatter(clos, in_meta)

    # eigen
    eige = nx.eigenvector_centrality(G, max_iter=200)

    clos = {nx.closeness_centrality(component(G), u=n) for n in sampler(component(G))}
    in_meta = {"title": f"{G.name}, eigenvector centrality",
               "folder": "-".join(G.name.split("-")[::-1]),
               "file": f"eigen-cent-{G.name}",
               "xlab": "C_b", "ylab": "P(C_b)"}
    plotting.scatter(eige, in_meta)

# helpers
def component(G):
    S = sorted(nx.strongly_connected_components(G), key = len, reverse = True)
    return G.subgraph(S[0])

def sampler(G):
    N = random.sample(G.nodes(), 1000)
    return N

# call stack
def main():
    centrality(S[0])

if __name__ == "__main__":
    main()
