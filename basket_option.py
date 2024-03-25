from scipy.stats import norm
import numpy as np

""" arithmetic mean basket call/put options """

# basket option variable
r = 0.05  # Risk-free rate
T = 3  # Time to maturity
M = 10000  # Number of simulations
N = 50  # Number of time steps
S1 = 100
S2 = 100
K = 90
sigma1 = 0.3
sigma2 = 0.3
p = 0.5
option_type = 'call'
mc_method = 'geometric'


def geometricc(S1, S2, sigma1, sigma2, r, T, K, p, option_type):
    # Calculate constants for the geometric Asian option

    sigma_Bg = np.sqrt(sigma1 ** 2 + sigma2 ** 2 + 2 * sigma1 * sigma2 * p) / 2
    u_Bg = r - (sigma1 ** 2 + sigma2 ** 2) / 4 + sigma_Bg ** 2 / 2
    Bg0 = np.sqrt(S1 * S2)
    d1 = (np.log(Bg0 / K) + (u_Bg + sigma_Bg ** 2 / 2) * T) / sigma_Bg * np.sqrt(T)
    d2 = d1 - sigma_Bg * np.sqrt(T)

    # Calculate geometric mean basket call/put option price
    if option_type == 'call':
        geo = np.exp(-r * T) * (Bg0 * np.exp(u_Bg * T) * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == 'put':
        geo = np.exp(-r * T) * (K * norm.cdf(-d2) - Bg0 * np.exp(u_Bg * T) * norm.cdf(-d1))
    else:
        raise ValueError('Unable to identify options type')
    print(f"Geometric basket option:{geo}")
    return geo


def arithmetic(S1, S2, K, sigma1, sigma2, p, option_type, M, mc_method):
    delta = T / N
    geo = geometricc(S1, S2, sigma1, sigma2, r, T, K, p, option_type)
    # Initialize payoff arrays
    arithPayoff = np.zeros(M)
    geoPayoff = np.zeros(M)

    # Monte Carlo simulation
    np.random.seed(1000)  # set seed
    for i in range(M):
        growthFactors1 = np.exp((r - 0.5 * sigma1 ** 2) * delta + sigma1 * np.sqrt(delta) * np.random.randn(N))
        growthFactors2 = np.exp((r - 0.5 * sigma2 ** 2) * delta + sigma2 * np.sqrt(delta) * np.random.randn(N))
        Spath1 = S1 * np.cumprod(growthFactors1)
        Spath2 = S2 * np.cumprod(growthFactors2)

        # Arithmetic mean
        arithMean = np.mean((Spath1 + Spath2) / 2, axis=0)
        arithPayoff[i] = np.exp(-r * T) * max(arithMean - K, 0)

        # Geometric mean
        geoMean = np.exp(np.sum(np.log(Spath1 * Spath2)) / (2 * N))
        geoPayoff[i] = np.exp(-r * T) * max(geoMean - K, 0)

    # Standard Monte Carlo
    Pmean = np.mean(arithPayoff)
    Pstd = np.std(arithPayoff)

    # Control Variate
    covXY = np.mean(arithPayoff * geoPayoff) - np.mean(arithPayoff) * np.mean(geoPayoff)
    theta = covXY / np.var(geoPayoff)

    # Control variate version
    Z = arithPayoff + theta * (geo - geoPayoff)
    Zmean = np.mean(Z)
    Zstd = np.std(Z)
    if mc_method == 'None':
        ari = [Pmean - 1.96 * Pstd / np.sqrt(M), Pmean + 1.96 * Pstd / np.sqrt(M)]
    elif mc_method == 'geometric':
        ari = [Zmean - 1.96 * Zstd / np.sqrt(M), Zmean + 1.96 * Zstd / np.sqrt(M)]
    else:
        raise ValueError('Unable to identify Monte Carlo method')
    print(f"Geometric basket option:{ari}")
    return ari


if __name__ == "__main__":
    arithmetic(S1, S2, K, sigma1, sigma2, p, option_type, M, mc_method)
