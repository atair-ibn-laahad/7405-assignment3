# Implement Black-Scholes Formulas for European call / put options
import math
from scipy.stats import norm


def black_scholes_european_options(s_0: float, sigma: float, r: float, q: float, T: float, K: float, option_type: str):
    """
    Implement Black-Scholes Formulas for European call/put options.

    :param s_0: spot price of asset S(0)
    :param sigma: volatility
    :param r: risk-free interest rate
    :param q: repo rate
    :param T: time to maturity in years
    :param K: strike price
    :param option_type: call or put
    :return:
    """

    d1 = (math.log(s_0 / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        return s_0 * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * math.exp(-r * T) * norm.cdf(-d2) - s_0 * math.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError('Invalid option_type')