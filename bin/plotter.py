# plotter.py
#   plots gnutella
# by: Noah Syrkis

# imports
import os
from matplotlib import pyplot as plt
import json
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from construct import S
import powerlaw
from tqdm import tqdm


# plotting
class Plotter(object):

    def __init__(self, data, name, graph):
        self.data = data
        self.name = name
        self.graph = graph
        self.theme = 'seaborn'

    def plot(self):
        data = self.data
        plt.style.use(self.theme)
        deg_data = [[data['degs']['in'], data['degs']['out']],
                    [data['degs']['ccdf_in'], data['degs']['ccdf_out']]]
        self.__degdist(deg_data)
        G_cen = data['centrality']
        C_cen = data['C']['centrality']
        self.__cendist(G_cen, C_cen)
        self.__attack(data)
        self.__fitting(data)

    def __fitting(self, data):
        _, y = data['degs']['in']
        y = np.array(y); mask = y >= 3
        fit = powerlaw.Fit(y[mask], verbose=False)
        fig = fit.plot_ccdf(label='CCDF', color='r', linestyle='--', marker='o')
        fit.lognormal.plot_ccdf(ax=fig, color='c', linestyle='--', label='log-normal fit')
        fit.power_law.plot_ccdf(ax=fig, color='g', linestyle='--', label='power-law fit')
        fit.exponential.plot_ccdf(ax=fig, color='b', linestyle='--', label='exponential fit')
        fit.truncated_power_law.plot_ccdf(ax=fig, color='k', linestyle='--', label='truncated power law fit')
        plt.legend(); plt.title(f"{self.name} fit"); plt.ylabel(r"$P(k>=x)$"); plt.xlabel(r'$x$')
        plt.savefig(f'../plots/{self.name}/fitting-{self.name}.png', dpi=300); plt.close()

    def __cendist(self, G_cen, C_cen):
        fig, axes = plt.subplots(5, 1, figsize=(8, 14))
        fig.suptitle(f'{self.name} cen. dist.')
        for idx, key in enumerate(G_cen.keys()):
            axes[idx].loglog(G_cen[key][0], G_cen[key][1], 'ro')
            axes[idx].loglog(C_cen[key][0], C_cen[key][1], 'bo')
            axes[idx].set_title(f"{key} plot")
        plt.savefig(f'../plots/{self.name}/centrality-{self.name}.png', dpi=300); plt.close()

    def __attack(self, data):
        kinds = ['random', 'degree', 'eigen', 'pagerank']; colors = 'brgy'
        G = data['attack']
        C = data['C']['attack']
        for i in range(len(G) - 1):
            exec(f"plt.plot(G[-1], G[i], colors[i], label='{kinds[i]}')")
            # exec(f"plt.plot(C[-1], C[i], colors[i], linestyle='--', label='conf. {kinds[i]}')")
        plt.xlabel('fraction attacked'); plt.ylabel('frac. of nodes in largest comp.')
        plt.legend(); plt.title(f"attack plot of {self.name}")
        plt.savefig(f'../plots/{self.name}/attack-{self.name}.png', dpi=300); plt.close()

    def __degdist(self, data):
        kinds = ['loglog', 'loglog']; color = ['ro', 'bo']
        titles = ['in degree', 'out degree']
        fig, axes = plt.subplots(2, 2, figsize=(14, 8))
        fig.suptitle(f'{self.name} deg. dist.')
        for idx in range(len(axes)):
            focus = data[idx]
            for jdx in range(len(axes[idx])):
                x, y = focus[jdx]
                exec(f"axes[idx][jdx].{kinds[idx]}(x[:-1], y[:-1], '{color[jdx]}')")
                axes[0][jdx].set_xlabel(r'$k$'); axes[0][jdx].set_ylabel(r'$P(k)$')
                axes[1][jdx].set_xlabel(r'$x$'); axes[1][jdx].set_ylabel(r'$P(k >= x)$')
                axes[0][jdx].set_title(titles[jdx])
        plt.savefig(f'../plots/{self.name}/degree-dist-{self.name}.png', dpi=300); plt.margins(y=40.0); plt.close()


def main():
    dumps = [f"../data/dumps/{target}" for target in sorted(os.listdir('../data/dumps/'))]
    for i in tqdm(range(len(dumps))):
        with open(dumps[i], 'r') as data_file:
            name = dumps[i].split('/')[-1].split('.')[0]
            data = json.load(data_file)
            graph = S[i]
            plot = Plotter(data, name, graph)
            plot.plot()


if __name__ == "__main__":
    main()
