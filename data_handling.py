import yfinance as yf

def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, auto_adjust=True) #auto adjust to take dividends and splits in consideration
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker} between {start} and {end}")
    return data
