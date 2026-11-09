# Stock Intelligence Lab

**L.L.M Academy의 리서치·기획·산업 분석 수업 방법을 그대로 따라가며, 주가·거래량과 금융 뉴스로 종목을 분석하고 예측을 백테스트로 검증하는 웹 서비스를 만드는 개인 프로젝트입니다.**

관심 회사를 누르면 최근 이슈와 모델 예측을 근거와 함께 보여 주고, 그 예측이 실제 투자에 도움이 되는지 과거 데이터로 확인할 수 있는 서비스를 목표로 합니다. 데이터를 먼저 확보하고 검증한 뒤 모델과 화면을 만드는 순서로 진행합니다.

> **개발 진행 중 · 2026-11-10 기준**
> 강의 Day 1~11을 마쳤습니다. 가격 · 공시 · 뉴스 데이터를 받아 교차검증하고(시각은 모두 UTC로 확인), 기존 주식 앱 리뷰 · 커뮤니티 VOC 128건으로 페인포인트 Top 3를 정했습니다. 1위는 **"화면의 숫자가 언제 기준인지 · 맞는지 모른다"** 입니다. 경쟁 서비스(Yahoo Finance · 토스증권)와 국내 투자자문 규제도 조사했습니다. **공개 화면에 쓸 수 있는 가격 데이터 소스는 아직 없습니다.** 사용자용 웹 서비스 · DB · 예측 모델은 아직 구현하지 않았습니다.

## 어떤 프로젝트인가요?

- **목표 사용자 가설:** 종목 뉴스와 전망을 여기저기서 찾아보는 개인투자자
- **만들려는 것:** 관심 회사의 최근 이슈 키워드, 모델 예측(생성 시각 · 모델 버전 · 과거 적중률 포함), 로그인 없는 포트폴리오
- **핵심 질문:** 숫자 시계열(가격·거래량)에 뉴스를 더하면 5거래일 수익률 방향 예측이 나아지는가, 그리고 그게 거래비용을 뺀 투자 성과로 이어지는가
- **데이터 원칙:** 숫자와 라이선스는 공식 원문(A 등급)에서만 가져오고, 확인하지 못한 것은 "미확인"으로 표시합니다. 무료로 받을 수 있다는 것과 광고가 붙은 서비스에 써도 된다는 것은 따로 판단합니다.

사용자 문제와 기능은 아직 가설이며 강의 Day 4·9·11에서 검증합니다. 이 프로젝트는 **정보 제공 · 학습 목적이며 투자 권유가 아닙니다.**

## 어떤 수업을 바탕으로 하나요?

강의의 지역 자산 조사 방법을 소재만 "주식 + 금융 뉴스"로 바꿔 적용합니다. 강의의 원래 날짜와 실제 작업 날짜는 구분합니다.

| 강의 | 원래 수업 날짜 | 프로젝트에 적용하는 내용 | 상태 |
|---|---|---|---|
| Day 01 — 온보딩 | 10/26 | 학습계획서, 강의↔프로젝트 매핑, 서비스 가설 | 완료 |
| Day 02 — Local 오리엔테이션 | 10/27 | 저장소, 리서치 규칙(CLAUDE.md), 키워드 맵, 가격 데이터 확보 | 완료 |
| Day 03 — 자산 조사 방법론 1 | 10/28 | 소스 판정, SEC·GDELT 실측, 교차검증 표, 데이터 명세 | 완료 |
| Day 04 — 자산 조사 방법론 2 | 10/29 | 기존 주식 서비스 사용자 VOC 수집·분석 | 완료 |
| Day 05 — 콘텐츠 아카이빙 | 10/30 | 수집 규칙, metadata.csv, 시간대 확정 | 완료 |
| Day 06 — 자산 인벤토리 | 11/02 | 데이터 소스 인벤토리와 학습용·서비스용 Top 3 | 완료 |
| Day 07 — 브랜드 페르소나·세계관 | 11/03 | 서비스 톤, 투자자 페르소나, 문구 스킬 | 완료 |
| Day 08 — 디지털 내러티브 | 11/04 | 사용자 여정 → 화면 → 데이터 | 완료 |
| Day 09 — 산업 구조 | 11/05 | 경쟁 서비스 원페이지, 투자자문 규제 확인 | 완료 |
| Day 10 — 밸류체인 맵핑 | 11/06 | 데이터 흐름도와 비용·병목 | 완료 |
| Day 11 — 페인포인트 | 11/09 | 투자자 여정 지도, 페인포인트 Top 3 | 완료 |

수업별 상세 매핑은 [강의와 프로젝트 연결 안내](docs/COURSE_GUIDE.md)에 있습니다.

## 처음 방문했다면 이 순서로 보세요

