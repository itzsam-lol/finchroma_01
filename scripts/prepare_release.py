"""Stage release/ (Parquet, CSV, sample, docs, manifest) and Kaggle metadata.

Usage: python scripts/prepare_release.py --kaggle-user USER [--hf-user USER] [--github-url URL]
"""
import argparse
import json
import shutil

from finchrona import config
from finchrona.provenance import sha256_file, utc_now

p = argparse.ArgumentParser()
p.add_argument("--kaggle-user", required=True)
a = p.parse_args()

rel = config.RELEASE_DIR
if rel.exists():
    shutil.rmtree(rel)
rel.mkdir()
q = json.loads((config.REPORT_DIR / "quality_report.json").read_text())

roles = {}
for name in ("finchrona_treasury_rates.parquet", "finchrona_treasury_rates.csv"):
    shutil.copy(config.PROCESSED_DIR / name, rel / name)
    roles[name] = "primary analytical file" if name.endswith("parquet") else "CSV copy of the same data"
shutil.copy(config.SAMPLE_DIR / "sample_last_60_days.csv", rel / "sample_last_60_days.csv")
roles["sample_last_60_days.csv"] = "small sample (most recent 60 days)"
for doc in ("data_dictionary.md", "methodology.md", "licensing_and_attribution.md"):
    shutil.copy(config.ROOT / "docs" / doc, rel / doc)
    roles[doc] = "documentation"
shutil.copy(config.REPORT_DIR / "quality_report.md", rel / "quality_report.md")
roles["quality_report.md"] = "documentation"
shutil.copy(config.ROOT / "docs" / "data_card.md", rel / "README.md")
roles["README.md"] = "dataset card"

manifest = {
    "dataset": "FinChrona: Open Financial Time Series", "version": config.DATASET_VERSION,
    "cutoff_date": q["date_max"], "generated_utc": utc_now(), "rows": q["rows"],
    "files": [{"name": n, "role": r, "bytes": (rel / n).stat().st_size, "sha256": sha256_file(rel / n)}
              for n, r in roles.items()],
}
(rel / "release_manifest.json").write_text(json.dumps(manifest, indent=1))
shutil.copy(rel / "release_manifest.json", config.REPORT_DIR / "release_manifest.json")

meta = {
    "title": "FinChrona: Open Financial Time Series",
    "id": f"{a.kaggle_user}/finchrona-financial-time-series",
    "subtitle": "Daily US Treasury par, real and bill rates, 1990-2026, one clean schema",
    "description": (rel / "README.md").read_text(encoding="utf-8").split("---", 2)[-1].strip()
    if (rel / "README.md").read_text(encoding="utf-8").startswith("---")
    else (rel / "README.md").read_text(encoding="utf-8"),
    "licenses": [{"name": "CC0-1.0"}],
    "keywords": ["finance", "economics", "time series", "interest rates", "treasury"],
}
(rel / "dataset-metadata.json").write_text(json.dumps(meta, indent=1))
print("staged", len(manifest["files"]), "files in", rel)
