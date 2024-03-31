import numpy as np


def binomial_tree_american_option(s_0: float, sigma: float, r: float, T: float, K: float, N: int, option_type: str):
    """
    Calculate the price of an American option using the binomial tree method.

    :param s_0: spot price of asset S(0)
    :param sigma: volatility
    :param r: risk-free interest rate
    :param T: time to maturity in years
    :param K: strike price
    :param N: number of steps
    :param option_type: call or put
    :return:
    """
    # length of time step
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    # Risk-neutral probability
    p = (np.exp(r * dt) - d) / (u - d)

    # Function to calculate the option value at a node
    def option_value_at_node(s, k, option_type):
        if option_type == "call":
            return max(s - k, 0)
        else:  # put
            return max(k - s, 0)

    # Use a 2D array to simulate the binomial tree
    # Initializing asset price at maturity
    asset_prices = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        # a quite tricky way to get the correct number of elements in each row, it will generate the s * u and s * d
        asset_prices[i, :i + 1] = s_0 * (u ** np.arange(i, -1, -1)) * (d ** np.arange(0, i + 1))

    # Initialize option values at maturity
    option_values = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        option_values[N, i] = option_value_at_node(asset_prices[N, i], K, option_type)

    # Iterate backwards to get option value at the initial node
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            hold_value = np.exp(-r * dt) * (p * option_values[j + 1, i + 1] + (1 - p) * option_values[j + 1, i])  # the f
            exercise_value = option_value_at_node(asset_prices[j, i], K, option_type)
            option_values[j, i] = max(hold_value, exercise_value)

    return option_values[0, 0]


if __name__ == '__main__':
    S0 = 100
    sigma = 0.2
    r = 0.05
    T = 3
    K = 90
    N = 252
    option_type = 'call'
    print(binomial_tree_american_option(S0, sigma, r, T, K, N, option_type))
