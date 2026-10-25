"""Schema and integrity checks. validate() returns a list of failure messages."""
import pandas as pd

from . import config


def validate(df: pd.DataFrame) -> list[str]:
    errs = []
    missing = [c for c in config.COLUMNS if c not in df.columns]
    if missing:
        return [f"missing columns: {missing}"]
    dates_ok = pd.api.types.is_datetime64_any_dtype(df["observation_date"])
    if not dates_ok:
        errs.append("observation_date is not datetime")
    elif df["observation_date"].isna().any():
        errs.append("null observation_date")
    if not pd.api.types.is_numeric_dtype(df["value_pct"]):
        errs.append("value_pct is not numeric")
    elif df["value_pct"].isna().any():
        errs.append("null value_pct")
    dup = int(df.duplicated(config.PRIMARY_KEY).sum())
    if dup:
        errs.append(f"{dup} duplicate primary keys")
    if not set(df["curve_type"].dropna()) <= config.CURVE_TYPES:
        errs.append("invalid curve_type values")
    if not set(df["quote_basis"].dropna()) <= config.QUOTE_BASIS_VALUES:
        errs.append("invalid quote_basis values")
    if not set(df["maturity_unit"].dropna()) <= config.MATURITY_UNITS:
        errs.append("invalid maturity_unit values")
    if (df["maturity_value"] <= 0).any():
        errs.append("non-positive maturity_value")
    if dates_ok and (df["observation_date"].dt.dayofweek >= 5).any():
        errs.append("weekend observation dates present")
    return errs
