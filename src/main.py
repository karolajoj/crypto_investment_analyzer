import argparse
import sys
from typing import List
from data_fetcher import BinanceDataFetcher


def check_virtual_env() -> None:
    """Ensure the script runs in a virtual environment."""
    if not (hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)):
        print("ERROR: This script must run in a virtual environment.")
        print("Activate the virtual environment with: venv\\Scripts\\activate")
        sys.exit(1)


def parse_percentiles(percentiles_str: str) -> List[float]:
    """Parse comma-separated percentiles into a list of floats."""
    try:
        return [float(p) for p in percentiles_str.split(",")]
    except ValueError as e:
        print(f"ERROR: Invalid percentiles format. Use comma-separated numbers (e.g., 25,50,75). Error: {e}")
        sys.exit(1)


def main() -> None:
    """Main function to parse CLI arguments and fetch data."""
    check_virtual_env()
    fetcher = BinanceDataFetcher()

    parser = argparse.ArgumentParser(description="Cryptocurrency Investment Analyzer")
    parser.add_argument("--currency", type=str, default="ETH", help="Cryptocurrency code (e.g., ETH, BTC)")
    parser.add_argument("--timeframe", type=str, required=True, help="Timeframe (e.g., 1h, 1d)")
    parser.add_argument("--start-date", type=str, default="20.07.2025 00:00:00", help="Start date (DD.MM.YYYY HH:MM:SS, Warsaw time)")
    parser.add_argument("--end-date", type=str, default="25.07.2025 23:59:59", help="End date (DD.MM.YYYY HH:MM:SS, Warsaw time; defaults to today)")
    parser.add_argument("--lookback", type=str, default=None, nargs="?", help="Lookback period (e.g., 30d, 12h, 60m, or empty)")
    parser.add_argument("--percentiles", type=str, default="25,50,75", help="Comma-separated percentiles (e.g., 25,50,75)")

    args = parser.parse_args()

    try:
        data = fetcher.fetch_klines(
            symbol=f"{args.currency}USDT",
            timeframe=args.timeframe,
            start_date=args.start_date,
            end_date=args.end_date,
            lookback=args.lookback,
        )
        print(f"Fetched {len(data)} rows for {args.currency} ({args.timeframe}) from {args.start_date} to {args.end_date}")
        print(data.head())

    except Exception as e:
        print(f"Error fetching data for {args.currency}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
