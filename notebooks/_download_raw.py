"""Download raw NYC Open Data extracts used by the notebooks.

Caches files under data/raw so later notebook runs do not re-download.
"""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def fetch_csv(url: str) -> pd.DataFrame:
    request = Request(url, headers={"User-Agent": "nyc-housing-edu/1.0"})
    with urlopen(request, timeout=180) as response:
        return pd.read_csv(response, low_memory=False)


def download_paged(dataset_id: str, dest: Path, page_size: int = 50000, params=None) -> None:
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"cached {dest.name} ({dest.stat().st_size} bytes)")
        return
    frames = []
    offset = 0
    while True:
        query = {"$limit": page_size, "$offset": offset}
        if params:
            query.update(params)
        url = f"https://data.cityofnewyork.us/resource/{dataset_id}.csv?{urlencode(query)}"
        print(f"GET {dataset_id} offset={offset}")
        part = fetch_csv(url)
        print(f"  rows={len(part)}")
        if part.empty:
            break
        frames.append(part)
        offset += len(part)
        if len(part) < page_size:
            break
    if not frames:
        raise RuntimeError(f"No rows downloaded for {dataset_id}")
    out = pd.concat(frames, ignore_index=True)
    out.to_csv(dest, index=False)
    print(f"wrote {dest.name} {out.shape}")


if __name__ == "__main__":
    download_paged("hg8x-zxpr", RAW / "housing_raw.csv", page_size=50000)
    download_paged(
        "7ym2-wayt",
        RAW / "segment_borough.csv",
        page_size=50000,
        params={"$select": "segmentid,boro", "$group": "segmentid,boro", "$order": "segmentid"},
    )
    download_paged("btm5-ppia", RAW / "traffic_raw.csv", page_size=50000)
