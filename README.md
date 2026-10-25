# FinChrona

*Open financial data, built for research.*

FinChrona v1.0.0 is a daily history of **US Treasury par yield curves (nominal and real/TIPS) and bill rates**, 1990-01-02 to 2026-10-23, in one consistent long schema (180,815 rows, 7 columns). Source: U.S. Department of the Treasury, Daily Treasury Rates.

- Kaggle: https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series
- Hugging Face: not yet published (credentials unavailable at release time)
- Parquet file in this repo: `data/processed/finchrona_treasury_rates.parquet`; CSV and docs on Kaggle.

## Schema
`observation_date, curve_type, quote_basis, maturity_label, maturity_value, maturity_unit, value_pct` (percent per annum). Key: `(observation_date, curve_type, quote_basis, maturity_label)`. Details: [docs/data_dictionary.md](docs/data_dictionary.md).

## Quickstart
```bash
pip install -e ".[dev]"
python examples/quickstart.py     # loads the Parquet, checks quality, plots the 10Y-2Y term spread
```
On the real data, the 10Y minus 2Y spread was negative on 1,052 of 9,209 days. This is a descriptive statistic, not a forecast.

## Reproduce the build (public, no credentials)
```bash
pip install -e ".[dev]"
python scripts/download_data.py        # slow: ~90 yearly CSVs, 1 s delay, server ~20 s/request
python scripts/build_dataset.py
python scripts/validate_dataset.py
python scripts/generate_reports.py
pytest
```

## Validation
Zero duplicate keys and nulls; 180,815 non-null source cells map to exactly 180,815 rows. See [reports/quality_report.md](reports/quality_report.md) and [docs/methodology.md](docs/methodology.md).

## Limitations
Not point-in-time (no publication timestamps or revisions); no imputation, so maturities appear only when published; par yields are modelled points; daily snapshot, not real-time. See [docs/data_card.md](docs/data_card.md).

## Licence
Code and docs: MIT. Data: US Government work; compiled dataset under CC0 1.0. Treasury publishes no explicit licence text on the pages inspected; see [docs/licensing_and_attribution.md](docs/licensing_and_attribution.md). Cite via `CITATION.cff`.

## Issues and contributions
Open a GitHub issue or pull request.
