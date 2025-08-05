from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo
import pytest
import pandas as pd
from unittest.mock import patch
from src.data_fetcher import BinanceDataFetcher
from tests.mock_data import MOCK_PIONEX_DATA_1D, MOCK_PIONEX_DATA_1H, MOCK_TRADING_VIEW_DATA_1D, MOCK_TRADING_VIEW_DATA_1H

warsaw_tz = ZoneInfo("Europe/Warsaw")

# TODO : Wydzielić te same dane wejściowe z fetch_klines np symbol, start, end, timeframe

@pytest.fixture
def fetcher() -> BinanceDataFetcher:
    """Fixture for BinanceDataFetcher."""
    return BinanceDataFetcher()

@pytest.mark.parametrize(
    "symbol, data_source",
    [(symbol, "pionex") for symbol in ["ETHUSDT", "BTCUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT"]] + [(symbol, "tradingview") for symbol in ["ETHUSDT", "BTCUSDT", "XRPUSDT", "BNBUSDT", "SOLUSDT"]],
)
def test_validate_percentage_difference(fetcher: BinanceDataFetcher, symbol: str, data_source: str) -> None:
    """Validate that no values from Binance API differ from mock data (Pionex or TradingView) by more than 0.15%."""
    mock_data = MOCK_PIONEX_DATA_1D[symbol] if data_source == "pionex" else MOCK_TRADING_VIEW_DATA_1D[symbol]
    df = fetcher.fetch_klines(symbol, "1d", "20.07.2025", end_date="22.07.2025")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_convert("Europe/Warsaw")
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].round(2)
    binance_data = df[["open_time", "open", "high", "low", "close"]].values.tolist()

    assert len(mock_data) == len(binance_data), f"Data length mismatch for {symbol}: {data_source}={len(mock_data)}, Binance={len(binance_data)}"

    for i in range(len(mock_data)):
        mock_row = mock_data[i]
        binance_row = binance_data[i]

        for j in range(1, 5):  # Skip open_time (index 0), compare fields 1-4 (open, high, low, close)
            mock_val = mock_row[j]
            binance_val = binance_row[j]
            diff = abs((mock_val - binance_val) / mock_val * 100)
            assert diff <= 0.15, f"Percentage difference exceeds 0.15% for {symbol} ({data_source}) at row {i}, column {j}: {diff:.2f}%"


@pytest.mark.parametrize("data_source", ["pionex", "tradingview"])
def test_validate_eth_1h_data(fetcher: BinanceDataFetcher, data_source: str) -> None:
    """Validate 1-hour ETHUSDT data from Binance API against 1-hour mock data (Pionex or TradingView) at 00:00, 01:00, 02:00 on 20.07.2025."""
    mock_data = MOCK_PIONEX_DATA_1H if data_source == "pionex" else MOCK_TRADING_VIEW_DATA_1H
    df = fetcher.fetch_klines("ETHUSDT", "1h", "20.07.2025 00:00:00", end_date="20.07.2025 02:00:00")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_convert("Europe/Warsaw")
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].round(2)
    binance_data = df[["open_time", "open", "high", "low", "close"]].values.tolist()

    assert len(binance_data) == 3, f"Expected 3 1h intervals (00:00, 01:00, 02:00), got {len(binance_data)}"
    assert len(mock_data) >= 3, f"Mock data {data_source} must have at least 3 entries, got {len(mock_data)}"

    target_indices = [0, 1, 2]  # Corresponding to 00:00, 01:00, 02:00
    for i, idx in enumerate(target_indices):
        mock_row = mock_data[idx]
        binance_row = binance_data[i]

        # Validate timestamp
        mock_time = mock_row[0]  # datetime object
        binance_time = binance_row[0]  # datetime object
        assert abs((mock_time - binance_time).total_seconds()) < 1, f"Timestamp mismatch for {data_source} at {mock_time.hour}:00: mock={mock_time}, binance={binance_time}"

        # Validate values with 0.15% tolerance
        for j in range(1, 5):  # Compare open, high, low, close
            mock_val = mock_row[j]
            binance_val = binance_row[j]
            diff = abs((mock_val - binance_val) / mock_val * 100)
            assert diff <= 0.15, f"Percentage difference exceeds 0.15% for {data_source} at {mock_time.hour}:00, column {j}: {diff:.2f}%"


