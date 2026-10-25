"""Quickstart: load FinChrona Treasury rates, check quality, plot the 10Y-2Y term spread.

Run from the repo root:  python examples/quickstart.py
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

path = Path(__file__).resolve().parents[1] / "data" / "processed" / "finchrona_treasury_rates.parquet"
df = pd.read_parquet(path)
print("shape:", df.shape)
print(df.dtypes)
print("date range:", df.observation_date.min().date(), "to", df.observation_date.max().date())
print("nulls:", int(df.isna().sum().sum()), "| duplicate keys:",
      int(df.duplicated(["observation_date", "curve_type", "quote_basis", "maturity_label"]).sum()))

nom = df[df.curve_type == "par_nominal"].pivot(index="observation_date", columns="maturity_label", values="value_pct")
spread = (nom["10Y"] - nom["2Y"]).dropna()
print("days with 10Y-2Y < 0:", int((spread < 0).sum()), "of", len(spread))

fig, ax = plt.subplots(figsize=(9, 4))
spread.plot(ax=ax, lw=0.8)
ax.axhline(0, color="k", lw=0.5)
ax.set_title("US Treasury par yield: 10Y minus 2Y (percentage points)")
ax.set_ylabel("spread (pp)")
fig.tight_layout()
out = Path(__file__).resolve().parent / "term_spread.png"
fig.savefig(out, dpi=120)
print("saved", out.name)
# Descriptive only: negative spreads mean the 2Y yield exceeded the 10Y yield (curve inversion) on those days.