1. **이 README:** 목적, 수업과의 관계, 현재 상태
2. **[Day별 결과 화면 (cjax.vercel.app)](https://cjax.vercel.app):** 교시마다 배운 것 · 이 프로젝트에서 한 것 · 결과. 열리지 않으면 저장소를 내려받아 `stock-intelligence-lab/index.html`을 브라우저로 여세요.
3. **[페인포인트 정의서](painpoint/painpoint_def.md) · [여정 지도](painpoint/journey_map.html):** VOC 128건으로 정한 Top 3와 가설 판정
4. **[경쟁 서비스 원페이지](research/users_competitors/onepage.md) · [규제 요약](research/users_competitors/regulation.md):** Yahoo Finance · 토스증권 · 국내 투자자문 규제
5. **[교차검증 표](research/crosscheck.md):** 데이터 소스에 대한 주장 20개와 판정 (Day 5 정정 포함)
6. **[데이터 명세](research/data/data_spec.md):** 실제로 확보한 데이터, 열 정의, 한계
7. **소스별 노트:** [yfinance](research/market_data/yfinance.md) · [Alpha Vantage](research/market_data/alpha_vantage.md) · [SEC EDGAR](research/news_data/sec_edgar.md) · [GDELT](research/news_data/gdelt.md) · [Stooq](research/market_data/stooq.md)

## 현재 확보한 데이터

| 데이터 | 출처 | 범위 | 용도와 조건 |
|---|---|---|---|
| 일봉 가격 | yfinance (Yahoo Finance) | 7종목, 22~45년 (AAPL 1980-12-12~, 57,030행) | **로컬 학습용만.** Yahoo 약관상 개인 용도·자동 수집 금지라 저장소에 올리지 않음 |
| 공시 목록 | SEC EDGAR | AAPL 1,006건(2015~) + 이전 1,271건(1994~) | 미국 정부 공개 자료, 무료 |
| 앱 리뷰 · 커뮤니티 VOC | App Store RSS · Aside(Reddit · Google Play · YouTube) | 128건 (2020-12~2026-11) | 원문은 Git 제외, 요약과 태그만 커밋 |
| 뉴스 기사 | GDELT GKG 2.1 | 15분 배치 1개 = 1,443건 샘플, 이력은 2015-02~ | 상업 이용·재배포 가능, 출처 표기 필수 |

**확인된 것:** IBM 100거래일 종가가 yfinance와 Alpha Vantage에서 100% 일치합니다. SEC · GDELT · Alpha Vantage의 시각은 모두 UTC입니다(Day 5).
**현재 한계:**
- 뉴스 이력이 약 11년이라, 뉴스까지 쓰는 학습 기간은 2015년 이후로 제한됩니다.
- 상장폐지 종목이 없어 생존편향이 있습니다.
- 공개 서비스에 보여줄 가격 데이터 공급자는 아직 정하지 않았습니다.

## 폴더 구성

이 프로젝트는 [cj_ax](https://github.com/so-jung0729/cj_ax) 저장소의 `stock-intelligence-lab/` 폴더에 있습니다. 모든 데이터는 `research/data/` 한 곳에 모았습니다. 모든 명령은 이 폴더(`stock-intelligence-lab/`)에서 실행합니다.

```text
cj_ax/stock-intelligence-lab/
  README.md                     프로젝트 소개와 읽는 순서
  CLAUDE.md                     리서치·출처 등급·보안 규칙
  index.html                    Day별 결과 화면
  requirements.txt              Python 패키지
  .env.example                  값이 비어 있는 환경변수 예시
  docs/
    COURSE_GUIDE.md             강의 Day와 프로젝트 산출물 연결
    day01_learning_plan.md      학습계획서
  research/
    keyword_map.md              데이터 소스·사용자·경쟁 서비스 키워드 (v2 판정 포함)
    crosscheck.md               교차검증 표
    market_data/                가격 데이터 제공처 노트
    news_data/                  뉴스·공시 제공처 노트
    users_competitors/          VOC 분석 · 경쟁 원페이지 · 규제 (Day 4 · 9)
    data/                       ★ 모든 데이터
      data_spec.md              데이터 명세
      *.csv                     정리본 (prices_daily.csv는 Git 제외)
      archive/                  재배포 가능한 원본 (SEC, GDELT)
      raw/                      작업용 원본, 약관상 재배포 불가 (Git 제외)
      checks/                   API 호출 확인 기록 (403·429 응답, 가격 대조 결과)
  scripts/                      다운로드 · 교차검증 · 정리본 생성
  archive/                      현장 수집 요약 노트 · metadata.csv · tags.md (Day 5)
  inventory/                    데이터 소스 인벤토리 (Day 6)
  persona/                      서비스·사용자 페르소나 (Day 7)
  screens/                      훅 · 화면 흐름 · HTML 시안 (Day 8)
  valuechain/                   밸류체인 v0 · v1 · 분석 (Day 10)
  painpoint/                    여정 지도 · 페인포인트 정의서 (Day 11)
  .claude/skills/               화면 문구 스킬 issue-lens-voice (Day 7)
```

## 실행해 보기

Python 3.12에서 확인했습니다. 가격 원본은 저장소에 없으므로 직접 받아야 합니다. API 키는 필요 없습니다.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts/probe_yfinance.py AAPL MSFT NVDA AMZN GOOGL SPY 005930.KS
.venv\Scripts\python scripts/build_day03_tables.py
```

가격 교차검증(yfinance vs Alpha Vantage)은 Alpha Vantage demo 응답이 `research/data/raw/alphavantage/`에 있어야 합니다.

## 자료를 읽을 때

- 출처 등급: **A** 공식 원문·실측 / **B** 공공·연구 / **C** 언론 / **D** 개인·커뮤니티. 숫자와 라이선스는 A·B만 씁니다.
- 교차검증 판정: 일치 · 부분일치 · 불일치 · 단일출처 · 미확인. "일치"만 확정 사실로 씁니다.
- AI가 정리한 내용은 원문 확인 전까지 사실로 쓰지 않습니다. 약관 해석은 법률 자문이 아닙니다.
