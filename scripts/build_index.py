"""루트 index.html — 과제 결과를 한 줄기(01~07)의 카드로 보여 주는 단일 입구를 만든다.

저장소 루트에서 실행:
    python scripts/build_index.py

하는 일
1. scripts/build_local_package.py로 Day 04~08·고객여정 상세 페이지를 먼저 만든다.
2. 홈: 문제(Day 04) → 근거(05) → 자산(06) → 목소리(07) → 고객(여정) → 화면(08) → 기업(09~10)
   한 줄기를 카드로 그린다. 숫자는 모두 저장소의 csv·md에서 읽는다.
3. 상세 화면: Day 페이지와 기업 원페이지·밸류체인을 index.html 안에 넣어(srcdoc) 파일 하나로 열리게 한다.

원본은 csv·md와 각 html 파일이다. index.html은 생성물이므로 직접 고치지 않는다.
"""
import csv
import html
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_local_package as lp  # noqa: E402
import build_painpoint as bp  # noqa: E402

ROOT = lp.ROOT
H = html.escape


def rows(rel):
    return lp.rows(rel)


def read(rel):
    return lp.read(rel)


# ---------- 상세 화면에 넣을 페이지 ----------
DETAIL = [  # (route, 탭 이름, 파일)
    ("day04", "01 조사", "local_package/day04.html"),
    ("day05", "02 아카이브", "local_package/day05.html"),
    ("day06", "03 인벤토리", "local_package/day06.html"),
    ("day07", "04 브랜드·세계관", "local_package/day07.html"),
    ("journey", "05 고객 여정", "local_package/journey.html"),
    ("day08", "06 스토리보드", "local_package/day08.html"),
    ("industry", "08 산업 가치사슬", "valuechain/industry/valuechain_v1.html"),
    ("painpoint", "09 여정·페인포인트", "painpoint/journey_map.html"),
    ("actors", "09 세 사람 여정", "painpoint/journey_3actors.html"),
]
DETAIL_ROUTES = {r for r, _, _ in DETAIL}


def embed_local(rel, css):
    """local_package 페이지를 srcdoc용으로 바꾼다: CSS 인라인, 상단 탭 숨김, 링크를 루트 기준으로."""
    t = read(rel)
    t = t.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}\nheader.hero nav.tabs{{display:none}}</style>")
    t = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', "", t)

    def href(m):
        h = m.group(1)
        if h.startswith(("http", "#", "mailto:")):
            return f'href="{h}" target="_blank" rel="noopener"' if h.startswith("http") else m.group(0)
        name = os.path.splitext(os.path.basename(h))[0]
        if h.endswith(".html") and "/" not in h and name in DETAIL_ROUTES:
            return f'href="index.html#{name}" target="_top"'
        if h in ("../index.html",):
            return 'href="index.html" target="_top"'
        target = os.path.normpath(os.path.join("local_package", h)).replace("\\", "/")
        return f'href="{target}" target="_blank" rel="noopener"'

    t = re.sub(r'href="([^"]+)"(?: target="[^"]*")?(?: rel="[^"]*")?', href, t)
    t = re.sub(r'src="\.\./([^"]+)"', r'src="\1"', t)
    return t


def embed_company(rel):
    t = read(rel)
    t = t.replace('<html lang="ko">', '<html lang="ko" data-theme="light">', 1)
    t = t.replace("</body>", "<script>document.querySelectorAll('a[href^=\"http\"]').forEach(function(a){a.target='_blank';a.rel='noopener'});</script></body>", 1)
    return t


# ---------- 작은 차트 ----------
def spark(item, color):
    data = sorted([r for r in rows("research/data/auction_item_daily.csv") if r["item"] == item], key=lambda r: r["date"])
    v = [float(r["price_per_kg"]) for r in data]
    W, Hh, pad = 220, 70, 6
    lo, hi = min(v), max(v)
    pts = " ".join(f"{pad + k * (W - 2 * pad) / (len(v) - 1):.1f},{pad + (hi - x) / (hi - lo) * (Hh - 2 * pad):.1f}" for k, x in enumerate(v))
    return (f'<svg viewBox="0 0 {W} {Hh}" class="spark" role="img" aria-label="{item} 일별 kg당 가격">'
            f'<polyline fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round" points="{pts}"/></svg>')


def hbar(pct, color):
    return f'<span class="hbar"><i style="width:{max(2, min(100, pct)):.0f}%;background:{color}"></i></span>'


# ---------- 카드 ----------
def card(thumb, title, sub="", tone="", href="", chips=""):
    tag = "a" if href else "div"
    link = f' href="{href}" data-route="{href[1:]}"' if href.startswith("#") else (f' href="{href}"' if href else "")
    return (f'<{tag} class="kc"{link}><div class="th {tone}">{thumb}</div>'
            f'<div class="kt"><b>{title}</b>{f"<span>{sub}</span>" if sub else ""}{f"<em>{chips}</em>" if chips else ""}</div></{tag}>')


