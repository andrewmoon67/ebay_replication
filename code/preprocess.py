import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y')
df['log_revenue'] = np.log(df['revenue'])

# Step 2 — Separate treated and untreated units and create pivot tables

# Treated units: search_stays_on == 0
treated_df = df[df['search_stays_on'] == 0].copy()

# Untreated units (control): search_stays_on == 1
untreated_df = df[df['search_stays_on'] == 1].copy()

def make_pivot(group_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pivot to dma x treatment_period using mean log_revenue,
    rename columns to log_revenue_pre/post, and compute diff.
    """
    pivot = group_df.pivot_table(
        index='dma',
        columns='treatment_period',
        values='log_revenue',
        aggfunc='mean'
    )

    # Ensure both columns exist (0 = pre, 1 = post)
    # If a column is missing, it will raise a clearer error.
    if 0 not in pivot.columns or 1 not in pivot.columns:
        raise ValueError(f"Missing treatment_period 0 or 1 in pivot. Found columns: {list(pivot.columns)}")

    pivot = pivot.rename(columns={
        0: 'log_revenue_pre',
        1: 'log_revenue_post'
    })

    pivot['log_revenue_diff'] = pivot['log_revenue_post'] - pivot['log_revenue_pre']

    # Make the csv nicer (dma as a normal column, not index)
    pivot = pivot.reset_index()

    return pivot

treated_pivot = make_pivot(treated_df)
untreated_pivot = make_pivot(untreated_df)

# Save to temp/
treated_pivot.to_csv('temp/treated_pivot.csv', index=False)
untreated_pivot.to_csv('temp/untreated_pivot.csv', index=False)

print("Saved temp/treated_pivot.csv and temp/untreated_pivot.csv")

# Step 3 — Print summary statistics

num_treated_dmas = treated_df['dma'].nunique()
num_untreated_dmas = untreated_df['dma'].nunique()

min_date = df['date'].min().date()
max_date = df['date'].max().date()

print(f"Treated DMAs: {num_treated_dmas}")
print(f"Untreated DMAs: {num_untreated_dmas}")
print(f"Date range: {min_date} to {max_date}")

# Step 4 — Reproduce Figure 5.2 (Avg revenue by group over time)

# Group by date and search_stays_on, compute mean revenue
ts = (
    df.groupby(['date', 'search_stays_on'])['revenue']
      .mean()
      .reset_index()
)

# Split for plotting
control_ts = ts[ts['search_stays_on'] == 1].sort_values('date')
treated_ts = ts[ts['search_stays_on'] == 0].sort_values('date')

# Plot
plt.figure(figsize=(10, 6))
plt.plot(control_ts['date'], control_ts['revenue'], label='Control (search stays on)')
plt.plot(treated_ts['date'], treated_ts['revenue'], label='Treatment (search goes off)')

# Treatment date vertical dashed line
treatment_date = pd.to_datetime('2012-05-22')
plt.axvline(treatment_date, linestyle='--')

# Labels/title/legend
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Average Revenue per Day: Treatment vs Control DMAs')
plt.legend()

plt.tight_layout()
plt.savefig('output/figures/figure_5_2.png', dpi=300)
plt.close()

print("Saved output/figures/figure_5_2.png")

# Step 5 — Reproduce Figure 5.3 (Log-scale difference over time)

# Group by date and group, compute mean log_revenue
log_ts = (
    df.groupby(['date', 'search_stays_on'])['log_revenue']
      .mean()
      .reset_index()
)

# Pivot so each date has a column for each group
# 1 = control (search stays on), 0 = treated (search goes off)
log_pivot = log_ts.pivot(index='date', columns='search_stays_on', values='log_revenue').sort_index()

# Make sure both columns exist
if 0 not in log_pivot.columns or 1 not in log_pivot.columns:
    raise ValueError(f"Expected columns 0 and 1 after pivot, got: {list(log_pivot.columns)}")

# Compute difference: log(avg control revenue) - log(avg treatment revenue)
log_pivot['log_diff'] = log_pivot[1] - log_pivot[0]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(log_pivot.index, log_pivot['log_diff'])

# Treatment date line
treatment_date = pd.to_datetime('2012-05-22')
plt.axvline(treatment_date, linestyle='--')

# Labels/title
plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Log-Scale Average Revenue Difference: Control - Treatment')

plt.tight_layout()
plt.savefig('output/figures/figure_5_3.png', dpi=300)
plt.close()

print("Saved output/figures/figure_5_3.png")
