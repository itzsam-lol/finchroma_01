"""Download raw Treasury yearly CSVs. Usage: python scripts/download_data.py [--end-year YYYY] [--refresh]"""
import argparse
from datetime import date

from finchrona.ingestion import download_all

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--end-year", type=int, default=date.today().year)
    p.add_argument("--refresh", action="store_true", help="re-download existing files")
    a = p.parse_args()
    m = download_all(a.end_year, refresh=a.refresh)
    print(f"{len(m)} raw files in manifest")
