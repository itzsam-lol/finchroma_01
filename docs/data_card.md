# FinChrona: Open Financial Time Series

*Open financial data, built for research.* Version 1.0.0, cutoff 2026-10-23.

## What this is
Daily US Treasury par yield curves (nominal and real/TIPS) and Treasury bill rates, reshaped into one long schema: 180,815 rows, 7 columns, 1990-01-02 to 2026-10-23.

| curve_type | coverage | rows |
|---|---|---|
| par_nominal | 1990-01-02 .. 2026-10-23 | 99,894 |
| par_real | 2003-01-02 .. 2026-10-23 | 27,609 |
| bill_rate (bank discount and coupon equivalent) | 2002-01-02 .. 2026-10-23 | 53,312 |

## Files
- `finchrona_treasury_rates.parquet`: primary file.
- `finchrona_treasury_rates.csv`: same data.
- `sample_last_60_days.csv`, `data_dictionary.md`, `methodology.md`, `quality_report.md`, `release_manifest.json` (SHA-256 of every file).

## Columns
`observation_date`, `curve_type`, `quote_basis`, `maturity_label`, `maturity_value`, `maturity_unit`, `value_pct` (percent per annum). Primary key: `(observation_date, curve_type, quote_basis, maturity_label)`. See `data_dictionary.md`.

## Usage
```python
import pandas as pd
df = pd.read_parquet("finchrona_treasury_rates.parquet")
nom = df[df.curve_type == "par_nominal"].pivot(index="observation_date", columns="maturity_label", values="value_pct")
spread = nom["10Y"] - nom["2Y"]
```

## Source and licence
Source: U.S. Department of the Treasury, Daily Treasury Rates (https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics), retrieved 2026-10-25. US Government work, not subject to US copyright; the compiled dataset is released under CC0 1.0. Treasury publishes no explicit licence text on the pages inspected; see `licensing_and_attribution.md`. Not endorsed by the Treasury.

## Quality
Zero duplicate keys, zero nulls, no weekend dates; 180,815 non-null source cells map to exactly 180,815 rows. 5,032 negative values exist (4,940 real yields, 92 bill rates); these are genuine, not errors.

## Limitations
- Blank source cells (maturity not offered) have no row; nothing is imputed. The 30Y nominal series is absent 2002-02-19 to 2006-02-08, as published.
- Not point-in-time: no publication timestamps or revision history; Treasury may restate values.
- Par yields are modelled curve points, bill rates are indicative quotes; neither is a tradable price.
- Daily frequency only; not real-time. Not investment advice.

## Links
GitHub: https://github.com/itzsam-lol/finchroma_01 · Kaggle: https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series

## Citation
FinChrona: Open Financial Time Series, v1.0.0 (2026). https://github.com/itzsam-lol/finchroma_01
