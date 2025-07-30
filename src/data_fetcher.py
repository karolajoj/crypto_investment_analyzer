from typing import Optional
from datetime import datetime, timedelta, UTC
from zoneinfo import ZoneInfo
import pandas as pd
from binance.client import Client


class BinanceDataFetcher:
    """Fetch historical data from Binance API with timezone awareness and second-level precision."""

    def __init__(self) -> None:
        self.client = Client()

    def fetch_klines(
        self,
        symbol: str,
        timeframe: str,
        start_date: str,
        end_date: Optional[str] = None,
        lookback: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch historical klines from Binance API with precise timestamps.

        Args:
            symbol (str): Trading pair (e.g., 'ETHUSDT', 'BTCUSDT', 'XRPUSDT', 'BNBUSDT', 'SOLUSDT').
            timeframe (str): Interval (e.g., '1m', '5m', '15m', '30m', '1h', '4h', '1d').
            start_date (str): Start date in DD.MM.YYYY HH:MM:SS or DD.MM.YYYY format (Warsaw time; defaults to 00:00:00 if no time).
            end_date (Optional[str]): End date in DD.MM.YYYY HH:MM:SS or DD.MM.YYYY format (Warsaw time; defaults to 23:59:59 if no time, or current time if None).
            lookback (Optional[str]): Lookback period (e.g., '30d', '12h', '60m'); if None, uses start_date as-is.

        Returns:
            pd.DataFrame: Historical data with columns: open_time, open, high, low, close, volume.

        Raises:
            ValueError: If date or lookback format is invalid.
            RuntimeError: If API call fails.
        """
        try:
            # Convert timeframe to Binance format
            timeframe_map = {
                "1m": Client.KLINE_INTERVAL_1MINUTE,
                "5m": Client.KLINE_INTERVAL_5MINUTE,
                "15m": Client.KLINE_INTERVAL_15MINUTE,
                "30m": Client.KLINE_INTERVAL_30MINUTE,
                "1h": Client.KLINE_INTERVAL_1HOUR,
                "4h": Client.KLINE_INTERVAL_4HOUR,
                "1d": Client.KLINE_INTERVAL_1DAY,
            }
            if timeframe not in timeframe_map:
                raise ValueError(f"Unsupported timeframe: {timeframe}")

            # Parse start_date with fallback to 00:00:00 if no time provided
            warsaw_tz = ZoneInfo("Europe/Warsaw")
            try:
                start_dt = datetime.strptime(start_date, "%d.%m.%Y %H:%M:%S").replace(tzinfo=warsaw_tz)
            except ValueError:
                start_dt = datetime.strptime(start_date, "%d.%m.%Y").replace(hour=0, minute=0, second=0, tzinfo=warsaw_tz)

            # Parse lookback if provided
            if lookback:
                units = int(lookback[:-1])
                unit_type = lookback[-1].lower()
                if unit_type == "d":
                    delta = timedelta(days=units)
                elif unit_type == "h":
                    delta = timedelta(hours=units)
                elif unit_type == "m":
                    delta = timedelta(minutes=units)
                else:
                    raise ValueError("Lookback must end with 'd', 'h', or 'm'.")
                start_dt -= delta

            # Set end_date with fallback to 23:59:59 if no time, or current time if None
            if end_date:
                try:
                    end_dt = datetime.strptime(end_date, "%d.%m.%Y %H:%M:%S").replace(tzinfo=warsaw_tz)
                except ValueError:
                    end_dt = datetime.strptime(end_date, "%d.%m.%Y").replace(hour=23, minute=59, second=59, tzinfo=warsaw_tz)
            else:
                end_dt = datetime.now(warsaw_tz)

            # Convert to UTC for API call
            start_utc = start_dt.astimezone(UTC)
            end_utc = end_dt.astimezone(UTC)

            klines = self.client.get_historical_klines(
                symbol=symbol,
                interval=timeframe_map[timeframe],
                start_str=start_utc.strftime("%Y-%m-%d %H:%M:%S"),
                end_str=end_utc.strftime("%Y-%m-%d %H:%M:%S"),
            )

            # Convert to DataFrame with correct timezone adjustment
            df = pd.DataFrame(
                klines,
                columns=[
                    "open_time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "quote_asset_volume",
                    "num_trades",
                    "taker_buy_base_volume",
                    "taker_buy_quote_volume",
                    "ignore",
                ],
            )
            df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_convert(warsaw_tz)
            df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
            return df[["open_time", "open", "high", "low", "close", "volume"]]

        except ValueError as ve:
            raise ValueError(f"Invalid input: {ve}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch klines: {e}")
