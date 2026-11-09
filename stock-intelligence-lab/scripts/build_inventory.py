"""Day 06: 데이터 소스 인벤토리 v1 → csv + xlsx(시트 3개, 총점은 수식) + 근거 검증

사실 열(자산명~근거 파일)과 평가 열(D · L · S)을 분리한다. 점수는 inventory/scoring.md 척도.
사용법:
    python scripts/build_inventory.py
"""
import csv
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "inventory"
W = {"공통": (0.4, 0.3, 0.3), "학습용": (0.4, 0.5, 0.1), "서비스 표시용": (0.3, 0.1, 0.6)}
COLS = ["asset_id", "자산명", "유형", "시장", "한 줄 설명", "근거 파일", "D 데이터 가용성", "L 학습 가치",
        "S 서비스 사용", "연계 용도", "비고"]

# (자산명, 유형, 시장, 설명, 근거[; 구분], D, L, S, 용도, 비고)
ROWS = [
    ("yfinance (Yahoo 일봉)", "가격", "global", "상장 이후 일봉 · 수정종가 · 분할 · 배당을 키 없이 받음",
     "research/market_data/yfinance.md;20261110_global_yfinance_일봉_01;research/crosscheck.md#1", 5, 5, 1,
     "학습데이터", "Yahoo 약관: 개인 용도 · 자동 수집 금지. 상장폐지 종목 없음(생존편향)"),
    ("SEC EDGAR", "공시", "us", "미국 상장사 공시 목록과 UTC 접수 시각",
     "research/news_data/sec_edgar.md;20261110_us_sec_실적공시_01;research/crosscheck.md#14", 5, 5, 4,
     "이벤트라벨 · 화면표시", "재게시 조건 원문 미확인 → 5점 보류. 요청에 연락처 헤더 필요"),
    ("GDELT GKG 2.1", "뉴스", "global", "15분 배치 기사 목록 · 제목 · 기관명 · 톤, 2015-02부터",
     "research/news_data/gdelt.md;20261110_global_gdelt_뉴스배치_01;research/crosscheck.md#16", 5, 3, 5,
     "화면표시 · 학습데이터", "기관명→티커 매핑 필요. 출처 표기 필수"),
    ("Alpha Vantage", "가격 · 뉴스", "us", "일봉 · 종목별 관련도가 붙은 뉴스 · 감성",
     "research/market_data/alpha_vantage.md;20261110_us_alphavantage_뉴스_01;research/crosscheck.md#6", 3, 3, 2,
     "학습데이터 · 기준선", "무료는 개인·비상업, 일 25회. 수정주가 · 뉴스는 유료. 상업 계약 조건 확인 필요"),
    ("App Store 리뷰 RSS", "사용자VOC", "global", "앱별 최근 리뷰 최대 500건 공개 피드",
     "research/users_competitors/voc_tagged.csv;20261110_global_appstore_리뷰묶음_01", 5, 1, 2,
     "지표후보 · 사용자 조사", "원문 재게시 안 함, 요약만"),
    ("Google Play 리뷰", "사용자VOC", "kr", "토스 · 키움 앱 공개 리뷰",
     "archive/metadata.csv (source=googleplay);research/users_competitors/fieldwork_plan.md", 3, 1, 2,
     "사용자 조사", "공식 피드 없음 → Aside 수동 수집"),
    ("Reddit r/stocks · r/investing", "사용자VOC", "us", "AI 분석 · 포트폴리오 앱에 대한 공개 글",
     "archive/metadata.csv (source=reddit);research/users_competitors/source_map.md", 3, 1, 2,
     "사용자 조사", "API 약관 확인 전 Aside 열람만"),
    ("Nasdaq Data Link", "가격", "us", "데이터셋별 라이선스가 명시된 데이터 마켓",
     "research/keyword_map.md#v2", 2, 3, 3, "학습데이터 · 화면표시", "확인 필요 (근거 1개, 사전 지식)"),
    ("Polygon (Massive)", "가격 · 뉴스", "us", "미국 주식 일봉 · 뉴스 유료 API",
     "research/keyword_map.md#v2", 2, 3, 3, "화면표시", "확인 필요 (근거 1개, 사전 지식)"),
    ("Finnhub", "뉴스", "us", "종목 코드로 회사 뉴스 조회",
     "research/keyword_map.md#v2", 2, 3, 2, "학습데이터", "확인 필요 (근거 1개, 사전 지식)"),
    ("KRX 정보데이터시스템", "가격 · 시장", "kr", "한국 시장 공식 시세",
     "research/keyword_map.md#v2", 2, 3, 2, "학습데이터", "확인 필요. 한국 종목을 넣을 때만"),
    ("OpenDART", "공시", "kr", "한국 공시 공식 API",
     "research/keyword_map.md#v2", 2, 3, 3, "이벤트라벨", "확인 필요. 한국 종목을 넣을 때만"),
    ("VIX", "시장", "us", "시장 변동성 지수, 피처 후보",
     "research/keyword_map.md#v2", 2, 3, 2, "학습데이터", "확인 필요. 받는 경로(yfinance ^VIX 등)에 따라 S 달라짐"),
    ("FRED", "시장", "us", "미국 연준 공개 거시 데이터",
     "research/keyword_map.md#v2", 2, 3, 3, "학습데이터", "확인 필요 (근거 1개, 사전 지식)"),
    ("미국 재무부 금리", "시장", "us", "국채 수익률 공개 데이터",
     "research/keyword_map.md#v2", 2, 3, 3, "학습데이터", "확인 필요 (근거 1개, 사전 지식)"),
    ("네이버 종목토론실", "사용자VOC", "kr", "국내 개인투자자 종목 게시판",
     "research/keyword_map.md#v2", 1, 1, 1, "사용자 조사", "미수집. 닉네임 노출 위험"),
]


