# Investment Allocation Assistant (Educational Project)

An interactive Python tool that:
- pulls market data with **yfinance**
- computes **returns, volatility, correlations, beta**
- proposes a **simple Markowitz-style allocation** based on a risk profile
- exports results to **Excel** (formatted) and a **PDF report**

> **Disclaimer**: This project is for **educational purposes only**. It is **not** financial advice.

## Features
- Sector selection (configurable tickers + benchmark index/ETF)
- Monthly log-returns, correlation matrix, rolling beta
- Portfolio optimization (target-volatility approximation)
- Export:
  - `outputs/analysis_<sector>.xlsx`
  - `outputs/report_<sector>.pdf`

## Quick start

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run (CLI)
```bash
python -m invest_assistant --sector Technologie --profile Equilibre --amount 2500
```

Outputs are saved in `outputs/`.

## Repo structure
- `src/invest_assistant/` — library code
- `notebooks/` — optional exploration
- `tests/` — small unit tests (sanity checks)
- `outputs/` — generated files (gitignored)

## Notes for reviewers
- Network calls are isolated in `data.py`
- Caching is used to avoid repeated API calls
- Code is typed, documented, and lint-friendly
