# K-푸드 기업 리서치와 밸류체인 맵

L.L.M Academy Day 09·Day 10 과제 저장소입니다. AX 데이터·서비스 트랙(푸드 & 리테일) 기준으로 식품 기업 6곳을 조사하고, 생산자부터 물류까지의 돈과 데이터 흐름을 맵으로 정리했습니다.

> **상태: 사람 검증 전 초안입니다.** 점수는 AI 제안이고, 팀 결정과 원문 대조가 남아 있습니다. 개인 실습 자료이며 투자 판단 자료가 아닙니다.

## 바로 보기

**[통합 페이지 열기](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/index.html)**: 기업 카드를 누르면 Day 09 원페이지와 Day 10 밸류체인 맵을 볼 수 있습니다.

기업별 페이지를 바로 열 수도 있습니다.

| 기업 | Day 09 | Day 10 |
|---|---|---|
| CJ프레시웨이 | [원페이지](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/research/company/CJ%ED%94%84%EB%A0%88%EC%8B%9C%EC%9B%A8%EC%9D%B4/onepager.html) | [밸류체인 맵](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/valuechain/valuechain_v1.html) |
| 풀무원 | [원페이지](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/research/company/%ED%92%80%EB%AC%B4%EC%9B%90/onepager.html) | [밸류체인 맵](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/valuechain/%ED%92%80%EB%AC%B4%EC%9B%90/valuechain_v1.html) |
| 컬리 | [원페이지](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/research/company/%EC%BB%AC%EB%A6%AC/onepager.html) | [밸류체인 맵](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/valuechain/%EC%BB%AC%EB%A6%AC/valuechain_v1.html) |
| 현대그린푸드 | [원페이지](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/research/company/%ED%98%84%EB%8C%80%EA%B7%B8%EB%A6%B0%ED%91%B8%EB%93%9C/onepager.html) | [밸류체인 맵](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/valuechain/%ED%98%84%EB%8C%80%EA%B7%B8%EB%A6%B0%ED%91%B8%EB%93%9C/valuechain_v1.html) |
| 오리온 | [원페이지](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/research/company/%EC%98%A4%EB%A6%AC%EC%98%A8/onepager.html) | [밸류체인 맵](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/valuechain/%EC%98%A4%EB%A6%AC%EC%98%A8/valuechain_v1.html) |
| 오아시스 | [원페이지](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/research/company/%EC%98%A4%EC%95%84%EC%8B%9C%EC%8A%A4/onepager.html) | [밸류체인 맵](https://htmlpreview.github.io/?https://github.com/so-jung0729/cj_ax/blob/main/valuechain/%EC%98%A4%EC%95%84%EC%8B%9C%EC%8A%A4/valuechain_v1.html) |

링크는 외부 미리보기 서비스 htmlpreview를 거칩니다. 열리지 않으면 저장소를 내려받아 `index.html`을 브라우저로 여세요.

## 기업 6곳

위 3곳은 후보 기업, 아래 3곳은 비교용 경쟁사입니다.

| 기업 | 유형 | 경쟁 상대 | 우선 기회 (AI 제안) | 영향·실현 | 살피 고객과 일치 |
|---|---|---|---|---|---|
| **CJ프레시웨이** (선정) | B2B 식자재 유통·급식 | 현대그린푸드 | 대구 식당용 7일 시세 전망·보충 알림 | 3·3 | 높음 |
| 풀무원 | 식품 제조사 | 오리온 | 계약 품목 기상·시세 위험 알림 | 3·2 | 일부 |
| 컬리 | 온라인 식품 플랫폼 + 자체 배송 | 오아시스 | 지역 생산자 시세·제철 출하 리포트 | 2·3 | 낮음 |
| 현대그린푸드 | 단체급식·식자재 유통 | CJ프레시웨이 | 외식 고객용 7일 시세 전망·보충 알림 | 3·3 | 중간 |
| 오리온 | 제과 제조사 | 풀무원 | 계약 감자 기상·시세 위험 알림 | 3·2 | 낮음 |
| 오아시스 | 온라인 식품 + 직영 매장 | 컬리 | 대구·경북 생산자 시세·제철 리포트 | 2·3 | 낮음 |

매출과 데이터 단절까지 함께 보려면 [research/company/compare.md](research/company/compare.md)를 보세요.

## 폴더 구조

```text
index.html                     6곳을 한 파일로 모은 통합 페이지
scripts/build_index.mjs        index.html 생성 스크립트
research/company/
  candidates.md                후보 기업 선정 기록
  compare.md                   6곳 비교표
  <기업명>/
    onepager.html              Day 09 산업 리서치 원페이지
    questions.md               리서치 질문
    sources.md                 출처 목록
    sources/                   공시 원문과 보도 요약 메모
    parts/                     주제별 정리와 점검표
    verify.md                  핵심 사실 대조표
valuechain/
  valuechain_v1.html 등        CJ프레시웨이 맵 (폴더 바로 아래)
  <기업명>/                    나머지 5곳의 맵
    valuechain_v1.html         Day 10 발표용 맵
    valuechain_v1.md           Mermaid 맵, 근거, 데이터 15칸
    analysis.md                마커 근거, 불일치, 체크리스트
    valuechain_v0.md           검증 전 초안
    activities_v0.md, stakeholders.md, signals.md   중간 작업
```

Day 10 맵에는 세 화면이 있습니다.

- **단계 카드:** 단계를 누르면 지금 볼 것, 누가, 돈, 데이터를 보여 줍니다.
- **먼저 할 일:** 우선 기회의 근거, 한계, 우선순위를 보여 줍니다.
- **네 층 맵 (제출용):** 활동, 이해관계자, 돈, 데이터를 1280×720 한 장에 담았습니다.

## 표기

| 표기 | 뜻 |
|---|---|
| `[F]` | 원문에서 확인한 사실 |
| `[I]` / `해석` | 해석 |
| `[U]` / `미확인` | 확인하지 못한 내용 |
| `[n]` | `sources.md`의 출처 번호 |

맵에는 금액과 비율을 넣지 않았습니다. 원문 수치와 출처는 각 기업의 `valuechain_v1.md`와 `analysis.md`에 있습니다.

## 자료와 한계

- 공시는 DART 사업보고서 2025.12 기준이고, 2026-11-05~06에 수집했습니다. IR·보도자료·기사는 2026-11-06 기준 최신 자료입니다.
- 보도자료와 기사는 저작권을 고려해 요약만 저장했습니다. 수치를 인용하기 전에 원문을 확인해야 합니다.
- 자동 점검은 숫자가 인용한 원문 줄에 있는지만 확인합니다. 문장의 뜻까지 검증하지는 않습니다.
- 페르소나 등 살피 관련 내용은 가상 설계이며, 실제 매장 데이터로 검증하지 않았습니다.
- 예측 오차(MAE)는 측정하지 않았습니다.
- 지역 자산은 임시값입니다. `local_package/`를 찾지 못했습니다.
- 금칙 그룹 정의를 찾지 못해 기업명 사용 가능 여부를 강사에게 확인해야 합니다.

## 통합 페이지 다시 만들기

`index.html`은 원본 페이지를 복사해 담은 파일입니다. 원본을 고쳤다면 저장소 루트에서 다시 실행하세요. Node.js가 필요합니다.

```bash
node scripts/build_index.mjs
```
