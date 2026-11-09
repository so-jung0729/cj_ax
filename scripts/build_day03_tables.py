"""Day 03 과제: 원본(research/data/raw · archive)을 열 이름을 통일한 정리본 CSV 3종으로 만든다.

출력 (research/data/):
  prices_daily.csv          yfinance 일봉, 종목 여러 개를 세로로 합침 (Yahoo 약관상 커밋 제외)
  sec_filings_aapl.csv      SEC EDGAR AAPL 최근 공시 목록
  gdelt_gkg_sample.csv      GDELT GKG 15분 파일 1개에서 뽑은 기사 목록
사용법:
    python scripts/build_day03_tables.py
"""
import csv
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "data"
RAW = DATA / "raw"
ARCHIVE = DATA / "archive"
OUT = DATA


def build_prices() -> pd.DataFrame:
    frames = []
    for f in sorted((RAW / "yfinance").glob("*_daily_max.csv")):
        df = pd.read_csv(f)
        ticker = f.name.split("_daily_max")[0].upper()
        # 원본 Date는 시간대가 붙은 문자열(예: 1980-12-12 00:00:00-05:00) → 거래소 현지 날짜만 남김
        df["date"] = df["Date"].str.slice(0, 10)
        df["ticker"] = ticker
        df = df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close",
                                "Adj Close": "adj_close", "Volume": "volume",
                                "Dividends": "dividend", "Stock Splits": "split_ratio"})
        frames.append(df[["ticker", "date", "open", "high", "low", "close", "adj_close",
                          "volume", "dividend", "split_ratio"]])
    out = pd.concat(frames, ignore_index=True)
    out["source"] = "yfinance"
    return out


def build_sec() -> pd.DataFrame:
    d = json.loads((ARCHIVE / "sec" / "20261110_sec_aapl_submissions.json").read_text(encoding="utf-8"))
    r = d["filings"]["recent"]
    df = pd.DataFrame({
        "accession_number": r["accessionNumber"],
        "form": r["form"],
        "filing_date": r["filingDate"],
        "report_date": r["reportDate"],
        "acceptance_datetime_raw": r["acceptanceDateTime"],  # 시간대 미확정이라 원문 그대로 보관
        "items": r["items"],
        "primary_document": r["primaryDocument"],
    })
    df.insert(0, "ticker", d["tickers"][0])
    df.insert(1, "cik", d["cik"])
    df["source"] = "sec_edgar"
    return df


def build_gdelt() -> pd.DataFrame:
    csv.field_size_limit(10**8)
    path = ARCHIVE / "gdelt" / "20261109160000.gkg.csv.zip"
    z = zipfile.ZipFile(path)
    rows = csv.reader(io.TextIOWrapper(z.open(z.namelist()[0]), encoding="utf-8", errors="replace"),
                      delimiter="\t")
    records = []
    for r in rows:
        title = re.search(r"<PAGE_TITLE>(.*?)</PAGE_TITLE>", r[26])
        records.append({
            "gkg_record_id": r[0],
            "date_raw": r[1],  # 시간대 미확정
            "source_domain": r[3],
            "url": r[4],
            "title": title.group(1) if title else "",
            "organizations": r[13],
            "tone": float(r[15].split(",")[0]) if r[15] else None,
        })
    df = pd.DataFrame(records)
    df["source"] = "gdelt_gkg"
    return df


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("prices_daily.csv", build_prices),
                     ("sec_filings_aapl.csv", build_sec),
                     ("gdelt_gkg_sample.csv", build_gdelt)]:
        df = fn()
        df.to_csv(OUT / name, index=False, encoding="utf-8")
        dup = int(df.duplicated().sum())
        nulls = {c: int(v) for c, v in df.isna().sum().items() if v}
        print(f"{name}: {len(df)}행 · 열 {list(df.columns)} · 완전중복 {dup} · 결측 {nulls or '없음'}")
