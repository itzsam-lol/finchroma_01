# FinChrona

*Open financial data, built for research.*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23730813.svg)](https://doi.org/10.5281/zenodo.23730813) [![Kaggle](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series) [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Dataset-yellow?logo=huggingface)](https://huggingface.co/datasets/samisonhf/finchrona)

FinChrona v1.0.0 is a curated historical dataset of **U.S. Treasury nominal par yields, real/TIPS par yields, and Treasury bill rates**, standardized into a consistent long-format schema. The release contains **180,815 rows and 7 columns**, with observations through **2026-10-23**. Source data was retrieved on **2026-10-25**.

## Access the dataset

- **Zenodo archive (version 1.0.0):** https://doi.org/10.5281/zenodo.23730813
- **Zenodo concept DOI (all versions):** https://doi.org/10.5281/zenodo.23730812
- **Kaggle dataset:** https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series
- **Hugging Face dataset:** https://huggingface.co/datasets/samisonhf/finchrona
- **Kaggle EDA notebook:** https://www.kaggle.com/code/samuraiiii/finchrona-treasury-rates-eda

The Parquet dataset is included in this repository at `data/processed/finchrona_treasury_rates.parquet`. The full release, including the CSV and supporting documentation, is available through the dataset links above.

## Dataset coverage

| Series (`curve_type`) | Coverage | Rows in v1.0.0 |
|---|---|---:|
| `par_nominal` | 1990-01-02 to 2026-10-23 | 99,894 |
| `par_real` | 2003-01-02 to 2026-10-23 | 27,609 |
| `bill_rate` | 2002-01-02 to 2026-10-23 | 53,312 |
| **Total** | Varies by series and maturity | **180,815** |

Bill rates include `bank_discount` and `coupon_equivalent` quote conventions. Coverage varies by series and maturity; a missing source maturity is not filled or forward-imputed.

## Schema

Each row represents one rate observation. The canonical columns are:

| Column | Description |
|---|---|
| `observation_date` | U.S. Treasury business date associated with the observation (`YYYY-MM-DD`); not a publication timestamp. |
| `curve_type` | `par_nominal`, `par_real`, or `bill_rate`. |
| `quote_basis` | `par_yield`, `bank_discount`, or `coupon_equivalent`, as appropriate to the series. |
| `maturity_label` | Compact maturity identifier such as `4W`, `1M`, `1.5M`, `2Y`, or `10Y`. |
| `maturity_value` | Numeric maturity quantity, interpreted together with `maturity_unit`. |
| `maturity_unit` | `week`, `month`, or `year`. |
| `value_pct` | Annualized rate in percentage units: `3.74` means `3.74%`, not `0.0374`. |

**Primary key:** `(observation_date, curve_type, quote_basis, maturity_label)`.

See [`docs/data_dictionary.md`](docs/data_dictionary.md) for full definitions, types, units, and conventions.

## Quickstart

Install the project and its development dependencies:

```bash
pip install -e ".[dev]"
```

Run the example:

```bash
python examples/quickstart.py
```

The quickstart loads the Parquet dataset, checks basic data quality, and plots the nominal 10-year minus 2-year term spread. In the v1.0.0 snapshot, the spread was negative on 1,052 of 9,209 matched observation dates. This is a descriptive statistic, not a forecast or a trading signal.

## Reproduce the dataset build

The public-source pipeline can be run without private credentials, subject to source availability and applicable source terms:

```bash
pip install -e ".[dev]"
python scripts/download_data.py
python scripts/build_dataset.py
python scripts/validate_dataset.py
python scripts/generate_reports.py
pytest
```

The download step retrieves yearly Treasury CSV files and may take several minutes due to request spacing and source response times. See [`docs/methodology.md`](docs/methodology.md) for the detailed workflow and refresh procedure.

## Data quality

The v1.0.0 validation report records:

- 180,815 rows and 7 columns.
- No null values in the processed output.
- No duplicate primary keys.
- 180,815 non-null source cells reconciled to 180,815 output rows.
- Negative observations are retained where present: 5,032 in total in this release (4,940 real-yield observations and 92 bill-rate observations).

These checks describe the processed snapshot; they do not guarantee that every source observation is error-free. Read [`reports/quality_report.md`](reports/quality_report.md) for detailed coverage and validation results.

## Methodology and provenance

The dataset is compiled from the U.S. Department of the Treasury's official [Daily Treasury Rates](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics) data. The pipeline downloads the published CSV tables, records source and file-integrity information, transforms the source tables into long format, standardizes maturity labels and quote conventions, and validates the result.

Relevant documentation:

- [`docs/methodology.md`](docs/methodology.md)
- [`docs/data_dictionary.md`](docs/data_dictionary.md)
- [`reports/quality_report.md`](reports/quality_report.md)
- [`docs/data_card.md`](docs/data_card.md)
- [`docs/licensing_and_attribution.md`](docs/licensing_and_attribution.md)

FinChrona is independently maintained and is not affiliated with or endorsed by the U.S. Department of the Treasury.

## Limitations

- **Historical snapshot, not point-in-time:** the release does not preserve complete publication timestamps or a full history of source revisions. `observation_date` must not be treated as the earliest time information was available.
- **No imputation:** blank source cells are omitted; maturities appear only when present in the published source.
- **Model-derived rates:** Treasury par yields are curve points, not guaranteed executable trading prices. Bill rates retain their published quote conventions.
- **Daily frequency:** this is not a real-time market feed.
- **Coverage varies:** series start dates and available maturities differ. The 30-year nominal series has a source gap from 2002-02-19 through 2006-02-08, as documented in the source data.
- **No investment advice:** the dataset is for research and analysis, not trading recommendations.

For forecasting or backtesting, check that each input would have been available at the simulated prediction time and use an evaluation design appropriate for time-series data.

## Licensing

- **Code:** MIT License; see [`LICENSE`](LICENSE).
- **Dataset:** the compiled dataset is designated CC0 1.0 in [`docs/licensing_and_attribution.md`](docs/licensing_and_attribution.md).

The licensing documentation records that no explicit dataset-licence text was found on the Treasury pages inspected and explains the project's rationale and residual uncertainty. Users should review that document and applicable source terms, particularly for uses outside the United States. The MIT licence for the repository code should not be read as replacing the separately documented dataset terms.

## Cite FinChrona

For the exact v1.0.0 release, cite:

> Satyam. (2026). *FinChrona v1.0.0: Open Financial Time Series | U.S. Treasury Rates, 1990–2026* (Version 1.0.0) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.23730813

- **Version DOI:** [10.5281/zenodo.23730813](https://doi.org/10.5281/zenodo.23730813)
- **Concept DOI (all versions):** [10.5281/zenodo.23730812](https://doi.org/10.5281/zenodo.23730812)

BibTeX:

```bibtex
@misc{satyam2026finchrona,
  author    = {Satyam},
  title     = {FinChrona v1.0.0: Open Financial Time Series | U.S. Treasury Rates, 1990--2026},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.0.0},
  doi       = {10.5281/zenodo.23730813},
  url       = {https://doi.org/10.5281/zenodo.23730813},
  note      = {Dataset}
}
```

## Release policy

The published release is v1.0.0, with an observation cutoff of 2026-10-23. The intended maintenance cadence is quarterly and manual; this is a target, not an automated update or guarantee. New releases should document coverage changes, source revisions, transformation changes, and updated checksums.

## Issues and contributions

Please open a [GitHub issue](https://github.com/itzsam-lol/finchroma_01/issues) to report a data-quality problem, suggest an improvement, or discuss a contribution. Reproducible bug reports should include the affected file, observation date or record key, and steps to reproduce the issue. Do not include secrets or private credentials in issues.
