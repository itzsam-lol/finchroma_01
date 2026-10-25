"""Reshape Treasury wide CSVs into the canonical long schema."""
import re
from pathlib import Path

import pandas as pd

from . import config

_MAT = re.compile(r"^(\d+(?:\.\d+)?)\s*(WEEKS?|WK|MO(?:NTHS?)?|YR|YEARS?)\b", re.I)
_UNIT = {"W": "week", "M": "month", "Y": "year"}


def parse_maturity(text: str) -> tuple[str, float, str]:
    """'1.5 Month' -> ('1.5M', 1.5, 'month')."""
    m = _MAT.match(text.strip())
    if not m:
        raise ValueError(f"unrecognised maturity header: {text!r}")
    value = float(m.group(1))
    unit = _UNIT[m.group(2)[0].upper()]
    return f"{value:g}{unit[0].upper()}", value, unit


def split_header(header: str, curve_type: str) -> tuple[str, str]:
    """Return (maturity text, quote_basis) for a source column header."""
    if curve_type == "bill_rate":
        for suffix, basis in config.QUOTE_BASES.items():
            if header.upper().endswith(suffix):
                return header[: -len(suffix)].strip(), basis
        raise ValueError(f"unrecognised bill header: {header!r}")
    return header, "par_yield"


def wide_to_long(df: pd.DataFrame, curve_type: str) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    parts = []
    for col in [c for c in df.columns if c != "Date"]:
        mat_text, basis = split_header(col, curve_type)
        label, value, unit = parse_maturity(mat_text)
        part = df[["Date", col]].rename(columns={"Date": "observation_date", col: "value_pct"})
        part["value_pct"] = pd.to_numeric(part["value_pct"], errors="coerce")
        part = part.dropna(subset=["value_pct"])  # no imputation: blank cells emit no row
        part["curve_type"] = curve_type
        part["quote_basis"] = basis
        part["maturity_label"] = label
        part["maturity_value"] = value
        part["maturity_unit"] = unit
        parts.append(part)
    return pd.concat(parts, ignore_index=True)[config.COLUMNS]


def build(raw_dir: Path = config.RAW_DIR) -> tuple[pd.DataFrame, dict]:
    """Build the full dataset; returns (dataframe, reconciliation stats)."""
    frames, src_cells = [], 0
    for typ, curve in config.CURVES.items():
        for path in sorted(raw_dir.glob(f"{typ}_*.csv")):
            df = pd.read_csv(path, encoding="utf-8-sig")
            src_cells += int(df.drop(columns=df.columns[0]).notna().sum().sum())
            frames.append(wide_to_long(df, curve))
    out = pd.concat(frames, ignore_index=True)
    before = len(out)
    out = out.drop_duplicates()
    out = out.sort_values(
        ["observation_date", "curve_type", "quote_basis", "maturity_unit", "maturity_value"]
    ).reset_index(drop=True)
    out["observation_date"] = out["observation_date"].astype("datetime64[ns]")
    return out, {"source_non_null_cells": src_cells, "rows_before_dedup": before, "rows_after_dedup": len(out)}
