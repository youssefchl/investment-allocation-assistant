from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.optimize import minimize


@dataclass(frozen=True)
class Analytics:
    returns_monthly: pd.DataFrame
    correlation: pd.DataFrame
    beta: pd.Series
    base100: pd.DataFrame


def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).dropna()


def compute_analytics(prices_daily: pd.DataFrame, prices_monthly: pd.DataFrame, tickers: list[str], benchmark: str) -> Analytics:
    monthly_lr = log_returns(prices_monthly)

    asset_lr = monthly_lr[tickers]
    bench_lr = monthly_lr[benchmark]

    # Correlation (assets only)
    corr = asset_lr.corr()

    # Beta over full sample (simple CAPM beta estimate)
    betas = {}
    var_b = float(np.var(bench_lr, ddof=1))
    for t in tickers:
        cov = float(np.cov(asset_lr[t], bench_lr, ddof=1)[0, 1])
        betas[t] = cov / var_b if var_b > 0 else np.nan
    beta = pd.Series(betas).sort_values(ascending=False)

    base100 = (prices_daily[tickers] / prices_daily[tickers].iloc[0]) * 100

    return Analytics(returns_monthly=asset_lr, correlation=corr, beta=beta, base100=base100)


def optimize_target_vol(returns_monthly: pd.DataFrame, target_vol: float) -> pd.Series:
    """Find long-only weights whose volatility is close to target_vol.

    Objective: minimize (vol(w) - target_vol)^2
    Constraints: sum(w)=1, 0<=w<=1
    """
    cov = returns_monthly.cov().values
    mean = returns_monthly.mean().values
    n = len(mean)
    x0 = np.ones(n) / n

    def portfolio_vol(w: np.ndarray) -> float:
        return float(np.sqrt(w.T @ cov @ w))

    def obj(w: np.ndarray) -> float:
        v = portfolio_vol(w)
        return (v - target_vol) ** 2

    cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
    bounds = [(0.0, 1.0)] * n

    res = minimize(obj, x0, bounds=bounds, constraints=cons, method="SLSQP")
    if not res.success:
        # fallback to equal weights
        w = x0
    else:
        w = np.clip(res.x, 0.0, 1.0)
        w = w / np.sum(w)

    return pd.Series(w, index=returns_monthly.columns, name="weight")
