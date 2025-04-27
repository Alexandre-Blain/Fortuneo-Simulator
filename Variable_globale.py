#Classe qui conserve en mémoire les variables 

from dataclasses import dataclass,field
import numpy as np
import pandas as pd
from pathlib import Path
from excel_manager import (read_investments, read_initial_prices,
                           write_sheets, get_open_price,
                           write_investments)

@dataclass(slots=True)
class VariableGlobale :
    PORTFOLIO_DATA: pd.DataFrame = field(default_factory=pd.DataFrame)
    EXCEL_PATH : str = ""
    SUFFIX = {"Paris": "PA", #EU West
              "N.E. Amsterdam": "AS",
               }


excel = Path(r"Portfolio_folder\portfolio.xlsx")

# --------------------------------------------------------------------------- #
# 1. Load data
invest_df = read_investments(excel)

if "amount_invested" not in invest_df.columns:
    # create an *empty float* column so assignments are always compatible
    invest_df["amount_invested"] = np.nan
else:
    # cast existing column to float once
    invest_df["amount_invested"] = invest_df["amount_invested"].astype(float)

if "fee_paid" not in invest_df.columns:
    invest_df["fee_paid"] = np.nan


    
VariableGlobale =  VariableGlobale(PORTFOLIO_DATA=invest_df,
                                   EXCEL_PATH=excel)



