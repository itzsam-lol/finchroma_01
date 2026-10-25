# Kaggle final audit (2026-10-25)

No metadata or data was changed during this audit, and no dataset version was created. All checks below were read-only.

## Verified facts
**Live metadata (CLI `kaggle datasets metadata`, fetched fresh):** title and subtitle as intended; licence `CC0-1.0`; keywords `finance`, `economics`; `expectedUpdateFrequency: quarterly`; `userSpecifiedSources` present (1,261 characters); `usabilityRating: 0.7059` (7.06). Dataset status `ready`.

**CLI limitation:** the metadata download returns only an `info` object. It does not return `resources`, file descriptions or column schemas, and the file-listing call returns names and sizes only (it showed empty descriptions even for files whose descriptions the UI displays). So `resources` could not be read back via the CLI, and the local `kaggle_meta/dataset-metadata.json` is the only record of what was submitted.

**Files:** the 9 published files match the 9 `resources` paths exactly (names and sizes checked with `kaggle datasets files`).

**File descriptions (checked on each file's page):** all 9 render under "About this file" with the intended text: README.md, data_dictionary.md, finchrona_treasury_rates.csv, finchrona_treasury_rates.parquet, licensing_and_attribution.md, methodology.md, quality_report.md, release_manifest.json, sample_last_60_days.csv.

**Provenance and update frequency (public page):** the Sources panel shows the applied text; "Expected update frequency" shows Quarterly. The CSV page lists all 7 columns in order.

**Notebook:** public at https://www.kaggle.com/code/samuraiiii/finchrona-treasury-rates-eda, Version 1 of 1, input `samuraiiii/finchrona-financial-time-series`. On the rendered page I confirmed the intro, load output (shape 180815x7, "Loaded Parquet"), coverage tables, the nominal yield-curve chart (selected date 2026-10-23, 14 maturities) and the real-yield chart. The Kaggle log has no tracebacks and the run status was COMPLETE. I did not scroll to the bill-rate and summary cells.

## Not verified / unresolved
1. **Column descriptors do not display.** The CSV's Detail, Compact and Column views and the file edit dialog show no column description text, and I found no visible description for any of the 7 columns. The CLI accepted the `schema.fields` (7 fields, correct order, supported types per the documentation) without error, but I cannot show that Kaggle stored them. **Treat as not applied.**
2. **Pending Actions cards still show all four items** even though update frequency visibly shows Quarterly and Sources is populated. So the cards are not a reliable indicator, or they are evaluated on something other than what is displayed. I could not determine which; the cause is unknown. Not claimed complete.
3. **Provenance "Collection Methodology" field is empty.** Kaggle's provenance editor has two boxes, Sources and Collection Methodology. The CLI only sets Sources (`userSpecifiedSources`). This is a plausible reason the provenance card persists, but it is unproven.
4. **Usability score:** original 7.06; final observed 7.06 (unchanged, since nothing was changed).

## Cause assessment (assumptions, not verified)
- Column schemas may only be stored when supplied through `kaggle datasets version`/`create` rather than `metadata --update`. The documentation does not say. Testing this requires a new dataset version.
- The score may be recomputed only at version time; it did move from 6.47 to 7.06 after the metadata update, so this is uncertain.

## Recommended actions (not performed; need your decision)
1. **Manual, low risk:** open https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series/data, scroll to Metadata > Provenance, click Edit, and fill Collection Methodology, e.g. "Public Treasury CSV files (one per curve per year, 1990 to 2026) were downloaded with a documented pipeline, converted to a long schema, normalized for maturity labels and quote conventions, and validated. No values were imputed. See methodology.md." Then Save. Then reload and check whether the provenance card clears.
2. **Needs approval (creates a new dataset version v2):** if column descriptors still do not appear, run from a staged folder containing the same files plus `dataset-metadata.json`: `kaggle datasets version -p <folder> -m "Add column descriptors"`. This re-uploads the data. I did not do it because the instructions say to avoid a new version unless necessary and because it is unproven to fix the issue.
3. **Update cadence:** Quarterly is kept, but it is a single-maintainer manual target. If that is not sustainable, change it to `not specified` with `kaggle datasets metadata --update`.

## Limitations of this audit
Kaggle's UI state could be read only through the page and a screenshot of rendered output; no private API was used. Tab, cache or propagation delays could affect what I saw.
