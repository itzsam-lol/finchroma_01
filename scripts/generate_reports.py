"""Generate quality and source-profile reports from actual data."""
import json

import pandas as pd

from finchrona import config
from finchrona.provenance import sha256_file, utc_now
from finchrona.validation import validate

if __name__ == "__main__":
    pq = config.PROCESSED_DIR / "finchrona_treasury_rates.parquet"
    df = pd.read_parquet(pq)
    recon = json.loads((config.PROCESSED_DIR / "build_reconciliation.json").read_text())
    raw_manifest = json.loads((config.RAW_DIR / "raw_manifest.json").read_text())
    errs = validate(df)

    series = (df.groupby(["curve_type", "quote_basis", "maturity_label"])["observation_date"]
              .agg(["min", "max", "count"]).reset_index())
    series["min"] = series["min"].dt.strftime("%Y-%m-%d")
    series["max"] = series["max"].dt.strftime("%Y-%m-%d")
    by_curve = {}
    for c, g in df.groupby("curve_type"):
        days = g["observation_date"].drop_duplicates().sort_values()
        gaps = days.diff().dt.days
        by_curve[c] = {
            "rows": int(len(g)), "observation_days": int(days.nunique()),
            "first_date": days.min().strftime("%Y-%m-%d"), "last_date": days.max().strftime("%Y-%m-%d"),
            "max_gap_calendar_days": int(gaps.max()), "gaps_over_5_days": int((gaps > 5).sum()),
        }
    v = df["value_pct"]
    q = {
        "generated_utc": utc_now(), "dataset_version": config.DATASET_VERSION,
        "rows": int(len(df)), "columns": {c: str(t) for c, t in df.dtypes.items()},
        "null_counts": {c: int(n) for c, n in df.isna().sum().items()},
        "duplicate_primary_keys": int(df.duplicated(config.PRIMARY_KEY).sum()),
        "validation_failures": errs,
        "date_min": df["observation_date"].min().strftime("%Y-%m-%d"),
        "date_max": df["observation_date"].max().strftime("%Y-%m-%d"),
        "value_pct_min": float(v.min()), "value_pct_max": float(v.max()),
        "negative_values": int((v < 0).sum()),
        "reconciliation": {**recon, "rows_equal_source_non_null_cells": recon["source_non_null_cells"] == recon["rows_after_dedup"]},
        "by_curve": by_curve, "raw_files": len(raw_manifest),
        "files": {p.name: {"bytes": p.stat().st_size, "sha256": sha256_file(p)}
                  for p in sorted(config.PROCESSED_DIR.glob("finchrona_treasury_rates.*"))},
    }
    config.REPORT_DIR.mkdir(exist_ok=True)
    (config.REPORT_DIR / "quality_report.json").write_text(json.dumps(q, indent=1))
    series.to_csv(config.REPORT_DIR / "series_coverage.csv", index=False)

    profile = {"generated_utc": utc_now(), "source_files": len(raw_manifest),
               "total_raw_bytes": sum(m["bytes"] for m in raw_manifest),
               "series_count": int(len(series)),
               "series": series.to_dict("records")}
    (config.REPORT_DIR / "source_profile.json").write_text(json.dumps(profile, indent=1))

    md = [f"# Quality report (v{config.DATASET_VERSION})", "",
          f"Generated {q['generated_utc']} from `{pq.name}`.", "",
          f"- Rows: **{q['rows']:,}**; columns: {len(q['columns'])}",
          f"- Date range: {q['date_min']} to {q['date_max']}",
          f"- Duplicate primary keys: {q['duplicate_primary_keys']}",
          f"- Null counts: {q['null_counts']}",
          f"- Validation failures: {errs or 'none'}",
          f"- Value range (percent): {q['value_pct_min']} to {q['value_pct_max']}; negative values: {q['negative_values']}",
          f"- Source-to-output reconciliation: {recon['source_non_null_cells']:,} non-null source cells -> {recon['rows_after_dedup']:,} rows (equal: {q['reconciliation']['rows_equal_source_non_null_cells']})",
          "", "## Coverage by curve", "",
          "| curve | rows | days | first | last | max gap (days) | gaps >5d |", "|---|---|---|---|---|---|---|"]
    for c, s in by_curve.items():
        md.append(f"| {c} | {s['rows']:,} | {s['observation_days']:,} | {s['first_date']} | {s['last_date']} | {s['max_gap_calendar_days']} | {s['gaps_over_5_days']} |")
    md += ["", "## Files", "", "| file | bytes | sha256 |", "|---|---|---|"]
    md += [f"| {n} | {f['bytes']:,} | `{f['sha256']}` |" for n, f in q["files"].items()]
    md += ["", "Per-series coverage: `reports/series_coverage.csv`."]
    (config.REPORT_DIR / "quality_report.md").write_text("\n".join(md) + "\n")

    pm = ["# Source profile", "", f"Generated {profile['generated_utc']} from the downloaded raw files.", "",
          f"- Raw files: {profile['source_files']} ({profile['total_raw_bytes']:,} bytes)",
          f"- Distinct series (curve x basis x maturity): {profile['series_count']}", "",
          "| curve | basis | maturity | first | last | observations |", "|---|---|---|---|---|---|"]
    pm += [f"| {r['curve_type']} | {r['quote_basis']} | {r['maturity_label']} | {r['min']} | {r['max']} | {r['count']:,} |" for r in profile["series"]]
    (config.REPORT_DIR / "source_profile.md").write_text("\n".join(pm) + "\n")
    print(json.dumps({k: q[k] for k in ("rows", "date_min", "date_max", "validation_failures")}))
