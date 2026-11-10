# 화면용 가격 데이터 요금 · 표시 조건 (Day 09 · 4번째 리서치)

**조사 방법:** Aside 세션(`C85yYQ53e7ebtSHv`)이 16:44 UTC 이후 "suspended" 상태로 멈춰 결과를 받지 못했다(Aside 앱에서 승인을 기다리는 것으로 보임). 그래서 Claude가 공식 요금 페이지를 직접 열어 확인했다. `[F]` 원문 사실 · `[I]` 해석 · `[U]` 미확인. 확인일 2026-11-10.

## 공급사별
| 공급사 | 요금제 · 월 가격 | 공개 화면 표시 · 재배포 | 출처 |
|---|---|---|---|
| **Massive (구 Polygon)** | Stocks Advanced **199 USD/월** (20년 이상 이력, 실시간), Financials & Ratios 29 USD/월 [F][1] | 두 요금제 모두 **"Individual use only"** [F][1]. 사업용은 별도 business pricing 링크만 있고 조건 · 가격은 페이지에 없음 [U][1] | [1] |
| **Tiingo** | Starter 0 · Power 30 USD/월(개인), Business internal commercial use **50 USD/월** [F][2] | "Internal use"는 본인만 쓰는 것이고 다른 사람과 공유 · 표시할 수 없음 [F][2]. 재배포 요금은 상품 페이지 · 영업팀 문의 [F][2], 금액 미확인 [U] | [2] |
| **Alpha Vantage** | 무료는 개인 · 비상업, 상업 이용은 premium@alphavantage.co 문의 [F][3] | 다른 사람이 정보에 접근하는 상업 활동은 commercial use [F][3] | [3] |
| **Nasdaq Data Link** | 확인 안 함 [U] | 확인 안 함 [U] | — |

## 결론
- 개인 · 내부용 요금(월 0~199 USD)으로는 **공개 화면에 가격을 보여 줄 수 없다** [I][1][2][3]
- 공개 표시 · 재배포 요금은 세 곳 모두 **영업 문의**이고 공개 가격이 없다 [U]
- Yahoo Finance도 시세를 ICE Data Services에서 라이선스로 받는다(yahoo_finance.md [2]) → 공개 가격 화면에는 **재배포 라이선스 계약**이 필요하다 [I]
- **이슈렌즈 첫 버전의 선택지 [I]:** ① 가격 차트 없이 공시 · 기사 · 예측만 보여 주기 ② 가격은 숫자 대신 "종목 페이지 링크"로 넘기기 ③ 재배포 견적 받기 (Tiingo · Massive 영업 문의)

## 출처
| # | 제목 | URL | 등급 | 확인일 |
|---|---|---|---|---|
| 1 | Massive Pricing | https://massive.com/pricing | A | 2026-11-10 |
| 2 | Tiingo Pricing | https://www.tiingo.com/about/pricing | A | 2026-11-10 |
| 3 | Alpha Vantage Terms of Service (Day 2 확인) | https://www.alphavantage.co/terms_of_service/ | A | 2026-11-10 |

## 추가 확인 (2026-11-10): 무료로 시세 추이를 보여 주는 방법
**질문:** yfinance처럼 파이썬 라이브러리는 무료인데 그걸로 보여 주면 안 되나?
- **라이브러리 무료 ≠ 데이터 무료.** yfinance 코드는 Apache 라이선스로 무료지만, 받아 오는 데이터는 Yahoo 것이고 Yahoo 약관은 개인 용도 · 자동 수집 금지다 [F] (research/market_data/yfinance.md). 그래서 학습용으로만 쓴다
- **TradingView 위젯은 무료로 웹사이트에 넣을 수 있다:** "We provide widgets as a technology piece for FREE with default TradingView branding" [F][4]. 조건은 TradingView 브랜딩(저작권 링크)을 그대로 두는 것 [F][4][5]
- 위젯 데이터는 TradingView가 화면에 그리고, 우리는 가격을 저장 · 재배포하지 않는다 [I]. 유료 플랜과 상관없이 위젯 데이터는 같고, 실시간이 필요하면 거래소와 직접 계약해야 한다 [F][4]
- **결정:** 화면의 시세 추이는 TradingView 위젯(Symbol Overview)으로 표시한다. 시안 `screens/screen_v0.html`에 적용. 우리 숫자(예측 · 공시 시각)와 위젯 시세를 섞어 계산하지 않는다

| # | 제목 | URL | 등급 | 확인일 |
|---|---|---|---|---|
| 4 | TradingView Widgets | https://www.tradingview.com/widget/ | A | 2026-11-10 |
| 5 | TradingView Terms of Use, Policies, and Disclaimers (위젯 출처 표기) | https://in.tradingview.com/policies | A (검색 발췌) | 2026-11-10 |