def evidence_ok(ev):
    """근거 파일이 실제로 있는지 확인 (metadata id는 metadata.csv에서)."""
    meta = (ROOT / "archive" / "metadata.csv").read_text(encoding="utf-8") if (ROOT / "archive" / "metadata.csv").exists() else ""
    missing = []
    for e in ev.split(";"):
        e = e.strip()
        if e.startswith("2026"):
            if e not in meta:
                missing.append(e)
        elif "(source=" in e:
            src = e.split("source=")[1].rstrip(")")
            if f",{src}," not in meta:
                missing.append(e)
        elif not (ROOT / e.split("#")[0].split(" ")[0]).exists():
            missing.append(e)
    return missing


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = []
    for i, r in enumerate(ROWS, 1):
        d = dict(zip(COLS, [f"A{i:02d}", *r]))
        for name, (wd, wl, ws) in W.items():
            d[f"총점_{name}"] = round(r[5] * wd + r[6] * wl + r[7] * ws, 2)
        d["근거 수"] = len(r[4].split(";"))
        d["누락 근거"] = "; ".join(evidence_ok(r[4]))
        rows.append(d)

    fields = COLS + [f"총점_{n}" for n in W] + ["근거 수", "누락 근거"]
    with open(INV / "inventory_v1.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    # xlsx: 강의와 같은 시트 3개, 총점은 수식으로
    wb = Workbook()
    ws = wb.active
    ws.title = "inventory"
    ws.append(COLS)
    for d in rows:
        ws.append([d[c] for c in COLS])
    sc = wb.create_sheet("scoring")
    sc.append(["용도", "D 가중치", "L 가중치", "S 가중치"])
    for name, (a, b, c) in W.items():
        sc.append([name, a, b, c])
    sc.append([])
    sc.append(["asset_id", "자산명", "D", "L", "S", "공통", "학습용", "서비스 표시용"])
    for k, d in enumerate(rows):
        r = k + 7
        sc.append([d["asset_id"], d["자산명"], f"=inventory!G{k + 2}", f"=inventory!H{k + 2}", f"=inventory!I{k + 2}",
                   f"=C{r}*$B$2+D{r}*$C$2+E{r}*$D$2", f"=C{r}*$B$3+D{r}*$C$3+E{r}*$D$3", f"=C{r}*$B$4+D{r}*$C$4+E{r}*$D$4"])
    top = wb.create_sheet("top3")
    top.append(["용도", "순위", "asset_id", "자산명", "총점"])
    for name in ("학습용", "서비스 표시용"):
        for rank, d in enumerate(sorted(rows, key=lambda x: -x[f"총점_{name}"])[:3], 1):
            top.append([name, rank, d["asset_id"], d["자산명"], d[f"총점_{name}"]])
    for sheet in wb.worksheets:
        for c in sheet[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="FFF1A8")
    wb.save(INV / "inventory_v1.xlsx")

    for name in W:
        print(name, [(d["asset_id"], d["자산명"], d[f"총점_{name}"]) for d in sorted(rows, key=lambda x: -x[f"총점_{name}"])[:5]])
    miss = [(d["asset_id"], d["누락 근거"]) for d in rows if d["누락 근거"]]
    one = [d["asset_id"] for d in rows if d["근거 수"] < 2]
    print("근거 누락:", miss or "없음")
    print("근거 1개뿐(확인 필요):", one)


if __name__ == "__main__":
    main()
