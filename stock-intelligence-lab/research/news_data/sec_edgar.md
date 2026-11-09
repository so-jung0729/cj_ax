# SEC EDGAR

## 1. 한 줄 요약
미국 상장사의 모든 공시를 무료로 받을 수 있는 미국 정부 원천이다. 공시마다 **접수 시각(acceptanceDateTime)이 초 단위로** 붙어 있어서, 실적 발표 같은 이벤트를 가격 시계열과 정확히 맞출 수 있다. [1][3]

## 2. 기본 정보
| 항목 | 내용 | 출처 |
|---|---|---|
| 회사별 공시 목록 | `https://data.sec.gov/submissions/CIK##########.json` (CIK 10자리) | [3] |
| 응답 구조 | 회사 정보(name, tickers, exchanges, sic, fiscalYearEnd…) + `filings.recent` (최근 1,000여 건) + `filings.files` (이전 공시 파일 목록) | [3] |
| 공시 필드 | accessionNumber · filingDate · reportDate · **acceptanceDateTime** · form · items · primaryDocument · isXBRL 등 | [3] |
| AAPL 이력 | recent 1,006건(2015-10-05 ~ 2026-11-06) + 이전 파일 1,271건(1994-01-26 ~ 2015-10-03) | [3] |
| 요청 한도 | 초당 10회 | [1] |
| User-Agent | 요청 헤더에 회사명과 관리자 연락 이메일을 넣도록 요구 | [1] |
| 이용 조건 | "Anyone can access and download this information for free." 재사용 조건은 접근 안내 페이지에 별도 명시 없음 | [1] |

## 3. 서비스 관점에서 눈에 띄는 점
1. **실적 8-K 시각은 UTC이고 항상 장 마감 후다 (Day 5 정정).** ~~Day 3 원문:~~ AAPL 실적 8-K(item 2.02)는 2026-11-02, 07-30, 04-30 모두 `20:30Z`로 찍혀 있다. UTC로 읽으면 7/30·4/30(서머타임, UTC-4)은 동부 16:30(장 마감 후)이다. 하지만 11/02(서머타임 종료 후, UTC-5)는 **15:30, 즉 장중**이 된다. 세 번 모두 같은 시각에 발표했다면 "Z"가 진짜 UTC가 아닐 수 있다. **뉴스·공시를 장 전/장중/장 후로 나누는 로직 전체에 영향**을 주므로 Day 5 전에 확정해야 한다.
2. `items` 필드(예: 2.02 실적, 9.01 첨부)로 이벤트 종류를 바로 분류할 수 있어서, 뉴스보다 깨끗한 **이벤트 라벨**로 쓸 수 있다.
3. 30년 이상의 공시 이력이 있어서 yfinance의 20~45년 가격과 기간이 맞는다.

## 4. 주장별 교차검증
| 주장 | 출처 1 | 출처 2 | 판정 |
|---|---|---|---|
| 접수 시각이 UTC(`Z`)로 표기된다 | 실측 응답 `...T20:30:23.000Z` [3] | — | 단일출처 → EDGAR API 문서 확인 필요 |
| 무료로 내려받을 수 있다 | SEC 안내 [1] | 실측: 인증 없이 200 응답 [3] | 일치 |
| 요청 한도 초당 10회 | SEC 안내 [1] | — | 단일출처 (원문 A 등급이라 사용) |

## 5. 확인 필요 항목
- `company_tickers.json`(티커 → CIK 매핑)은 연락처 없는 User-Agent로 요청하면 **403**. 연락처를 넣은 User-Agent가 필요하다. → 실제 수집 스크립트에서 `.env`의 연락처 값을 쓰도록 할 것
- ~~`acceptanceDateTime`의 `Z`가 실제 UTC인지 → 미확인~~ → **Day 5 확인: UTC.** 11/02 건의 실제 값은 `21:30Z`(Day 3에 20:30Z로 잘못 읽음). 4건 모두 16:30 ET
- 공시 원문을 서비스 화면에 인용·재게시할 때의 조건 → **미확인** (미국 정부 저작물 원칙은 Day 6에서 원문 확인)

## 6. 출처 목록
| # | URL | 등급 | 기준 시점 | 확인일 |
|---|---|---|---|---|
| 1 | https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data | A (공식 안내) | 2024-06-26 최종 검토 | 2026-11-10 |
| 2 | https://www.sec.gov/files/company_tickers.json | A (실측: 403) | 2026-11-10 | 2026-11-10 |
| 3 | `https://data.sec.gov/submissions/CIK0000320193.json` 실측 → `research/data/archive/sec/20261110_sec_aapl_submissions.json` | A (실측) | 2026-11-06 공시까지 | 2026-11-10 |