def big(num, label="", small=""):
    return f'<strong>{num}</strong>{f"<small>{label}</small>" if label else ""}{small}'


def chip(*xs):
    return "".join(f"<i>{H(x)}</i>" for x in xs)


def chapter(no, key, day, title, answer, cards, route, bridge=""):
    more = f'<a class="more" href="#{route}" data-route="{route}">자세히 보기 →</a>' if route else ""
    out = (f'<section class="ch" id="ch{no}"><div class="ch-h"><span class="no">{no}</span>'
           f'<div><p class="ck"><b>{key}</b> · {day}</p><h2>{title}</h2><p class="ans">{answer}</p></div>{more}</div>'
           f'<div class="rail">{"".join(cards)}</div></section>')
    if bridge:
        out += f'<p class="bridge"><span>그래서</span>{bridge}</p>'
    return out


# ---------- 홈 ----------
def build_home():
    m = {r["item"]: r for r in rows("research/metrics.csv")}
    pct = lambda r, k: float(r[k]) * 100
    tagged = rows("research/voices/voices_tagged.csv")
    ev = Counter(r["evidence_level"] for r in tagged)
    src = Counter(r["source_type"] for r in tagged)
    score = rows("inventory/scoring.csv")
    inv_types = Counter(r["유형"] for r in rows("inventory/inventory_v1.csv"))
    jm = {(r["segment"], r["stage"], r["row"]): r for r in rows("plan/journey_map.csv")}
    comps = rows("research/company/companies.csv")
    insights = re.findall(r"^## (\d)\. (.+)$", read("research/insights.md"), re.M)
    flow = [l for l in read("storyboard/screen_flow.md").splitlines() if re.match(r"^\| \d ", l)]
    screens = [s for s in ([c.strip() for c in l.strip().strip("|").split("|")] for l in flow) if len(s) >= 6]
    screens = [[c.replace("`", "") for c in s] for s in screens]

    # 01 문제
    c01 = [
        card(big(f'{pct(m["무"], "price_change"):+.1f}%', "무 kg당 가격") + spark("무", "#D9480F"), "무 값이 한 달 새 절반 가까이로",
             f'첫 5영업일 {int(float(m["무"]["first5_avg_price"]))}원 → 최근 5영업일 {int(float(m["무"]["last5_avg_price"]))}원', "t-red", chips=chip("계산값", "aT 경매")),
        card(big(f'{pct(m["무"], "volume_change"):+.1f}%', "무 반입 물량"), "같은 기간 물량은 두 배", "값이 내린 첫 번째 이유 후보 (공급 증가형 하락)", "t-blue", chips=chip("계산값", "M3·M5")),
        card(big(f'{pct(m["배추"], "price_change"):+.1f}%', "배추 kg당 가격") + spark("배추", "#D9480F"), "배추도 크게 하락",
             f'날마다 흔들림(변동계수) {pct(m["배추"], "price_cv"):.1f}%', "t-red", chips=chip("계산값")),
        card(big(f'{pct(m["감자"], "top_origin_share"):.1f}%', "감자 물량 중 평창군"), "물량은 몇 곳에 몰린다",
             f'양파는 무안군 {pct(m["양파"], "top_origin_share"):.1f}%', "t-yellow", chips=chip("계산값", "산지 쏠림")),
    ] + [card(big(f"인사이트 {n}"), H(t), "", "t-gray", "#day04", chip("Day 04")) for n, t in insights]
    # 02 근거
    total = sum(ev.values())
    stack = "".join(f'<i style="flex:{n};background:{c}"></i>' for n, c in
                    [(ev["원문 확인"], "#2B8A3E"), (ev["검색 요약"], "#1C64C8"), (ev["제목만"], "#B08900"), (ev["미확인"], "#ADB5BD")])
    c02 = [
        card(big(f"{total}건", "수집·태깅") + f'<span class="stack">{stack}</span>', "사람들의 말 모으기",
             f'원문 확인 {ev["원문 확인"]} · 검색 요약 {ev["검색 요약"]} · 제목만 {ev["제목만"]} · 미확인 {ev["미확인"]}', "t-green", "#day05"),
        card(big(f'{src["기사"]}·{src["채용공고"]}·{src["기존서비스"]}', "기사 · 채용공고 · 기존 서비스"), "어디서 모았나",
             f'연구보고서 {src["연구보고서"]}건 포함 · 한 소스 70% 이하 기준 통과', "t-gray", "#day05"),
        card(big("14열", "metadata.csv"), "다시 찾을 수 있게", "id · URL · 게시일 · 수집일 · 저작권 · 태그 3층", "t-gray", "#day05"),
        card(big("조건부 통과", "점검 다섯 관점"), "근거만 ⚠", "게시일 미확인 4행 — 나머지 4관점 통과", "t-yellow", "#day05"),
    ]
    # 03 자산
    c03 = [card(big(f'{float(r["트랙총점"]):.2f}', f'{r["트랙순위"]}위 · {r["유형"]}') + hbar(float(r["트랙총점"]) / 5 * 100, "#111418" if int(r["트랙순위"]) <= 3 else "#ADB5BD"),
                H(r["자산명"]), H(r["근거수치"]), "t-yellow" if int(r["트랙순위"]) <= 3 else "t-gray", "#day06",
                chip("Top 3") if int(r["트랙순위"]) <= 3 else "") for r in score[:5]]
    c03.insert(0, card(big(f'{sum(inv_types.values())}개', f"자산 {len(inv_types)}유형"), "후보 자산 전부 채점",
                       " · ".join(f"{k} {v}" for k, v in inv_types.items()), "t-gray", "#day06"))
    # 04 목소리
    c04 = [
        card('<p class="quote">평소와 달라진 품목을, 이유와 함께 먼저 보여 드립니다.</p>', "핵심 메시지", "브랜드 페르소나 · 정체성: 수급 안내자", "t-dark", "#day07"),
        card(big("3", "성격") + '<span class="pills"><i>차분한</i><i>정확한</i><i>먼저 살피는</i></span>', "말투", "존댓말 · 한 문장에 정보 하나 · 숫자엔 단위와 기준일", "t-gray", "#day07"),
        card(big("10개", "금칙어") + '<span class="ban">폭등 · 폭락 · 대란 · 지금 사세요 …</span>', "과장하지 않는다", "기사 제목의 과장 표현에서 뽑음", "t-red", "#day07"),
        card(big("7 → 0", "스킬 적용 전후 금칙어"), "브랜드 스킬로 고정", ".claude/skills/brand-sugeup-radar", "t-green", "#day07"),
        card(big("세계관"), "숫자가 밤사이 바뀌는 세계", "하루 약 10만9천 건 낙찰, 한 건 4초 (T12 · data_spec)", "t-dark", "#day07", chip("배경")),
        card(big("갈등"), "봄엔 폭락, 여름엔 급등", "양파 평년 대비 −47.3% (T03) · 배추 +137.8% (T01)", "t-gray", "#day07", chip("사건 2")),
        card(big("약속"), "판단은 대신하지 않는다", "사라고도 기다리라고도 말하지 않는다", "t-yellow", "#day07", chip("가치")),
    ]
    # 05 고객
    emo = lambda sg: [int(jm[(sg, st, "감정")]["text"]) for st in lp.STAGES]
    dots = lambda sg: "".join(f'<i style="--v:{v}" title="{st} {v}"></i>' for st, v in zip(lp.STAGES, emo(sg)))
    segs = [("SG1", "계획형 구매 담당", "유통사 농산 MD · 소싱·예측으로 대응", "t-blue", "1차 대상"),
            ("SG2", "단가 고정형 급식", "식품비 고정 · 식단을 바꿔 버팀", "t-purple", "2차 후보"),
            ("SG3", "버티는 소규모 식당", "값을 못 올림 · 재료 대체 고민", "t-orange", "2차 후보")]
    c05 = [card(big(sg, pri) + f'<span class="emo">{dots(sg)}</span>', name, d, tone, "#journey", chip("감정: 시세→판단→구매→원가"))
           for sg, name, d, tone, pri in segs]
    c05.append(card(big("이상 판단", "가장 막히는 단계"), "세 유형 모두 여기서 −2", "‘왜 변했지?’를 따로 찾아야 하는 순간 → 이유 카드", "t-red", "#journey", chip("결정적 순간")))
    # 06 화면
    tones = {"발견 (훅)": "t-yellow", "결과 (전환)": "t-red", "행동": "t-green"}
    c06 = [card(big(s[0].split()[0], s[1]) + f'<span class="ev">{H(s[4].split(" (")[0])}</span>', H(" ".join(s[0].split()[1:])), H(s[2]),
                tones.get(s[1], "t-gray"), "#day08") for s in screens]
    # 07 기업
    c07 = [card(big(H(c["기업"]), c["구분"]), H(c["우선 기회"]), f'{H(c["유형"])} · 2025 매출 {H(c["2025 매출"])}',
                "t-dark" if c["구분"] == "후보" else "t-gray", f'#{c["id"]}/day9', chip("원페이지", "밸류체인")) for c in comps]
    # 08 산업 가치사슬 (valuechain/industry/valuechain_v1.md 요약)
    vc = [("①", "산지 생산·출하", "농가·계약재배", "데이터: 작황 / 통계청 공개", ("기회 O2",), "t-gray"),
          ("②", "도매시장·산지 유통", "도매시장법인·중도매인", "데이터: 경락가·반입량·산지 / aT 공개 ← 팀 자산", ("병목 B1",), "t-teal"),
          ("③", "가공·제조", "풀무원·오리온·CJ·현대·컬리", "데이터: 생산실적 / 제조사 내부", (), "t-gray"),
          ("④", "유통·플랫폼", "CJ·현대·푸드머스 · 컬리·오아시스", "데이터: 재고·수요 예측 / 내부", ("비용 C1",), "t-gray"),
          ("⑤", "주문·소비", "구매 담당(SG1)·급식·식당·가정", "돈의 시작점 · 데이터: 주문 / 내부", ("★ 기회 O1", "병목 B2"), "t-teal"),
          ("⑥", "물류·배송", "기업 물류센터·3PL", "데이터: 배송·폐기 / 내부", ("비용 C2", "기회 O3"), "t-gray")]
    c08 = [card(big(n, "단계") + f'<span class="pub">{"공개 데이터" if n in ("①", "②") else "내부 데이터"}</span>', f"{s} — {who}", d, tone, "#industry", chip(*mk))
           for n, s, who, d, mk, tone in vc]
    c08.insert(0, card(big("1칸", "모두가 볼 수 있는 데이터"), "② 경매만 공개, 주문·수요는 산지로 안 돌아감",
                       "6곳 모두 ‘주문·수요 → 산지’ 경로 미확인 (병목 B2)", "t-red", "#industry", chip("데이터 단절")))
    c08.append(card(big("★ O1", "영향 3 · 실현 3"), "수급 레이더가 들어갈 칸", "② 공개 경매 데이터 → ⑤ 구매 담당에게 평소 대비 변화와 이유", "t-green", "#industry", chip("먼저 간다")))

    # 09 페인포인트 (painpoint/painpoint_def.md 요약)
    vocs = [r for r in rows("painpoint/voc_classified.csv") if not r["VOC 구분"].startswith("2차")]
    pps = [("P1", "평소 값·물량·산지를 한곳에서 비교할 수 없음", "구매 담당 · 이상 알아차리기·이유 찾기", "3 × 3 × 5 = 45", "VOC 3건 · 기사·채용공고", "신호: 가격 변화율 M1 · 출렁임 M2", "t-red", "painpoint"),
           ("P2", "출하가 몰려 값이 무너짐", "산지 생산자 · 출하 정하기 (손 넘김 ①)", "2 × 5 × 4 = 40", "VOC 2건 · 가설", "신호: 반입량 M3 · 산지 쏠림 M4", "t-orange", "actors"),
           ("P3", "원가 상승분을 판매가에 넘기지 못함", "구매 담당 → 거래처 (손 넘김 ③)", "4 × 5 × 2 = 40", "VOC 5건 · 출처 1종 · 가설", "신호: +20% 오른 품목 수", "t-yellow", "actors")]
    c09 = [card(big(f"{len(vocs)}건", "VOC (기사·채용공고 요약)"), "수집물 25건 중 사람의 말만 분류", "단계 · 유형(불만/요청/질문/칭찬) · 강도(1~3) 세 축", "t-gray", "#painpoint", chip("커뮤니티·유튜브 0건"))]
    c09 += [card(big(n, sc) , H(t), f"{H(w)} · {H(e)} · {H(s)}", tone, f"#{r}", chip("Top 3", "빈도×강도×해결")) for n, t, w, sc, e, s, tone, r in pps]
    c09.append(card(big("6단계", "SG1 여정 지도"), "한 사람 · 6단계 × 6층", "모든 칸에 근거 id 또는 ‘수집 필요’ · 감정은 VOC 건수로", "t-blue", "#painpoint", chip("journey_map.html")))
    c09.append(card(big("손 넘김 3", "세 사람 여정"), "생산자 → 중도매인 → 구매 담당", "넘어가는 지점의 데이터 = 대시보드 지표 후보", "t-teal", "#actors", chip("journey_3actors.html")))
    chapters = [
        ("01", "문제", "Day 04 조사 방법론", "값은 크게, 자주 방향을 바꾼다",
         f'무 kg당 가격 {pct(m["무"], "price_change"):+.1f}%, 같은 기간 물량 {pct(m["무"], "volume_change"):+.1f}%. 구매자는 “얼마”보다 “평소와 얼마나, 왜 다른지”를 알기 어렵다.',
         c01, "day04", "이 말과 숫자를 다시 찾을 수 있게 보관한다"),
        ("02", "근거", "Day 05 아카이빙", f"말은 {total}건, 원문까지 본 것은 {ev['원문 확인']}건",
         "모든 수집물에 출처·날짜·저작권을 달고, 근거 수준을 숨기지 않는다.", c02, "day05", "근거가 가장 단단한 품목부터 고른다"),
        ("03", "자산", "Day 06 인벤토리", "데이터가 가장 단단한 세 품목: 양파 · 무 · 배추",
         "자산 30개를 데이터 가용성·수요·위험·시장성·스토리로 채점(데이터·서비스 트랙 가중).", c03, "day06", "이 품목을 어떤 목소리로 말할지 정한다"),
        ("04", "목소리", "Day 07 브랜드 페르소나 · 세계관", "판단은 대신하지 않고, 변화와 이유를 먼저",
         "차분하고 정확하게, 먼저 살핀다. 기준일과 출처 없는 숫자는 말하지 않는다.", c04, "day07", "누구에게 말할지 정한다"),
        ("05", "고객", "고객 유형 · 고객여정지도", "세 유형 모두 ‘이상 판단’에서 가장 막힌다",
         "누가 사는가 × 급변에 어떻게 버티는가로 3유형. 여정 4단계: 시세 확인 → 이상 판단 → 구매·발주 → 원가 반영.", c05, "journey",
         "막히는 순간에 이유 카드를 놓는다"),
        ("06", "화면", "Day 08 스토리보드", "무 알림 → 이유 카드 → 알림 받기",
         "훅 “무 kg당 가격이 첫 주보다 45.6% 낮습니다” → 전환 “같은 기간 물량은 두 배였습니다” → 버튼 1개.", c06, "day08",
         "이 화면이 붙을 수 있는 기업을 본다"),
        ("07", "기업", "Day 09 산업 구조 · 기업 원페이지", "수급 정보가 필요한 기업 6곳",
         "식자재 유통 2 · 식품 제조 2 · 온라인 식품 2. 6곳의 우선 기회가 모두 ‘시세 전망·위험 알림·시세 리포트’다. 카드를 누르면 원페이지와 기업별 밸류체인.", c07, "",
         "6곳을 한 줄기에 겹쳐 비어 있는 칸을 찾는다"),
        ("08", "산업", "Day 10 산업 밸류체인 맵", "산지에서 식탁까지 6단계, 모두가 볼 수 있는 데이터는 하나",
         "활동·이해관계자·돈·데이터 네 층으로 겹치면 ② 경매만 공개되고 주문·수요는 산지로 돌아가지 않는다. 그 사이가 수급 레이더의 자리.", c08, "industry",
         "회사 쪽 병목을 고객 쪽에서 다시 본다"),
        ("09", "페인포인트", "Day 11 고객 여정 · 페인포인트 도출", "가장 먼저 풀 문제: 평소 값·물량·산지를 한곳에서 비교할 수 없다",
         "VOC를 단계·유형·강도로 분류하고 빈도 × 강도 × 해결 가능성으로 Top 3를 골랐다. Top 1이 내일 AX 기회와 MVP의 출발점.", c09, "painpoint"),
    ]
    story = "".join(chapter(*c) for c in chapters)
    line = "".join(f'<a href="#ch{no}" class="sl"><b>{no}</b>{key}</a>' for no, key, *_ in chapters)
    todo = ("유튜브 5건·커뮤니티 10건 수집", "검색 요약 15건 원문 대조", "본인 채점과 AI 채점 비교", "구매 담당자 인터뷰 → 여정 교체", "새 세션에서 브랜드 스킬 호출 확인", "VOC 표본 10건 사람 판정 (painpoint/review_sample.md)")
    return f"""<main class="home" id="home">
  <section class="hero">
    <p class="eyebrow">강의 과제 · 개인 프로젝트 · Day 04~11 한 줄기</p>
    <h1>수급 레이더</h1>
    <p class="lead">평소와 달라진 품목을, 이유와 함께 먼저 보여 드립니다.</p>
    <div class="hero-data">
      <div><small>무 kg당 가격</small><b>{pct(m["무"], "price_change"):+.1f}%</b></div>
      <div><small>같은 기간 무 물량</small><b>{pct(m["무"], "volume_change"):+.1f}%</b></div>
      <div><small>수집·태깅</small><b>{total}건</b></div>
      <div><small>핵심 품목</small><b>양파·무·배추</b></div>
      <div><small>Top 1 페인포인트</small><b>판단 재료가 흩어짐</b></div>
    </div>
    <p class="hero-note">aT 전국 공영도매시장 경매 2026-10-06 ~ 11-05 (27영업일) 계산값 · 첫 5영업일 대비 최근 5영업일</p>
  </section>
  <nav class="storyline" aria-label="한 줄기">{line}</nav>
  {story}
  <section class="ch"><div class="ch-h"><span class="no">+</span><div><p class="ck"><b>남은 일</b></p><h2>사람이 확인해야 할 것</h2></div></div>
  <div class="rail">{"".join(card(big(str(i + 1)), H(t), "", "t-gray") for i, t in enumerate(todo))}</div></section>
  <p class="foot">수급 레이더 · 강의 과제용 개인 프로젝트 · 2026-11-09 · 숫자는 공공데이터 계산값이며 구매·투자 판단 자료가 아니에요. 이 페이지는 <code>python scripts/build_index.py</code>로 원본 csv·md에서 만듭니다.</p>
</main>"""


