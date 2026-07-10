# linear regression analysis
# level regression and first difference regression
# ZORI ~ FFR + CPI

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('Loading combined dataset...')
df = pd.read_csv('../data/combined_data.csv')
df['Month'] = pd.to_datetime(df['Month'].astype(str))
df = df.dropna(subset=['Fed Funds Rate', 'CPI', 'ZORI'])

cities = ['Sacramento, CA', 'Stockton, CA', 'Fresno, CA']

print("\nLinear Regression Analysis: ZORI ~ FFR + CPI")
level_results = []
for city in cities:
    city_data = df[df['RegionName'] == city].copy()
    X = city_data[['Fed Funds Rate', 'CPI']].values
    y = city_data['ZORI'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    print(f"\n{city}:")
    print(f"  β₀ (intercept)  = {model.intercept_:.4f}")
    print(f"  β₁ (FFR coeff)  = {model.coef_[0]:.4f}")
    print(f"  β₂ (CPI coeff)  = {model.coef_[1]:.4f}")
    print(f"  R² Score        = {r2:.4f}")
    
    level_results.append({
        'City': city,
        'Intercept': round(model.intercept_, 4),
        'Coef FFR': round(model.coef_[0], 4),
        'Coef CPI': round(model.coef_[1], 4),
        'R-squared': round(r2, 4)
    })

print('\nFirst Difference Regression Analysis: ΔZORI ~ ΔFFR + ΔCPI')
diff_results = []
for city in cities:
    city_data = df[df['RegionName'] == city].copy()
    city_data = city_data.sort_values('Month')
    city_data['ΔZORI'] = city_data['ZORI'].diff()
    city_data['ΔFFR'] = city_data['Fed Funds Rate'].diff()
    city_data['ΔCPI'] = city_data['CPI'].diff()
    city_data = city_data.dropna(subset=['ΔZORI', 'ΔFFR', 'ΔCPI'])
    x = city_data[['ΔFFR', 'ΔCPI']].values
    y = city_data['ΔZORI'].values

    model = LinearRegression()
    model.fit(x, y)

    y_pred = model.predict(x)
    r2 = r2_score(y, y_pred)

    print(f"\n{city}:")
    print(f"  β₀ (intercept)  = {model.intercept_:.4f}")
    print(f"  β₁ (ΔFFR coeff) = {model.coef_[0]:.4f}")
    print(f"  β₂ (ΔCPI coeff) = {model.coef_[1]:.4f}")
    print(f"  R² Score        = {r2:.4f}")
    
    diff_results.append({
        'City': city,
        'Type': 'First Difference',
        'β₀': round(model.intercept_, 4),
        'β₁ ΔFFR': round(model.coef_[0], 4),
        'β₂ ΔCPI': round(model.coef_[1], 4),
        'R²': round(r2, 4)
    })

print("\nGenerating regression comparison chart...")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle(
    'Regression Analysis: Level vs First Difference\n'
    'SCC Real Estate Analysis Club — Market Tracker',
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
    city_data = city_data.sort_values('Month')

    # Top row — Level regression
    X_level = city_data[['Fed Funds Rate', 'CPI']].values
    y_level = city_data['ZORI'].values
    model_level = LinearRegression().fit(X_level, y_level)
    r2_level = r2_score(y_level, model_level.predict(X_level))

    axes[0][idx].scatter(
        city_data['CPI'],
        city_data['ZORI'],
        color=colors[city],
        alpha=0.5,
        s=25
    )
    axes[0][idx].set_title(
        f"{city}\nLevel R² = {r2_level:.4f}",
        fontsize=10
    )
    axes[0][idx].set_xlabel('CPI')
    axes[0][idx].set_ylabel('ZORI ($)')

    # Bottom row — First difference regression
    city_data['ΔZORI'] = city_data['ZORI'].diff()
    city_data['ΔFFR']  = city_data['Fed Funds Rate'].diff()
    city_data['ΔCPI']  = city_data['CPI'].diff()
    city_data = city_data.dropna(subset=['ΔZORI', 'ΔFFR', 'ΔCPI'])

    X_diff = city_data[['ΔFFR', 'ΔCPI']].values
    y_diff = city_data['ΔZORI'].values
    model_diff = LinearRegression().fit(X_diff, y_diff)
    r2_diff = r2_score(y_diff, model_diff.predict(X_diff))

    axes[1][idx].scatter(
        city_data['ΔCPI'],
        city_data['ΔZORI'],
        color=colors[city],
        alpha=0.5,
        s=25
    )
    axes[1][idx].set_title(
        f"{city}\nFirst Diff R² = {r2_diff:.4f}",
        fontsize=10
    )
    axes[1][idx].set_xlabel('ΔCPI')
    axes[1][idx].set_ylabel('ΔZORI ($)')

plt.tight_layout()
plt.savefig('../reports/regression_analysis.png', dpi=150)
print("Saved to reports/regression_analysis.png")
plt.show()

# Save results
results_df = pd.DataFrame(level_results + diff_results)
results_df.to_csv('../data/regression_results.csv', index=False)
print("\nRegression results saved to data/regression_results.csv")