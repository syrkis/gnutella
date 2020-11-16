# plotter.py
#   plots gnutella
# by: Noah Syrkis

# imports
import os
from matplotlib import pyplot as plt
import json

# plotting
class Plotter:

    def __init__(self, data):
        self.data = data

    def plot(self):
        print(self.data['indeg']['dict'])
        # deg dist
        # closenss
        # fitting
        # assortativity
        # clustering
        # shortest paths

    def __degdist(self, x, y):


def main():
    targets = [f"../data/dumps/{target}" for target in os.listdir('../data/dumps/')]
    for target in targets:
        with open(target, 'r') as data_file:
            data = json.load(data_file)
            plot = Plotter(data)
            plot.plot()


if __name__ == "__main__":
    main()
