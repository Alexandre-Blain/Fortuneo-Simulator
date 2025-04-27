from datetime import timedelta, date
import pandas as pd
import yfinance as yf

# ---------- Excel I/O --------------------------------------------------------

def read_investments(path: str) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Investments")

def read_initial_prices(path: str) -> pd.DataFrame:
    try:
        return pd.read_excel(path, sheet_name="Initial_Prices")
    except ValueError:
        return pd.DataFrame(columns=["fortuneo_code", "yahoo_ticker",
                                     "price_at_purchase"])

def write_sheets(path: str, pnl_df: pd.DataFrame,
                 init_df: pd.DataFrame) -> None:
    with pd.ExcelWriter(path, engine="openpyxl",
                        mode="a", if_sheet_exists="replace") as wrt:
        pnl_df.to_excel(wrt, sheet_name="PNL_Report", index=False)
        init_df.to_excel(wrt, sheet_name="Initial_Prices", index=False)

def write_investments(path: str, df: pd.DataFrame) -> None:
    """Overwrite the Investments sheet with updated data (fees, etc.)."""
    with pd.ExcelWriter(path, engine="openpyxl",
                        mode="a", if_sheet_exists="replace") as wrt:
        df.to_excel(wrt, sheet_name="Investments", index=False)


# ---------- Price helpers ----------------------------------------------------

def get_open_price(symbol: str, on: date) -> float | None:
    """Open price on `on` date (next session if holiday/week-end)."""
    hist = yf.download(symbol,
                       start=on,
                       end=on + timedelta(days=2),
                       progress=False,
                       auto_adjust=False)
    try:
        return float(hist.iloc[0]["Open"])
    except (IndexError, KeyError):
        return None
