import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Load combined data
print("Loading combined data...")
df = pd.read_csv('../data/combined_data.csv')
df['Month'] = pd.to_datetime(df['Month'].astype(str))

# Set up the chart
fig, ax1 = plt.subplots(figsize=(14, 7))

# Define colors for each city
colors = {
    'Sacramento, CA': '#8B1A1A',
    'Stockton, CA':   '#1a3c34',
    'Fresno, CA':     '#2b4a8b'
}

# Plot ZORI rent for each city on left axis
for city, color in colors.items():
    city_data = df[df['RegionName'] == city]
    ax1.plot(
        city_data['Month'],
        city_data['ZORI'],
        label=city,
        color=color,
        linewidth=2
    )

ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Avg Asking Rent (ZORI $)', fontsize=12)
ax1.tick_params(axis='y')

# Plot Fed Funds Rate on right axis
ax2 = ax1.twinx()
macro = df[df['RegionName'] == 'Sacramento, CA']
ax2.plot(
    macro['Month'],
    macro['Fed Funds Rate'],
    label='Fed Funds Rate',
    color='orange',
    linewidth=1.5,
    linestyle='--'
)

ax2.set_ylabel('Fed Funds Rate (%)', fontsize=12)

# Titles and labels
plt.title(
    'Sacramento Metro Rent Trends vs Fed Funds Rate\n'
    'SCC Real Estate Analysis Club — Market Tracker',
    fontsize=14,
    fontweight='bold'
)

# Combine legends from both axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()

# Save to reports folder
output_path = '../reports/market_report.png'
plt.savefig(output_path, dpi=150)
print(f"Chart saved to {output_path}")
plt.show()