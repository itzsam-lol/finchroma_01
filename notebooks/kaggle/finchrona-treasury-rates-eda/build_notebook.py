"""Generate finchrona-treasury-rates-eda.ipynb (source of truth for the notebook text)."""
from pathlib import Path

import nbformat as nbf

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell
cells = []

cells.append(md("""# FinChrona Treasury Rates: Exploratory Data Analysis

**FinChrona: Open Financial Time Series** — *Open financial data, built for research.*

This notebook walks through the FinChrona v1.0.0 dataset: daily U.S. Treasury **nominal par yields**, **real (TIPS) par yields** and **Treasury bill rates**, compiled from the U.S. Department of the Treasury's *Daily Treasury Rates* ([source](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics)) into one long-format schema.

- Kaggle dataset: <https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series>
- GitHub (code, docs): <https://github.com/itzsam-lol/finchroma_01>
- Hugging Face: <https://huggingface.co/datasets/samisonhf/finchrona>

**Coverage.** Nominal par yields start 1990-01-02, bill rates 2002-01-02 and real/TIPS yields 2003-01-02, through the data cutoff of 2026-10-23 (retrieved 2026-10-25). The coverage cells below recompute these from the data.

**Licence caveat.** The source is a U.S. Government work and the compiled dataset is published under CC0 1.0, but Treasury's pages did not state an explicit data licence; see the dataset's `licensing_and_attribution.md`. FinChrona is independently maintained and not endorsed by the U.S. Treasury.

**Limitations.** A historical snapshot: no publication timestamps, no revision history, not real-time, not investment advice. Rates are Treasury curve estimates or indicative bill quotations, not prices at which anyone is guaranteed to trade."""))

cells.append(md("## 1. Load the data"))
cells.append(code('''import glob, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams.update({"figure.figsize": (10, 4.5), "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False})

def find_file(name):
    roots = [os.environ.get("FINCHRONA_DATA_DIR", ""), "/kaggle/input"]
    for root in filter(None, roots):
        hits = glob.glob(os.path.join(root, "**", name), recursive=True)
        if hits:
            return hits[0]
    return None

print("Files in the mounted dataset:")
for root in filter(None, [os.environ.get("FINCHRONA_DATA_DIR", ""), "/kaggle/input"]):
    for p in sorted(glob.glob(os.path.join(root, "**", "*"), recursive=True)):
        if os.path.isfile(p):
            print("  ", os.path.relpath(p, root))

parquet, csv = find_file("finchrona_treasury_rates.parquet"), find_file("finchrona_treasury_rates.csv")
try:
    if parquet is None:
        raise FileNotFoundError
    df = pd.read_parquet(parquet)
    print("\\nLoaded Parquet:", os.path.basename(parquet))
except Exception:
    df = pd.read_csv(csv)
    print("\\nLoaded CSV fallback:", os.path.basename(csv))
df["observation_date"] = pd.to_datetime(df["observation_date"])
for c in ["curve_type", "quote_basis", "maturity_label", "maturity_unit"]:
    df[c] = df[c].astype(str)'''))
cells.append(code('''EXPECTED = ["observation_date", "curve_type", "quote_basis", "maturity_label", "maturity_value", "maturity_unit", "value_pct"]
KEY = ["observation_date", "curve_type", "quote_basis", "maturity_label"]
assert list(df.columns) == EXPECTED, df.columns.tolist()
assert set(df.curve_type) == {"par_nominal", "par_real", "bill_rate"}
assert set(df.quote_basis) == {"par_yield", "bank_discount", "coupon_equivalent"}
assert set(df.maturity_unit) == {"week", "month", "year"}
assert df.value_pct.notna().all() and (df.maturity_value > 0).all()

print("Shape:", df.shape)
print("Date range:", df.observation_date.min().date(), "to", df.observation_date.max().date())
print("Curve types:", sorted(df.curve_type.unique()))
print("Quote bases:", sorted(df.quote_basis.unique()))
print("Maturity labels:", df.drop_duplicates(["maturity_value", "maturity_unit"]).assign(m=lambda d: d.maturity_value * d.maturity_unit.map({"week": 7/30.4375, "month": 1, "year": 12})).sort_values("m").maturity_label.unique().tolist())
print("\\nColumn types:"); print(df.dtypes.to_string())
print("\\nMissing values per column:"); print(df.isna().sum().to_string())
df.head()'''))

