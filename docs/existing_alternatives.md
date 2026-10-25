# Existing alternatives

- **Treasury's own site** publishes the same numbers as one CSV per curve per year with differing column sets (new maturities such as 1.5 Month, 2 Mo and 4 Mo were added over time). FinChrona does not claim new data; it provides one schema across all years and curves.
- **FRED** (Treasury constant maturity series, e.g. DGS10) offers convenient access, but its terms prohibit caching/archiving, so FinChrona does not use it.
- **Kaggle / Hugging Face / GitHub** host various community copies of Treasury yield data of varying provenance and coverage. A systematic comparison was not performed; no claim of uniqueness is made.

Contribution is engineering only: a consistent long schema, explicit maturity units, no imputation, checksummed raw files, a rebuild pipeline and a quality report.
