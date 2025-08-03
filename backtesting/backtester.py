import pandas as pd
from pricing.black_scholes import black_scholes_price

def run_backtest_with_pnl(data,option_type,strike,T,r,sigma,logger,position_type="long",contracts=1,execution_date=None):

    results = [] #will store simulation results before dataframe is made
    execution_price = None 
    execution_found = False #flag to check if execution date is found in data


    if execution_date: #checking if execution data is within the data range
        execution_datatime = pd.to_datetime(execution_date)
        if execution_datatime < data.index.min() or execution_datatime > data.index.max():
            logger.warning(f"Execution date {execution_date} is outside the data range. " f"Therefore, No PnL will be calculated.")
            execution_date = None

    for date, row in data.iterrows(): 
        if hasattr(row["Close"], "iloc"): #for handling case of data being a series
            S = float(row["Close"].iloc[0])
        else:
            S = float(row["Close"])

        option_price, useless = black_scholes_price(S, strike, T, r, sigma, option_type)

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
