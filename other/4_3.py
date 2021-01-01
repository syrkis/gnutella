import networkx as nx
from matplotlib import pyplot as plt
import powerlaw
from collections import Counter
from tqdm import tqdm
import random
import warnings
warnings.filterwarnings("ignore")

n = 10 ** 4
alphas = [2.2, 2.5, 3.0]
_2_2, _2_5, _3_0 = [], [], []

def run():
    for i in range(len(alphas)):
        degrees = nx.utils.powerlaw_sequence(n, alphas[i])
        degrees = [int(d) for d in degrees]
        if sum(degrees) % 2 != 0:
            degrees[-1] += random.choice([1, -1])
        G = nx.configuration_model(degrees)
        G = nx.Graph(G)
        fit = powerlaw.Fit(list(dict(G.degree()).values()), verbose=False)
        if i % 3 == 0:
            _2_2.append(fit.alpha)
        elif i % 3 == 1:
            _2_5.append(fit.alpha)
        else:
            _3_0.append(fit.alpha)

for i in tqdm(range(10)):
    run()

plt.plot(_2_2, label='gamma 2.2')
plt.plot(_2_5, label='gamma 2.5')
plt.plot(_3_0, label='gamma 3.0')
plt.legend()
plt.title('fitted seeded gamma v. fitted gamma')
plt.ylabel(r'$\gamma$')
plt.xlabel('run number')
plt.show()
