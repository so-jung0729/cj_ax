"""yfinance로 종목별 전체 일봉 이력을 받아 범위·결측·분할/배당 정보를 확인한다.

사용법:
    python scripts/probe_yfinance.py AAPL MSFT NVDA SPY

결과: archive/yfinance/<ticker>_daily_max.csv (커밋 제외) + 콘솔 요약
"""
import sys
from datetime import date
from pathlib import Path

import yfinance as yf

OUT_DIR = Path(__file__).resolve().parents[1] / "archive" / "yfinance"


def probe(ticker: str) -> dict:
    # auto_adjust=False → 원가격(Close)과 수정종가(Adj Close)를 둘 다 받는다
    df = yf.Ticker(ticker).history(period="max", interval="1d", auto_adjust=False, actions=True)
    if df.empty:
        return {"ticker": ticker, "rows": 0}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_DIR / f"{ticker.lower()}_daily_max.csv")

    first, last = df.index.min(), df.index.max()
    return {
        "ticker": ticker,
        "rows": len(df),
        "first": first.date(),
        "last": last.date(),
        "years": round((last - first).days / 365.25, 1),
        "tz": str(df.index.tz),
        "columns": list(df.columns),
        "null_close": int(df["Close"].isna().sum()),
        "splits": int((df["Stock Splits"] != 0).sum()),
        "dividends": int((df["Dividends"] != 0).sum()),
    }


if __name__ == "__main__":
    tickers = sys.argv[1:] or ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "SPY"]
    print(f"probe date: {date.today()}")
    for t in tickers:
        print(probe(t))
