import io

import pandas as pd
import pytest

from finchrona import config, transforms
from finchrona.validation import validate

NOMINAL = 'Date,"1 Mo","1.5 Month","10 Yr"\n12/31/2025,3.74,,4.18\n12/30/2025,3.65,3.71,4.14\n'
BILLS = 'Date,"4 WEEKS BANK DISCOUNT","4 WEEKS COUPON EQUIVALENT"\n12/31/2025,3.59,3.65\n'


def long(text, curve):
    return transforms.wide_to_long(pd.read_csv(io.StringIO(text)), curve)


def test_parse_maturity():
    assert transforms.parse_maturity("1.5 Month") == ("1.5M", 1.5, "month")
    assert transforms.parse_maturity("10 YR") == ("10Y", 10.0, "year")
    assert transforms.parse_maturity("4 WEEKS") == ("4W", 4.0, "week")
    with pytest.raises(ValueError):
        transforms.parse_maturity("bogus")


def test_blank_cells_not_imputed():
    df = long(NOMINAL, "par_nominal")
    assert len(df) == 5  # 6 cells, one blank
    assert not ((df.maturity_label == "1.5M") & (df.observation_date == "2025-12-31")).any()


def test_bill_basis_split():
    df = long(BILLS, "bill_rate")
    assert set(df.quote_basis) == {"bank_discount", "coupon_equivalent"}
    assert set(df.maturity_label) == {"4W"}


def test_valid_frame_passes_and_is_deterministic():
    a, b = long(NOMINAL, "par_nominal"), long(NOMINAL, "par_nominal")
    pd.testing.assert_frame_equal(a, b)
    assert validate(a) == []
    assert list(a.columns) == config.COLUMNS


def test_missing_column():
    assert "missing columns" in validate(long(NOMINAL, "par_nominal").drop(columns=["value_pct"]))[0]


def test_duplicate_keys():
    df = long(NOMINAL, "par_nominal")
    assert any("duplicate" in e for e in validate(pd.concat([df, df])))


def test_invalid_category_and_timestamp_and_type():
    df = long(NOMINAL, "par_nominal")
    assert any("curve_type" in e for e in validate(df.assign(curve_type="x")))
    assert any("not datetime" in e for e in validate(df.assign(observation_date="2025-12-31")))
    assert any("not numeric" in e for e in validate(df.assign(value_pct="a")))
    assert any("weekend" in e for e in validate(df.assign(observation_date=pd.Timestamp("2025-12-28"))))


def test_unrecognised_bill_header():
    with pytest.raises(ValueError):
        transforms.split_header("4 WEEKS OTHER", "bill_rate")
