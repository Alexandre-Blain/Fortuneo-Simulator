from datetime import date
from math import isnan

def calculate_pnl(price_then: float,
                  price_now: float,
                  amount: float,
                  invested_on: date) -> dict[str, float]:
    """Return shares, current value, pnl abs/%, and annualized return."""
    shares = amount / price_then
    current_value = shares * price_now
    pnl = current_value - amount
    pnl_pct = pnl / amount * 100

    days = (date.today() - invested_on).days
    ann_return = 0.0
    if days > 0 and price_then > 0 and not isnan(price_now):
        ann_return = (price_now / price_then) ** (365 / days) - 1

    return {
        "shares": round(shares, 6),
        "current_value": round(current_value, 2),
        "pnl": round(pnl, 2),
        "pnl_pct": round(pnl_pct, 2),
        "annualized_return": round(ann_return * 100, 2),
    }