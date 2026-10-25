# Final release report: FinChrona v1.0.0

## Dataset
US Treasury daily par nominal, par real and bill rates; 180,815 rows, 7 columns; 1990-01-02 to 2026-10-23 (cutoff). Parquet 326,516 B (sha256 `cdbb54e2f00fafe80e6e749dc252915aa0852fc9cae101b4865098f7938689ba`), CSV 9,523,188 B (sha256 `51b491451672db5f6d1bdf4a2cde391ee1adf81804e4341e219716e6ad49f3dd`). Chosen for redistribution clarity and coherence (docs/dataset_decision.md). Licence: US Government work; compiled data CC0 1.0; residual uncertainty documented in docs/licensing_and_attribution.md.

## Release status
| Destination | Status |
|---|---|
| GitHub https://github.com/itzsam-lol/finchroma_01 | published and verified (commit ab58bac on main, README reachable) |
| Kaggle https://www.kaggle.com/datasets/samuraiiii/finchrona-financial-time-series | published and verified (status ready, page 200, 9 files, sizes match manifest) |
| Hugging Face | **not published**: the local token was rejected as invalid; run `hf auth login`, then `hf repos create <user>/finchrona --repo-type dataset` and `hf upload <user>/finchrona release . --repo-type dataset` after `python scripts/prepare_release.py --kaggle-user samuraiiii` |

## Tests
`pytest`: 8 passed. `validate_dataset.py`: OK. Quickstart executed.

## Next steps
1. Add FiscalData/SEC datasets. 2. Capture publication-time snapshots for point-in-time use. 3. Scheduled incremental updates.
