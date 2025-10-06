import yfinance as yf
import pandas as pd

def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, auto_adjust=True)
    if data.empty:
        raise ValueError(f"No data found for ticker {ticker} between {start} and {end}")
    
    print(f"Data columns: {data.columns.tolist()}")
    print(f"Data shape: {data.shape}")
    
    if isinstance(data.columns, pd.MultiIndex):
        print("MultiIndex columns detected - flattening...")
        data.columns = data.columns.get_level_values(0)
        print(f"Flattened columns: {data.columns.tolist()}")

    close_column = None
    for col in data.columns:
        col_str = str(col)
        if 'close' in col_str.lower():
            close_column = col
            break
    
    if close_column is None:
        close_column = data.columns[0]
        print(f"No 'Close' column found. Using '{close_column}' instead.")
    else:
        print(f"Using column '{close_column}' for closing prices.")
    
    # Rename the close column to 'Close' for consistency
    data = data.rename(columns={close_column: 'Close'})
    
    return data