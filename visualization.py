import matplotlib.pyplot as plt
import numpy as np

def plot_results(df, ticker, option_type):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    ax1.set_ylabel("Stock Price", color="tab:blue")
    ax1.plot(df.index, df["stock_price"], color="tab:blue", label="Stock Price", linewidth=2)
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left")

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Option Price", color="tab:red")
    
    # Check if option prices are very small and scale accordingly
    option_prices = df["option_price"]
    if option_prices.max() < 0.01:  # If all option prices are < 1 cent
        ax2.plot(df.index, option_prices * 100, color="tab:red", label=f"{option_type.title()} Option Price (cents)", linewidth=2)
        ax2.set_ylabel("Option Price (cents)", color="tab:red")
    else:
        ax2.plot(df.index, option_prices, color="tab:red", label=f"{option_type.title()} Option Price", linewidth=2)
    
    ax2.tick_params(axis='y', labelcolor="tab:red")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left")

    fig.tight_layout()
    plt.title(f"{ticker} - Stock vs {option_type.title()} Option Price")
    plt.show(block=True)

def plot_results_with_pnl(df, ticker, option_type, position_type):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

    ax1.set_ylabel("Stock Price", color="tab:blue")
    ax1.plot(df.index, df["stock_price"], color="tab:blue", label="Stock Price", linewidth=2)
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left")

    ax2.set_ylabel("Option Price", color="tab:red")
    
    option_prices = df["option_price"]
    if option_prices.max() < 0.01:
        ax2.plot(df.index, option_prices * 100, color="tab:red", label=f"{option_type.title()} Option Price (cents)", linewidth=2)
        ax2.set_ylabel("Option Price (cents)", color="tab:red")
    else:
        ax2.plot(df.index, option_prices, color="tab:red", label=f"{option_type.title()} Option Price", linewidth=2)
    
    ax2.tick_params(axis='y', labelcolor="tab:red")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left")

    # Plot 3: PnL
    ax3.set_xlabel("Date")
    ax3.set_ylabel("PnL ($)", color="tab:green")
    pnl = df["pnl"].dropna()
    
    if len(pnl) > 0:
        ax3.fill_between(pnl.index, pnl, 0, where=(pnl >= 0), color="green", alpha=0.3, label="Profit")
        ax3.fill_between(pnl.index, pnl, 0, where=(pnl < 0), color="red", alpha=0.3, label="Loss")
        ax3.plot(pnl.index, pnl, color="black", linewidth=2, label="PnL")
        ax3.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax3.grid(True, alpha=0.3)
        ax3.legend(loc="upper left")

    plt.suptitle(f"{ticker} - {option_type.title()} ({position_type}) - Comprehensive Analysis")
    fig.tight_layout()
    plt.show(block=True)