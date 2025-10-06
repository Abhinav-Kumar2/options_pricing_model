import numpy as np
import math

def monte_carlo_price(S, K, T, r, sigma, option_type="call", simulations=100000, american=False, steps=252):
    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    option_type = option_type.lower()
    
    if T <= 0:
        if option_type == "call":
            return max(0.0, S - K), {"ex": True}
        else:
            return max(0.0, K - S), {"ex": True}

    if not american:
        Z = np.random.standard_normal(simulations)
        ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        
        if option_type == "call":
            payoffs = np.maximum(ST - K, 0.0)
        else:
            payoffs = np.maximum(K - ST, 0.0)
            
        price = np.exp(-r * T) * np.mean(payoffs)
        std_error = np.exp(-r * T) * np.std(payoffs) / np.sqrt(simulations)
        
        note = {
            "method": "Monte Carlo (European)",
            "simulations": simulations,
            "std_error": std_error,
            "min_payoff": np.min(payoffs),
            "max_payoff": np.max(payoffs)
        }
        
    else:
        # American option pricing using Least Squares Monte Carlo (LSM)
        dt = T / steps
        discount = np.exp(-r * dt)
        
        Z = np.random.standard_normal((steps, simulations))
        prices = np.zeros((steps + 1, simulations))
        prices[0] = S
        
        for t in range(1, steps + 1):
            prices[t] = prices[t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[t-1])
        
        cash_flows = np.zeros_like(prices)
        
        if option_type == "call":
            cash_flows[-1] = np.maximum(prices[-1] - K, 0.0)
        else:
            cash_flows[-1] = np.maximum(K - prices[-1], 0.0)
        
        # Backward induction for American exercise
        for t in range(steps - 1, 0, -1):
            if option_type == "call":
                in_the_money = prices[t] > K
                exercise_value = prices[t] - K
            else:
                in_the_money = prices[t] < K
                exercise_value = K - prices[t]
            
            itm_paths = np.where(in_the_money)[0]
            
            if len(itm_paths) > 0:
                X = prices[t, itm_paths]
                Y = cash_flows[t+1, itm_paths] * discount
                
                X_sq = X ** 2
                A = np.column_stack([np.ones_like(X), X, X_sq])
                coeffs = np.linalg.lstsq(A, Y, rcond=None)[0]
                continuation_value = A @ coeffs
                
                exercise_now = exercise_value[itm_paths] > continuation_value
                exercise_paths = itm_paths[exercise_now]
                
                cash_flows[t, exercise_paths] = exercise_value[exercise_paths]
                cash_flows[t+1:, exercise_paths] = 0
        
        price = np.mean(np.sum(cash_flows * discount ** np.arange(steps + 1).reshape(-1, 1), axis=0))
        
        note = {"method": "Monte Carlo (American LSM)","simulations": simulations,"steps": steps,"dt": dt,"exercise_ratio": np.mean(cash_flows[1:] > 0)}
    
    return price, note


def price(S, K, T, r, sigma, option_type="call", simulations=100000, american=False, steps=252):
    return monte_carlo_price(S, K, T, r, sigma, option_type, simulations, american, steps)