# Data dictionary

File: `finchrona_treasury_rates.parquet` (and `.csv`, same columns, dates as `YYYY-MM-DD`). Long format, one row per observation.

| column | type | definition | valid values | missing |
|---|---|---|---|---|
| observation_date | datetime64[ns] (date) | US business date of the quote | 1990-01-02 .. cutoff; never Sat/Sun | never null |
| curve_type | string | `par_nominal` nominal par yield curve; `par_real` TIPS par real yield curve; `bill_rate` daily bill rates | those three | never null |
| quote_basis | string | `par_yield` for the two curves; `bank_discount` or `coupon_equivalent` for bills | those three | never null |
| maturity_label | string | compact label, e.g. `1.5M`, `4W`, `10Y` | derived from value+unit | never null |
| maturity_value | float64 | numeric maturity in `maturity_unit` | > 0 | never null |
| maturity_unit | string | `week`, `month` or `year` (kept as published, not converted) | those three | never null |
| value_pct | float64 | rate in percent per annum (3.74 = 3.74%) | par_nominal >= 0; par_real and bills may be slightly negative | never null; absent cells have no row |

Wide pivot: `df.pivot(index="observation_date", columns="maturity_label", values="value_pct")` after filtering curve_type and quote_basis.
Source column names map as: `1 Mo`->1M, `1.5 Month`->1.5M, `10 Yr`->10Y, `4 WEEKS BANK DISCOUNT`->4W/bank_discount.
