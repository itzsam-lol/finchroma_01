"""Static configuration for the FinChrona v1 build (US Treasury rates)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
SAMPLE_DIR = ROOT / "data" / "samples"
REPORT_DIR = ROOT / "reports"
RELEASE_DIR = ROOT / "release"

DATASET_VERSION = "1.0.0"
USER_AGENT = "FinChrona/1.0 (research dataset builder; contact: loligey96@gmail.com)"
URL_TEMPLATE = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "daily-treasury-rates.csv/{year}/all?type={type}&field_tdr_date_value={year}&page&_format=csv"
)
START_YEAR = 1990
REQUEST_DELAY_S = 1.0

# source `type` parameter -> curve_type recorded in the dataset
CURVES = {
    "daily_treasury_yield_curve": "par_nominal",
    "daily_treasury_real_yield_curve": "par_real",
    "daily_treasury_bill_rates": "bill_rate",
}
# bill-rate columns carry a quote basis suffix
QUOTE_BASES = {"BANK DISCOUNT": "bank_discount", "COUPON EQUIVALENT": "coupon_equivalent"}

COLUMNS = [
    "observation_date", "curve_type", "quote_basis", "maturity_label",
    "maturity_value", "maturity_unit", "value_pct",
]
PRIMARY_KEY = ["observation_date", "curve_type", "quote_basis", "maturity_label"]
CURVE_TYPES = set(CURVES.values())
QUOTE_BASIS_VALUES = {"par_yield", "bank_discount", "coupon_equivalent"}
MATURITY_UNITS = {"week", "month", "year"}