cells.append(md("""## 2. Coverage overview

Each row is one rate for one curve, quote basis and maturity on one date. Blank cells in Treasury's wide tables (for example a maturity that was not yet offered) have **no row**, so maturities have different start dates. Nothing is imputed."""))
cells.append(code('''cov = (df.groupby("curve_type").agg(rows=("value_pct", "size"), first_date=("observation_date", "min"), last_date=("observation_date", "max"),
                                    observation_dates=("observation_date", "nunique"), series=("maturity_label", "nunique")))
cov["first_date"], cov["last_date"] = cov.first_date.dt.date, cov.last_date.dt.date
display(cov)

series = (df.groupby(["curve_type", "quote_basis", "maturity_label"]).observation_date.agg(["min", "max", "count"])
            .rename(columns={"min": "first", "max": "last", "count": "observations"}))
series["first"], series["last"] = series["first"].dt.date, series["last"].dt.date
print("Series start dates (maturities enter the data when Treasury first published them):")
display(series.loc[["par_nominal"]].sort_values("first"))'''))

cells.append(md("""## 3. Data-quality checks

The record key is `(observation_date, curve_type, quote_basis, maturity_label)`. Gaps are measured between consecutive observation dates; weekends and market holidays produce normal gaps of a few days, so only gaps longer than 5 calendar days are flagged."""))
cells.append(code('''dups = int(df.duplicated(KEY).sum())
print("Duplicate primary keys:", dups)
print("Weekend observation dates:", int((df.observation_date.dt.dayofweek >= 5).sum()))
print("\\nRows by curve_type / quote_basis:"); print(df.groupby(["curve_type", "quote_basis"]).size().to_string())
print("\\nvalue_pct range by curve_type / quote_basis:")
display(df.groupby(["curve_type", "quote_basis"]).value_pct.agg(["min", "median", "max"]))
neg = df[df.value_pct < 0].groupby(["curve_type", "quote_basis"]).size()
print("Negative values by series:"); print(neg.to_string() if len(neg) else "none")

gaps = {}
for c, g in df.groupby("curve_type"):
    d = g.observation_date.drop_duplicates().sort_values()
    gaps[c] = d.diff().dt.days.dropna()
print("\\nLargest gap between consecutive observation dates (calendar days):")
for c, s in gaps.items():
    print(f"  {c}: {int(s.max())} days; gaps > 5 days: {int((s > 5).sum())}")
assert dups == 0'''))

cells.append(md("""## 4. The latest nominal yield curve

Maturities are ordered by their actual length (converting week/month/year to months **for ordering only**), not alphabetically. We choose the most recent date whose set of maturities is the fullest seen over the last 30 observation dates, and print that date rather than assuming it is the final date."""))
cells.append(code('''MONTHS = {"week": 7 / 30.4375, "month": 1.0, "year": 12.0}
nom = df[(df.curve_type == "par_nominal") & (df.quote_basis == "par_yield")].copy()
nom["maturity_months"] = nom.maturity_value * nom.maturity_unit.map(MONTHS)
order = nom.drop_duplicates("maturity_label").sort_values("maturity_months").maturity_label.tolist()

counts = nom.groupby("observation_date").maturity_label.nunique()
recent = counts.tail(30)
curve_date = recent[recent == recent.max()].index.max()
curve = nom[nom.observation_date == curve_date].set_index("maturity_label").loc[lambda d: d.index.isin(order)].sort_values("maturity_months")
print(f"Selected date: {curve_date.date()}  ({len(curve)} maturities; last observation date is {counts.index.max().date()})")

fig, ax = plt.subplots()
ax.plot(range(len(curve)), curve.value_pct, marker="o")
ax.set_xticks(range(len(curve))); ax.set_xticklabels(curve.index)
ax.set_xlabel("Maturity (ordered by length; evenly spaced categories)"); ax.set_ylabel("Par yield (%)")
ax.set_title(f"U.S. Treasury nominal par yield curve, {curve_date.date()}")
plt.show()'''))

cells.append(md("## 5. Yield history for selected maturities"))
cells.append(code('''wide = nom.pivot(index="observation_date", columns="maturity_label", values="value_pct")
picks = [m for m in ["3M", "2Y", "10Y", "30Y"] if m in wide.columns]
fig, ax = plt.subplots()
for m in picks:
    ax.plot(wide.index, wide[m], lw=1, label=m)
ax.xaxis.set_major_locator(mdates.YearLocator(5)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_ylabel("Par yield (%)"); ax.set_title("Nominal Treasury par yields by maturity"); ax.legend(title="Maturity")
plt.show()
print("The 30Y series has a publication gap from 2002-02-19 to 2006-02-08 (no 30-year was issued); no values are filled:")
print("  30Y observations in 2003:", int(wide["30Y"].loc["2003"].notna().sum()))'''))

