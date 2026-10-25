"""Download yearly Treasury CSV files with retries and a provenance manifest."""
import json
import time
from pathlib import Path

import requests

from . import config
from .provenance import sha256_file, utc_now


def fetch(url: str, retries: int = 4) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, headers={"User-Agent": config.USER_AGENT}, timeout=60)
            if r.status_code == 200:
                return r.content
            last = f"HTTP {r.status_code}"
        except requests.RequestException as e:  # network error: retry with backoff
            last = repr(e)
        time.sleep(2 ** attempt)
    raise RuntimeError(f"failed to fetch {url}: {last}")


def download_all(end_year: int, raw_dir: Path = config.RAW_DIR, refresh: bool = False) -> list[dict]:
    """Download every (curve, year) file. Returns manifest entries."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for typ in config.CURVES:
        for year in range(config.START_YEAR, end_year + 1):
            path = raw_dir / f"{typ}_{year}.csv"
            url = config.URL_TEMPLATE.format(year=year, type=typ)
            retrieved = None
            if refresh or not path.exists():
                path.write_bytes(fetch(url))
                retrieved = utc_now()
                time.sleep(config.REQUEST_DELAY_S)
            if path.read_text(encoding="utf-8-sig").count("\n") < 1:
                path.unlink()  # year predates this curve
                continue
            manifest.append({
                "file": path.name, "source_type": typ, "year": year, "url": url,
                "retrieved_at_utc": retrieved, "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            })
    (raw_dir / "raw_manifest.json").write_text(json.dumps(manifest, indent=1))
    return manifest
