import math
import numpy as np

def binomial_price(S, K, T, r, sigma, option_type="call", steps=200, american=False):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    option_type = option_type.lower()
    n = int(max(1, steps))

    # handle degenerate T==0
    if T <= 0:
        if option_type == "call":
            return max(0.0, S - K), {"ex": True}
        else:
            return max(0.0, K - S), {"ex": True}

    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-r * dt)
    p = (math.exp(r * dt) - d) / (u - d)  # risk-neutral probability

    # stock price at node i (i = number of up moves): S * u^i * d^(n-i)
    i = np.arange(0, n + 1)
    ST = S * (u ** i) * (d ** (n - i))
    if option_type == "call":
        values = np.maximum(ST - K, 0.0)
    else:
        values = np.maximum(K - ST, 0.0)

    # backward induction
    for step in range(n - 1, -1, -1):
        values = disc * (p * values[1:step + 2] + (1 - p) * values[0:step + 1])
        if american:
            # stock prices at current step
            i = np.arange(0, step + 1)
            S_now = S * (u ** i) * (d ** (step - i))
            if option_type == "call":
                exercise = np.maximum(S_now - K, 0.0)
            else:
                exercise = np.maximum(K - S_now, 0.0)
            values = np.maximum(values, exercise)  # early exercise check

    price = float(values[0])
    note = {"method": "CRR Binomial","steps": n,"dt": dt,"u": u,"d": d,"p": p,}
    return price, note

def price(S, K, T, r, sigma, option_type="call", steps=200, american=False):
    price_val, note = binomial_price(S, K, T, r, sigma, option_type=option_type, steps=steps, american=american)
    return price_val, note