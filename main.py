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
    
    initial_price = float(data['Close'].iloc[0])
    
    logger.info(f"Backtest Parameters:")
    logger.info(f"  Ticker: {args.ticker}")
    logger.info(f"  Option Type: {args.option_type}")
    logger.info(f"  Strike: {args.strike}")
    logger.info(f"  Initial Stock Price: {initial_price:.2f}")
    logger.info(f"  Risk-free Rate: {r:.3f}")
    logger.info(f"  Volatility: {sigma:.3f}")
    logger.info(f"  Time to Expiry: {T:.3f} years ({T*365:.1f} days)")
    logger.info(f"  Pricing Model: {args.pricing_model}")
    logger.info(f"  Steps: {args.steps}")
    logger.info(f"  American: {args.american}")
    logger.info(f"  Position: {args.position}")
    logger.info(f"  Contracts: {args.contracts}")
    logger.info(f"  Execution Date: {args.execution_date}")
    
    logger.info("Running backtest with PnL tracking...")
    results = run_backtest_with_pnl(data,args.option_type,args.strike,T,r,sigma,logger,position_type=args.position,contracts=args.contracts,execution_date=args.execution_date,pricing_model=args.pricing_model,steps=args.steps,american=args.american)
    results.to_csv("backtest_pnl_results.csv")
    logger.info("Results saved to backtest_pnl_results.csv")

    if results["pnl"].notna().any():
        logger.info("Plotting PnL chart...")
        plot_results_with_pnl(results, args.ticker, args.option_type, args.position)
    else:
        logger.warning("No PnL calculated — plotting stock & option prices instead.")
        plot_results(results, args.ticker, args.option_type)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()