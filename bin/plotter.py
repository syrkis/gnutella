# plotter.py
#   plots gnutella
# by: Noah Syrkis

# imports
import os
from matplotlib import pyplot as plt
import json


# plotting
class Plotter(object):

    def __init__(self, data):
        self.data = data

    def plot(self):
        data = self.data
        print(data['centrality'].keys())
        deg_data = [[data['degs']['in'], data['degs']['out']],
                    [data['degs']['ccdf_in'], data['degs']['ccdf_out']]]
        self.__degdist(deg_data)
        G_cen = data['centrality']
        C_cen = data['C']['centrality']
        self.__cendist(G_cen, C_cen)

    def __cendist(self, G_cen, C_cen):
        fig, axes = plt.subplots(5, 1, figsize=(8, 14))
        fig.suptitle('{self.G.name} cen. dist.')
        for idx, key in enumerate(G_cen.keys()):
            axes[idx].loglog(G_cen[key][0], G_cen[key][1], 'ro')
            axes[idx].loglog(C_cen[key][0], C_cen[key][1], 'bo')
        plt.show()

    def __degdist(self, data):
        kinds = ['loglog', 'loglog']
        fig, axes = plt.subplots(2, 2, figsize=(14, 8))
        fig.suptitle('{self.G.name} deg. dist.')
        for idx in range(len(axes)):
            focus = data[idx]
            for jdx in range(len(axes[idx])):
                x, y = focus[jdx]
                exec(f"axes[idx][jdx].{kinds[idx]}(x, y, 'ro')")
        plt.show()


def main():
    targets = [f"../data/dumps/{target}" for target in os.listdir('../data/dumps/')]
    for target in targets:
        with open(target, 'r') as data_file:
            data = json.load(data_file)
            plot = Plotter(data)
            plot.plot()


if __name__ == "__main__":
    main()