CSS = """
:root{color-scheme:light;--ink:#111418;--ink2:#4A5159;--ink3:#6B727A;--line:#E6E8EB;--band:#F5F6F7;--accent:#FFD400}
*{box-sizing:border-box} html,body{height:100%}
body{margin:0;background:#fff;color:var(--ink);font-family:Pretendard,"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif;font-size:16px;line-height:1.5;word-break:keep-all;overflow-wrap:anywhere}
[hidden]{display:none!important} a{color:inherit} :focus-visible{outline:3px solid #1C64C8;outline-offset:2px}
.home{max-width:1280px;margin:0 auto;padding:28px 28px 56px}
.hero{background:var(--ink);color:#fff;border-radius:24px;padding:34px 36px 26px;position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;right:-60px;top:-60px;width:260px;height:260px;border-radius:50%;background:var(--accent);opacity:.95}
.hero>*{position:relative;z-index:1}
.eyebrow{margin:0;color:var(--accent);font-weight:800;font-size:14px;letter-spacing:.02em}
.hero h1{margin:6px 0 2px;font-size:44px;line-height:1.15;font-weight:900;letter-spacing:-.04em}
.lead{margin:0 0 22px;font-size:21px;font-weight:700;color:#E3E5E8;max-width:640px}
.hero-data{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;max-width:1040px}
.hero-data div{background:#22272E;border-radius:14px;padding:12px 14px}
.hero-data small{display:block;color:#AEB4BA;font-size:13px;font-weight:700}
.hero-data b{font-size:26px;font-weight:900;letter-spacing:-.03em}
.hero-note{margin:12px 0 0;color:#8D949B;font-size:13px}
.storyline{position:sticky;top:0;z-index:5;display:flex;gap:6px;overflow-x:auto;padding:12px 0;margin:6px 0 4px;background:#fff;scrollbar-width:none}
.storyline::-webkit-scrollbar{display:none}
.sl{flex:1 0 auto;display:flex;align-items:center;gap:8px;padding:8px 14px;border-radius:99px;background:var(--band);text-decoration:none;font-weight:800;font-size:15px;white-space:nowrap}
.sl b{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:var(--ink);color:#fff;font-size:12px}
.sl:hover{background:var(--accent)}
.ch{margin-top:30px;scroll-margin-top:70px}
.ch-h{display:flex;gap:16px;align-items:flex-start;margin-bottom:14px}
.no{flex:none;display:grid;place-items:center;width:52px;height:52px;border-radius:16px;background:var(--accent);font-size:20px;font-weight:900}
.ch-h>div{flex:1;min-width:0}
.ck{margin:0;font-size:14px;color:var(--ink3)} .ck b{color:var(--ink)}
.ch h2{margin:2px 0 4px;font-size:26px;line-height:1.3;font-weight:900;letter-spacing:-.03em}
.ans{margin:0;color:var(--ink2);font-size:16.5px;max-width:880px}
.more{flex:none;align-self:center;font-weight:800;font-size:15px;text-decoration:none;padding:8px 14px;border-radius:99px;background:var(--band);white-space:nowrap}
.more:hover{background:var(--accent)}
.rail{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}
.kc{display:flex;flex-direction:column;border-radius:18px;overflow:hidden;background:var(--band);text-decoration:none;transition:transform .12s, box-shadow .12s}
a.kc:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(17,20,24,.10)}
.th{position:relative;min-height:138px;padding:16px 16px 14px;display:flex;flex-direction:column;justify-content:flex-end;gap:2px;background:#E9ECEF}
.th strong{font-size:30px;line-height:1.1;font-weight:900;letter-spacing:-.04em}
.th small{font-size:13px;font-weight:700;opacity:.75}
.t-red{background:#FFE8DD;color:#9C2F00} .t-blue{background:#E1ECFC;color:#0F3F82} .t-green{background:#E0F3E5;color:#1E6B30}
.t-yellow{background:#FFF1A8;color:#4D3D00} .t-gray{background:#ECEEF0;color:#2A2F36} .t-dark{background:var(--ink);color:#fff}
.t-purple{background:#ECE5FF;color:#4527A0} .t-teal{background:#D5F0EA;color:#00594A}
.pub{display:inline-block;align-self:flex-start;margin-top:6px;font-size:12px;font-weight:800;padding:1px 8px;border-radius:99px;background:rgba(255,255,255,.75)} .t-orange{background:#FFE6CC;color:#8A3B00}
.kt{padding:12px 16px 16px;display:flex;flex-direction:column;gap:3px}
.kt b{font-size:16.5px;line-height:1.35;font-weight:800;letter-spacing:-.02em}
.kt span{font-size:14px;color:var(--ink2);line-height:1.45}
.kt em{font-style:normal;display:flex;flex-wrap:wrap;gap:4px;margin-top:4px}
.kt em i,.pills i{font-style:normal;font-size:12px;font-weight:700;padding:1px 8px;border-radius:99px;background:#fff;color:var(--ink2)}
.spark{width:100%;height:44px;margin-top:6px}
.hbar{display:block;height:8px;border-radius:99px;background:rgba(17,20,24,.10);margin-top:8px;overflow:hidden}
.hbar i{display:block;height:100%;border-radius:99px}
.stack{display:flex;height:10px;border-radius:99px;overflow:hidden;margin-top:10px}
.pills{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px} .pills i{background:#fff}
.ban{font-size:13px;font-weight:700;margin-top:6px}
.quote{margin:0;font-size:19px;line-height:1.4;font-weight:900;letter-spacing:-.03em}
.quote:before{content:"“";display:block;color:var(--accent);font-size:40px;line-height:.6}
.ev{display:inline-block;margin-top:6px;font-family:ui-monospace,Consolas,monospace;font-size:12px;font-weight:700;background:rgba(255,255,255,.7);padding:1px 6px;border-radius:6px;align-self:flex-start}
.emo{display:flex;gap:6px;align-items:flex-end;height:46px;margin-top:8px}
.emo i{flex:1;border-radius:6px 6px 2px 2px;background:currentColor;opacity:.75;height:calc((var(--v) + 2.6) * 16%)}
.bridge{margin:18px 0 0 18px;padding-left:44px;border-left:3px dashed #CED4DA;color:var(--ink2);font-size:16px;font-weight:700;min-height:42px;display:flex;align-items:center;gap:10px}
.bridge span{flex:none;white-space:nowrap;background:var(--ink);color:#fff;font-size:12.5px;padding:2px 10px;border-radius:99px}
.foot{margin:34px 0 0;font-size:14px;color:var(--ink3)}
code{background:var(--band);padding:1px 6px;border-radius:6px;font-size:13px}
.view{display:flex;flex-direction:column;height:100%;height:100dvh}
.bar{flex:none;display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;padding:8px 16px;background:var(--ink);color:#fff}
.back{color:#fff;font-size:15px;font-weight:700;text-decoration:none;padding:5px 10px;border-radius:8px;white-space:nowrap}
.back:hover,.tab:hover,.switch a:hover{background:#2A2F36}
.cur{font-size:18px;font-weight:800;white-space:nowrap}
.tabs,.switch{display:flex;gap:4px;flex-wrap:wrap}
.tab{padding:5px 14px;border-radius:99px;color:#E3E5E8;font-size:15px;font-weight:700;text-decoration:none;white-space:nowrap}
.tab[aria-current="page"]{background:var(--accent);color:var(--ink)}
.switch{margin-left:auto}
.switch a{padding:4px 10px;border-radius:8px;color:#C9CDD2;font-size:14px;font-weight:700;text-decoration:none;white-space:nowrap}
.switch a[aria-current="true"]{color:#fff;box-shadow:inset 0 0 0 1.5px #6B727A}
.open{color:#C9CDD2;font-size:14px;font-weight:700;white-space:nowrap}
iframe{flex:1;min-height:0;width:100%;border:0;background:#fff}
@media (max-width:760px){
  .home{padding:16px 16px 40px}
  .hero{padding:24px 20px 20px;border-radius:20px} .hero h1{font-size:34px} .lead{font-size:17px}
  .hero:after{width:150px;height:150px;right:-50px;top:-50px}
  .hero-data{grid-template-columns:1fr 1fr} .hero-data b{font-size:21px}
  .ch-h{flex-wrap:wrap;gap:12px} .no{width:42px;height:42px;font-size:17px;border-radius:13px}
  .ch h2{font-size:21px} .ch-h>div{flex:1 1 calc(100% - 60px)} .more{order:3;margin-left:54px}
  .rail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 6px;gap:12px}
  .kc{flex:0 0 74%;scroll-snap-align:start}
  .bridge{margin-left:8px;padding-left:22px;font-size:15px}
  .switch{margin-left:0}
}
"""

