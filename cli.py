import argparse
from config import (DEFAULT_TICKER, DEFAULT_OPTION_TYPE, DEFAULT_STRIKE_PRICE, DEFAULT_START_DATE, DEFAULT_END_DATE)

def parse_args():
    parser = argparse.ArgumentParser(description="Black-Scholes-Merton Model Option Pricing Backtester")
    parser.add_argument("--ticker", type=str, default=DEFAULT_TICKER, help="Stock ticker symbol")
    parser.add_argument("--option_type", type=str, choices=["call", "put"], default=DEFAULT_OPTION_TYPE, help="Calls or Puts Option")
    parser.add_argument("--strike", type=float, default=DEFAULT_STRIKE_PRICE, help="Strike price")
    parser.add_argument("--start", type=str, default=DEFAULT_START_DATE, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default=DEFAULT_END_DATE, help="End date (YYYY-MM-DD)")
    parser.add_argument("--r", type=float, default=None, help="Risk-free rate (annualized)")
    parser.add_argument("--sigma", type=float, default=None, help="Volatility (annualized)")
    parser.add_argument("--expiry_days", type=int, default=None, help="Time to expiry in days") #will convert to years in main 
    parser.add_argument("--position", type=str, choices=["long", "short"], default="long", help="Long or short option position")
    parser.add_argument("--contracts", type=int, default=1, help="Number of option contracts (1 contract = 100 shares)")
    parser.add_argument("--execution_date", type=str, default=None,help="Date when option position is opened (YYYY-MM-DD)")
    return parser.parse_args()
