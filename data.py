from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class MarketData:
    prices_daily: pd.DataFrame  # close prices
    prices_monthly: pd.DataFrame  # month-end close prices


def _ensure_close(df: pd.DataFrame) -> pd.DataFrame:
    # yfinance returns a multi-index if multiple tickers; we always want Close prices
    if isinstance(df.columns, pd.MultiIndex):
        if ("Close" in df.columns.get_level_values(0)) or ("close" in df.columns.get_level_values(0)):
            df = df["Close"]
    return df.dropna(how="all")


def download_prices(tickers: Iterable[str], period: str = "1y", interval: str = "1d") -> MarketData:
    tickers = list(dict.fromkeys(tickers))  # stable unique
    raw = yf.download(tickers, period=period, interval=interval, auto_adjust=False, progress=False, group_by="column")
    close = _ensure_close(raw)
    close = close.sort_index()
    monthly = close.resample("M").last()
    return MarketData(prices_daily=close, prices_monthly=monthly)


@lru_cache(maxsize=256)
def company_info(ticker: str) -> dict:
    # Cached to avoid repeated network calls
    return yf.Ticker(ticker).info