SCRIPT = """
(function () {
  var detail = %(detail)s, comps = %(comps)s;
  var pages = JSON.parse(document.getElementById('data').textContent);
  var home = document.getElementById('home'), view = document.getElementById('view');
  var frame = document.getElementById('frame'), shown = '';
  function a(route, text, cur) { return '<a href="#' + route + '" data-route="' + route + '"' + (cur ? ' aria-current="' + cur + '"' : '') + '>' + text + '</a>'; }
  function openHref(path) {
    var q = location.search.slice(1);
    return q.indexOf('https://github.com/') === 0 && q.indexOf('/index.html') > 0 ? location.pathname + '?' + q.split('/index.html')[0] + '/' + encodeURI(path) : encodeURI(path);
  }
  function render(route) {
    var parts = route.split('/'), d = detail.filter(function (x) { return x[0] === parts[0]; })[0];
    var c = comps.filter(function (x) { return x.id === parts[0]; })[0];
    if (!d && !c) {
      home.hidden = false; view.hidden = true; document.title = '수급 레이더 · 과제 결과';
      var el = route && document.getElementById(route);
      if (el) el.scrollIntoView(); else if (!route) window.scrollTo(0, 0);
      return;
    }
    home.hidden = true; view.hidden = false;
    var tabs = document.getElementById('tabs'), sw = document.getElementById('switch'), key, html, path;
    if (d) {
      document.getElementById('cur').textContent = '수급 레이더';
      tabs.innerHTML = detail.map(function (x) { return a(x[0], x[1], x[0] === d[0] ? 'page' : '').replace('<a ', '<a class="tab" '); }).join('');
      sw.innerHTML = ''; key = d[0]; html = pages.detail[d[0]]; path = d[2]; document.title = d[1] + ' · 수급 레이더';
    } else {
      var day = parts[1] === 'day10' ? 'day10' : 'day9';
      document.getElementById('cur').textContent = c.name;
      tabs.innerHTML = a(c.id + '/day9', 'Day 09 원페이지', day === 'day9' ? 'page' : '').replace('<a ', '<a class="tab" ') +
                       a(c.id + '/day10', 'Day 10 밸류체인 맵', day === 'day10' ? 'page' : '').replace('<a ', '<a class="tab" ');
      sw.innerHTML = comps.map(function (x) { return a(x.id + '/' + day, x.name, String(x.id === c.id)); }).join('');
      key = c.id + '/' + day; html = pages.company[c.id][day]; path = c[day]; document.title = c.name + (day === 'day9' ? ' Day 09' : ' Day 10');
    }
    document.getElementById('open').href = openHref(path);
    if (shown !== key) { frame.title = document.title; frame.srcdoc = html; shown = key; }
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-route]');
    if (!t) return;
    e.preventDefault();
    render(t.dataset.route);
    try { history.pushState(null, '', '#' + t.dataset.route); } catch (err) {}
  });
  window.addEventListener('popstate', function () { render(location.hash.slice(1)); });
  window.addEventListener('hashchange', function () { render(location.hash.slice(1)); });
  render(location.hash.slice(1));
})();
"""


