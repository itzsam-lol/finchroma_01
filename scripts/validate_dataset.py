"""Validate the processed Parquet file. Exit code 1 on failure."""
import pandas as pd

from finchrona import config
from finchrona.validation import validate

if __name__ == "__main__":
    path = config.PROCESSED_DIR / "finchrona_treasury_rates.parquet"
    errs = validate(pd.read_parquet(path))
    print("FAILED:" if errs else "OK: dataset passes all checks", *errs, sep="\n")
    raise SystemExit(1 if errs else 0)
