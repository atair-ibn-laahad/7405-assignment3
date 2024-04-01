# Implied volatility calculation
import numpy as np
from scipy.stats import norm

from tasks.black_scholes_european import black_scholes_european_options


def implied_volatility(s_0: float, r: float, q: float, T: float, K: float, option_premium: float, option_type: str, max_iter: int=500):
    """
    Calculate implied volatility for European call/put options using Black-Scholes formulas.

    :param s_0: spot price of asset S(0)
    :param r: risk-free interest rate
    :param q: repo rate
    :param T: time to maturity in years
    :param K: strike price
    :param option_premium: call/put option premium (price)
    :param option_type: call or put
    :return: implied volatility
    """

    sigma = np.sqrt(2 * (np.abs((np.log(s_0 / K) + (r - q) * T) / T)))
    for _ in range(max_iter):
        est_price = black_scholes_european_options(s_0, sigma, r, q, T, K, option_type)
        d1 = (np.log(s_0 / K) + (r - q) * T) / (sigma * np.sqrt(T)) + 0.5 * sigma * np.sqrt(T)
        vega = s_0 * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)

        # avoid division by zero
        if vega < 1e-10:
            return np.nan

        diff = est_price - option_premium

        # within tolerance
        if np.abs(diff) < 1e-10:
            return sigma
        sigma -= diff / vega

    return np.nan
