# Mock Pionex data for 20.07.2025 to 22.07.2025 (3 days, 1d timeframe)
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BASE_DATE = datetime(2025, 7, 20, tzinfo=ZoneInfo("Europe/Warsaw"))

# Data discrepancies between Pionex/TradingView and Binance:
# BTC 0.00% - 0.03%
# ETH 0.08% - 0.08%
# XRP 0.13% - 0.13%
# BNB 0.00% - 0.01%
# SOL 0.00% - 0.01%

MOCK_PIONEX_DATA_1D = {
    "ETHUSDT": [
        [BASE_DATE, 3592.00, 3823.45, 3579.13, 3756.70],
        [BASE_DATE + timedelta(days=1), 3756.70, 3856.99, 3701.02, 3762.33],
        [BASE_DATE + timedelta(days=2), 3762.33, 3798.65, 3616.55, 3746.21],
    ],
    "BTCUSDT": [
        [BASE_DATE, 117_840.01, 118_856.80, 116_467.03, 117_265.12],
        [BASE_DATE + timedelta(days=1), 117_265.12, 119_644.06, 116_515.00, 117_380.37],
        [BASE_DATE + timedelta(days=2), 117_380.37, 120_247.80, 116_128.00, 119_954.43],
    ],
    "XRPUSDT": [
        [BASE_DATE, 3.4244, 3.5578, 3.3858, 3.4537],
        [BASE_DATE + timedelta(days=1), 3.4537, 3.6495, 3.4077, 3.5495],
        [BASE_DATE + timedelta(days=2), 3.5495, 3.5787, 3.4228, 3.5505],
    ],
    "BNBUSDT": [
        [BASE_DATE, 733.20, 761.29, 731.54, 756.81],
        [BASE_DATE + timedelta(days=1), 756.81, 781.93, 746.06, 766.23],
        [BASE_DATE + timedelta(days=2), 766.23, 788.33, 745.02, 786.69],
    ],
    "SOLUSDT": [
        [BASE_DATE, 176.96, 183.66, 176.33, 181.43],
        [BASE_DATE + timedelta(days=1), 181.43, 199.27, 178.26, 195.71],
        [BASE_DATE + timedelta(days=2), 195.71, 206.29, 193.77, 205.69],
    ],
}

MOCK_TRADING_VIEW_DATA_1D = {
    "ETHUSDT": [
        [BASE_DATE, 3592.00, 3824.56, 3579.13, 3756.69],
        [BASE_DATE + timedelta(days=1), 3756.69, 3860.00, 3701.01, 3762.33],
        [BASE_DATE + timedelta(days=2), 3762.32, 3798.65, 3616.54, 3746.21],
    ],
    "BTCUSDT": [
        [BASE_DATE, 117_840.01, 118_856.80, 116_467.02, 117_265.12],
        [BASE_DATE + timedelta(days=1), 117_265.11, 119_676.73, 116_515.00, 117_380.36],
        [BASE_DATE + timedelta(days=2), 117_380.36, 120_247.80, 116_128.00, 119_954.42],
    ],
    "XRPUSDT": [
        [BASE_DATE, 3.4243, 3.5579, 3.3856, 3.4540],
        [BASE_DATE + timedelta(days=1), 3.4541, 3.6495, 3.4076, 3.5495],
        [BASE_DATE + timedelta(days=2), 3.5494, 3.5787, 3.4218, 3.5504],
    ],
    "BNBUSDT": [
        [BASE_DATE, 733.20, 761.29, 731.50, 756.82],
        [BASE_DATE + timedelta(days=1), 756.82, 781.99, 746.06, 766.22],
        [BASE_DATE + timedelta(days=2), 766.22, 788.35, 745.00, 786.68],
    ],
    "SOLUSDT": [
        [BASE_DATE, 176.97, 183.66, 176.33, 181.43],
        [BASE_DATE + timedelta(days=1), 181.44, 199.28, 178.25, 195.72],
        [BASE_DATE + timedelta(days=2), 195.72, 206.30, 193.75, 205.70],
    ],
}

MOCK_PIONEX_DATA_1H = [
    [BASE_DATE, 3571.44, 3590.68, 3562.67, 3576.71],  # 00:00
    [BASE_DATE + timedelta(hours=1), 3576.71, 3598.30, 3574.23, 3592.00],  # 01:00
    [BASE_DATE + timedelta(hours=2), 3592.00, 3597.40, 3579.13, 3591.11],  # 02:00
]

MOCK_TRADING_VIEW_DATA_1H = [
    [BASE_DATE, 3571.44, 3590.69, 3562.67, 3576.70],  # 00:00
    [BASE_DATE + timedelta(hours=1), 3576.71, 3598.31, 3574.23, 3592.01],  # 01:00
    [BASE_DATE + timedelta(hours=2), 3592.00, 3597.40, 3579.13, 3591.11],  # 02:00
]
