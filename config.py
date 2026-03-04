from __future__ import annotations

SECTORS: dict[str, dict[str, object]] = {
    "Technologie": {"tickers": ["AAPL", "MSFT", "NVDA"], "benchmark": "^IXIC"},
    "Banque": {"tickers": ["JPM", "BAC", "GS"], "benchmark": "^BKX"},
    "Sante": {"tickers": ["JNJ", "PFE", "MRK"], "benchmark": "XLV"},
    "Immobilier": {"tickers": ["AMT", "PLD", "CCI"], "benchmark": "XLRE"},
    "Consommation": {"tickers": ["PG", "KO", "PEP"], "benchmark": "XLP"},
    "Automobile": {"tickers": ["TSLA", "F", "GM"], "benchmark": "CARZ"},
    "Energie": {"tickers": ["XOM", "CVX", "COP"], "benchmark": "XLE"},
}

RISK_PROFILES = {
    "Prudent": {"target_monthly_vol": 0.04},
    "Equilibre": {"target_monthly_vol": 0.07},
    "Dynamique": {"target_monthly_vol": 0.10},
}
