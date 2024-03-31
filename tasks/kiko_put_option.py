import math
import numpy as np
import pandas as pd
from scipy.stats import norm, qmc

""" KIKO put options """

# KIKO option parameter
M = 2 ** 10
S = 100
sigma = 0.2
r = 0.05
T = 3
K = 90
L = 80
U = 125
N = 252
R = 1.5

def mc(S:float, sigma:float, r:float, T:float, K:float, L:float, U:float, N:int, R:float):
    # set the random seed
    seed = 1000
    np.random.seed(1000)
    # generate the paths of stock prices
    values = []
    sequencer = qmc.Sobol(d=N, seed=seed)
    # uniform samples
    X = np.array(sequencer.random(n=M))
    # standard normal samples
    Z = norm.ppf(X)
    # scaled samples
    delta = T/N
    growthFactors = (r - 0.5 * sigma * sigma) * delta + sigma * math.sqrt(delta) * Z
    growthFactors = pd.DataFrame(growthFactors)
    Spath = S * np.exp(growthFactors.cumsum(axis=1))

    # the simulated stock prices, M rows, N columns
    for ipath in Spath.index.to_list():
        ds_path_local = Spath.loc[ipath, :]
        price_max = ds_path_local.max()
        price_min = ds_path_local.min()
        if price_max >= U: # knock-out happened
            knockout_time = ds_path_local[ds_path_local >= U].index.to_list()[0]
            payoff = R * np.exp(-knockout_time * r * delta)
            values.append(payoff)
        elif price_min <= L: # knock-in happened
            final_price = ds_path_local.iloc[-1]
            payoff = np.exp(- r * T) * max(K - final_price, 0)
            values.append(payoff)
        else: # no knock-out, no knock-in
            values.append(0)

    Kmean = np.mean(values)
    Kstd = np.std(values)
    confkv = [Kmean - 1.96 * Kstd / np.sqrt(M), Kmean + 1.96 * Kstd / np.sqrt(M)]
    print(f"KIKO put option:{confkv}")
    return confkv

if __name__ == "__main__":
    mc(S, sigma, r, T, K, L, U, N, R)
