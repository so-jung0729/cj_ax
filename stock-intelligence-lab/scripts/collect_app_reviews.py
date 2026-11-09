"""Day 04: App Store 공개 리뷰 RSS에서 주식 정보 서비스 리뷰를 모은다.

- 작성자 이름·ID는 저장하지 않는다 (익명화). 본문·별점·작성 월·버전만.
- 원문은 research/data/raw/voc/ (Git 제외), 선별본은 research/data/raw/voc/reviews.csv
사용법:
    python scripts/collect_app_reviews.py
"""
import csv
import json
import random
import re
import sys
import time
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research" / "data" / "raw" / "voc"
FEED = "https://itunes.apple.com/{cc}/rss/customerreviews/page={p}/id={app_id}/sortby=mostrecent/json"

# (이름, 앱 ID, 스토어 국가, 목표 건수, 본문 필터 정규식)
APPS = [
    ("investing_com", 909998122, "kr", 30, None),
    ("kiwoom_heroS", 1570370057, "kr", 30, None),
    ("toss", 839333328, "kr", 20, r"주식|증권|투자|종목|매수|매도|차트"),  # 토스는 금융 앱 전체라 주식 관련만
    ("yahoo_finance", 328412701, "us", 30, None),
]


def fetch(app_id, cc, page):
    req = urllib.request.Request(FEED.format(cc=cc, p=page, app_id=app_id),
                                 headers={"User-Agent": "StockIntelligenceLab/0.1 educational research"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["feed"].get("entry", [])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    random.seed(20261110)
    picked = []
    for name, app_id, cc, n, pattern in APPS:
        rows = []
        for page in range(1, 11):  # 피드는 최대 10페이지(500건)
            try:
                entries = fetch(app_id, cc, page)
            except Exception as e:  # 페이지가 없으면 중단
                print(f"{name} p{page}: {e}")
                break
            if not entries:
                break
            for x in entries:
                text = x["content"]["label"].strip()
                if len(text) < 15 or (pattern and not re.search(pattern, text)):
                    continue
                rows.append({"app": name, "store": cc, "rating": int(x["im:rating"]["label"]),
                             "month": x["updated"]["label"][:7], "version": x["im:version"]["label"],
                             "title": x["title"]["label"].strip(), "text": text})
            time.sleep(1)
        (OUT / f"{name}_all.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        # 최근 리뷰에 치우치지 않도록 월별로 고르게 뽑는다
        by_month = defaultdict(list)
        for r in rows:
            by_month[r["month"]].append(r)
        months = sorted(by_month)
        chosen = []
        while len(chosen) < n and any(by_month.values()):
            for m in months:
                if by_month[m] and len(chosen) < n:
                    chosen.append(by_month[m].pop(random.randrange(len(by_month[m]))))
        print(f"{name}: 받은 {len(rows)}건 · 월 {months[0] if months else '-'}~{months[-1] if months else '-'} · 선별 {len(chosen)}건")
        picked += chosen

    seen, out = set(), []
    for r in picked:
        if r["text"] in seen:
            continue
        seen.add(r["text"])
        out.append(r)
    with open(OUT / "reviews.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "app", "store", "rating", "month", "version", "title", "text"])
        w.writeheader()
        for i, r in enumerate(out, 1):
            w.writerow({"id": f"R{i:03d}", **r})
    print(f"합계 {len(out)}건 (중복 제거 후) · 수집 {datetime.now():%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()
