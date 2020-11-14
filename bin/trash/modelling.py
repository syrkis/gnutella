# modelling.py
#   modelling of the gnutella network
# by: Noah Syrkis

"""Fits models to degree distributions (and plots it too)"""

# imports
import powerlaw
import networkx as nx
import pandas as pd
import numpy as np
from constructor import S
from matplotlib import pyplot as plt
import warnings
import random

# modelling
def modelling():
    for G in S.values():
        O, I = degree(G)
        OK, IK = power(O, I)

        # configuration model
        C = configuration(G)
        CO, CI = degree(C)
        COK, CIK = power(CO, CI)

        meta = {"file" : f"{G.name}-out"}
        ccdf(OK, meta)
        fitting(OK, COK, meta)

        meta = {"file" : f"{G.name}-in"}
        ccdf(IK, meta)
        fitting(IK, CIK, meta)

def configuration(G):
    model = nx.MultiDiGraph()
    in_deg_seq = list(dict(G.in_degree).values())
    out_deg_seq = list(dict(G.out_degree).values())

    in_stubs = []
    out_stubs = []

    for idx, deg in enumerate(in_deg_seq):
        for i in range(deg):
            in_stubs.append( (idx, i) ) 

    for idx, deg, in enumerate(out_deg_seq):
        for i in range(deg):
            out_stubs.append( (idx, i) )

    for node, edgenum in out_stubs:
        in_stub = in_stubs.pop(random.randint(0, len(in_stubs) -1))
        model.add_edge(node, in_stub[0])

    return model

# helpers
def fitting(D, C, meta):

    # init plot
    fig, (ax) = plt.subplots(1, 1, figsize=(14, 8))

    # CCDF of original network
    D.plot_ccdf(ax=ax, label='Original network: CCDF', linestyle='--', marker='v')

    # add fitted powerlaw,lognormal CCDF plots as dashed lines
    D.power_law.plot_ccdf(ax=ax, color='#f54e42', linestyle='-',
                                           label='Original network: power-law fit')

    D.lognormal.plot_ccdf(ax=ax, color='#f5bc42', linestyle='-',
                                           label='Original network: lognormal fit')

    # repeat for configurational model
    C.plot_ccdf(ax=ax, label='Configuration: CCDF', linestyle='--', marker='^')
    # add fitted powerlaw, lognormal CCDF plots as dashed lines
    C.power_law.plot_ccdf(ax=ax, color='#085087', linestyle='--',
                                                label='Configuration: power-law fit')
    C.lognormal.plot_ccdf(ax=ax, color='#5e98c4', linestyle='--',
                                                label='Configuration: lognormal fit')


    plt.legend()
    plt.savefig(f"../docs/plots/dev/{meta['file']}-fitccdf")

def degree(G):
    O = np.array(list(dict(G.out_degree).values()))
    I = np.array(list(dict(G.in_degree).values()))
    return O, I

def power(O, I):
    OK = powerlaw.Fit(O, verbose = False)
    IK = powerlaw.Fit(I, verbose = False)
    return OK, IK

def ccdf(D, meta):
    plt.figure(figsize=(14,8))
    fig = D.plot_ccdf(label='CCDF', linestyle='--', marker='o')
    plt.savefig(f'../docs/plots/dev/{meta["file"]}-XXXX')

    plt.close


# warnings
warnings.filterwarnings("ignore", message="invalid value encountered in true_divide")
warnings.filterwarnings("ignore", message="divide by zero encountered in true_divide")

    
# call stack
def main():
    modelling()


if __name__ == "__main__":
    main()
