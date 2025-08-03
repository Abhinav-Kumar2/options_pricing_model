from cli import parse_args
from config import (DEFAULT_RISK_FREE_RATE, DEFAULT_VOLATILITY, DEFAULT_TIME_TO_EXPIRY)
from data_logging import setup_logger
from data_handling import load_data
from visualization import plot_results_with_pnl, plot_results
from backtesting.backtester import run_backtest_with_pnl

def main():
    args = parse_args()
    logger = setup_logger("OptionsBacktest")

    r = args.r if args.r is not None else DEFAULT_RISK_FREE_RATE
    sigma = args.sigma if args.sigma is not None else DEFAULT_VOLATILITY
    T = (args.expiry_days / 365) if args.expiry_days else DEFAULT_TIME_TO_EXPIRY

    logger.info(f"Loading data for {args.ticker} from {args.start} to {args.end}...")
    data = load_data(args.ticker, start=args.start, end=args.end)
    logger.info("Running backtest with PnL tracking...")
    results = run_backtest_with_pnl(data, args.option_type, args.strike, T, r, sigma, logger, position_type=args.position, contracts=args.contracts, execution_date=args.execution_date)
    results.to_csv("backtest_pnl_results.csv")
    logger.info("Results saved to backtest_pnl_results.csv")

    if results["pnl"].notna().any():
        logger.info("Plotting PnL chart...")
        plot_results_with_pnl(results, args.ticker, args.option_type, args.position)
    else:
        logger.warning("No PnL calculated — plotting stock & option prices instead.")
        plot_results(results, args.ticker, args.option_type)

if __name__ == "__main__":
    main()
