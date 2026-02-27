import pandas as pd
import numpy as np

# Load pivot tables saved by preprocess.py
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# Step 2 — Compute pre-post differences (r_i) for each DMA
r_treated = treated_pivot["log_revenue_diff"]
r_control = untreated_pivot["log_revenue_diff"]

# Step 3 — DID estimate and standard error
did_estimate = r_treated.mean() - r_control.mean()

se = np.sqrt(r_treated.var(ddof=1) / r_treated.shape[0] +
             r_control.var(ddof=1) / r_control.shape[0])

print(f"Treated DMAs (n={r_treated.shape[0]}): mean diff = {r_treated.mean():.4f}")
print(f"Control DMAs (n={r_control.shape[0]}): mean diff = {r_control.mean():.4f}")
print(f"DID estimate (treated - control) = {did_estimate:.4f}")
print(f"Standard Error = {se:.4f}")

# Step 4 — 95% Confidence Interval
z = 1.96
ci_lower = did_estimate - z * se
ci_upper = did_estimate + z * se

# Create LaTeX table string
latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
 & Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & %.4f \\
Standard Error & %.4f \\
95\%% CI & [%.4f, %.4f] \\
\hline
\end{tabular}
\label{tab:did}
\end{table}
""" % (did_estimate, se, ci_lower, ci_upper)

# Ensure tables directory exists
import os
os.makedirs("output/tables", exist_ok=True)

# Write to file
with open("output/tables/did_table.tex", "w") as f:
    f.write(latex)

print("Saved output/tables/did_table.tex")