def test_fetch_klines_invalid_date(fetcher: BinanceDataFetcher) -> None:
    """Test invalid date format."""
    with pytest.raises(ValueError, match="time data .* does not match format"):
        fetcher.fetch_klines("BTCUSDT", "1h", "invalid-date", "25.07.2025")


def test_fetch_klines_invalid_lookback(fetcher: BinanceDataFetcher) -> None:
    """Test invalid lookback format."""
    with pytest.raises(ValueError, match="Lookback must end with 'd', 'h', or 'm'"):
        fetcher.fetch_klines("BTCUSDT", "1h", "20.07.2025", lookback="30x")

def test_fetch_klines_api_error(fetcher: BinanceDataFetcher) -> None:
    """Test API error handling."""
    with patch.object(fetcher.client, "get_historical_klines", side_effect=Exception("API error")):
        with pytest.raises(RuntimeError, match="Failed to fetch klines: API error"):
            fetcher.fetch_klines("BTCUSDT", "1h", "20.07.2025", "25.07.2025")

def test_fetch_klines_unsupported_timeframe(fetcher: BinanceDataFetcher) -> None:
    """Test handling of unsupported timeframe."""
    with pytest.raises(ValueError, match="Unsupported timeframe: invalid"):
        fetcher.fetch_klines("BTCUSDT", "invalid", "20.07.2025", "25.07.2025")

# TODO : Zweryfikować wszystkie testy
# TODO : Zweryfikować testy i działanie lookback
@pytest.mark.parametrize("lookback, expected_delta, mock_data, timeframe", [
    ("30d", timedelta(days=30), MOCK_PIONEX_DATA_1D["BTCUSDT"], "1d"),
    ("12h", timedelta(hours=12), MOCK_PIONEX_DATA_1H, "1h"),
    ("60m", timedelta(minutes=60), MOCK_PIONEX_DATA_1H, "1h"),
])
def test_fetch_klines_valid_lookback(fetcher: BinanceDataFetcher, lookback: str, expected_delta: timedelta, mock_data: list, timeframe: str) -> None:
    start_date = datetime(2025, 7, 20, tzinfo=warsaw_tz)
    expected_start = mock_data[0][0]  # Use the first timestamp from mock data
    with patch("binance.client.Client.get_historical_klines", return_value=[
        [int((dt - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds() * 1000), str(o), str(h), str(l), str(c), str(1.0), "", "", "", "", "", ""]
        for dt, o, h, l, c in mock_data
    ]):
        df = fetcher.fetch_klines("BTCUSDT", timeframe, "20.07.2025", lookback=lookback)
        assert not df.empty
        assert pd.to_datetime(df["open_time"].iloc[0], utc=True).tz_convert(warsaw_tz) == expected_start

def test_fetch_klines_end_date_not_specified(fetcher: BinanceDataFetcher) -> None:
    mock_end = datetime(2025, 7, 25, 12, 0, 0, tzinfo=warsaw_tz)
    with patch("datetime.datetime", wraps=datetime) as mock_datetime:
        mock_datetime.now.return_value = mock_end
        with patch("binance.client.Client.get_historical_klines", return_value=[
            [int((dt - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds() * 1000), str(o), str(h), str(l), str(c), str(1.0), "", "", "", "", "", ""]
            for dt, o, h, l, c in MOCK_PIONEX_DATA_1D["BTCUSDT"]
        ]):
            df = fetcher.fetch_klines("BTCUSDT", "1d", "20.07.2025")
            assert not df.empty
            assert pd.to_datetime(df["open_time"].iloc[-1], utc=True).tz_convert(warsaw_tz) <= mock_end
