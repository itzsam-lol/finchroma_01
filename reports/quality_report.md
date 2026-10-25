# Quality report (v1.0.0)

Generated 2026-10-25T13:11:46Z from `finchrona_treasury_rates.parquet`.

- Rows: **180,815**; columns: 7
- Date range: 1990-01-02 to 2026-10-23
- Duplicate primary keys: 0
- Null counts: {'observation_date': 0, 'curve_type': 0, 'quote_basis': 0, 'maturity_label': 0, 'maturity_value': 0, 'maturity_unit': 0, 'value_pct': 0}
- Validation failures: none
- Value range (percent): -1.91 to 9.18; negative values: 5032
- Source-to-output reconciliation: 180,815 non-null source cells -> 180,815 rows (equal: True)

## Coverage by curve

| curve | rows | days | first | last | max gap (days) | gaps >5d |
|---|---|---|---|---|---|---|
| bill_rate | 53,312 | 6,207 | 2002-01-02 | 2026-10-23 | 4 | 0 |
| par_nominal | 99,894 | 9,209 | 1990-01-02 | 2026-10-23 | 4 | 0 |
| par_real | 27,609 | 5,957 | 2003-01-02 | 2026-10-23 | 4 | 0 |

## Files

| file | bytes | sha256 |
|---|---|---|
| finchrona_treasury_rates.csv | 9,523,188 | `51b491451672db5f6d1bdf4a2cde391ee1adf81804e4341e219716e6ad49f3dd` |
| finchrona_treasury_rates.parquet | 326,516 | `cdbb54e2f00fafe80e6e749dc252915aa0852fc9cae101b4865098f7938689ba` |

Per-series coverage: `reports/series_coverage.csv`.
