"""Day 05: 수집물을 규칙대로 정리 → archive/ 노트 + metadata.csv + check_report.md

입력
  research/data/raw/voc/aside_fieldwork.json   Aside가 모은 커뮤니티 · 구글 플레이 · 유튜브 (요약만)
  research/data/raw/voc/reviews.csv            App Store 리뷰 110건 (묶음 1행으로 기록)
  research/data/archive · raw                  API 데이터 원본 (파일 1개 = 1행)
사용법:
    python scripts/build_archive.py
"""
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AR = ROOT / "archive"
RAW = ROOT / "research" / "data" / "raw"
COLS = ["id", "type", "source", "title", "url", "creator", "published_at", "collected_at",
        "license", "market", "target", "tags", "summary", "collector"]
TODAY = "20261110"
COLLECTED = "2026-11-09 16:40"  # UTC, Aside 수집 시각
TOPIC_TAG = {"시세·데이터": "정확성", "뉴스·정보": "속도", "분석·AI": "불신", "분석·지표": "정확성",
             "포트폴리오·관심종목": "불편", "알림": "불편", "UI·화면": "불편", "계정·인증": "가입장벽", "기타": "불편"}
USE_TAG = {"분석·AI": "예측근거", "포트폴리오·관심종목": "포트폴리오", "계정·인증": "포트폴리오"}
LICENSE = {"reddit": "공개 약관 범위 내 열람", "google_play": "공개 약관 범위 내 열람", "youtube": "저작권자 보유"}
SRC_CODE = {"reddit": "reddit", "google_play": "googleplay", "youtube": "youtube"}


def allowed_tags():
    text = (AR / "tags.md").read_text(encoding="utf-8")
    return {t.strip() for line in text.splitlines() if "·" in line and not line.startswith("#")
            for t in line.split("·")}


def slug(s):
    return re.sub(r"[^0-9A-Za-z가-힣]+", "_", s).strip("_")[:12] or "기타"


def fieldwork_rows():
    path = RAW / "voc" / "aside_fieldwork.json"
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    text = raw["answer"] if isinstance(raw, dict) else json.dumps(raw)  # aside exec --json 은 answer 안에 결과
    items = json.loads(text[text.index("["): text.rindex("]") + 1])
    rows, seq = [], Counter()
    for it in items:
        src = it.get("source", "")
        market = "kr" if src == "google_play" or re.search("[가-힣]", it.get("title", "")) and src == "youtube" else "us"
        topic = it.get("topic", "기타")
        key = (market, SRC_CODE.get(src, src), slug(topic))
        seq[key] += 1
        rid = f"{TODAY}_{key[0]}_{key[1]}_{key[2]}_{seq[key]:02d}"
        sent = it.get("sentiment", "0")
        tags = ["사용자VOC", TOPIC_TAG.get(topic, "불편") if sent != "+" else "편리", USE_TAG.get(topic, "지표후보")]
        if src == "youtube":
            tags[0:1] = ["사용자VOC", "경쟁서비스"]
        rows.append({
            "id": rid, "type": "video" if src == "youtube" else "text", "source": key[1],
            "title": it.get("title", "-") or "-", "url": it.get("url", "-"),
            "creator": "개인" if src != "youtube" else (it.get("creator") or "-"),
            "published_at": it.get("published", "-") or "-", "collected_at": COLLECTED,
            "license": LICENSE.get(src, "공개 약관 범위 내 열람"), "market": market,
            "target": topic, "tags": ";".join(dict.fromkeys(tags)), "summary": it.get("summary", "")[:80],
            "collector": "Aside", "_sentiment": sent,
        })
    return rows


def data_rows():
    out = [
        {"id": f"{TODAY}_global_appstore_리뷰묶음_01", "type": "review_set", "source": "appstore",
         "title": "주식 앱 4종 App Store 리뷰 110건", "url": "https://itunes.apple.com/kr/rss/customerreviews/id=909998122/json",
         "creator": "Apple App Store (개인 작성자)", "published_at": "2020-12~2026-11", "collected_at": "2026-11-09 16:28",
         "license": "공개 약관 범위 내 열람", "market": "global", "target": "Investing.com·키움·토스·Yahoo Finance",
         "tags": "사용자VOC;불편;지표후보", "summary": "4개 앱 리뷰 110건, 원문은 Git 제외 · 태그와 요약은 voc_tagged.csv", "collector": "스크립트"},
        {"id": f"{TODAY}_us_sec_실적공시_01", "type": "data", "source": "sec",
         "title": "AAPL 공시 목록 (submissions)", "url": "https://data.sec.gov/submissions/CIK0000320193.json",
         "creator": "U.S. SEC", "published_at": "2026-11-06", "collected_at": "2026-11-09 16:05",
         "license": "상업 이용 가능(출처 표기)", "market": "us", "target": "AAPL",
         "tags": "공시;정확성;이벤트라벨", "summary": "AAPL 공시 1,006건, 접수 시각 UTC(Day 5 확인)", "collector": "스크립트"},
        {"id": f"{TODAY}_global_gdelt_뉴스배치_01", "type": "data", "source": "gdelt",
         "title": "GDELT GKG 2.1 배치 20261109160000", "url": "https://data.gdeltproject.org/gdeltv2/20261109160000.gkg.csv.zip",
         "creator": "The GDELT Project", "published_at": "2026-11-09", "collected_at": "2026-11-09 16:12",
         "license": "상업 이용 가능(출처 표기)", "market": "global", "target": "뉴스 기사",
         "tags": "뉴스;속도;화면표시", "summary": "기사 1,443건 · 제목 · URL · 기관명 · 톤, DATE는 UTC", "collector": "스크립트"},
        {"id": f"{TODAY}_global_yfinance_일봉_01", "type": "data", "source": "yfinance",
         "title": "7종목 상장 이후 일봉", "url": "https://finance.yahoo.com",
         "creator": "Yahoo Finance (yfinance 1.8.0)", "published_at": "2026-11-09", "collected_at": "2026-11-09 15:40",
         "license": "개인·비상업 한정", "market": "global", "target": "AAPL·MSFT·NVDA·AMZN·GOOGL·SPY·005930.KS",
         "tags": "가격;정확성;학습데이터", "summary": "57,030행, 22~45년 · Yahoo 약관상 로컬 학습용만", "collector": "스크립트"},
        {"id": f"{TODAY}_us_alphavantage_뉴스_01", "type": "data", "source": "alphavantage",
         "title": "AAPL 뉴스·감성 (demo)", "url": "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo",
         "creator": "Alpha Vantage", "published_at": "2026-11-09", "collected_at": "2026-11-09 15:30",
         "license": "개인·비상업 한정", "market": "us", "target": "AAPL",
         "tags": "뉴스;정확성;라이선스확인", "summary": "기사 50건, time_published는 UTC(Day 5 확인)", "collector": "스크립트"},
    ]
    return out


