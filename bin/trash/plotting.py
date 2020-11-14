# plotting.py
#   various network analytical plotter functions
# by: Noah Syrkis

# imports
from matplotlib import pyplot as plt

#############
# functions #
#############


def scatter(data, meta):
    """
    takes in freq. plus meta data and outputs plot.
    data should be a dictionary.
    """

    # data prep
    x = [n / sum(list(data.keys())) for n in list(data.keys())]
    y = list(data.values())

    # linear plot
    plt.figure(figsize=(14,8))
    plt.plot(x, y, 'ob')
    plt.title(f"{meta['title']}, linear"); plt.xlabel(meta['xlab']); plt.ylabel(meta['ylab'])
    plt.savefig(f'../docs/plots/{meta["folder"]}/linear-{meta["file"]}')
    plt.close()

    # loglog plot
    plt.figure(figsize=(14,8))
    plt.loglog(x, y, 'ob')
    plt.title(f"{meta['title']}, loglog"); plt.xlabel(meta['xlab']); plt.ylabel(meta['ylab'])
    plt.savefig(f'../docs/plots/{meta["folder"]}/loglog-{meta["file"]}')
    plt.close()


def hister(data, meta):
    """
    takes in x and y lists, for value and freq.
    data should be list of lists.
    """
    plt.figure(figsize=(14,8))
    plt.bar(data[0], data[1])
    plt.title(meta['title']); plt.xlabel(meta['xlab']); plt.ylabel(meta['ylab'])
    plt.savefig(f'../docs/plots/{meta["folder"]}/{meta["file"]}')
    plt.close()

def ccdfer():
    pass


##########
# script #
##########


def main(): # save all plots
    pass


if __name__ == "__main__":
    main()
