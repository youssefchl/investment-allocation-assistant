from __future__ import annotations

import argparse
from pathlib import Path

from .config import SECTORS, RISK_PROFILES
from .data import download_prices
from .analytics import compute_analytics, optimize_target_vol
from .export import build_fiche, export_excel, export_pdf


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Educational Investment Allocation Assistant")
    p.add_argument("--sector", required=True, choices=SECTORS.keys())
    p.add_argument("--profile", required=True, choices=RISK_PROFILES.keys())
    p.add_argument("--amount", required=True, type=float)
    p.add_argument("--outdir", default="outputs", help="Output directory")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = SECTORS[args.sector]
    tickers = list(cfg["tickers"])
    benchmark = str(cfg["benchmark"])
    all_tickers = tickers + [benchmark]

    md = download_prices(all_tickers, period="1y", interval="1d")

    ana = compute_analytics(md.prices_daily, md.prices_monthly, tickers, benchmark)

    target_vol = float(RISK_PROFILES[args.profile]["target_monthly_vol"])
    weights = optimize_target_vol(ana.returns_monthly, target_vol)

    fiche = build_fiche(tickers)

    outdir = Path(args.outdir)
    excel_path = outdir / f"analysis_{args.sector}.xlsx"
    pdf_path = outdir / f"report_{args.sector}.pdf"

    export_excel(excel_path, ana.base100, ana.beta, ana.correlation, fiche)
    export_pdf(pdf_path, args.sector, md.prices_daily[tickers], ana.base100, ana.correlation, weights, args.amount)

    print(f"Saved: {excel_path}")
    print(f"Saved: {pdf_path}")


if __name__ == "__main__":
    main()