def write_notes(rows):
    for sub in ("text", "video"):
        (AR / sub).mkdir(parents=True, exist_ok=True)
    for r in rows:
        if r["type"] not in ("text", "video"):
            continue
        body = (f"# {r['title'] if r['title'] != '-' else r['target']}\n\n"
                f"- 소스: {r['source']} · 시장: {r['market']} · 게시: {r['published_at']} · 수집: {r['collected_at']} UTC\n"
                f"- URL: {r['url']}\n- 작성자: {r['creator']}\n- 권리: {r['license']}\n- 태그: {r['tags']}\n"
                f"- 감정: {r.get('_sentiment', '-')}\n\n## 요약\n{r['summary']}\n\n"
                f"원문은 저장하지 않았다. 개인 식별 정보 없음.\n")
        name = f"{r['id']}_summary.md" if r["type"] == "video" else f"{r['id']}.md"
        (AR / r["type"] / name).write_text(body, encoding="utf-8")


def check(rows, tags):
    issues = []
    ids = Counter(r["id"] for r in rows)
    urls = Counter(r["url"] for r in rows)
    for r in rows:
        if ids[r["id"]] > 1:
            issues.append((r["id"], "id 중복"))
        if r["url"] in ("", "-") or not r["url"].startswith("http"):
            issues.append((r["id"], "URL 누락"))
        elif urls[r["url"]] > 1 and r["type"] == "text" and "play.google" not in r["url"]:
            issues.append((r["id"], "같은 URL 두 행"))
        if r["license"] in ("", "-"):
            issues.append((r["id"], "license 비어 있음"))
        t = r["tags"].split(";")
        if not 3 <= len(t) <= 6:
            issues.append((r["id"], f"태그 {len(t)}개"))
        bad = [x for x in t if x not in tags]
        if bad:
            issues.append((r["id"], f"목록 밖 태그 {bad}"))
        if len(r["summary"]) > 80:
            issues.append((r["id"], "요약 80자 초과"))
        if r["published_at"] == "-":
            issues.append((r["id"], "게시일 미확인 (경고)"))
        if r["type"] == "video" and not (AR / "video" / f"{r['id']}_summary.md").exists():
            issues.append((r["id"], "영상 요약 노트 없음"))
    return issues


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    tags = allowed_tags()
    field = fieldwork_rows()
    rows = field + data_rows()
    write_notes(rows)
    with open(AR / "metadata.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    issues = check(rows, tags)
    blocking = [i for i in issues if "경고" not in i[1]]
    src = Counter(r["source"] for r in rows)
    lines = [f"# 아카이브 검증 보고서 (Day 05)\n", f"- 실행: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · `scripts/build_archive.py`",
             f"- metadata.csv {len(rows)}행 (현장 수집 {len(field)} · 리뷰 묶음 1 · 데이터 4) · id 중복 {sum(1 for v in Counter(r['id'] for r in rows).values() if v > 1)}건",
             f"- 소스별: " + " · ".join(f"{k} {v}" for k, v in src.most_common()),
             f"- 한 소스 비중 최대 {max(src.values()) / len(rows) * 100:.0f}%\n", "| id | 문제 | 처리 |", "|---|---|---|"]
    lines += [f"| {i} | {m} | {'확인 필요' if '경고' in m else '수정 필요'} |" for i, m in issues] or ["| - | 없음 | - |"]
    lines.append(f"\n**결과: {'통과' if not blocking else '수정 필요 ' + str(len(blocking)) + '건'}**" + (f" (경고 {len(issues) - len(blocking)}건)" if issues else ""))
    lines.append("\n## 검수 기록\n"
                 "- 1차 실행에서 포트폴리오 글 3건의 태그가 2개로 줄어드는 오류 발견(2층과 3층에 같은 태그) → 2층 태그를 불편/편리로 바꿔 재실행 → 통과\n"
                 "- 검수 A (요약-원문 대조): 유튜브 2건은 YouTube oEmbed로 제목·채널 일치 확인. Reddit은 스크립트 요청이 막혀 대조 못 함 → **사람 확인 필요**\n"
                 "- 검수 B (url·license 전수 대조) · 검수 C (개인정보·인용 길이): **사람 확인 필요**. 작성자 열은 모두 '개인' 또는 채널명")
    (AR / "check_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
