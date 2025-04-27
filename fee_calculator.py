# fee_calculator.py
# Fortuneo "Progress" tariff for Euronext actions

def progress_fee(gross_amount: float) -> float:
    """
    Return the fee (EUR) for a single buy order:
      • 4.90 € flat if the order ≤ 3 000 €
      • 0.15 % of the order amount if the order > 3 000 €
    """
    if gross_amount <= 3000:
        return 4.90
    return round(gross_amount * 0.0015, 2)  # 0.15 %
