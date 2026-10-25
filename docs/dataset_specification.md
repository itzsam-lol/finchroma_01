# Dataset specification: FinChrona Treasury Rates v1.0.0

1. **Purpose / users:** a clean, research-ready daily history of US Treasury yield curves for students, quants and ML researchers (term-structure studies, macro-finance features, teaching).
2. **Use cases:** yield-curve plots, term spreads, real vs nominal comparisons, bill-rate studies.
3. **Source:** US Department of the Treasury, Daily Treasury Par Yield Curve Rates, Par Real Yield Curve Rates and Bill Rates. https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics
4. **Population:** every maturity Treasury published for these three curves; no exclusions.
5. **Coverage:** par_nominal 1990-01-02, par_real 2003-01-02, bill_rate 2002-01-02, each to the cutoff **2026-10-23** (last business day in the build; retrieved 2026-10-25).
6. **Frequency:** daily, US business days on which Treasury published.
7. **Unit of observation:** one rate for one curve, quote basis and maturity on one date.
8. **Primary key:** `(observation_date, curve_type, quote_basis, maturity_label)`.
9. **Identifiers:** maturity label plus numeric value and unit; no security identifiers (these are curve points, not instruments).
10. **Timestamps:** `observation_date` is the US trading date of the closing bid-side quotes (America/New_York calendar date, no time of day). Publication time is not provided by the source, so this dataset is **not point-in-time**.
11. **Columns:** see `data_dictionary.md`.
12. **Missing values:** a blank source cell (maturity not yet offered or not published, e.g. 30Y 2002-02-19 to 2006-02-08) produces no row. Nothing is imputed.
13. **Method:** `docs/methodology.md`.
14. **Quality requirements:** schema validation, unique keys, no weekend dates, source cells equal output rows (`reports/quality_report.md`).
15. **Limitations:** no revision history (Treasury may restate), no intraday data, par yields are interpolated curve points rather than traded prices, bill rates are indicative quotes, negative real yields are genuine.
16. **Licence:** `licensing_and_attribution.md`.
17. **Versioning:** SemVer; `v1.0.0` is the first full-history snapshot. New data only extends the cutoff (minor), schema changes bump major.
18. **Artifacts:** Parquet (zstd, primary, ~0.3 MB), CSV (~9.5 MB), 60-day CSV sample.
