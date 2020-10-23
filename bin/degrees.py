# degrees.py
#   preliminary exploration of the gnutelle network
# by: Noah Syrkis


# imports
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter
from constructor import S
import plotting


#############
# functions #
#############


def degrees(G):
    """
    takes in nx graph.
    outputs various relevant plots.
    """
    # in degrees
    in_data = Counter(dict(G.in_degree).values())
    in_meta = {"title": f"{G.name}, in degree distribution",
               "folder": "-".join(G.name.split("-")[::-1]),
               "file": f"in-deg-dist-{G.name}",
               "xlab": "k", "ylab": "P(k)"}
    plotting.scatter(G, in_data, in_meta)

    # out degrees
    out_data = Counter(dict(G.out_degree).values())
    out_meta = {"title": f"{G.name}, out degree distribution",
                "folder": "-".join(G.name.split("-")[::-1]),
                "file": f"out-deg-dist-{G.name}",
                "xlab": "k", "ylab": "P(k"}
    plotting.scatter(G, out_data, out_meta)


def logbins(G):
    """
    takes in graph.
    saves log binned deg. dist. plots.
    """
    IN = list(dict(G.in_degree).values())
    OUT = list(dict(G.out_degree).values())
    w = np.ones_like(IN) / len(IN)
    plt.figure(figsize=(14, 8))
    plt.hist([IN, OUT], bins=np.logspace(np.log10(1), np.log10(max(IN)), num=15), weights=[w,w], log=True, label=["In degree", "Out degree"])
    plt.gca().set_yscale("symlog", linthresh=0.0001)
    plt.gca().set_xscale("log")
    plt.title(f"{G.name}, Log binning of in degree distribution")
    plt.xlabel(f"k"); plt.ylabel(f"P(k)"); plt.legend()
    plt.savefig(f"../docs/plots/{'-'.join(G.name.split('-')[::-1])}/log-bin-in-deg-{G.name}")
    plt.close()


def ccdfing(G):
    # indegree
    IN = list(dict(G.in_degree).values())
    n,x, _ = plt.hist(IN, density=True, cumulative=True, bins=100)
    plt.close()
    plt.figure(figsize=(14,8))
    bin_centers = 0.5*(x[1:]+x[:-1])
    y = [1 - v for v in n]
    plt.plot(bin_centers, y, 'ro')  ## using bin_centers rather than edges
    plt.title(f"{G.name}, in degree ccdf")
    plt.xlabel('x')
    plt.ylabel('P(x>k)')
    plt.gca().set_yscale("symlog", linthresh=0.00001)
    plt.gca().set_xscale("log")
    plt.savefig(f"../docs/plots/{'-'.join(G.name.split('-')[::-1])}/ccdf-in-deg-{G.name}")
    plt.close()

    # outdegree
    OUT = list(dict(G.out_degree).values())
    n,x, _ = plt.hist(OUT, density=True, cumulative=True, bins=100)
    plt.close()
    plt.figure(figsize=(14,8))
    bin_centers = 0.5*(x[1:]+x[:-1])
    y = [1 - v for v in n]
    plt.plot(bin_centers, y, 'ro')  ## using bin_centers rather than edges
    plt.title(f"{G.name}, out degree ccdf")
    plt.xlabel('x')
    plt.ylabel('P(x>k)')
    plt.gca().set_yscale("symlog", linthresh=0.00001)
    plt.gca().set_xscale("log")
    plt.savefig(f"../docs/plots/{'-'.join(G.name.split('-')[::-1])}/ccdf-out-deg-{G.name}")
    plt.close()


# call stack
def main():
    degrees(S[0])
    logbins(S[0])
    ccdfing(S[0])


if __name__ == "__main__":
    main()
