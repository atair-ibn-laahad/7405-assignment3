from scipy.stats import norm
import numpy as np

""" arithmetic Asian call/put options """

# Asian option variable
S = 100  # Current stock price
sigma = 0.2  # Volatility
r = 0.05  # Risk-free rate
T = 3  # Time to maturity
K = 90  # Strike price
N = 252  # Number of time steps
option_type = 'call'
M = 10000  # Number of simulations
mc_method = 'geometric'


def geometric(S, sigma, r, T, K, N, option_type):
    # Calculate constants for the geometric Asian option
    sigma_C = sigma * np.sqrt((N + 1) * (2 * N + 1) / (6 * N ** 2))
    u = (r - 0.5 * sigma ** 2) * (N + 1) / (2 * N) + 0.5 * sigma_C ** 2
    d1 = (np.log(S / K) + (u + 0.5 * sigma_C ** 2) * T) / (sigma_C * np.sqrt(T))
    d2 = d1 - sigma_C * np.sqrt(T)

    # Calculate geometric Asian call/put option price
    if option_type == 'call':
        geo = np.exp(-r * T) * (S * np.exp(u * T) * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == 'put':
        geo = np.exp(-r * T) * (K * norm.cdf(-d2) - S * np.exp(u * T) * norm.cdf(-d1))
    else:
        raise ValueError('Unable to identify options type')
    print(f"Geometric Asian option:{geo}")
    return geo


def arithmetic(S, sigma, r, T, K, N, option_type, M, mc_method):
    delta = T / N  # Time step size
    geo = geometric(S, sigma, r, T, K, N, option_type)
    # Initialize payoff arrays
    arithPayoff = np.zeros(M)
    geoPayoff = np.zeros(M)
    # Monte Carlo simulation
    np.random.seed(1000)  # set seed
    for i in range(M):
        growthFactors = np.exp((r - 0.5 * sigma ** 2) * delta + sigma * np.sqrt(delta) * np.random.randn(N))
        Spath = S * np.cumprod(growthFactors)

        # Arithmetic mean
        arithMean = np.mean(Spath)
        arithPayoff[i] = np.exp(-r * T) * max(arithMean - K, 0)

        # Geometric mean
        geoMean = np.exp(np.sum(np.log(Spath)) / N)
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
    print(f"Arithmetic Asian option:{ari}")
    return ari


if __name__ == "__main__":
    arithmetic(S, sigma, r, T, K, N, option_type, M, mc_method)
