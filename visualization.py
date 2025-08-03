import matplotlib.pyplot as plt

def plot_results(df, ticker, option_type):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price", color="tab:blue")
    ax1.plot(df.index, df["stock_price"], color="tab:blue", label="Stock Price")
    ax1.tick_params(axis='y', labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Option Price", color="tab:red")
    ax2.plot(df.index, df["option_price"], color="tab:red", label=f"{option_type.title()} Option Price")
    ax2.tick_params(axis='y', labelcolor="tab:red")

    fig.tight_layout()
    plt.title(f"{ticker} - Stock vs {option_type.title()} Option Price")
    plt.show(block=True)
    input("Press Enter to exit...")

def plot_results_with_pnl(df, ticker, option_type, position_type):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Stock Price", color="tab:blue")
    ax1.plot(df.index, df["stock_price"], color="tab:blue", label="Stock Price")
    ax1.tick_params(axis='y', labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("PnL ($)", color="tab:green")
    pnl = df["pnl"]

    ax2.fill_between(df.index, pnl, 0, where=(pnl >= 0), color="green", alpha=0.3, label="Profit")
    ax2.fill_between(df.index, pnl, 0, where=(pnl < 0), color="red", alpha=0.3, label="Loss")
    ax2.plot(df.index, pnl, color="black", linewidth=2, label="PnL")
    ax2.axhline(0, color="gray", linestyle="--", linewidth=1)

    plt.title(f"{ticker} - {option_type.title()} ({position_type}) PnL Simulation")
    fig.tight_layout()
    plt.legend(loc="upper left")
    plt.show(block=True)
    input("Press Enter to exit...")
