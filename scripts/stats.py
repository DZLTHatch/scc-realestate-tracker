# stats and correlation analysis for Sac Metro RE Market Tracker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Loading combined dataset...")
df = pd.read_csv('../data/combined_data.csv')
df['Month'] = pd.to_datetime(df['Month'].astype(str))

df = df.dropna(subset=['Fed Funds Rate', 'CPI', 'ZORI'])

print("\nStats by City")
cities = ['Sacramento, CA', 'Stockton, CA', 'Fresno, CA']

desc_results = []

for city in cities:
    city_data = df[df['RegionName'] == city]['ZORI']
    desc_results.append({
        'City': city,
        'Mean ZORI': round(city_data.mean(), 2),
        'Median ZORI': round(city_data.median(), 2),
        'Std Dev': round(city_data.std(), 2),
        'Min': round(city_data.min(), 2),
        'Max': round(city_data.max(), 2),
        'Total Change': round(city_data.iloc[-1] - city_data.iloc[0], 2)
    })
desc_df = pd.DataFrame(desc_results)
print(desc_df.to_string(index=False))

print("\nPearson Correlation: ZORI vs FFR --")

for city in cities:
    city_data = df[df['RegionName'] == city].copy()
    
    r_ffr, p_ffr = stats.pearsonr(
        city_data['Fed Funds Rate'],
        city_data['ZORI']
    )
    
    r_cpi, p_cpi = stats.pearsonr(
        city_data['CPI'],
        city_data['ZORI']
    )
    
    print(f"\n{city}:")
    print(f"  ZORI vs FFR  → r = {r_ffr:.4f}, p-value = {p_ffr:.4f}")
    print(f"  ZORI vs CPI  → r = {r_cpi:.4f}, p-value = {p_cpi:.4f}")


print("\nGenerating correlation heatmap...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(
    'Correlation: ZORI vs Macroeconomic Indicators\n'
    'SCC Real Estate Analysis Club -- Market Tracker',
    fontsize=13,
    fontweight='bold'
)

colors = {
    'Sacramento, CA': '#8B1A1A',
    'Stockton, CA': '#1a3c34',
    'Fresno, CA': '#2b4a8b'
}

for idx, city in enumerate(cities):
    city_data = df[df['RegionName'] == city].copy()
    r, p = stats.pearsonr(
        city_data['Fed Funds Rate'],
        city_data['ZORI']
    )
    
    axes[idx].scatter(
        city_data['Fed Funds Rate'],
        city_data['ZORI'],
        color=colors[city],
        alpha=0.6,
        s=30
    )
    

    m, b = np.polyfit(city_data['Fed Funds Rate'], city_data['ZORI'], 1)
    x_line = np.linspace(
        city_data['Fed Funds Rate'].min(),
        city_data['Fed Funds Rate'].max(),
        100
    )
    axes[idx].plot(x_line, m * x_line + b, color='orange', linewidth=2)
    
    axes[idx].set_title(f"{city}\nr = {r:.4f}, p = {p:.4f}", fontsize=11)
    axes[idx].set_xlabel('Fed Funds Rate (%)')
    axes[idx].set_ylabel('ZORI ($)')

plt.tight_layout()
plt.savefig('../reports/correlation_analysis.png', dpi=150)
print("Saved to reports/correlation_analysis.png")
plt.show()


desc_df.to_csv('../data/descriptive_stats.csv', index=False)
print("\nDescriptive stats saved to data/descriptive_stats.csv")