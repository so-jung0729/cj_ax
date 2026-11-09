"""Day 04~08 산출물(md·csv)을 local_package/의 Day별 HTML로 묶는다.

저장소 루트에서 실행:
    python scripts/build_local_package.py

md 파일이 원본이고 HTML은 보기용 사본이다. md를 고친 뒤 다시 실행하면 HTML이 갱신된다.
필요: pip install markdown
"""
import csv
import html
import os
import re
from collections import Counter

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "local_package")

PAGES = [
    ("../index.html", "← 한 줄기 전체 보기"),
    ("day04.html", "01 Day 04 조사"),
    ("day05.html", "02 Day 05 아카이브"),
    ("day06.html", "03 Day 06 인벤토리"),
    ("day07.html", "04 Day 07 브랜드·세계관"),
    ("journey.html", "05 고객 유형·여정"),
    ("day08.html", "06 Day 08 스토리보드"),
]


def p(*parts):
    return os.path.join(ROOT, *parts)


def read(rel):
    with open(p(rel), encoding="utf-8-sig") as f:
        return f.read()


def rows(rel):
    with open(p(rel), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def fix_links(body, rel):
    """md 안의 상대 링크를 local_package/ 기준으로 바꾼다."""
    base = os.path.dirname(rel)

    def repl(m):
        href = m.group(1)
        if re.match(r"^(https?:|#|mailto:)", href):
            return m.group(0)
        target = os.path.normpath(os.path.join(base, href)).replace("\\", "/")
        new = os.path.relpath(p(target), OUT).replace("\\", "/")
        return f'href="{new}"'

    return re.sub(r'href="([^"]+)"', repl, body)


def md_doc(rel, title=None, open_=False, code=False):
    text = read(rel)
    if code:
        body = f"<pre><code>{html.escape(text)}</code></pre>"
    else:
        if text.startswith("---"):
            text = re.sub(r"^---.*?---\s*", "", text, flags=re.S)
        body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
        body = fix_links(body, rel)
    title = title or rel
    return (f'<details class="doc"{" open" if open_ else ""}><summary><span>{html.escape(title)}</span>'
            f'<span class="path">{html.escape(rel)}</span></summary><div class="md">{body}</div></details>')


def csv_doc(rel, title, cols=None, open_=False):
    data = rows(rel)
    cols = cols or list(data[0].keys())
    th = "".join(f"<th>{html.escape(c)}</th>" for c in cols)
    tr = "".join("<tr>" + "".join(f"<td>{html.escape(r[c])}</td>" for c in cols) + "</tr>" for r in data)
    return (f'<details class="doc"{" open" if open_ else ""}><summary><span>{html.escape(title)}</span>'
            f'<span class="path">{html.escape(rel)}</span></summary><div class="md"><table>'
            f"<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div></details>")


def checklist(items):
    label = {"ok": "완료", "part": "일부", "no": "미완"}
    tr = "".join(f'<tr><td>{a}</td><td>{b}</td><td><span class="st {s}">{label[s]}</span></td><td>{c}</td></tr>'
                 for a, b, s, c in items)
    return ('<div class="card table-scroll"><table class="chk"><thead><tr><th>강의 요구 산출물</th><th>이 저장소의 파일</th>'
            f"<th>상태</th><th>메모</th></tr></thead><tbody>{tr}</tbody></table></div>")


def kpis(items):
    return '<div class="grid g4">' + "".join(
        f'<div class="card kpi"><b>{v}</b><span>{k}</span></div>' for v, k in items) + "</div>"


def page(fname, eyebrow, title, lead, body):
    nav = "".join(f'<a href="{f}" class="{"on" if f == fname else ""}">{n}</a>' for f, n in PAGES)
    doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title.split(" — ")[0])}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head><body>
