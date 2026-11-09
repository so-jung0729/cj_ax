# yfinance (Yahoo Finance 데이터)

## 1. 한 줄 요약
API 키 없이 종목별 **상장 이후 전체 일봉(20~45년)** 과 수정종가·분할·배당을 한 번에 받을 수 있다. 다만 Yahoo 약관은 **자동 수집을 금지하고 개인 용도 라이선스만 준다.** 그래서 **로컬 학습·연구용으로만 쓰고, 공개 서비스 표시용으로는 쓰지 않는다.** [1][2][4]

## 2. 기본 정보
| 항목 | 내용 | 출처 |
|---|---|---|
| 정체 | Yahoo와 무관한 오픈소스 라이브러리(Apache 라이선스). README: "intended for research and educational purposes", Yahoo API는 "intended for personal use only" | [1] |
| 받을 수 있는 것 | Open·High·Low·Close·**Adj Close**·Volume·Dividends·Stock Splits (ETF는 Capital Gains 추가) | [4] |
| 이력 길이 | AAPL 1980-12-12~ (45.9년), MSFT 40.7년, SPY 33.8년, AMZN 29.5년, NVDA 27.8년, 삼성전자(005930.KS) 26.8년, GOOGL 22.2년 | [4] |
| 시간대 | 미국 종목 America/New_York, 한국 종목 Asia/Seoul (인덱스에 시간대 포함) | [4] |
| Yahoo 약관: 라이선스 | "personal, royalty-free, non-transferable, ... revocable, and non-exclusive license" | [2] |
| Yahoo 약관: 자동 수집 | 금지 행위에 "access or collect data ... from our Services using any automated means" 포함 | [2] |
| Yahoo 약관: 상업·대량 이용 | 사전 서면 동의 없이 상업 활동·대량(high volume) 이용 금지 | [2] |

## 3. 서비스 관점에서 눈에 띄는 점
1. **20~30년 학습 데이터 목표를 무료로 바로 채울 수 있다.** 60일 입력 / 5일 라벨 윈도우를 만들기에 충분하다.
2. 원가격과 수정종가를 같이 받을 수 있어서 Day 3 품질 검증(분할·배당 조정 확인)을 하기 좋다.
3. 약관상 **회색지대가 아니라 명시적 금지(자동 수집)** 가 있다. 따라서 "연구용 데이터 ≠ 서비스용 데이터" 분리가 필수다.

## 4. 확인 필요 항목
- 삼성전자 `Close` 결측 1건: 어느 날짜인지, 휴장일 처리 문제인지 → Day 3 품질 검증에서 확인
- 상장폐지 종목은 받을 수 없음 → **생존편향** 문제. 백테스트 해석에 반영 필요
- 서비스 화면에 보여줄 가격 데이터 공급자 → **미정** (Day 6 인벤토리에서 선정)
- Yahoo 약관의 최종 개정일 → 본문에 "January 2, 2026 or later" 버전 언급까지만 확인, 정확한 개정일은 **미확인**

## 5. 출처 목록
| # | URL | 등급 | 기준 시점 | 확인일 |
|---|---|---|---|---|
| 1 | https://github.com/ranaroussi/yfinance (README "Legal Stuff") | A (라이브러리 공식 문서) | v1.8.0 | 2026-11-10 |
| 2 | https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html (Yahoo 이용약관 2(d)(ix), 2(i), 2(m)) | A (약관 원문) | 2026-01-02 이후 버전 | 2026-11-10 |
| 3 | https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.html (Yahoo Developer Network API 약관) | A (약관 원문) | REV 3-2022 | 2026-11-10 |
| 4 | `scripts/probe_yfinance.py` 실행 결과 (yfinance 1.8.0) | A (실측) | 2026-11-09 종가까지 | 2026-11-10 |
