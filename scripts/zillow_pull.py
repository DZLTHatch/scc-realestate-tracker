# clean and process ZORI rent data for sac, stockton, fresno

import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("pulling ZORI rent data...")

zillow_raw = pd.read_csv('../data/Metro_zori_uc_sfrcondomfr_sm_month.csv')

markets = ['Sacramento, CA', 'Stockton, CA', 'Fresno, CA']
zillow_filtered = zillow_raw[zillow_raw['RegionName'].isin(markets)]

zillow_long = zillow_filtered.melt(
    id_vars=['RegionName'],
    var_name='Date',
    value_name='ZORI'
)

zillow_long = zillow_long[pd.to_datetime(zillow_long['Date'], errors='coerce').notna()]
zillow_long['Date'] = pd.to_datetime(zillow_long['Date'])
zillow_long = zillow_long[zillow_long['Date'] >= '2015-01-01']
zillow_long = zillow_long.sort_values(['RegionName', 'Date'])

# Save to data folder
zillow_long.to_csv('../data/zillow_clean.csv', index=False)

print("Done! zillow_clean.csv saved to data folder.")
print(zillow_long.tail(9))