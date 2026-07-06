# merge macro + zillow rent data
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('Loading datasets...')
macro = pd.read_csv('../data/macro_data.csv')
zillow = pd.read_csv('../data/zillow_clean.csv')

macro['Month'] = pd.to_datetime(macro['Date']).dt.to_period('M')
zillow['Month'] = pd.to_datetime(zillow['Date']).dt.to_period('M')

combined = pd.merge(zillow, macro, on='Month', how='left')

combined = combined.drop(columns=['Date_x', 'Date_y'])

combined['ZORI'] = combined['ZORI'].round(2)
combined['Fed Funds Rate'] = combined['Fed Funds Rate'].round(2)
combined['CPI'] = combined['CPI'].round(3)

combined = combined.sort_values(['RegionName', 'Month'])

combined.to_csv('../data/combined_data.csv', index=False)
#  save it

print(combined.tail(9))