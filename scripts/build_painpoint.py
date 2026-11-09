"""Day 11 페인포인트 산출물의 md·html을 csv 원본에서 만든다.

저장소 루트에서 실행:
    python scripts/build_painpoint.py

원본: painpoint/journey_map.csv (SG1 여정), painpoint/journey_3actors.csv (세 사람 여정),
      painpoint/voc_classified.csv (근거 수준 표시용)
생성: painpoint/journey_map.md · journey_map.html · journey_3actors.md · journey_3actors.html
"""
import csv
import html
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PP = os.path.join(ROOT, "painpoint")
H = html.escape

ROWS = ["행동", "생각", "감정", "터치포인트", "페인포인트", "기회"]
TOP = {"P1": "평소 값·물량·산지를 한곳에서 비교할 수 없음", "P2": "출하가 몰려 값이 무너짐", "P3": "원가 상승분을 판매가에 넘기지 못함"}
# 손 넘김 지점: (번호, 앞 사람 단계, 뒤 사람 단계, 설명, 측정 신호, 페인포인트)
HANDOFFS = [
    ("①", "산지 생산자 · P3 경매 출하하기", "중도매인 · M1 경매 참여하기", "출하 → 경매: 반입이 한꺼번에 몰림",
     "반입량 변화율 M3 (무 +100.5%) · 산지 쏠림 M4 (감자 평창 52.9%)", "P2"),
    ("②", "중도매인 · M1 경매 참여하기", "구매 담당 · J2 이상 알아차리기", "낙찰 → 매입 판단: 기준가가 날마다 흔들림",
     "가격 변화율 M1 (무 −45.6%) · 가격 출렁임 M2 (배추 27.5%)", "P1"),
    ("③", "구매 담당 · J6 원가 반영하기", "거래처(급식·식당)", "납품 → 거래처 단가: 원가 상승분을 넘기지 못함",
     "+20% 넘게 오른 품목 수 · 같은 용도 품목 가격 차이", "P3"),
]


