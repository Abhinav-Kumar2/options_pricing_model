# Options Pricing Model + PnL Simulator (Black-Scholes-Merton Model)

A Python-based backtesting tool for options trading strategies, powered by the **Black-Scholes-Merton pricing model**.  
It allows you to simulate the price of call and put options, track **profit & loss (PnL)**, and visualize results with dynamic plots.

## Introduction
This project fetches historical stock price data from **Yahoo Finance**, calculates option prices using the **Black-Scholes-Merton model**, and simulates PnL for long/short option positions.  
It’s perfect for **quantitative traders**, **options enthusiasts**, or anyone exploring systematic options strategy testing.


## Features
- **Black-Scholes option pricing** for calls and puts
- **PnL tracking** for long or short option positions
- **Execution date simulation** to start PnL from a specific point
- **Historical data loading** via `yfinance`
- **Interactive visualizations** for:
  - Stock vs. Option prices
  - Profit & Loss charts
- **Command-line interface** for easy configuration

## Installation
```bash
# Clone this repository
git clone https://github.com/Abhinav-Kumar2/options_pricing_model.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate 

# Install dependencies
pip install -r libraries.txt
```

## Usage & Example
You can run the backtest directly from the command line.  
Example 1 — Long Call:
python main.py --ticker AAPL --option_type call --strike 105 \
    --start 2023-01-01 --end 2024-01-01 \
    --expiry_days 30 --position long --contracts 2 \
    --execution_date 2023-06-15

## Plots
![alt text](<Screenshot 2025-08-03 231922.png>)

![alt text](<Screenshot 2025-08-03 232024.png>)

```bash
##Project Structure
├── backtesting/
│   ├── backtester.py          # Core PnL simulation logic
├── pricing/
│   ├── black_scholes.py       # Black-Scholes pricing function
├── cli.py                     # CLI argument parser
├── config.py                  # Default settings
├── data_handling.py           # Yahoo Finance data loader
├── data_logging.py            # Logger setup
├── main.py                    # Entry point for running backtests
├── visualization.py           # Plotting functions
├── libraries.txt           # Dependencies list
└── README.md                 

```
## License
MIT

