# modeler.py
#   modelling of the gnutella network
# by: Noah Syrkis

"""Fits models to degree distributions (and plots it too)"""

# imports
import powerlaw
import networkx as nx
import pandas as pd
import numpy as np
from builder import S
from matplotlib import pyplot as plt

# modelling
def modelling():
    for G in S.values():
        O, I = degree(G)
        OK, IK = power(O, I)
        meta = {"file" : f"{G.name}-out"}
        ccdf(OK, meta)
        fitting(OK, meta)
        meta = {"file" : f"{G.name}-in"}
        fitting(IK, meta)
        ccdf(IK, meta)

# helpers
def fitting(D, meta):
    plt.figure(figsize=(14,8))
    fig = D.plot_ccdf(label="CCDF", color='r',  linestyle='--', marker='o')
    D.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='power-law fit')
    D.exponential.plot_ccdf(ax=fig, color='g', linestyle='--', label='exponential fit')
    D.lognormal.plot_ccdf(ax=fig, color='b', linestyle='--', label='lognormal fit')
    D.truncated_power_law.plot_ccdf(ax=fig, color='k', linestyle='--', label='Powerlaw w. exp. cutoff')
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
    
# call stack
def main():
    modelling()

if __name__ == "__main__":
    main()
