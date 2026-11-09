"""두 소스의 일봉 값을 날짜별로 대조한다 (Day 03 교차검증).

대조: yfinance IBM (원가격 Close) vs Alpha Vantage demo TIME_SERIES_DAILY IBM (as-traded close)
사용법:
    python scripts/crosscheck_prices.py
"""
import json
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
AV_FILE = ROOT / "research" / "data" / "raw" / "alphavantage" / "20261110_alphavantage_ibm_daily_demo.json"


def load_alpha_vantage(path: Path) -> pd.DataFrame:
    raw = json.loads(path.read_text(encoding="utf-8"))["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(raw, orient="index").astype(float)
    df.index = pd.to_datetime(df.index)
    return df.rename(columns={"1. open": "open", "2. high": "high", "3. low": "low",
                              "4. close": "close", "5. volume": "volume"}).sort_index()


def load_yfinance(ticker: str, start, end) -> pd.DataFrame:
    df = yf.Ticker(ticker).history(start=start, end=end + pd.Timedelta(days=1), auto_adjust=False)
    df.index = df.index.tz_localize(None).normalize()
    return df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 콘솔 한글 깨짐 방지
    av =load_alpha_vantage(AV_FILE)
    yfd = load_yfinance("IBM", av.index.min(), av.index.max())

    joined = av.merge(yfd, left_index=True, right_index=True, how="outer", suffixes=("_av", "_yf"))
    only_av = joined["close_yf"].isna().sum()
    only_yf = joined["close_av"].isna().sum()
    both = joined.dropna()

    close_diff = (both["close_av"] - both["close_yf"]).abs()
    vol_ratio = both["volume_yf"] / both["volume_av"]

    print(f"기간: {av.index.min().date()} ~ {av.index.max().date()}")
    print(f"AV 행 {len(av)}, yfinance 행 {len(yfd)}, 공통 {len(both)}, AV에만 {only_av}, yfinance에만 {only_yf}")
    print(f"종가 차이: 최대 {close_diff.max():.4f}, 0.01 초과 {int((close_diff > 0.01).sum())}일")
    print(f"거래량 비율(yf/av): 중앙값 {vol_ratio.median():.4f}, 최소 {vol_ratio.min():.4f}, 최대 {vol_ratio.max():.4f}")
    worst = close_diff.sort_values(ascending=False).head(3)
    print("종가 차이 상위 3일:", {d.date().isoformat(): round(v, 4) for d, v in worst.items()})
