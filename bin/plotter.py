# plotter.py
#   plots gnutella
# by: Noah Syrkis

# imports
import os
from matplotlib import pyplot as plt
import json
from construct import S


# plotting
class Plotter(object):

    def __init__(self, data, name, graph):
        self.data = data
        self.name = name
        self.graph = graph

    def plot(self):
        data = self.data
        deg_data = [[data['degs']['in'], data['degs']['out']],
                    [data['degs']['ccdf_in'], data['degs']['ccdf_out']]]
        self.__degdist(deg_data)
        G_cen = data['centrality']
        C_cen = data['C']['centrality']
        self.__cendist(G_cen, C_cen)
        rs, ds, es, pr, ps = self.data['attack']
        self.__attack(rs, ds, es, pr, ps)

    def __cendist(self, G_cen, C_cen):
        fig, axes = plt.subplots(5, 1, figsize=(8, 14))
        fig.suptitle(f'{self.name} cen. dist.')
        for idx, key in enumerate(G_cen.keys()):
            axes[idx].loglog(G_cen[key][0], G_cen[key][1], 'ro')
            axes[idx].loglog(C_cen[key][0], C_cen[key][1], 'bo')
        plt.show()

    def __attack(self, rs, ds, es, pr, ps):
        plt.plot(ps, rs, 'b', label='random')
        plt.plot(ps, ds, 'r', label='degree')
        plt.plot(ps, es, 'g', label='eigenv')
        plt.plot(ps, pr, 'y', label='pagerank')
        plt.xlabel('fraction attacked'); plt.ylabel('frac. of nodes in largest comp.')
        plt.legend(); plt.title(f"attack plot of {self.name}")
        plt.show()


    def __degdist(self, data):
        kinds = ['loglog', 'loglog']; color = ['ro', 'bo']
        fig, axes = plt.subplots(2, 2, figsize=(14, 8))
        fig.suptitle(f'{self.name} deg. dist.')
        for idx in range(len(axes)):
            focus = data[idx]
            for jdx in range(len(axes[idx])):
                x, y = focus[jdx]
                exec(f"axes[idx][jdx].{kinds[idx]}(x, y, '{color[jdx]}')")
        plt.show()


def main():
    dumps = [f"../data/dumps/{target}" for target in os.listdir('../data/dumps/')]
    for i in range(len(dumps)):
        with open(dumps[i], 'r') as data_file:
            name = dumps[i].split('/')[-1].split('.')[0]
            data = json.load(data_file)
            graph = S[i]
            plot = Plotter(data, name, graph)
            plt.plot()


if __name__ == "__main__":
    main()
