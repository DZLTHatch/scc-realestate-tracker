import pandas as pd
from fredapi import Fred
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FRED_API_KEY

fred = Fred(api_key=FRED_API_KEY)
# getting the Federal Funds Rate from FRED
print("pulling Federal Funds Rate...")
fed_funds_rate = fred.get_series('FEDFUNDS')

#pull CPI (inflationn)
print("pulling CPI...")
cpi = fred.get_series('CPIAUCSL')

macro_data = pd.DataFrame({
    'Fed Funds Rate': fed_funds_rate,
    "CPI": cpi

})

macro_data = macro_data[macro_data.index >= '2015-01-01']

# saves to data folder
macro_data.index.name = 'Date'
macro_data.to_csv('../data/macro_data.csv')

print("macro data saved to data/macro_data.csv")
print(macro_data.tail())

