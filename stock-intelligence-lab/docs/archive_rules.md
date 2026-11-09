# 아카이빙 규칙 (Day 05)

수집한 것을 파일명만 보고 다시 찾을 수 있게 한다. 수집은 사람(또는 Aside), 정리는 스크립트, 확인은 다시 사람.

## 어디에 두나
| 무엇 | 위치 | Git |
|---|---|---|
| 사용자 말(VOC) 요약 노트 | `archive/text/` (글 1건 = 노트 1개), `archive/video/` (영상 요약) | 커밋 |
| 리뷰 묶음 원문 | `research/data/raw/voc/` | 제외 |
| API로 받은 데이터 원본 | `research/data/archive/` (재배포 가능), `research/data/raw/` (불가) | 앞은 커밋, 뒤는 제외 |
| 수집물 목록 | `archive/metadata.csv` (1건 = 1행, 14열) | 커밋 |
| 태그 목록 | `archive/tags.md` | 커밋 |
| 검증 결과 | `archive/check_report.md` | 커밋 |

이미지는 저장하지 않는다(이 프로젝트에 필요한 이미지 자료 없음).

## 파일명 5요소
`날짜_시장_소스_주제_순번.확장자` — 예: `20261110_us_reddit_ai분석_01.md`

| 요소 | 값 |
|---|---|
| 날짜 | 수집일 YYYYMMDD |
| 시장 | `us` · `kr` · `global` |
| 소스 | `appstore` · `googleplay` · `reddit` · `youtube` · `sec` · `gdelt` · `yfinance` · `alphavantage` |
| 주제 | 한글 키워드 1개, 공백은 `_` |
| 순번 | 같은 날·시장·소스·주제 안에서 01부터 |

## metadata.csv 14열
`id, type, source, title, url, creator, published_at, collected_at, license, market, target, tags, summary, collector`
- 강의의 `region · place`를 `market · target`(시장 · 대상 서비스나 데이터)으로 바꿨다
- `type`: text · video · data · review_set
- `creator`: 기관·채널명, 개인은 "개인" (닉네임 금지)
- `license`: `공개 약관 범위 내 열람` · `저작권자 보유` · `상업 이용 가능(출처 표기)` · `개인·비상업 한정` 중 하나. 빈 값 금지
- **시각은 모두 UTC로 저장한다.** 세 데이터 소스(SEC · GDELT · Alpha Vantage)의 원문 시각은 Day 5에 UTC로 확인했다. 가격 날짜(미국 동부 거래일)와 맞출 때만 변환한다
- `collector`: 역할명 (`본인` · `Aside` · `스크립트`)