def rows(name):
    with open(os.path.join(PP, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def levels():
    out = {}
    with open(os.path.join(ROOT, "research/voices/voices_tagged.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            out[r["id"]] = r["evidence_level"]
    return out


LV = levels()
LV_CLS = {"원문 확인": "ok", "검색 요약": "sum", "제목만": "tt", "미확인": "un"}


def ev_html(ev):
    return "".join(f'<i class="ev {LV_CLS.get(LV.get(i, ""), "un")}" title="{H(LV.get(i, "미확인"))}">{H(i)}</i>' for i in ev.split("|") if i)


def ev_md(ev):
    return " · ".join(ev.split("|")) if ev else ""


def top_tag(text):
    for k in TOP:
        if text.startswith(k + " ") or text.startswith(k):
            return k
    return ""


def emo_value(text):
    t = text.replace("−", "-")
    for v in ("-2", "-1", "+1", "+2"):
        if t.startswith(v):
            return int(v)
    return None


# ---------- SG1 여정 ----------
def build_sg1():
    data = rows("journey_map.csv")
    stages = list(OrderedDict.fromkeys(r["stage"] for r in data))
    cell = {(r["stage"], r["row"]): r for r in data}

    md = ["# 고객 여정 지도 v1 — 식자재 유통사 농산 구매 담당자 (SG1)", "",
          "- 작성일: 2026-11-09 · Day 11 · 원본: [journey_map.csv](journey_map.csv) → `python scripts/build_painpoint.py`로 이 파일과 HTML 생성",
          "- **행위자:** [brand/customer_persona.md](../brand/customer_persona.md)의 페르소나 1 (한 사람)",
          "- **시나리오 · 목표:** 매일 아침 담당 품목(양파·무·배추)의 시세를 보고, 평소와 달라진 품목을 이유와 함께 파악해 매입과 거래처 단가를 정한다.",
          "- **단계:** 6개, 도구·장소가 바뀌는 곳에서 끊음. 감정은 같은 단계 VOC의 부정·중립·긍정 건수로 정하고 3건 미만은 \"근거 부족\", 없으면 \"수집 필요\".",
          "- **감정 최저점:** VOC 기준 J6 원가 반영하기 (−2, 5건 — 단 말한 사람은 급식·식당). J2·J3는 근거 부족이라 점수를 매기지 않음.",
          "- Day 07의 4단계 여정([plan/journey_map.csv](../plan/journey_map.csv))은 세 유형 비교용, 이 지도는 한 사람의 v1입니다.", "",
          "| 층 | " + " | ".join(stages) + " |", "|---" * (len(stages) + 1) + "|"]
    for r in ROWS:
        line = []
        for s in stages:
            c = cell.get((s, r), {"text": "", "evidence": ""})
            line.append((c["text"] + (f" ({ev_md(c['evidence'])})" if c["evidence"] else "")).replace("|", "/"))
        md.append(f"| **{r}** | " + " | ".join(line) + " |")
    md += ["", "Top 3 정의: [painpoint_def.md](painpoint_def.md) · 세 사람 여정: [journey_3actors.md](journey_3actors.md)"]
    with open(os.path.join(PP, "journey_map.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    # HTML
    head = "".join(f'<div class="sh"><span>{k+1}</span>{H(s.split(" ", 1)[1])}<small>{H(s.split(" ", 1)[0])}</small></div>' for k, s in enumerate(stages))
    body = ""
    for r in ROWS:
        body += f'<div class="rl">{r}</div>'
        for s in stages:
            c = cell.get((s, r), {"text": "", "evidence": ""})
            t = c["text"]
            if r == "감정":
                v = emo_value(t)
                cls = "emo" + (f" v{v + 2}" if v is not None else " none")
                body += f'<div class="c {cls}"><b>{H(t.split(" ", 1)[0]) if v is not None else ""}</b>{H(t if v is None else t.split(" ", 1)[1])}<div>{ev_html(c["evidence"])}</div></div>'
                continue
            k = top_tag(t) if r == "페인포인트" else ""
            cls = "c" + (" top" if k else "") + (" empty" if t in ("", "—") or t.startswith("수집 필요") else "")
            badge = f'<em class="no">{k}</em>' if k else ""
            shown = t[len(k):].strip() if k else t
            body += f'<div class="{cls}">{badge}{H(shown)}<div>{ev_html(c["evidence"])}</div></div>'
    # 감정 곡선 (VOC 근거가 있는 칸만 점, 나머지는 빈 원)
    W, Hh = 1000, 90
    xs = [W * (k + .5) / len(stages) for k in range(len(stages))]
    pts, svg = [], ""
    for k, s in enumerate(stages):
        v = emo_value(cell[(s, "감정")]["text"])
        y = 45 - (v or 0) * 18
        if v is None:
            svg += f'<circle cx="{xs[k]:.0f}" cy="45" r="6" fill="#fff" stroke="#ADB5BD" stroke-width="2" stroke-dasharray="3 2"/>'
        else:
            pts.append((xs[k], y))
            svg += f'<circle cx="{xs[k]:.0f}" cy="{y:.0f}" r="8" fill="#E8603C"/>'
    svg = f'<line x1="0" x2="{W}" y1="45" y2="45" stroke="#E6E8EB" stroke-dasharray="4 4"/>' + svg
    top_cards = "".join(f'<div class="tp"><em class="no">{k}</em><b>{H(v)}</b></div>' for k, v in TOP.items())
    page("journey_map.html", "고객 여정 지도 v1 — 식자재 구매 담당자 (SG1)",
         "Day 11 · 행위자 1명 · 6단계 × 6층 · 모든 칸에 근거 id 또는 “수집 필요”",
         "매일 아침 담당 품목의 시세를 보고, 평소와 달라진 품목을 이유와 함께 파악해 매입과 거래처 단가를 정한다.",
         f'<div class="tops">{top_cards}</div>'
         f'<div class="scroll"><div class="g" style="--n:{len(stages)}"><div></div>{head}'
         f'<div class="rl">감정 곡선</div><div class="curve" style="grid-column:span {len(stages)}"><svg viewBox="0 0 {W} {Hh}" preserveAspectRatio="none">{svg}</svg></div>'
         f'{body}</div></div>'
         '<p class="note">감정은 같은 단계 VOC의 부정·중립·긍정 건수로 정함. 3건 미만은 “근거 부족”(빈 원), VOC가 없으면 “수집 필요”. '
         'VOC 11건은 기사·채용공고 요약이며 구매 담당자 본인의 말은 아직 없음 (local_package/feedback.md #3).</p>')


# ---------- 세 사람 여정 ----------
def build_3actors():
    data = rows("journey_3actors.csv")
    actors = list(OrderedDict.fromkeys(r["actor"] for r in data))
    md = ["# 세 사람의 여정 — 산지 생산자 · 중도매인 · 구매 담당 (데이터·서비스 트랙 과제)", "",
          "- 작성일: 2026-11-09 · 원본: [journey_3actors.csv](journey_3actors.csv)",
          "- 수업 예시(구매자·판매자·물류)를 수급 레이더의 줄기에 맞게 바꿈: **판매자 = 산지 생산자, 물류·중개 = 중도매인, 구매자 = 식자재 구매 담당(SG1)**",
          "- 세 사람을 같은 단계 이름으로 맞추지 않고, 각자의 순서로 그린 뒤 손이 넘어가는 지점만 연결합니다.", ""]
    for a in actors:
        md += [f"## {a}", "", "| 단계 | 행동 | 페인포인트 |", "|---|---|---|"]
        stages = list(OrderedDict.fromkeys(r["stage"] for r in data if r["actor"] == a))
        for s in stages:
            g = {r["row"]: r for r in data if r["actor"] == a and r["stage"] == s}
            fmt = lambda k: (g[k]["text"] + (f" ({ev_md(g[k]['evidence'])})" if g[k]["evidence"] else "")) if k in g else ""
            md.append(f"| {s} | {fmt('행동')} | {fmt('페인포인트')} |")
        md.append("")
    md += ["## 손이 넘어가는 지점 = 대시보드 지표 후보", "", "| 지점 | 앞 → 뒤 | 무슨 일 | 측정 신호 | 페인포인트 |", "|---|---|---|---|---|"]
    md += [f"| {n} | {a} → {b} | {d} | {s} | {p} |" for n, a, b, d, s, p in HANDOFFS]
    md += ["", "신호 M1~M5는 [research/metrics.md](../research/metrics.md)의 정의, 값은 aT 경매 2026-10-06~11-05 계산값."]
    with open(os.path.join(PP, "journey_3actors.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    lanes = ""
    for a in actors:
        stages = list(OrderedDict.fromkeys(r["stage"] for r in data if r["actor"] == a))
        cards = ""
        for s in stages:
            g = {r["row"]: r for r in data if r["actor"] == a and r["stage"] == s}
            p = g.get("페인포인트", {"text": "", "evidence": ""})
            k = top_tag(p["text"])
            pcls = "pp" + (" top" if k else "") + (" empty" if p["text"] in ("", "—") or p["text"].startswith("수집 필요") else "")
            cards += (f'<div class="st"><b>{H(s)}</b><span>{H(g["행동"]["text"])}</span><div>{ev_html(g["행동"]["evidence"])}</div>'
                      f'<div class="{pcls}">{f"<em class=no>{k}</em>" if k else ""}{H(p["text"][len(k):].strip() if k else p["text"])}<div>{ev_html(p["evidence"])}</div></div></div>')
        lanes += f'<div class="lane"><div class="who">{H(a)}</div><div class="sts">{cards}</div></div>'
    hand = "".join(f'<div class="ho"><span class="hn">{n}</span><div><b>{H(d)}</b><small>{H(a)} → {H(b)}</small>'
                   f'<p>신호: {H(s)}</p></div><em class="no">{p}</em></div>' for n, a, b, d, s, p in HANDOFFS)
    page("journey_3actors.html", "세 사람의 여정 — 생산자 · 중도매인 · 구매 담당",
         "Day 11 과제 · 데이터·서비스 트랙 · 손이 넘어가는 지점 = 대시보드 지표 후보",
         "한 품목이 세 사람의 손을 거칩니다. 페인포인트는 손이 넘어가는 지점에서 생기고, 그 지점의 데이터가 지표가 됩니다.",
         f'<div class="lanes">{lanes}</div><h2>손이 넘어가는 지점</h2><div class="hos">{hand}</div>'
         '<p class="note">측정 신호의 값은 aT 경매 2026-10-06~11-05 계산값(research/metrics.csv). 생산자 몫·중도매인 VOC는 수집 필요.</p>')


CSS = """
:root{color-scheme:light;--ink:#111418;--ink2:#4A5159;--ink3:#6B727A;--line:#E6E8EB;--band:#F5F6F7;--accent:#FFD400;--coral:#E8603C}
*{box-sizing:border-box} body{margin:0;background:#fff;color:var(--ink);font-family:Pretendard,"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif;font-size:13.5px;line-height:1.45;word-break:keep-all;overflow-wrap:anywhere}
.page{max-width:1320px;margin:0 auto;padding:22px 20px 36px}
.eyebrow{margin:0;color:var(--ink3);font-weight:800;font-size:13px} h1{margin:2px 0 4px;font-size:26px;font-weight:900;letter-spacing:-.03em}
.lead{margin:0;font-size:15.5px;color:var(--ink2)} .lead b{background:linear-gradient(transparent 60%,var(--accent) 60%)}
h2{font-size:18px;margin:22px 0 10px}
.tops{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 4px}
.tp{display:flex;align-items:center;gap:8px;border:2px solid var(--coral);border-radius:12px;padding:6px 12px;background:#FCEBE5;font-size:14px}
.no{display:inline-grid;place-items:center;min-width:30px;height:24px;border-radius:99px;background:var(--coral);color:#fff;font-style:normal;font-weight:900;font-size:12px;padding:0 6px;margin-right:6px}
.scroll{overflow-x:auto;margin-top:12px}
.g{display:grid;grid-template-columns:92px repeat(var(--n),minmax(150px,1fr));gap:6px;min-width:1100px}
.sh{background:var(--ink);color:#fff;border-radius:10px;padding:8px 10px;font-weight:900;font-size:14px}
.sh span{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--accent);color:var(--ink);font-size:11px;margin-right:6px}
.sh small{display:block;color:#AEB4BA;font-weight:700;font-size:11px}
.rl{font-weight:900;font-size:12.5px;color:var(--ink2);padding:8px 2px}
.c{background:var(--band);border-radius:10px;padding:8px 10px}
.c.empty{background:#fff;border:1.5px dashed #CED4DA;color:var(--ink3)}
.c.top{background:#FCEBE5;box-shadow:inset 0 0 0 2.5px var(--coral);font-weight:700}
.c.emo b{display:block;font-size:20px;font-weight:900}
.c.emo.v0{background:#FFE3E3} .c.emo.v1{background:#FFF0F0} .c.emo.none{background:#fff;border:1.5px dashed #CED4DA;color:var(--ink3)}
.curve{background:#fff;border:1px solid var(--line);border-radius:10px;height:90px}
.curve svg{width:100%;height:100%}
.ev{display:inline-block;font-style:normal;font-size:10.5px;font-weight:800;border-radius:5px;padding:0 5px;margin:4px 3px 0 0;font-family:ui-monospace,Consolas,monospace}
.ev.ok{background:#E0F3E5;color:#1E6B30} .ev.sum{background:#E1ECFC;color:#0F3F82} .ev.tt{background:#FFF1A8;color:#4D3D00} .ev.un{background:#ECEEF0;color:#6B727A}
.note{margin:14px 0 0;font-size:12.5px;color:var(--ink3)}
.lanes{display:flex;flex-direction:column;gap:12px;margin-top:16px}
.lane{display:grid;grid-template-columns:120px 1fr;gap:10px;align-items:stretch}
.who{background:var(--ink);color:#fff;border-radius:12px;padding:12px;font-weight:900;font-size:15px;display:flex;align-items:center}
.sts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.st{background:var(--band);border-radius:12px;padding:10px 12px;display:flex;flex-direction:column;gap:3px}
.st b{font-size:13.5px} .st>span{color:var(--ink2)}
.pp{margin-top:6px;border-radius:8px;padding:6px 8px;background:#fff;font-size:12.5px}
.pp.top{background:#FCEBE5;box-shadow:inset 0 0 0 2px var(--coral);font-weight:700} .pp.empty{color:var(--ink3);border:1px dashed #CED4DA}
.hos{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.ho{display:flex;gap:10px;align-items:flex-start;border:2px dashed var(--coral);border-radius:14px;padding:12px}
.ho>div{flex:1} .ho b{display:block;font-size:14.5px} .ho small{color:var(--ink3)} .ho p{margin:6px 0 0;font-weight:700}
.hn{flex:none;display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--coral);color:#fff;font-weight:900}
@media (max-width:760px){.page{padding:16px} h1{font-size:22px} .lane{grid-template-columns:1fr} .sts{grid-template-columns:1fr 1fr} .hos{grid-template-columns:1fr}}
"""


def page(name, title, eyebrow, lead, body):
    doc = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>{H(title.split(" — ")[0])}</title><style>{CSS}</style></head><body><main class="page">'
           f'<p class="eyebrow">{H(eyebrow)}</p><h1>{H(title)}</h1><p class="lead">{H(lead)}</p>{body}</main></body></html>')
    with open(os.path.join(PP, name), "w", encoding="utf-8") as f:
        f.write(doc)


if __name__ == "__main__":
    build_sg1()
    build_3actors()
    print("painpoint/ md 2 · html 2 생성")
