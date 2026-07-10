# test whether FFR changes correlate with rent changes at different time lags (0, 3, 6, 12 months)

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('Loading combined dataset...')
df = pd.read_csv('../data/combined_data.csv')
df['Month'] = pd.to_datetime(df['Month'].astype(str))
df = df.dropna(subset=['Fed Funds Rate', 'CPI', 'ZORI'])

cities = ['Sacramento, CA', 'Stockton, CA', 'Fresno, CA']
lags = [0, 3, 6, 12]

colors = {
    'Sacramento, CA': 'blue',
    'Stockton, CA': 'green',
    'Fresno, CA': 'red'
}

print('\nLag Correlation: ΔFFR vs ΔZORI')

all_results = []

for city in cities:
    print(f"\n{city}:")
    city_data = df[df['RegionName'] == city].copy()
    city_data = city_data.sort_values('Month').reset_index(drop=True)

    city_data['ΔZORI'] = city_data['ZORI'].diff()
    city_data['ΔFFR'] = city_data['Fed Funds Rate'].diff()

    for lag in lags:
        city_data[f'ΔFFR_lag{lag}'] = city_data['ΔFFR'].shift(lag)
        
        # Drop NaN rows for this lag
        temp = city_data[['ΔZORI', f'ΔFFR_lag{lag}']].dropna()
        
        r, p = stats.pearsonr(temp[f'ΔFFR_lag{lag}'], temp['ΔZORI'])
        
        print(f"  Lag {lag:2d} months → r = {r:7.4f}, p = {p:.4f}")
        
        all_results.append({
            'City': city,
            'Lag (months)': lag,
            'r': round(r, 4),
            'p-value': round(p, 4),
            'Significant': 'Yes' if p < 0.05 else 'No'
        })

print('\nGenerating lag analysis chart...')
fig, axes = plt.subplots(1,3, figsize=(16,6))
fig.suptitle(
    'Lag Correlation: ΔFFR vs ΔZORI\n' 'SCC Real Estate Analysis Club -- Market Tracker', fontsize=13, fontweight='bold')
for idx, city in enumerate(cities):
    city_results = [r for r in all_results if r['City'] == city]
    lag_values = [r['Lag (months)'] for r in city_results]
    r_values   = [r['r'] for r in city_results]
    
    axes[idx].bar(
        lag_values,
        r_values,
        color=colors[city],
        alpha=0.8,
        width=2
    )
    
    # Add significance line
    axes[idx].axhline(
        y=0,
        color='black',
        linewidth=0.8,
        linestyle='-'
    )
    axes[idx].axhline(
        y=0.15,
        color='orange',
        linewidth=1,
        linestyle='--',
        label='r = 0.15 reference'
    )
    axes[idx].axhline(
        y=-0.15,
        color='orange',
        linewidth=1,
        linestyle='--'
    )
    
    axes[idx].set_title(f"{city}", fontsize=11)
    axes[idx].set_xlabel('Lag (months)')
    axes[idx].set_ylabel('Pearson r')
    axes[idx].set_xticks(lags)
    axes[idx].set_ylim(-0.4, 0.4)
    axes[idx].legend(fontsize=8)

plt.tight_layout()
plt.savefig('../reports/lag_analysis.png', dpi=150)
print("Saved to reports/lag_analysis.png")
plt.show()

# Save results
results_df = pd.DataFrame(all_results)
results_df.to_csv('../data/lag_results.csv', index=False)
print("\nLag results saved to data/lag_results.csv")
print("\nSummary Table")
print(results_df.to_string(index=False))