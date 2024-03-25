import asian_option
import basket_option
import kiko_put_option

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
asian_option.geometric(S, sigma, r, T, K, N, option_type)
asian_option.arithmetic(S, sigma, r, T, K, N, option_type, M, mc_method)


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
basket_option.geometricc(S1, S2, sigma1, sigma2, r, T, K, p, option_type)
basket_option.arithmetic(S1, S2, K, sigma1, sigma2, p, option_type, M, mc_method)


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
kiko_put_option.mc(S, sigma, r, T, K, L, U, N, R)