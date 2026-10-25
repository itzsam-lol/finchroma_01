# Source audit: US Treasury daily interest rate statistics (inspected 2026-10-25)

Landing page: https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics

CSV endpoint (no key, `User-Agent` set):
`https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all?type={type}&field_tdr_date_value={year}&page&_format=csv`

Types used: `daily_treasury_yield_curve`, `daily_treasury_real_yield_curve`, `daily_treasury_bill_rates`. Not used in v1: long-term rate/extrapolation factors and real long-term averages.

Verified by probing: columns change by era (1990 nominal file has 9 maturities from 3 Mo to 30 Yr; 2025 has 14 including 1.5 Month); bill files have a "BANK DISCOUNT" and "COUPON EQUIVALENT" column per maturity; dates are `MM/DD/YYYY`, newest first; blank cells occur where a maturity did not exist. Server responses are slow (~20 s per file), so the downloader sleeps 1 s between requests and retries with backoff.

Methodology notes (from Treasury's page): nominal par yields derive from closing market bid prices of the most recently auctioned securities; real yields are for TIPS; 30-year CMT was not published 2002-02-18 to 2006-02-09 (gap is preserved, not filled).

Profile of the actual downloaded data: `reports/source_profile.md`.
