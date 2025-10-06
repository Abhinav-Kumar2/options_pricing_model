import math
import numpy as np

def trinomial_price(S, K, T, r, sigma, option_type="call", steps=200, american=False):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    option_type = option_type.lower()
    n = int(max(1, steps))

    if T <= 0:
        if option_type == "call":
            return max(0.0, S - K), {"ex": True}
        else:
            return max(0.0, K - S), {"ex": True}

    dt = T / n
    nu = r - 0.5 * sigma * sigma

    dx = sigma * math.sqrt(3 * dt)
    edx = math.exp(dx)
    emdx = math.exp(-dx)

    pu = 0.5 * ((sigma * sigma * dt + (nu * dt) ** 2) / (dx * dx) + (nu * dt) / dx)
    pd = 0.5 * ((sigma * sigma * dt + (nu * dt) ** 2) / (dx * dx) - (nu * dt) / dx)
    pm = 1.0 - pu - pd

    disc = math.exp(-r * dt)

    j = np.arange(-n, n + 1)
    ST = S * np.exp(j * dx)
    if option_type == "call":
        values = np.maximum(ST - K, 0.0)
    else:
        values = np.maximum(K - ST, 0.0)

    for step in range(n - 1, -1, -1):
        new_values = np.empty(2 * step + 1)
        for idx, j_idx in enumerate(range(-step, step + 1)):
            center = idx + 1 
            v_up = values[center + 1]
            v_mid = values[center]
            v_down = values[center - 1]
            new_values[idx] = disc * (pu * v_up + pm * v_mid + pd * v_down)
            
        if american:
            j_current = np.arange(-step, step + 1)
            S_now = S * np.exp(j_current * dx)
            if option_type == "call":
                exercise = np.maximum(S_now - K, 0.0)
            else:
                exercise = np.maximum(K - S_now, 0.0)
            new_values = np.maximum(new_values, exercise)
            
        values = new_values

    price = float(values[0])
    note = {"method": "Trinomial", "steps": n,"dt": dt,"dx": dx,"pu": pu,"pm": pm,"pd": pd,}
    return price, note

def price(S, K, T, r, sigma, option_type="call", steps=200, american=False):
    return trinomial_price(S, K, T, r, sigma, option_type=option_type, steps=steps, american=american)