def main():
    bp.build_sg1()
    bp.build_3actors()
    lp.build_journey()
    lp.build_redirect()
    for f in (lp.build_day04, lp.build_day05, lp.build_day06, lp.build_day07, lp.build_day08):
        f()
    css = read("local_package/style.css")
    comps = rows("research/company/companies.csv")
    pages = {
        "detail": {r: embed_local(f, css) for r, _, f in DETAIL},
        "company": {c["id"]: {"day9": embed_company(c["day9"]), "day10": embed_company(c["day10"])} for c in comps},
    }
    data = json.dumps(pages, ensure_ascii=False).replace("<", "\\u003c")
    script = SCRIPT % {
        "detail": json.dumps([list(d) for d in DETAIL], ensure_ascii=False),
        "comps": json.dumps([{"id": c["id"], "name": c["기업"], "day9": c["day9"], "day10": c["day10"]} for c in comps], ensure_ascii=False),
    }
    doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>수급 레이더 · 과제 결과</title>
<style>{CSS}</style>
</head>
<body>
{build_home()}
<div class="view" id="view" hidden>
  <header class="bar">
    <a class="back" href="#" data-route="">← 한 줄기로</a>
    <span class="cur" id="cur"></span>
    <nav class="tabs" id="tabs" aria-label="화면 선택"></nav>
    <nav class="switch" id="switch" aria-label="다른 기업"></nav>
    <a class="open" id="open" target="_blank" rel="noopener">이 화면만 크게 ↗</a>
  </header>
  <iframe id="frame" title="상세"></iframe>
</div>
<script id="data" type="application/json">{data}</script>
<script>{script}</script>
</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"index.html 생성 ({len(doc) // 1024} KB) · 상세 {len(DETAIL)} · 기업 {len(comps)}")


if __name__ == "__main__":
    main()
