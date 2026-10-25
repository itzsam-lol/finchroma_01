"""Build curated dataset from data/raw. Usage: python scripts/build_dataset.py"""
import json

from finchrona import config, transforms
from finchrona.validation import validate

if __name__ == "__main__":
    df, recon = transforms.build()
    errs = validate(df)
    if errs:
        raise SystemExit(f"validation failed: {errs}")
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    config.SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(config.PROCESSED_DIR / "finchrona_treasury_rates.parquet", index=False, compression="zstd")
    df.to_csv(config.PROCESSED_DIR / "finchrona_treasury_rates.csv", index=False, date_format="%Y-%m-%d")
    cutoff = df["observation_date"].max()
    df[df["observation_date"] >= cutoff - __import__("pandas").Timedelta(days=60)].to_csv(
        config.SAMPLE_DIR / "sample_last_60_days.csv", index=False, date_format="%Y-%m-%d")
    (config.PROCESSED_DIR / "build_reconciliation.json").write_text(json.dumps(recon, indent=1))
    print(len(df), "rows;", recon)
