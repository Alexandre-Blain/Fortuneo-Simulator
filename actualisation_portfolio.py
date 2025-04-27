"""
Run:  python main.py
The script updates / creates three sheets in portfolio.xlsx:
  • Investments      (user maintained)
  • Initial_Prices   (persisted purchase prices)
  • PNL_Report       (fresh performance metrics)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from fee_calculator import progress_fee
from fortuneo_price import fortuneo_to_yf_symbol, get_last_close
from pnl_calculator import calculate_pnl
from excel_manager import (read_investments, read_initial_prices,
                           write_sheets, get_open_price,
                           write_investments)
from Variable_globale import VariableGlobale as VG


excel = VG.EXCEL_PATH
price_cache = read_initial_prices(excel)
invest_df = VG.PORTFOLIO_DATA
results: list[dict] = []

# --------------------------------------------------------------------------- #
# 2. Process each line
for idx, row in invest_df.iterrows():
    code   = str(row["fortuneo_code"]).strip()
    net_am = float(row["net_amount_invested"])
    dt_inv = pd.to_datetime(row["date_invested"]).date()

    fee   = progress_fee(net_am)
    amount = net_am - fee          # amount after fee

    # write back into DataFrame (so it can be saved to Excel later)
    invest_df.loc[idx, "amount_invested"] = float(amount)
    invest_df.loc[idx, "fee_paid"]        = float(fee)

    ticker = fortuneo_to_yf_symbol(code)

    # --- purchase price (cached) -------------------------------------------
    cache_row = price_cache[price_cache["fortuneo_code"] == code]
    if cache_row.empty:
        px_then = get_open_price(ticker, dt_inv)
        if px_then is None:
            results.append({
                "fortuneo_code": code,
                "yahoo_ticker": ticker,
                "error": "purchase price unavailable",
            })
            continue
        price_cache = pd.concat([price_cache, pd.DataFrame([{
            "fortuneo_code": code,
            "yahoo_ticker":  ticker,
            "price_at_purchase": px_then,
        }])], ignore_index=True)
    else:
        px_then = float(cache_row.iloc[0]["price_at_purchase"])

    # --- current price ------------------------------------------------------
    px_now = get_last_close(ticker)
    if px_now is None:
        results.append({
            "fortuneo_code": code,
            "yahoo_ticker":  ticker,
            "error": "latest price unavailable",
        })
        continue

    # --- metrics ------------------------------------------------------------
    perf = calculate_pnl(px_then, px_now, amount, dt_inv)
    results.append({
        "fortuneo_code": code,
        "yahoo_ticker":  ticker,
        "net_amount_invested": net_am,
        "fee_paid": fee,
        "amount_invested": amount,
        "date_invested":  dt_inv,
        "price_at_purchase": round(px_then, 2),
        "price_now":       round(px_now, 2),
        **perf
    })

# --------------------------------------------------------------------------- #
# 3. Build PNL report DataFrame
pnl_df = pd.DataFrame(results)

if not pnl_df.empty and "amount_invested" in pnl_df.columns:
    total_invested = pnl_df["amount_invested"].sum()
    pnl_df["weight_in_portfolio"] = (pnl_df["amount_invested"] /
                                     total_invested * 100).round(2)

if not pnl_df.empty and "pnl" in pnl_df.columns:
    total_pnl = pnl_df["pnl"].sum()
    if total_pnl != 0:
        pnl_df["contribution_to_pnl"] = (pnl_df["pnl"] /
                                         total_pnl * 100).round(2)

# --------------------------------------------------------------------------- #
# 4. Persist
write_sheets(excel, pnl_df, price_cache)
write_investments(excel, invest_df)     

print("✓  PNL_Report & Initial_Prices updated.")

