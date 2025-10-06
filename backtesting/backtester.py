import pandas as pd
from pricing.black_scholes import black_scholes_price
from pricing.binomial_options import binomial_price
from pricing.trinomial_options import trinomial_price
from pricing.monte_carlo import monte_carlo_price  

def run_backtest_with_pnl(data,option_type,strike,T,r,sigma,logger,position_type="long",contracts=1,execution_date=None,pricing_model="black_scholes",steps=200,american=False,simulations=100000):

    results = [] #will store simulation results before dataframe is made
    execution_price = None 
    execution_found = False #flag to check if execution date is found in data

    if execution_date: #checking if execution data is within the data range
        execution_datatime = pd.to_datetime(execution_date)
        if execution_datatime < data.index.min() or execution_datatime > data.index.max():
            logger.warning(f"Execution date {execution_date} is outside the data range. " f"Therefore, No PnL will be calculated.")
            execution_date = None

    initial_date = data.index[0]     # Store initial date for time decay calculation
    
    for date, row in data.iterrows(): 
        if hasattr(row["Close"], "iloc"): #for handling case of data being a series
            S = float(row["Close"].iloc[0])
        else:
            S = float(row["Close"])

        # Calculate time decay
        days_passed = (date - initial_date).days
        remaining_T = max(0, T - days_passed/365.0)

        try:
            if pricing_model == "black_scholes":
                option_price, _ = black_scholes_price(S=S,K=strike,T=remaining_T,r=r,sigma=sigma,option_type=option_type)
            elif pricing_model == "binomial":
                option_price, _ = binomial_price(S=S, K=strike,T=remaining_T,r=r,sigma=sigma,steps=steps,option_type=option_type,american=american)
            elif pricing_model == "trinomial":
                option_price, _ = trinomial_price(S=S,K=strike,T=remaining_T,r=r,sigma=sigma,option_type=option_type,steps=steps,american=american)
            elif pricing_model == "monte_carlo":
                option_price, _ = monte_carlo_price(S=S,K=strike,T=remaining_T,r=r,sigma=sigma,option_type=option_type,simulations=simulations,american=american,
                    steps=min(steps, 252)  # Use steps for LSM time steps
                )
            else:
                logger.error(f"Unsupported pricing model: {pricing_model}")
                continue
        except Exception as e:
            logger.error(f"Error pricing option on {date}: {e}")
            option_price = 0.0

        pnl = None

        if execution_date: #checking if we should start calculating PnL
            if date >= pd.to_datetime(execution_date):
                if not execution_found: #to prevent it starting from entry date multiple times (for first day of trade)
                    execution_price = option_price
                    execution_found = True
                if position_type == "long":
                    pnl = (option_price - execution_price) * contracts * 100
                else:
                    pnl = (execution_price - option_price) * contracts * 100

        results.append({"date": date, "stock_price": S, "option_price": option_price, "pnl": pnl})

    dataframe = pd.DataFrame(results).set_index("date")
    logger.info("Backtest with PnL completed. Sample results:\n%s", dataframe.head())
    return dataframe