cells.append(md("""## 6. Nominal 10-year minus 2-year spread

Computed on matched dates only (both maturities present, one row per date and series by the record key). This is a **descriptive term-spread statistic**, not a recession predictor or a trading signal."""))
cells.append(code('''spread = (wide["10Y"] - wide["2Y"]).dropna().rename("spread_pp")
assert spread.index.is_unique
print(f"Matched dates: {len(spread):,}  ({spread.index.min().date()} to {spread.index.max().date()})")
print(spread.describe().round(3).to_string())
inv = int((spread < 0).sum())
print(f"\\nDates with 10Y - 2Y < 0: {inv:,} ({inv / len(spread):.1%})")

fig, ax = plt.subplots()
ax.plot(spread.index, spread, lw=0.8)
ax.fill_between(spread.index, spread, 0, where=spread < 0, color="tab:red", alpha=0.4, label="2Y above 10Y")
ax.axhline(0, color="k", lw=0.6)
ax.set_ylabel("Percentage points"); ax.set_title("Nominal par yield spread: 10Y minus 2Y"); ax.legend()
plt.show()'''))

cells.append(md("""## 7. Real (TIPS) par yields

Real yields begin in 2003 and the 30Y real point in 2010, so history is shorter than for nominal yields. A negative real yield means the inflation-adjusted return implied by the curve point was below zero; these values are retained."""))
cells.append(code('''real = df[(df.curve_type == "par_real")].pivot(index="observation_date", columns="maturity_label", values="value_pct")
real = real[[c for c in ["5Y", "10Y", "30Y"] if c in real.columns]]
print("Date range:", real.index.min().date(), "to", real.index.max().date())
print("Negative observations:", {c: int((real[c] < 0).sum()) for c in real.columns})
fig, ax = plt.subplots()
for c in real.columns:
    ax.plot(real.index, real[c], lw=1, label=c)
ax.axhline(0, color="k", lw=0.6)
ax.set_ylabel("Real par yield (%)"); ax.set_title("Real (TIPS) par yields"); ax.legend(title="Maturity")
plt.show()'''))

cells.append(md("""## 8. Treasury bill rates

Bills are quoted two ways in the source: **bank discount** (annualized discount from face value, on a 360-day basis) and **coupon equivalent** (a yield-style measure comparable to coupon securities). They are different conventions, so they are shown in separate panels rather than treated as interchangeable."""))
cells.append(code('''bills = df[df.curve_type == "bill_rate"]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True)
for ax, basis in zip(axes, ["bank_discount", "coupon_equivalent"]):
    w = bills[bills.quote_basis == basis].pivot(index="observation_date", columns="maturity_label", values="value_pct")
    for m in [c for c in ["4W", "13W", "26W", "52W"] if c in w.columns]:
        ax.plot(w.index, w[m], lw=0.9, label=m)
    ax.set_title(basis.replace("_", " ").title()); ax.set_ylabel("Rate (%)"); ax.legend(title="Maturity")
fig.suptitle("Treasury bill rates by quote basis"); fig.tight_layout(); plt.show()
print("Bill maturities and first dates:")
print(bills.groupby("maturity_label").observation_date.min().dt.date.sort_values().to_string())'''))

cells.append(md("## 9. Summary and limitations"))
cells.append(code('''last = nom.observation_date.max()
print("What the data show (all computed above):")
print(f"- {len(df):,} rows; {df.observation_date.min().date()} to {df.observation_date.max().date()}; {df.curve_type.nunique()} curve types, no duplicate keys.")
print(f"- On {curve_date.date()} the nominal curve spanned {curve.value_pct.min():.2f}% to {curve.value_pct.max():.2f}% across {len(curve)} maturities.")
print(f"- The 10Y-2Y spread was negative on {inv:,} of {len(spread):,} matched dates.")
print(f"- Real yields were negative on {int((df[df.curve_type=='par_real'].value_pct < 0).sum()):,} observations.")'''))
cells.append(md("""**Limitations.** This is a historical snapshot built from Treasury's published tables. `observation_date` is the market date of the observation, not a full point-in-time publication timestamp, and historical revisions are not preserved. Par yields are curve estimates and bill rates are indicative quotations, not guaranteed trading prices. Nothing here is investment advice or a forecast.

**Next steps.** See `data_dictionary.md` for column definitions, `methodology.md` for how the files were built, and `quality_report.md` for release checks. Source: U.S. Department of the Treasury, Daily Treasury Rates; compiled by FinChrona."""))

nb = nbf.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"}})
out = Path(__file__).parent / "finchrona-treasury-rates-eda.ipynb"
nbf.write(nb, out)
print("wrote", out.name, len(cells), "cells")
