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
