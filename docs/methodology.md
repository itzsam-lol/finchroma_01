# Methodology

1. `scripts/download_data.py` fetches one CSV per curve per year (1990 to current year), records URL, retrieval time, size and SHA-256 in `data/raw/raw_manifest.json`. Years before a curve existed return an empty file and are skipped.
2. `finchrona.transforms.wide_to_long` melts each wide file to the canonical long schema, parses maturity headers into value+unit, splits bill columns into quote bases, and drops blank cells (no imputation, no forward fill).
3. Frames are concatenated, exact duplicates dropped (0 found), and sorted deterministically.
4. `finchrona.validation` checks schema, types, unique primary key, category values, positive maturities, no weekend dates.
5. `scripts/generate_reports.py` reconciles non-null source cells to output rows and writes coverage and quality reports.

Extreme values are never removed. Negative real yields (min -1.91) are genuine (2020-21 and other periods).

Integrity notes: survivorship bias and corporate actions do not apply (curves, not securities); identifier changes do not apply; temporal-leakage risk remains for users: `observation_date` is the close date and the value was not available before the close; Treasury may restate history, which this snapshot cannot detect.

Update procedure: rerun download with `--refresh` for the current year, rebuild, validate, regenerate reports, `python scripts/prepare_release.py`, then publish a new Kaggle version / HF commit / GitHub tag. Source-coverage changes (new data or Treasury restatement) bump the minor version; processing-logic changes are recorded in `CHANGELOG.md`.