<header class="hero"><div class="wrap"><nav class="tabs">{nav}</nav>
<div class="eyebrow">{eyebrow}</div><h1>{html.escape(title)}</h1><p class="lead">{lead}</p></div></header>
<main class="wrap">{body}
<p class="foot">수급 레이더 · 강의 과제용 개인 프로젝트 · 전체 흐름은 루트 <a href="../index.html">index.html</a> · 이 페이지는 <code>python scripts/build_local_package.py</code>로 md·csv 원본에서 생성했습니다. 원본 파일이 기준입니다.</p>
</main>
<button class="theme" id="theme" type="button">밝기 전환</button>
<script>document.getElementById('theme').onclick=()=>{{const r=document.documentElement;const d=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=d?'light':'dark';}};</script>
</body></html>"""
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(doc)


# ---------- 차트 (인라인 SVG) ----------
COLORS = ["var(--c1)", "var(--c2)", "var(--c3)", "var(--c4)", "var(--c5)", "var(--c6)"]


def price_index_chart():
    data = rows("research/data/auction_item_daily.csv")
    items = ["감자", "양파", "배추", "무", "콩나물", "숙주나물"]
    series = {i: [float(r["price_per_kg"]) for r in sorted([r for r in data if r["item"] == i], key=lambda r: r["date"])] for i in items}
    dates = sorted({r["date"] for r in data})
    W, H, L, B, T = 760, 300, 44, 30, 14
    lo, hi = 40, 140
    x = lambda k: L + k * (W - L - 12) / (len(dates) - 1)
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    s = ""
    for g in range(40, 141, 20):
        s += f'<line x1="{L}" x2="{W-12}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="var(--line)"/><text x="{L-6}" y="{y(g)+4:.1f}" font-size="11" text-anchor="end" fill="var(--muted)">{g}</text>'
    for k in (0, 13, 26):
        s += f'<text x="{x(k):.1f}" y="{H-8}" font-size="11" text-anchor="middle" fill="var(--muted)">{dates[k][5:]}</text>'
    for idx, i in enumerate(items):
        base = series[i][0]
        pts = " ".join(f"{x(k):.1f},{y(v / base * 100):.1f}" for k, v in enumerate(series[i]))
        width = 3 if i in ("무", "배추", "양파") else 1.6
        s += f'<polyline fill="none" stroke="{COLORS[idx]}" stroke-width="{width}" points="{pts}"/>'
    legend = "".join(f'<span><i style="background:{COLORS[k]}"></i>{i}</span>' for k, i in enumerate(items))
    return (f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="품목별 kg당 가격 지수">{s}</svg>'
            f'<div class="legend">{legend}<span>· 10/06 = 100, kg당 가중가격 (aT 경매 계산값)</span></div>')


def bars(pairs, color="var(--c1)", unit="", width=520):
    mx = max(v for _, v in pairs) or 1
    h = 26 * len(pairs) + 8
    s = ""
    for k, (lab, v) in enumerate(pairs):
        yy = 6 + k * 26
        w = v / mx * (width - 170)
        s += (f'<text x="0" y="{yy+14}" font-size="12.5" fill="var(--ink)">{html.escape(lab)}</text>'
              f'<rect x="110" y="{yy+2}" width="{w:.1f}" height="16" rx="4" fill="{color}"/>'
              f'<text x="{116+w:.1f}" y="{yy+15}" font-size="12" fill="var(--muted)">{v}{unit}</text>')
    return f'<svg class="chart" viewBox="0 0 {width} {h}" role="img">{s}</svg>'


def journey_sentiment_chart():
    data = rows("research/voices/voices_tagged.csv")
    stages = ["모니터링", "판단", "구매", "원가 반영"]
    sent = [("-", "var(--bad)", "부정"), ("0", "var(--c6)", "중립"), ("+", "var(--ok)", "긍정")]
    W, rowh = 560, 34
    s = ""
    mx = max(Counter(r["journey"] for r in data).values())
    for k, st in enumerate(stages):
        yy = 4 + k * rowh
        s += f'<text x="0" y="{yy+17}" font-size="12.5" fill="var(--ink)">{st}</text>'
        xx = 90
        for code, col, _ in sent:
            n = sum(1 for r in data if r["journey"] == st and r["sentiment"] == code)
            w = n / mx * (W - 130)
            if n:
                s += f'<rect x="{xx:.1f}" y="{yy+3}" width="{w:.1f}" height="20" fill="{col}"/><text x="{xx+w/2:.1f}" y="{yy+17}" font-size="11.5" text-anchor="middle" fill="#fff">{n}</text>'
            xx += w
    legend = "".join(f'<span><i style="background:{c}"></i>{l}</span>' for _, c, l in sent)
    return f'<svg class="chart" viewBox="0 0 {W} {4+len(stages)*rowh}" role="img" aria-label="여정 단계별 감정">{s}</svg><div class="legend">{legend}</div>'


def score_chart():
    data = rows("inventory/scoring.csv")
    types = ["품목", "산지", "시장", "위험요인", "수요신호", "안전규제"]
    col = dict(zip(types, COLORS))
    W, rh = 640, 22
    s = ""
    for k, r in enumerate(data):
        yy = 4 + k * rh
        v = float(r["트랙총점"])
        w = v / 5 * (W - 230)
        bold = ' font-weight="700"' if int(r["트랙순위"]) <= 3 else ""
        s += (f'<text x="0" y="{yy+14}" font-size="12"{bold} fill="var(--ink)">{r["트랙순위"]}. {html.escape(r["자산명"])}</text>'
              f'<rect x="190" y="{yy+3}" width="{w:.1f}" height="14" rx="3" fill="{col[r["유형"]]}"/>'
              f'<text x="{196+w:.1f}" y="{yy+14}" font-size="11.5" fill="var(--muted)">{v:.2f}</text>')
    legend = "".join(f'<span><i style="background:{col[t]}"></i>{t}</span>' for t in types)
    return f'<svg class="chart" viewBox="0 0 {W} {8+len(data)*rh}" role="img" aria-label="자산 30개 트랙 가중 총점">{s}</svg><div class="legend">{legend}</div>'


def change_chart():
    """M1 가격 변화율(첫 5영업일 대비 최근 5영업일)을 0 기준 막대로."""
    data = rows("research/metrics.csv")
    W, rh, mid = 420, 26, 230
    s = f'<line x1="{mid}" x2="{mid}" y1="0" y2="{len(data)*rh+4}" stroke="var(--line)"/>'
    for k, r in enumerate(sorted(data, key=lambda r: float(r["price_change"]))):
        v = float(r["price_change"])
        w = abs(v) / .5 * 170
        yy = 4 + k * rh
        x0 = mid - w if v < 0 else mid
        col = "var(--bad)" if v < -.2 else ("var(--c6)" if abs(v) < .02 else "var(--c1)")
        s += (f'<text x="0" y="{yy+14}" font-size="12.5" fill="var(--ink)">{r["item"]}</text>'
              f'<rect x="{x0:.1f}" y="{yy+2}" width="{max(w, 1.5):.1f}" height="16" rx="3" fill="{col}"/>'
              f'<text x="{(x0 - 6) if v < 0 else (mid + w + 6):.1f}" y="{yy+14}" font-size="12" text-anchor="{"end" if v < 0 else "start"}" fill="var(--muted)">{v*100:+.1f}%</text>')
    return f'<svg class="chart" viewBox="0 0 {W} {len(data)*rh+8}" role="img" aria-label="품목별 가격 변화율">{s}</svg>'


def stacked(parts):
    total = sum(n for _, n, _ in parts)
    seg = "".join(f'<span style="flex:{n};background:{c}" title="{l} {n}">{n}</span>' for l, n, c in parts)
    leg = "".join(f'<span><i style="background:{c}"></i>{l} {n}</span>' for l, n, c in parts)
    return f'<div class="stack">{seg}</div><div class="legend">{leg}<span>· 합계 {total}</span></div>'


# ---------- 페이지 ----------
def build_redirect():
    """예전 주소(local_package/index.html)로 들어와도 루트 index.html로 보낸다."""
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../index.html">'
                '<title>수급 레이더</title></head><body><a href="../index.html">전체 결과(index.html)로 이동</a></body></html>')


def build_day04():
    tagged = rows("research/voices/voices_tagged.csv")
    src = Counter(r["source_type"] for r in tagged)
    m = {r["item"]: r for r in rows("research/metrics.csv")}
    body = checklist([
        ("리뷰 분석 리포트 + 차트", "research/voices/ (voices_tagged.csv · report.md) + 이 페이지 차트", "ok", "리뷰 100건 대신 기사·공고·서비스 25건 (ROADMAP 단계 2)"),
        ("디지털 필드워크 계획서", "research/fieldwork_plan.md", "ok", "질문 6 → 소스 → 항목 → 분량"),
        ("자막 추출 테스트 1건", "archive/test/README.md", "no", "yt-dlp·Node 없음 — 미실시 기록"),
        ("지표 후보 정의 (데이터·서비스)", "research/metrics.md · metrics.csv", "ok", "6개, 계산식·한계 포함"),
        ("인사이트 3 (근거 id)", "research/insights.md", "ok", "근거 수준 표시"),
        ("소스별 표준 프롬프트", "research/fieldwork_plan.md 3절", "ok", "팀 CLAUDE.md 대신"),
        ("태깅 검수 10건", "research/voices/review_log.md", "part", "AI 점검만, 본인 확인 칸 비어 있음"),
    ])
    k = kpis([(f"{len(tagged)}건", "수집·태깅한 자료"), ("4건", "원문까지 확인"), (f"{float(m['무']['price_change'])*100:+.1f}%".replace("-", "−"), "무 kg당 가격 변화 (첫 주 → 최근 5일)"), ("52.9%", "감자 물량 중 평창군 비중")])
    chart1 = f'<div class="card">{price_index_chart()}</div>'
    chart2 = f'<div class="grid g2"><div class="card"><h4 style="margin:0 0 8px">여정 단계별 감정 (25건)</h4>{journey_sentiment_chart()}</div><div class="card"><h4 style="margin:0 0 8px">소스 분포</h4>{bars(sorted(src.items(), key=lambda x:-x[1]), "var(--c2)", "건", 460)}</div></div>'
    body += (f'<h2><span class="n">01</span>한눈에</h2>{k}'
             f'<h2><span class="n">02</span>차트 ① 한 달 사이 가격 흐름</h2><p class="sub">무·배추는 절반 가까이 내렸고, 감자·양파·콩나물·숙주는 ±10% 안에서 움직였습니다.</p>{chart1}'
             f'<h2><span class="n">03</span>차트 ② 사람들의 말</h2><p class="sub">부정 감정은 "원가 반영" 단계에 몰리고, 긍정은 예측·정보 서비스 쪽입니다.</p>{chart2}'
             f'<h2><span class="n">04</span>산출물</h2>'
             f'{md_doc("research/insights.md", "인사이트 3가지", open_=True)}'
             f'{md_doc("research/voices/report.md", "사람들의 말 분석 리포트")}'
             f'{md_doc("research/fieldwork_plan.md", "디지털 필드워크 계획서")}'
             f'{md_doc("research/metrics.md", "지표 후보 정의")}'
             f'{csv_doc("research/voices/voices_tagged.csv", "태깅 결과 (voices_tagged.csv)")}'
             f'{md_doc("research/voices/review_log.md", "태깅 검수 기록")}'
             f'{md_doc("archive/test/README.md", "자막 추출 테스트 — 미실시 기록")}')
    page("day04.html", "DAY 04 · 10/29 · 지역 자산 조사 방법론 2", "Day 04 — 사람들의 말에서 인사이트 도출",
         "공공데이터가 보여 주는 \"무슨 일이 있었나\" 옆에, 기사·채용공고·기존 서비스 속 사람들의 말로 \"무엇이 곤란한가\"를 채웠습니다.", body)


def build_day05():
    meta = rows("archive/metadata.csv")
    types = Counter(r["tags"].split("|")[0].replace("유형:", "") for r in meta)
    lic = Counter(r["license"] for r in meta)
    body = checklist([
        ("archive/video · image · text 폴더와 파일", "archive/text/ 노트 4건", "part", "video·image 0건 — 보강 목록"),
        ("archive/metadata.csv 20행 이상", "archive/metadata.csv", "ok", f"{len(meta)}행 · 14열 · id 중복 0"),
        ("tags.md · check_report.md \"통과\"", "archive/tags.md · check_report.md", "ok", "조건부 통과 (검색 요약 행 단독 근거 금지)"),
        ("collect_sheet.csv · questions.md", "archive/collect_sheet.csv · questions.md", "ok", "질문 7개"),
        ("파일명 5요소", "archive/text/20261109_기사_전국_배추급등_T01.md 등", "ok", "수집일_소스_장소_주제_id"),
    ])
    k = kpis([(f"{len(meta)}행", "metadata.csv"), (f"{len(types)}종", "자산 유형 태그"), ("56%", "가장 많은 소스(기사) 비중"), ("0건", "이름·닉네임")])
    charts = (f'<div class="grid g2"><div class="card"><h4 style="margin:0 0 8px">유형 태그</h4>{bars(sorted(types.items(), key=lambda x:-x[1]), "var(--c3)", "건", 460)}</div>'
              f'<div class="card"><h4 style="margin:0 0 8px">저작권 표기</h4>{bars(list(lic.items()), "var(--c4)", "건", 460)}</div></div>')
    body += (f'<h2><span class="n">01</span>한눈에</h2>{k}<h2><span class="n">02</span>분포</h2>{charts}'
             f'<h2><span class="n">03</span>산출물</h2>'
             f'{csv_doc("archive/metadata.csv", "metadata.csv — 수집물 25건", ["id", "type", "source", "title", "creator", "published_at", "license", "tags", "summary"], open_=True)}'
             f'{md_doc("archive/check_report.md", "점검 보고서")}{md_doc("archive/tags.md", "태그 규칙")}'
             f'{csv_doc("archive/collect_sheet.csv", "수집 시트")}{md_doc("archive/questions.md", "남은 질문")}'
             f'{md_doc("archive/text/20261109_기사_전국_배추급등_T01.md", "요약 노트 예시 · T01")}'
             f'{md_doc("archive/text/20261109_채용공고_서울_농산MD_J01.md", "요약 노트 예시 · J01")}')
    page("day05.html", "DAY 05 · 10/30 · 콘텐츠 아카이빙", "Day 05 — 수집한 것을 다시 찾을 수 있는 상태로",
         "수집물 한 건 = metadata.csv 한 줄. 소스·URL·일시·저작권을 남기고, 기사는 요약만 저장했습니다.", body)


def build_day06():
    sc = rows("inventory/scoring.csv")
    top = sc[:3]
    cards = "".join(f'<div class="card"><div class="eyebrow" style="color:var(--signal)">{r["트랙순위"]}위 · {r["asset_id"]}</div><h3 style="margin:2px 0">{r["자산명"]}</h3>'
                    f'<div class="kpi"><b>{float(r["트랙총점"]):.2f}</b><span>트랙 총점 · 공통 {r["공통순위"]}위 · 균등 {r["균등순위"]}위</span></div>'
                    f'<div style="font-size:13px;color:var(--muted);margin-top:6px">{html.escape(r["근거수치"])}</div></div>' for r in top)
    body = checklist([
        ("inventory_v1.xlsx (inventory · scoring · top3 시트)", "inventory/inventory_v1.xlsx", "ok", "scripts/build_inventory.py로 생성, 총점은 시트 수식"),
        ("자산 30개 · 근거 id 2개 이상", "inventory/inventory_v1.csv", "ok", "6유형: 품목·산지·시장·위험요인·수요신호·안전규제"),
        ("candidates.md · evidence_check.md \"통과\"", "inventory/", "ok", "근거 파일 존재 자동 검증"),
        ("top3_rationale.md (7항목)", "inventory/top3_rationale.md", "ok", "공통·트랙 Top 3 나란히"),
        ("2인 독립 채점 · 캘리브레이션", "-", "no", "혼자 진행 — 본인 채점 비교 예정"),
        ("Google Sheets 공유", "-", "no", "개인 프로젝트라 생략"),
    ])
    body += (f'<h2><span class="n">01</span>Top 3 (트랙 가중치)</h2><p class="sub">데이터 가용성 35 · 수요 규모 25 · 위험 크기 20 · 시장성 10 · 스토리성 10</p><div class="grid g3">{cards}</div>'
             f'<h2><span class="n">02</span>자산 30개 점수</h2><p class="sub">가중치를 바꿔도 양파·배추는 Top 3에 남습니다. 무와 가락시장이 3위를 두고 바뀝니다.</p><div class="card">{score_chart()}</div>'
             f'<h2><span class="n">03</span>산출물</h2>{md_doc("inventory/top3_rationale.md", "핵심 자산 선정 근거표", open_=True)}'
             f'{csv_doc("inventory/inventory_v1.csv", "inventory 시트 — 30개 · 11열")}'
             f'{csv_doc("inventory/scoring.csv", "scoring 시트 — 기준별 점수·총점", ["asset_id", "자산명", "유형", "데이터가용성", "수요규모", "위험크기", "시장성", "스토리성", "트랙총점", "트랙순위", "공통순위", "균등순위", "근거수치"])}'
             f'{md_doc("inventory/candidates.md", "후보 정리 기록")}{md_doc("inventory/evidence_check.md", "근거 검증 보고서")}'
             f'{md_doc("scripts/build_inventory.py", "점수 계산·검증 스크립트", code=True)}')
    page("day06.html", "DAY 06 · 11/02 · 지역 자산 인벤토리", "Day 06 — 수집물 더미를 자산 목록으로",
         "수집물과 경매 데이터에서 품목·산지·데이터 자산 30개를 꺼내 1·3·5점 척도로 채점하고, 대시보드 핵심 데이터 자산 Top 3를 골랐습니다.", body)


def build_day07():
    body = checklist([
        ("brand/persona_sheet.md (9항목)", "brand/persona_sheet.md", "ok", "핵심 자산 A02 양파, 사실/창작 표시"),
        ("brand/customer_persona.md", "brand/customer_persona.md", "ok", "상황→행동→동기→불만, 근거 id"),
        ("figjam_notes.md · tone_table.md", "brand/", "ok", "FigJam 대신 텍스트 발산, 여섯 질문 점검"),
        (".claude/skills/brand-…/SKILL.md + worldview.md", ".claude/skills/brand-sugeup-radar/", "ok", "SKILL 40줄 이내"),
        ("brand/test/before · after · diff_note", "brand/test/", "ok", "after 금칙어 0건"),
        ("segment_definition.md (데)", "plan/segment_definition.md", "ok", "축 2개 · 2×2 · 세그먼트 3"),
        ("onepager.md (데)", "plan/onepager.md", "ok", "10항목, 성공 신호에 숫자 없음"),
        ("새 세션 스킬 호출 확인", "-", "part", "본인 확인 필요"),
    ])
    persona = ('<div class="grid g3">'
               '<div class="card"><div class="eyebrow" style="color:var(--signal)">정체성 [창작]</div><p style="font-size:17px;font-weight:700;margin:4px 0">평소와 달라진 품목을 이유와 함께 먼저 알려 주는 수급 안내자</p>'
               '<span class="pill">차분한</span><span class="pill">정확한</span><span class="pill">먼저 살피는</span></div>'
               '<div class="card"><div class="eyebrow" style="color:var(--signal)">가치와 약속</div><p style="font-size:17px;font-weight:700;margin:4px 0">판단은 대신하지 않고, 변화와 이유를 먼저 보여 드린다.</p>'
               '<div style="font-size:13px;color:var(--muted)">금칙어: 폭등 · 폭락 · 대란 · 금값 · 역대급 · 반드시 오릅니다 · 지금 사세요 · 무조건 · 100% · 대박</div></div>'
               '<div class="card"><div class="eyebrow" style="color:var(--signal)">고객 (SG1 대표)</div><p style="font-size:17px;font-weight:700;margin:4px 0">식자재 유통사 농산 구매 담당자</p>'
               '<div style="font-size:13px;color:var(--muted)">소싱·수요 예측·시장 분석 (J01) · 불만: 급변(T03·T01), 흩어진 이유(S01~S03)</div></div></div>'
               '<h3>핵심 메시지 3</h3><div class="msg">평소와 달라진 품목을, 이유와 함께 먼저 보여 드립니다.</div>'
               '<div class="msg">모든 숫자에는 기준일과 출처가 붙어 있습니다.</div><div class="msg">판단은 담당자님이 합니다. 저희는 변화와 이유를 보여 드립니다.</div>')
    world = ('<div class="flow">'
             '<div class="s" style="--c:var(--c1)"><b>배경 [사실]</b>하루 약 10만9천 건의 경매. 밤 10시 반 시작, 한 건 4초. 숫자가 밤사이 방향을 바꾸는 세계</div>'
             '<div class="s" style="--c:var(--c2)"><b>인물</b>주인공: 구매 담당자 (J01) · 조력자: 레이더 [창작] · 주변: 중도매인·산지 농가·식당</div>'
             '<div class="s" style="--c:var(--bad)"><b>갈등</b>근거로 내리는 판단 vs 늦게 아는 급변·기준 없는 숫자 · 사건: 5월 양파(T03), 7월 배추(T01)</div>'
             '<div class="s" style="--c:var(--c3)"><b>가치</b>판단은 대신하지 않고 변화와 이유를 먼저</div>'
             '<div class="s" style="--c:var(--c4)"><b>톤앤매너</b>존댓말 · 짧은 문장 · 숫자엔 단위·기준·기준일 · 어두운 바탕에 바뀐 값 하나만 강조</div></div>')
    bef, aft = read("brand/test/before.md"), read("brand/test/after.md")
    pick = lambda t: markdown.markdown(t.split("## 앱 알림")[1], extensions=["sane_lists"])
    vs = (f'<div class="vs"><div class="card bad"><h4>스킬 없이 (before) — 금칙어 7 · 느낌표 5 · 구매 지시 3</h4><div class="md" style="padding:0">{pick(bef)}</div></div>'
          f'<div class="card good"><h4>스킬로 (after) — 금칙어 0 · 기준일·출처 3/3</h4><div class="md" style="padding:0">{pick(aft)}</div></div></div>')
    body += (f'<h2><span class="n">01</span>브랜드 페르소나</h2><p class="sub">이 프로젝트의 브랜드는 캐릭터가 아니라 서비스의 목소리입니다. 핵심 자산: A02 양파.</p>{persona}'
             f'<h2><span class="n">02</span>세계관 다섯 요소</h2><p class="sub">가치를 뒤집으면 갈등이 됩니다: "변화와 이유를 먼저" ↔ "늦게, 이유 없이, 과장되게".</p>{world}'
             f'<h2><span class="n">03</span>스킬 적용 전후</h2><p class="sub">같은 숫자(무 −45%)가 "사라는 신호"에서 "변화와 이유"로 바뀝니다.</p>{vs}'
             f'<h2><span class="n">04</span>산출물</h2>'
             f'{md_doc("brand/persona_sheet.md", "브랜드 페르소나 시트 (9항목)", open_=True)}'
             f'{md_doc("brand/customer_persona.md", "고객 페르소나")}'
             f'{md_doc(".claude/skills/brand-sugeup-radar/worldview.md", "세계관 바이블 worldview.md")}'
             f'{md_doc(".claude/skills/brand-sugeup-radar/SKILL.md", "브랜드 스킬 SKILL.md (Claude Code 지시서)", code=True)}'
             f'{md_doc("brand/figjam_notes.md", "발산 메모 → 다섯 요소")}{md_doc("brand/tone_table.md", "톤앤매너 Do / Don\'t · 여섯 질문")}'
             f'{md_doc("brand/test/diff_note.md", "적용 전후 비교표")}'
             f'{md_doc("plan/segment_definition.md", "사용자 세그먼트 정의 (데이터·서비스 과제)")}'
             f'{md_doc("plan/onepager.md", "한 장 기획서 (데이터·서비스 과제)")}{md_doc("brand/progress.md", "진행 기록")}')
    page("day07.html", "DAY 07 · 11/03 · 브랜드 페르소나 & 세계관", "Day 07 — 자산에 성격을 입히고 파일로 고정",
         "어떤 목소리로(브랜드 페르소나) 누구에게(고객 페르소나) 말할지 정하고, 세계관 바이블을 Claude Code가 읽는 브랜드 스킬로 바꿨습니다.", body)


def build_day08():
    body = checklist([
        ("훅 후보 5 · 구조 (채널·훅·전환·행동유도)", "storyboard/hooks_v1.md · structure_v1.md", "ok", "앱 화면 · 질문형 훅"),
        ("storyboard_v1.md 6~8컷 (여덟 칸)", "storyboard/storyboard_v1.md", "ok", "7컷"),
        ("review_v1.md 일관성 검토", "storyboard/review_v1.md", "ok", "위반 0 · 지적 2건 반영"),
        ("화면 흐름 표 + 시안 6화면 이상 (데)", "storyboard/screen_flow.md · screens/screens_v0.html", "ok", "Claude Design 대신 HTML 시안 7화면"),
        ("이벤트 데이터 명세 초안 (데)", "storyboard/events.md", "ok", "10개 이벤트"),
        ("local_package/ + 00_README.md", "local_package/", "ok", "원본 링크 방식"),
    ])
    stages = ('<div class="flow">'
              '<div class="s" style="--c:#C9772B"><b>① 훅 · 발견 (컷 1)</b>무 kg당 가격이 첫 주보다 45.6% 낮습니다. 이유를 보시겠어요?</div>'
              '<div class="s" style="--c:#4C6B8A"><b>② 전개 · 입력·결과 (컷 2~5)</b>담당 품목 → 알림 기준 → 수급판 → 산지</div>'
              '<div class="s" style="--c:#8A4C8A"><b>③ 전환 (컷 6)</b>같은 기간 물량은 두 배였습니다. 평소와 달라진 품목을, 이유와 함께 먼저 보여 드립니다.</div>'
              '<div class="s" style="--c:#2E8B6A"><b>④ 행동유도 (컷 7)</b>[이 품목 알림 받기] 버튼 1개</div></div>')
    body += (f'<h2><span class="n">01</span>네 단계</h2><p class="sub">훅과 전환을 이어 읽으면 "왜 45.6% 낮지?" → "물량이 두 배였기 때문". 대표 고객: SG1 구매 담당자.</p>{stages}'
             f'<h2><span class="n">02</span>화면 시안 7개</h2><p class="sub">숫자는 research/metrics.csv 계산값. 화면 아래에 생기는 데이터(이벤트)를 표시했습니다. <a href="../storyboard/screens/screens_v0.html">새 창에서 열기</a></p>'
             f'<iframe class="screens" src="../storyboard/screens/screens_v0.html" title="수급 레이더 화면 시안"></iframe>'
             f'<h2><span class="n">03</span>산출물</h2>'
             f'{md_doc("storyboard/storyboard_v1.md", "스토리보드 v1 — 7컷 샷 리스트", open_=True)}'
             f'{md_doc("storyboard/screen_flow.md", "화면 흐름 v0 — 여정 → 화면 → 데이터")}'
             f'{md_doc("storyboard/events.md", "이벤트 데이터 명세")}{md_doc("storyboard/review_v1.md", "일관성 검토")}'
             f'{md_doc("storyboard/hooks_v1.md", "훅 후보 5")}{md_doc("storyboard/structure_v1.md", "구조 v1")}'
             f'{md_doc("storyboard/screens/prompt.md", "시안 생성 프롬프트·수정 이력")}')
    page("day08.html", "DAY 08 · 11/04 · 디지털 내러티브 스토리보드", "Day 08 — 스토리보드로 Local 모듈 마무리",
         "브랜드 스킬과 고객 페르소나를 앱 화면 7컷(훅 → 전개 → 전환 → 행동유도)으로 옮기고, 화면마다 생기는 데이터를 이벤트 명세로 정리했습니다.", body)


SEG_NAME = {"SG1": "SG1 계획형 구매 담당", "SG2": "SG2 단가 고정형 급식", "SG3": "SG3 버티는 소규모 식당"}
STAGES = ["모니터링", "판단", "구매", "원가 반영"]
STAGE_SUB = {"모니터링": "시세 확인", "판단": "이상 판단", "구매": "구매·발주", "원가 반영": "원가·메뉴 반영"}
ROWS = [("행동", "행동"), ("생각", "생각 (요지)"), ("접점", "접점"), ("감정", "감정 [I]"), ("불편", "불편"),
        ("데이터", "데이터 근거"), ("기회", "수급 레이더 기회"), ("화면", "화면 · 이벤트")]
EMO_LABEL = {-2: "매우 불편", -1: "불편", 0: "보통", 1: "좋음", 2: "매우 좋음"}


def evidence_levels():
    lv = {r["id"]: r["evidence_level"] for r in rows("research/voices/voices_tagged.csv")}
    cls = {"원문 확인": "e-ok", "검색 요약": "e-sum", "제목만": "e-title", "미확인": "e-un"}
    return lambda i: ("e-calc", "계산값") if i.startswith("M") else (cls.get(lv.get(i, ""), "e-un"), lv.get(i, "미확인"))


def emotion_chart(cells):
    W, H, L, R, T, B = 720, 200, 70, 20, 16, 30
    x = lambda k: L + (k + .5) * (W - L - R) / 4
    y = lambda v: T + (2 - v) / 4 * (H - T - B)
    s = ""
    for v in range(-2, 3):
        s += (f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="var(--line)"{" stroke-dasharray=\"3 3\"" if v else ""}/>'
              f'<text x="{L-8}" y="{y(v)+4:.1f}" font-size="11" text-anchor="end" fill="var(--muted)">{f"{v:+d}" if v else "0"} {EMO_LABEL[v]}</text>')
    for k, st in enumerate(STAGES):
        s += f'<text x="{x(k):.1f}" y="{H-8}" font-size="12" text-anchor="middle" fill="var(--ink)">{st}</text>'
    for idx, (sg, col) in enumerate(zip(SEG_NAME, ["var(--c1)", "var(--c4)", "var(--c2)"])):
        pts = [(x(k), y(int(cells[(sg, st, "감정")]["text"]) + (idx - 1) * .06)) for k, st in enumerate(STAGES)]
        w = 3.2 if sg == "SG1" else 2
        s += f'<polyline fill="none" stroke="{col}" stroke-width="{w}" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}"/>'
        s += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="{5 if sg == "SG1" else 4}" fill="{col}" stroke="var(--card)" stroke-width="2"/>' for a, b in pts)
    s += (f'<rect x="{x(1)-48:.1f}" y="{T-6}" width="96" height="{H-T-B+12}" rx="10" fill="var(--signal)" opacity=".10"/>'
          f'<text x="{x(1):.1f}" y="{T+6}" font-size="11" font-weight="700" text-anchor="middle" fill="var(--signal)">결정적 순간</text>')
    legend = "".join(f'<span><i style="background:{c}"></i>{SEG_NAME[s_]}</span>' for s_, c in zip(SEG_NAME, ["var(--c1)", "var(--c4)", "var(--c2)"]))
    return (f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="고객 유형별 여정 단계 감정 곡선">{s}</svg>'
            f'<div class="legend">{legend}<span>· 점수는 수집물 감정 태그와 불편 내용을 본 해석 [I], 측정값 아님</span></div>')


def journey_grid(sg, cells, lvl):
    tag_label = {"F": ("t-f", "F"), "I": ("t-i", "I"), "U": ("t-u", "U")}
    out = '<div class="jm-head"></div>' + "".join(
        f'<div class="jm-head"><span>{k+1}</span>{STAGE_SUB[st]}<small>{st}</small></div>' for k, st in enumerate(STAGES))
    for key, label in ROWS:
        if not any(cells.get((sg, st, key), {}).get("text") for st in STAGES):
            continue
        out += f'<div class="jm-lab">{label}</div>'
        for st in STAGES:
            c = cells.get((sg, st, key), {"text": "", "evidence": "", "tag": ""})
            if not c["text"]:
                out += '<div class="jm-cell empty">—</div>'
                continue
            ev = "".join(f'<span class="ev {lvl(i)[0]}" title="{html.escape(lvl(i)[1])}">{i}</span>' for i in c["evidence"].split("|") if i)
            tg = f'<span class="tg {tag_label[c["tag"]][0]}">{tag_label[c["tag"]][1]}</span>' if c["tag"] else ""
            if key == "감정":
                v = int(c["text"])
                out += f'<div class="jm-cell emo" style="--v:{v}"><b>{f"{v:+d}" if v else "0"}</b> {EMO_LABEL[v]} {tg}<div>{ev}</div></div>'
            else:
                extra = " key" if key in ("기회", "화면") else ""
                extra += " moment" if st == "판단" else ""
                out += f'<div class="jm-cell{extra}">{html.escape(c["text"])} {tg}<div>{ev}</div></div>'
    return f'<div class="table-scroll"><div class="jm">{out}</div></div>'


def build_journey():
    data = rows("plan/journey_map.csv")
    cells = {(r["segment"], r["stage"], r["row"]): r for r in data}
    lvl = evidence_levels()
    types = [
        ("SG1", "1차 대상", "var(--c1)", "식자재 유통사·프랜차이즈·식자재마트의 농산 구매 담당(MD)",
         "소싱·협력사 개발, 수요 예측·시장 분석", "숫자는 많지만 왜 변했는지·산지 상황은 따로 찾아야 함", "J01 · J03 · J04 · S04 · S05", "강함"),
        ("SG2", "2차 후보", "var(--c4)", "학교·단체 급식의 식단·식재료 담당",
         "정해진 식품비 안에서 식단을 꾸림", "식품비 +8.7% 대비 배춧값 +78% (2022)", "T13 · T14", "약함"),
        ("SG3", "2차 후보", "var(--c2)", "김치·겉절이를 기본 반찬으로 내는 소규모 한식당 운영자",
         "배춧값이 오르면 다른 채소로 바꿀지 고민", "5명 미만 사업장 약 52%가 원가 상승분을 판매가에 반영 못 함", "T01 · T02 · T06", "중간"),
    ]
    tcards = "".join(
        f'<div class="card seg" style="--c:{c}"><div class="seg-top"><b>{SEG_NAME[s]}</b><span class="pill">{pri}</span></div>'
        f'<p class="who">{who}</p><dl><dt>하는 일</dt><dd>{do}</dd><dt>핵심 불편</dt><dd>{pain}</dd>'
        f'<dt>근거</dt><dd>{ev} · 근거 강도 <b>{strength}</b></dd></dl></div>'
        for s, pri, c, who, do, pain, ev, strength in types)
    matrix = ('<div class="mx"><div></div><div class="mx-h">조직 구매</div><div class="mx-h">개인 사업자</div>'
              '<div class="mx-h side">소싱·예측으로 대응</div><div class="mx-c" style="--c:var(--c1)"><b>SG1 계획형 구매 담당</b>J01 · J03 · J04</div>'
              '<div class="mx-c none">근거 없음 — 유형으로 두지 않음</div>'
              '<div class="mx-h side">메뉴·재료 대체로 대응</div><div class="mx-c" style="--c:var(--c4)"><b>SG2 단가 고정형 급식</b>T13 · T14</div>'
              '<div class="mx-c" style="--c:var(--c2)"><b>SG3 버티는 소규모 식당</b>T01 · T02 · T06</div></div>')
    excluded = ('<div class="grid g3">'
                '<div class="card"><b>산지 농민·생산자</b> <small>T03 · T07</small><br><span class="muted">같은 하락이 이쪽엔 위험. 출하 판단은 범위 밖</span></div>'
                '<div class="card"><b>정부·연구기관</b> <small>T03 · T08 · R01</small><br><span class="muted">데이터·예측을 만드는 쪽 = 출처</span></div>'
                '<div class="card"><b>중도매인</b> <small>T11 · T12</small><br><span class="muted">구매 여정의 접점으로만 다룸</span></div></div>')
    tabs = "".join(f'<button type="button" class="segtab{" on" if s == "SG1" else ""}" data-sg="{s}">{SEG_NAME[s]}</button>' for s in SEG_NAME)
    grids = "".join(f'<div class="jm-wrap" data-sg="{s}"{"" if s == "SG1" else " hidden"}>{journey_grid(s, cells, lvl)}</div>' for s in SEG_NAME)
    legend = ('<div class="legend"><span><span class="ev e-ok">id</span> 원문 확인</span><span><span class="ev e-sum">id</span> 검색 요약</span>'
              '<span><span class="ev e-title">id</span> 제목만</span><span><span class="ev e-un">id</span> 미확인</span><span><span class="ev e-calc">M</span> 계산값</span>'
              '<span><span class="tg t-f">F</span> 사실</span><span><span class="tg t-i">I</span> 해석</span><span><span class="tg t-u">U</span> 미확인</span></div>')
    script = ("<script>document.querySelectorAll('.segtab').forEach(b=>b.onclick=()=>{document.querySelectorAll('.segtab').forEach(x=>x.classList.toggle('on',x===b));"
              "document.querySelectorAll('.jm-wrap').forEach(w=>w.hidden=w.dataset.sg!==b.dataset.sg);});</script>")
    body = (f'<h2><span class="n">01</span>고객 유형 지정</h2><p class="sub">인구통계가 아니라 수집물에서 읽은 행동 질문 두 개로 나눕니다. '
            f'Q1 누가 사는가 × Q2 값이 크게 바뀌면 어떻게 버티는가. 사용자 인터뷰 전 가설입니다.</p>'
            f'<div class="grid g2" style="align-items:start"><div class="card">{matrix}</div>'
            f'<div class="card"><b>첫 버전의 지정 방식</b><p style="margin:6px 0 0">가입할 때 본인이 Q1·Q2에 답해 유형을 고릅니다 (<code>segment_set</code>). '
            f'행동 기록으로 자동 분류하는 것은 사용자 데이터가 생긴 뒤에 합니다. 유형에 따라 바뀌는 것은 <b>데이터가 아니라 화면 문구와 알림 빈도</b>입니다.</p></div></div>'
            f'<div class="grid g3" style="margin-top:12px">{tcards}</div>'
            f'<h3 style="margin:22px 0 8px">유형에서 뺀 사람들</h3>{excluded}'
            f'<h2><span class="n">02</span>감정 곡선 비교</h2><p class="sub">세 유형 모두 <b>판단</b> 단계에서 가장 낮습니다. "왜 변했는지"를 따로 찾아야 하는 순간이고, '
            f'스토리보드의 전환 컷(6 이유 카드)이 놓이는 자리입니다.</p><div class="card">{emotion_chart(cells)}</div>'
            f'<h2><span class="n">03</span>고객여정지도</h2><p class="sub">단계는 Day 04 태깅의 journey 값 4개를 그대로 씁니다. 칸마다 근거 id와 [F]/[I]/[U]를 붙였습니다. '
            f'‘생각’ 칸은 수집물의 요지를 정리한 것이고 직접 인용이 아닙니다. 구매 단계에서 서비스는 구매를 권하지 않습니다.</p>'
            f'<div class="segtabs">{tabs}</div>{grids}{legend}'
            f'<h2><span class="n">04</span>여정에서 나온 결정</h2>'
            f'<div class="flow"><div class="s" style="--c:var(--c1)"><b>첫 화면</b>가격표가 아니라 평소와 달라진 품목 3개 (모니터링 불편 → 화면 1)</div>'
            f'<div class="s" style="--c:var(--signal)"><b>핵심 화면</b>숫자 옆 이유 한 줄 + 기준일 + 출처 (판단 불편 → 화면 6, 지표: 근거 열람률)</div>'
            f'<div class="s" style="--c:var(--c3)"><b>행동</b>구매 버튼 없이 알림 받기 1개 (구매 단계 비개입 → 화면 7)</div>'
            f'<div class="s" style="--c:var(--c4)"><b>유형별 차이</b>SG1 품목별 임계값 · SG2 월 요약 · SG3 주 1회 쉬운 말</div></div>'
            f'<h2><span class="n">05</span>원본</h2>{md_doc("plan/customer_types.md", "고객 유형 지정 — 규칙·유형·제외·결정")}'
            f'{csv_doc("plan/journey_map.csv", "여정지도 데이터 (이 페이지의 원본)")}{script}')
    page("journey.html", "고객 유형 · 고객여정지도 · 2026-11-09", "고객 유형과 고객여정지도",
         "Day 04 수집물 25건과 Day 07 세그먼트를 바탕으로 수급 레이더의 고객을 세 유형으로 지정하고, 같은 4단계(시세 확인 → 이상 판단 → 구매·발주 → 원가·메뉴 반영)로 여정을 그렸습니다.", body)


if __name__ == "__main__":
    build_journey()
    build_redirect()
    build_day04()
    build_day05()
    build_day06()
    build_day07()
    build_day08()
    print("local_package/ HTML 7개 생성")
