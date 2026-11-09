# 원천 데이터셋 명세 v0 (Day 03 과제)

데이터는 모두 `research/data/` 한 곳에 있다. 정리본 CSV는 이 폴더 바로 아래, 재배포 가능한 원본은 `archive/`(커밋), 약관상 재배포 불가·작업용 원본은 `raw/`(커밋 제외), 호출 확인 기록은 `checks/`. 만드는 코드는 `scripts/build_day03_tables.py`.
Day 6 인벤토리의 "데이터 가용성" 점수는 이 명세의 완성도로 매긴다.

---

## 1. prices_daily.csv — 일봉 가격
| 항목 | 내용 |
|---|---|
| 출처 | yfinance 1.8.0 (Yahoo Finance 데이터), `scripts/probe_yfinance.py`로 다운로드, 2026-11-10 |
| 이용 조건 | Yahoo 약관상 개인 용도, 자동 수집 금지 → **로컬 학습용만, 저장소 커밋 제외** |
| 행 단위 | 종목 1개 × 거래일 1일. 총 57,030행 |
| 범위 | 7종목: AAPL · MSFT · NVDA · AMZN · GOOGL · SPY · 005930.KS, 종목별 상장일 ~ 2026-11-09 |
| 키 | (`ticker`, `date`) 중복 0건 |

| 열 | 의미 | 단위·형식 | 예시 |
|---|---|---|---|
| ticker | 종목 코드 (Yahoo 표기) | 문자열 | AAPL, 005930.KS |
| date | 거래일 (거래소 현지 날짜) | YYYY-MM-DD | 2026-11-09 |
| open · high · low · close | 원가격 (분할·배당 미조정) | 현지 통화 (USD, KRW) | 245.00 |
| adj_close | 분할·배당 조정 종가 | 현지 통화 | |
| volume | 거래량 | 주 | 3494073 |
| dividend | 그날 배당 | 주당 현지 통화, 없으면 0 | |
| split_ratio | 그날 분할 비율 | 배수, 없으면 0 | 4.0 |
| source | 소스 이름 | 고정값 `yfinance` | |

품질 메모
- **결측 1건:** 005930.KS 2026-11-09 `close`·`adj_close` 비어 있음. 다운로드 시점(한국 시간 11/10)의 마지막 행이라 미확정 행으로 추정 → 수집 시 마지막 거래일 결측은 버리고 다음 날 다시 받는 규칙 필요 (Day 5)
- 통화가 섞여 있음(USD/KRW). 학습에는 수익률을 쓰므로 문제없지만, 화면에 보여줄 때는 통화 열이 필요
- 상장폐지 종목 없음 → 생존편향

활용 가설: 60거래일 입력 / 5거래일 수익률 방향 라벨을 종목당 수천 개 만들 수 있는가 → 가능(최소 GOOGL 5,592일)

---

## 2. sec_filings_aapl.csv — 공시 목록
| 항목 | 내용 |
|---|---|
| 출처 | `https://data.sec.gov/submissions/CIK0000320193.json`, SEC EDGAR, 2026-11-10 다운로드 |
| 이용 조건 | 미국 정부 공개 자료, 무료. 재게시 조건은 Day 6에서 원문 확인 |
| 행 단위 | 공시 1건. 1,006행 (2015-10-05 ~ 2026-11-06, `filings.recent`만) |
| 키 | `accession_number` |

| 열 | 의미 | 단위·형식 | 예시 |
|---|---|---|---|
| ticker · cik | 종목 코드 · SEC 회사 번호 | 문자열 | AAPL · 0000320193 |
| accession_number | 공시 고유 번호 | 문자열 | |
| form | 공시 종류 | 문자열 | 8-K, 10-Q, 4 |
| filing_date | 접수일 | YYYY-MM-DD | 2026-11-02 |
| report_date | 보고 대상일 | YYYY-MM-DD, 없으면 빈칸 | 2026-09-26 |
| acceptance_datetime_raw | 접수 시각 원문 | ISO 문자열, **시간대 미확정** | 2026-11-02T20:30:23.000Z |
| items | 8-K 항목 번호 | 쉼표 구분 | 2.02,9.01 |
| primary_document | 본문 파일명 | 문자열 | |
| source | 고정값 `sec_edgar` | | |

품질 메모
- 1994~2015 공시는 `filings.files`의 별도 파일에 있음 → 아직 미포함
- form 분포: Form 4(내부자 거래) 602건이 대부분. 이벤트 피처로는 8-K(101건) · 10-Q(33건) · 10-K가 핵심
- `acceptance_datetime_raw`는 시간대 해석이 불일치해서(교차검증 #14) 변환하지 않고 원문 그대로 둠

활용 가설: 실적 발표(8-K item 2.02) 전후로 수익률·변동성이 달라지는가

---

## 3. gdelt_gkg_sample.csv — 뉴스 기사 목록 (샘플)
| 항목 | 내용 |
|---|---|
| 출처 | `https://data.gdeltproject.org/gdeltv2/20261109160000.gkg.csv.zip`, GDELT GKG 2.1, 2026-11-10 다운로드 |
| 이용 조건 | 상업 이용·재배포 가능, GDELT 인용과 링크 필수 |
| 행 단위 | 기사 1건. 1,443행 (15분 배치 1개) |
| 키 | `gkg_record_id` (URL 중복 0건) |

| 열 | 의미 | 단위·형식 | 예시 |
|---|---|---|---|
| gkg_record_id | GKG 레코드 ID | 문자열 | 20261109160000-0 |
| date_raw | 배치 시각 (파일 내 모든 행 동일) | YYYYMMDDHHMMSS, **시간대 미확정** | 20261109160000 |
| source_domain | 언론사 도메인 | 문자열 | mashable.com |
| url | 기사 URL | 문자열 | |
| title | 기사 제목 (`<PAGE_TITLE>`) | 문자열, 4건 빈 값 | |
| organizations | 기사에 나온 기관명 | 세미콜론 구분 | apple;nvidia |
| tone | 평균 톤 점수 | 실수, 이 파일 범위 -15.2 ~ 16.7 | -1.15 |
| source | 고정값 `gdelt_gkg` | | |

품질 메모
- 종목 코드가 없음. 기관명 → 티커 매핑 테이블 필요 (Apple Inc ≠ apple 과일 구분)
- 금융과 무관한 기사가 대부분(연예·지역 뉴스). 이 샘플에서 Apple · Nvidia · Microsoft가 기관 열에 나온 기사는 65건
- 제목 4건이 빈 값

활용 가설: 기업별 하루 기사 수와 평균 톤이 다음 5거래일 수익률·변동성과 관계가 있는가
