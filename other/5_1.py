import networkx as nx
import random 
import numpy as np
import pandas as pd
from tqdm import tqdm
import powerlaw
from matplotlib import pyplot as plt
import matplotlib; matplotlib.rcParams["figure.dpi"] = 100
import warnings

alphas = []
n = 10 ** 4
N = {i : [j for j in range(1, 5)] for i in range(1, 5)}
D = []

for node in tqdm(range(5, n + 1)):
    samples = [k for k in N.keys()]
    weights = [len(v) for v in N.values()]
    choices = random.choices(samples, weights, k=4)
    N[node] = choices
    for choice in choices:
        N[choice].append(node)
    if node in (10 ** 2, 10 ** 3, 10 ** 4):
        D.append([len(v) for v in N.values()])


# 5.1.1

for i in range(len(D)):
    df = pd.DataFrame(D[i])
    print(df.describe())

# 5.1.2

fig, axis = plt.subplots(1, 1, figsize=(16, 8))
warnings.filterwarnings("ignore")
colors = ['r', 'g', 'b'][::-1]
labels = ['10 ** 2', '10 ** 3', '10 ** 4']
for i in range(len(D)):
    # frq = [d / max(D[i]) for d in D[i]]
    frq = D[i]
    fit = powerlaw.Fit(frq, ax=axis, verbose=False)
    fit.plot_ccdf(ax=axis, marker='o', color=colors[i], label=f'{labels[i]}, alpha = {round(fit.alpha, 3)}')
    fit.power_law.plot_ccdf(ax=axis, linestyle='--', color=colors[i], label=f'{labels[i]}, alpha = {round(fit.alpha, 3)}')
    alphas.append(fit.alpha)
plt.title('Power law fitting to BA instances with $N = 10^{\{2, 3, 4\}}$')
plt.xlabel(r'$x$'); plt.ylabel(r'$P(k >= x)$'); plt.legend()
plt.show()

# 5.1.3
print(alphas) # alphas are all around 3, as expected
