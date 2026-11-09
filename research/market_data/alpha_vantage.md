# Alpha Vantage

## 1. 한 줄 요약
가격(일봉)과 종목별 뉴스·감성을 한 곳에서 주는 후보지만, **무료 키는 개인·비상업 용도로 제한되고, 수정주가와 뉴스 API는 유료(premium)** 라서 광고가 붙는 공개 서비스에는 그대로 쓸 수 없다. [1][2]

## 2. 기본 정보
| 항목 | 내용 | 출처 |
|---|---|---|
| 일봉 (`TIME_SERIES_DAILY`) | 원가격(as-traded) OHLCV. `compact`(최근 100개)는 무료, `full`(25년 이상)은 유료 키 전용 | [1] |
| 수정주가 (`TIME_SERIES_DAILY_ADJUSTED`) | 수정 종가 + 분할·배당 이벤트 포함. **유료 함수** | [1] |
| 뉴스 (`NEWS_SENTIMENT`) | 종목(`tickers`)·주제(`topics`)·기간(`time_from/time_to`, `YYYYMMDDTHHMM`) 필터, `limit` 최대 1000. **유료 함수** | [1] |
| 무료 호출 한도 | 하루 25회. 단, 검증된 오픈소스·교육 프로젝트는 무제한 요청 가능하다고 안내 | [3] |
| 무료 이용 범위 | "personal, non-commercial use". 본인 외 다른 사람이 정보에 직·간접적으로 접근하는 상업 활동은 commercial use. 상업 이용은 별도 문의(premium@alphavantage.co) | [2] |

### 실제 응답 확인 (demo 키, 2026-11-10)
- 일봉 IBM: `Meta Data` + `Time Series (Daily)`, 키는 `1. open` ~ `5. volume`(값은 문자열), **Time Zone: US/Eastern**, compact 100행 (2026-06-17 ~ 2026-11-06) [4]
- 뉴스 AAPL: `feed` 50건, 필드 `title, url, time_published, summary, source, overall_sentiment_score/label, ticker_sentiment[]`
  - `time_published` 형식 `20261109T121405` (초 단위), **시간대 표기 없음**
  - `ticker_sentiment[]` 안에 `ticker, relevance_score, ticker_sentiment_score/label` → 종목 연결과 관련성 점수를 바로 쓸 수 있음 [4]
- 원본: `archive/20261110_alphavantage_*_demo.json` (커밋 제외)

## 3. 서비스 관점에서 눈에 띄는 점
1. **종목별 관련성 점수(relevance_score)** 가 기사마다 붙어 있어 `news_tickers` 테이블을 거의 그대로 만들 수 있다.
2. 감성 점수가 이미 제공되지만, 이건 공급자의 분류 결과다. 우리 모델(FinBERT 등)과 비교하는 **기준선**으로 쓰는 편이 맞다.
3. 무료 키로는 수정주가와 장기 이력을 받을 수 없어서, **60일 윈도우 학습용 데이터를 무료 키만으로는 확보하기 어렵다**.

## 4. 확인 필요 항목
- `time_published`의 시간대 (UTC? US/Eastern?) → **미확인**. 뉴스와 가격을 맞추는 데 핵심이라 반드시 확인
- 뉴스 아카이브의 시작 시점 (몇 년까지 거슬러 갈 수 있나) → **미확인**
- 유료 플랜 가격, 유료 플랜에서도 공개 웹 표시·모델 학습이 허용되는지 → **미확인** (약관 원문에 해당 조항 없음, 문의 필요)
- "교육 프로젝트 무제한" 조건이 이 프로젝트(교육과정 개인 프로젝트)에 해당하는지 → **미확인**
- 약관의 최종 개정일 → 원문 PDF에 표시 없음

## 5. 출처 목록
| # | URL | 등급 | 기준 시점 | 확인일 |
|---|---|---|---|---|
| 1 | https://www.alphavantage.co/documentation/ | A (공식 문서) | 확인 시점 현재 | 2026-11-10 |
| 2 | https://www.alphavantage.co/terms_of_service/ (PDF) | A (이용약관 원문) | 개정일 표기 없음 | 2026-11-10 |
| 3 | https://www.alphavantage.co/support/ | A (공식 안내) | 확인 시점 현재 | 2026-11-10 |
| 4 | demo 키 실제 호출 (`function=NEWS_SENTIMENT&tickers=AAPL`, `function=TIME_SERIES_DAILY&symbol=IBM`) | A (실측) | 2026-11-10 응답 | 2026-11-10 |
