# Closed-form formulas for geometric Asian call/put options and geometric basket call/put options.
import numpy as np
from scipy.stats import norm


def closed_form_geometric_asian_options(s_0: float, sigma: float, r: float, T: float, K: float, n: int, option_type: str):
    """
    Implement closed-form formulas for geometric Asian call/put options.
    Control variate for arithmetic asian option, LECTURE 5.

    :param s_0: spot price of asset S(0)
    :param sigma: volatility
    :param r: risk-free interest rate
    :param T: time to maturity in years
    :param K: strike price
    :param n: number of monitoring points
    :param option_type: call or put
    :return:
    """
    sigma_hat = sigma * np.sqrt((n + 1) * (2 * n + 1) / (6 * n ** 2))
    mu_hat = (r - 0.5 * sigma ** 2) * (n + 1) / (2 * n) + 0.5 * sigma_hat ** 2

    d1 = (np.log(s_0 / K) + (mu_hat + 0.5 * sigma_hat ** 2) * T) / (sigma_hat * np.sqrt(T))
    d2 = d1 - sigma_hat * np.sqrt(T)

    if option_type == 'call':
        return np.exp(-r * T) * (s_0 * np.exp(mu_hat * T) * norm.cdf(d1) - K * norm.cdf(d2))
    elif option_type == 'put':
        return np.exp(-r * T) * (K * norm.cdf(-d2) - s_0 * np.exp(mu_hat * T) * norm.cdf(-d1))
    else:
        raise ValueError('Invalid option_type')


def closed_form_geometric_basket_options(s_0: float, sigma: float, r: float, T: float, K: float, rho: float, option_type: str):
    # TODO: ?
    pass
