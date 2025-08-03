import math
from scipy.stats import norm #for normal distribution

def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    N_minus_d1 = norm.cdf(-d1)
    N_minus_d2 = norm.cdf(-d2)

    if option_type.lower() == "call":
        price = S * N_d1 - K * math.exp(-r * T) * N_d2
    elif option_type.lower() == "put":
        price = K * math.exp(-r * T) * N_minus_d2 - S * N_minus_d1

    note = {"d1": d1, "d2": d2, "N(d1)": N_d1, "N(d2)": N_d2, "N(-d1)": N_minus_d1, "N(-d2)": N_minus_d2}

    return price, note
