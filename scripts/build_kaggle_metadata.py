"""Write Kaggle dataset-metadata.json (files, columns, provenance, cadence) for the live dataset.

Apply with:  kaggle datasets metadata samuraiiii/finchrona-financial-time-series --update -p kaggle_meta
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "kaggle_meta"
OUT.mkdir(exist_ok=True)

COLUMNS = [
    ("observation_date", "datetime", "The U.S. Treasury business date associated with the rate observation, represented as YYYY-MM-DD. This is the observation date, not necessarily the date the information first became publicly available."),
    ("curve_type", "string", "Identifies the rate series: `par_nominal` for the nominal Treasury par yield curve, `par_real` for the real/TIPS par yield curve, or `bill_rate` for Treasury bill rates."),
    ("quote_basis", "string", "Specifies the source quote convention. Par yield observations use `par_yield`; Treasury bill observations use `bank_discount` or `coupon_equivalent`, as provided by the source."),
    ("maturity_label", "string", "A compact maturity identifier, such as `4W`, `1M`, `1.5M`, `2Y` or `10Y`, used to filter and compare rate observations."),
    ("maturity_value", "numeric", "The numeric maturity quantity associated with the observation. Interpret this value together with `maturity_unit`; it is not a standalone duration in years."),
    ("maturity_unit", "string", "The unit associated with `maturity_value`: week, month or year. The unit is retained as represented by the source rather than silently converting all maturities into a common unit."),
    ("value_pct", "numeric", "The annualized rate expressed in percentage units, not as a decimal fraction. For example, 3.74 represents 3.74%. Negative real yields and bill-rate observations are retained when present in the source."),
]
SCHEMA = {"fields": [{"name": n, "title": n, "type": t, "description": d} for n, t, d in COLUMNS]}

FILES = {
    "finchrona_treasury_rates.parquet": ("The complete curated FinChrona dataset in Parquet format. Contains daily U.S. Treasury nominal par yields, real/TIPS par yields, and Treasury bill rates in a seven-column long-format schema. Intended as the primary file for analytical and research workflows.", True),
    "finchrona_treasury_rates.csv": ("CSV representation of the complete FinChrona dataset, containing the same observations and schema as the primary Parquet file. Suitable for spreadsheets, general-purpose data tools, and workflows that do not support Parquet.", True),
    "sample_last_60_days.csv": ("A small extract from the end of the historical dataset (the most recent 60 calendar days before the cutoff) for inspecting the schema and testing analysis workflows without loading the complete dataset.", True),
    "data_dictionary.md": ("Column-level reference defining data types, units, valid values, quote conventions, missingness semantics, and the record key.", False),
    "methodology.md": ("Documentation of source acquisition, transformations from the Treasury's published tables, maturity normalization, data organization, validation, reproducibility, and known limitations.", False),
    "licensing_and_attribution.md": ("Documents the source terms investigated for FinChrona, the project's licensing rationale, requested attribution, and unresolved legal uncertainties.", False),
    "quality_report.md": ("Machine-generated quality summary documenting row counts, historical coverage, missingness, duplicate checks, value ranges, and source-to-output reconciliation for this release.", False),
    "README.md": ("Dataset card: overview of FinChrona's purpose, contents, schema, provenance, usage example, coverage, licensing, and limitations.", False),
    "release_manifest.json": ("Release-integrity manifest recording dataset version, cutoff date, file sizes, SHA-256 checksums, and artifact roles.", False),
}
resources = []
for path, (desc, tabular) in FILES.items():
    r = {"path": path, "description": desc}
    if tabular:
        r["schema"] = SCHEMA
    resources.append(r)

SOURCES = (
    "FinChrona v1.0.0 was compiled from the U.S. Department of the Treasury's official Daily Treasury Rates data.\n\n"
    "Official source: https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics\n\n"
    "The source files were retrieved on 2026-10-25, with a release cutoff date of 2026-10-23. The release combines nominal par yields, "
    "real/TIPS par yields and Treasury bill rates into a consistent seven-column long-format schema.\n\n"
    "The reproducible pipeline acquires public Treasury CSV files, records source URLs and file checksums, transforms the original tables "
    "into long format, normalizes maturity labels and quote conventions, and executes schema and data-quality checks.\n\n"
    "Blank source cells are not imputed or forward-filled. The dataset preserves negative real yields and bill-rate values where the source reports them.\n\n"
    "This release is a historical snapshot. It does not preserve complete publication timestamps or a historical record of revisions. "
    "It is not a real-time feed and is not investment advice.\n\n"
    "See the dataset card, data dictionary, methodology and licensing documentation for detailed definitions, attribution and limitations. "
    "FinChrona is independently maintained and is not affiliated with or endorsed by the U.S. Treasury."
)

meta = {
    "title": "FinChrona: Open Financial Time Series",
    "id": "samuraiiii/finchrona-financial-time-series",
    "subtitle": "Daily US Treasury par, real/TIPS and bill rates, 1990-2026, in one long schema",
    "description": (ROOT / "docs" / "data_card.md").read_text(encoding="utf-8"),
    "licenses": [{"name": "CC0-1.0"}],
    "keywords": ["finance", "economics"],
    "expectedUpdateFrequency": "quarterly",
    "userSpecifiedSources": SOURCES,
    "resources": resources,
}
(OUT / "dataset-metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
assert all(len(r["schema"]["fields"]) == 7 for r in resources if "schema" in r)
assert len(meta["subtitle"]) <= 80
print("wrote", OUT / "dataset-metadata.json", "-", len(resources), "resources")
