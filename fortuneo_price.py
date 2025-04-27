"""
Convert a “TICKER - ISIN - MARKET” string (Fortuneo export) to a Yahoo symbol
and fetch the most-recent close with yfinance.
"""

from typing import Optional
import yfinance as yf
from Variable_globale import VariableGlobale as VG


def fortuneo_to_yf_symbol(line: str) -> str:
    """'HO - FR0000121329 - Paris' → 'HO.PA'"""
    ticker, _, market = (p.strip() for p in line.split(" - ", 2))
    suffix = VG.SUFFIX.get(market)
    if suffix is None:
        raise KeyError(f"Unknown market '{market}' – add it to _SUFFIX")
    return f"{ticker}.{suffix}" if suffix else ticker

def get_last_close(symbol: str) -> Optional[float]:
    """Return the last available daily close price (None if unavailable)."""
    hist = yf.download(symbol, period="5d", interval="1d", progress=False,
                       auto_adjust=False)  # explicit! new default is True
    if hist.empty:
        return None
    return float(hist["Close"].iloc[-1])

