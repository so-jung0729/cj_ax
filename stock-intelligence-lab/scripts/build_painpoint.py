"""Day 11: VOC 128건(앱 리뷰 110 + 현장 수집 18) → 원인별 묶음 · 점수 · 여정 단계 감정

규칙 기반 묶음: (주제, 부정) → 원인 후보. 점수 = 빈도 × 강도 × 해결 가능성 (각 1~3)
사용법:
    python scripts/build_painpoint.py
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "painpoint"

CAUSES = {  # 원인 코드: (주제, 진술 요약)
    "C1": ("시세·데이터", "화면의 숫자가 맞는지 · 어느 범위 기준인지 믿기 어렵다"),
    "C2": ("분석·AI", "AI 분석이 결과에 맞춰 이유를 붙이거나 숫자를 지어낸다"),
    "C3": ("포트폴리오·관심종목", "관심목록 · 포트폴리오가 저장 · 갱신 · 집계되지 않는다"),
    "C4": ("계정·인증", "가입 · 인증 · 계좌 연동에서 막힌다"),
    "C5": ("알림", "알림이 늦거나 원하지 않는 알림이 온다"),
    "C6": ("분석·지표", "쓰던 지표 · 계산 도구가 바뀌거나 사라진다"),
    "C7": ("UI·화면", "업데이트로 보던 정보 배치가 바뀌거나 가려진다"),
}
# 해결 가능성: 우리 서비스(정보 웹, 매매 없음)가 지금 데이터로 풀 수 있나
SOLVE = {"C1": 3, "C2": 2, "C3": 2, "C4": 1, "C5": 1, "C6": 2, "C7": 1}
# 강도 (근거 id로 직접): 3 = 손실·이탈·사기 언급, 2 = 기능을 끄거나 재설치·우회를 반복, 1 = 불편 표현만
SEVERITY = {
    "C1": (2, "R016 재설치 반복 · R087 다른 회사 재무 표시 · Play 거래량 비정상"),
    "C2": (3, "R077 '사기로 유치' · R064 투자자 혼선"),
    "C3": (2, "R013 저장 실패 · 순서 뒤섞임 · Play 투자원금 기록 어긋남"),
    "C4": (3, "R032 · R037 다른 증권사로 이탈"),
    "C5": (2, "Play 알림을 모두 끔 · R030 알림 끌 수 없음"),
    "C6": (2, "R055 다른 앱과 비교 · R078 계산기 따로 봐야 함"),
    "C7": (2, "R082 쓸모없어짐 · Play 차트 문제로 다른 증권사로 이동(1건)"),
}
STAGE_MAP = {"가입·계정": "가입·계정", "정보 탐색": "정보 탐색", "판단": "판단", "거래": "거래", "관리": "관리"}


def load():
    rows = []
    for r in csv.DictReader(open(ROOT / "research/users_competitors/voc_tagged.csv", encoding="utf-8")):
        rows.append({"id": r["id"], "src": "앱 리뷰", "topic": r["topic"], "sent": r["sentiment"],
                     "stage": r["stage"], "rating": int(r["rating"]), "rel": r["relevant"]})
    for r in csv.DictReader(open(ROOT / "archive/metadata.csv", encoding="utf-8")):
        if r["source"] not in ("reddit", "googleplay", "youtube"):
            continue
        note = (ROOT / "archive" / ("video" if r["type"] == "video" else "text") /
                (r["id"] + ("_summary.md" if r["type"] == "video" else ".md"))).read_text(encoding="utf-8")
        sent = note.split("- 감정: ")[1].split("\n")[0].strip()
        rows.append({"id": r["id"], "src": {"reddit": "커뮤니티", "googleplay": "앱 리뷰(Play)", "youtube": "영상"}[r["source"]],
                     "topic": r["target"], "sent": sent, "stage": None, "rating": None, "rel": "Y"})
    return rows


def level(n, cuts=(5, 10)):
    return 1 if n < cuts[0] else 2 if n < cuts[1] else 3


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = load()
    groups = defaultdict(list)
    for r in rows:
        if r["sent"] != "-":
            continue
        for c, (topic, _) in CAUSES.items():
            if r["topic"] == topic and (c != "C7" or r["rel"] == "Y"):
                groups[c].append(r)
    table = []
    for c, (topic, text) in CAUSES.items():
        g = groups[c]
        n = len(g)
        kinds = sorted({x["src"] for x in g})
        low = sum(1 for x in g if x["rating"] in (1, 2))
        sev, sev_ev = SEVERITY[c]
        f = level(n)
        s = SOLVE[c]
        table.append({"code": c, "topic": topic, "text": text, "n": n, "kinds": kinds, "low_rating": low,
                      "freq": f, "sev": sev, "sev_evidence": sev_ev, "solve": s, "score": f * sev * s, "ids": [x["id"] for x in g]})
    table.sort(key=lambda x: (-x["score"], -len(x["kinds"]), -x["n"]))

    # 여정 단계별 감정 (앱 리뷰 중 질문 관련, +1/−1 평균 → −2~+2로 환산)
    st = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        if r["stage"] and r["rel"] == "Y":
            st[r["stage"]][{"+": 0, "-": 1}.get(r["sent"], 2)] += 1
    stage_emotion = {k: {"pos": v[0], "neg": v[1], "neu": v[2], "score": round(2 * (v[0] - v[1]) / max(1, sum(v)), 1)} for k, v in st.items()}

    OUT.mkdir(exist_ok=True)
    (OUT / "painpoint_scores.json").write_text(json.dumps({"total_voc": len(rows), "candidates": table, "stage_emotion": stage_emotion},
                                                         ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"VOC {len(rows)}건 (부정 {sum(1 for r in rows if r['sent'] == '-')})")
    for t in table:
        print(t["code"], t["topic"], "n", t["n"], t["kinds"], "빈도", t["freq"], "강도", t["sev"], "해결", t["solve"], "=", t["score"])
    print(json.dumps(stage_emotion, ensure_ascii=False))


if __name__ == "__main__":
    main()
