# did_analysis.py
# Computes the difference-in-differences estimate for the eBay paid search experiment.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Reference: Blake et al. (2014), Taddy Ch. 5

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

# Standard error
se = np.sqrt(
    r_treated.var(ddof=1) / r_treated.shape[0] +
    r_control.var(ddof=1) / r_control.shape[0]
)

# 95% CI
z = 1.96
ci_lower = did_estimate - z * se
ci_upper = did_estimate + z * se

# LaTeX table output
latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{l c}
\hline
 & Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f,\ %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}
""" % (did_estimate, se, ci_lower, ci_upper)

import os
os.makedirs("output/tables", exist_ok=True)

with open("output/tables/did_table.tex", "w") as f:
    f.write(latex)

print("Saved output/tables/did_table.tex")
