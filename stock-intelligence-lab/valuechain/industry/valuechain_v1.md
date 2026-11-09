# 산업 밸류체인 맵 v1 — 주식 정보 산업 (기업 6곳 통합)

- 입력: 기업 6곳 원페이지(`research/company/*/onepager.md`), 비교표 [compare.md](../../research/company/compare.md), Day 10 서비스 밸류체인 [v1](../valuechain_v1.md)
- 무엇이 다른가: 서비스 하나가 아니라 **6곳이 같은 줄기의 어느 칸에 서 있는지**를 한 장에 겹쳤다
- 표기: 실선 = 데이터(상품), 굵은 선 = 돈(소비자 → 원천), 점선 = 피드백. 금액은 그림 밖 메모에 출처와 함께
- 태그: [F] 원문 · [I] 해석 · [U] 미확인. 마커 근거는 [analysis.md](analysis.md)
- 상태: **기업 원페이지와 대조 완료, 사람 대조 전**

## 한 줄 요약
데이터는 ① 거래소에서 생겨 ② 공급사를 거쳐야 ③ 플랫폼 화면에 올라갈 수 있고, 돈은 반대로 ⑤ 광고주 · 매매 수수료에서 시작해 ③ → ② → ①로 **두 번 차감되며** 올라간다. 공개 원천(SEC · 공시 · 공개 뉴스)만 이 고리를 거치지 않는다. 이슈렌즈는 그 틈에 선다 [I].

```mermaid
flowchart LR
  subgraph S1["① 원천"]
    E1["<b>거래소</b><br/>ICE(NYSE) · KRX · 넥스트레이드 · 나스닥"]
    E2["<b>공개 원천</b><br/>SEC EDGAR · DART · 공개 뉴스(GDELT)"]:::asset
  end
  subgraph S2["② 가공 · 라이선스"]
    V1["<b>데이터 공급사</b><br/>ICE Data · LSEG(Refinitiv) · S&P · Morningstar · FnGuide · 코스콤"]
    B1["병목 B1<br/>공개 화면용 가격은 계약 필요, 요금 비공개"]:::bottleneck
  end
  subgraph S3["③ 플랫폼"]
    P1["<b>광고 · 구독형</b><br/>Yahoo Finance · Investing.com · 네이버페이 증권"]
    P2["<b>증권사 앱</b><br/>토스증권 (정보 무료 + 매매)"]
    P3["<b>이슈렌즈</b> (우리)<br/>공개 원천 직접 사용"]:::asset
    B2["병목 B2<br/>숫자 정확성 · 기준 시각이 보이지 않음"]:::bottleneck
    O1["★ 기회 O1<br/>숫자마다 기준 시각 · 출처"]:::opp
  end
  subgraph S4["④ 이용"]
    U1["<b>개인투자자</b> SG1~3<br/>(커뮤니티 · 핀플루언서)"]
    B3["병목 B3<br/>포트폴리오는 로그인 · 계좌에 묶임"]:::bottleneck
    O3["기회 O3<br/>로그인 없는 관심목록"]:::opp
  end
  subgraph S5["⑤ 행동"]
    A1["<b>광고주</b> · <b>구독</b>"]
    A2["<b>매매 · 환전</b> (증권사)"]
    K2["규제 K2<br/>유료 · 양방향이면 신고 · 등록"]:::cost
  end

  E1 -->|"체결가"| V1
  V1 -->|"시세 · 추정치 · 재무 (라이선스)"| P1
  V1 -->|"투자정보"| P2
  E2 -->|"공시 · 기사 (무료, GDELT는 재배포 가능)"| P3
  E2 --> P2
  P1 -->|"화면 (참고용 면책)"| U1
  P2 -->|"AI 요약 (면책)"| U1
  P3 -->|"숫자 + 기준 시각 + 출처 · 적중률"| U1
  U1 --> A1
  U1 --> A2

  A1 ==>|"시작점: 광고비 · 구독료"| P1
  A2 ==>|"시작점: 매매 · 환전 수수료"| P2
  P1 ==>|"라이선스료 (차감 1)"| V1
  P2 ==>|"라이선스료"| V1
  V1 ==>|"거래소 데이터 요금 (차감 2 · LSEG는 고객에 회수)"| E1

  U1 -.->|"관심목록 · 클릭"| P3
  P3 -.->|"예측 적중 기록"| P3

  classDef asset fill:#D5F0EA,stroke:#00594A,color:#00594A
  classDef bottleneck fill:#FFE8DD,stroke:#D9480F,color:#9C2F00
  classDef cost fill:#FFF1A8,stroke:#B08900,color:#4D3D00
  classDef opp fill:#E0F3E5,stroke:#2B8A3E,color:#1E6B30
```

## 단계별 메모 (출처는 각 원페이지)
| 단계 | 누가 | 돈 | 데이터 |
|---|---|---|---|
| ① 원천 | ICE(NYSE) · KRX · 넥스트레이드 · SEC · DART | ICE: 거래소 데이터 · 연결 10.31억 USD(2025) [F] | 체결가는 거래소 소유, 공시 · 공개 뉴스는 누구나 |
| ② 가공 | ICE Data · LSEG · S&P · Morningstar · FnGuide · 코스콤 | LSEG 총수익 89.86억 GBP, 제3자 콘텐츠 회수 3.60억 GBP [F] | 재배포 조건 · 요금은 비공개 계약 [U] |
| ③ 플랫폼 | Yahoo · Investing.com · 네이버 · 토스 · 이슈렌즈 | Yahoo 구독 9.95~49.95 USD/월, 토스 수수료 5,778억 원 [F] | Investing.com "실시간 · 정확 보장 안 함" [F] |
| ④ 이용 | 개인투자자 | 무료 | VOC: 숫자 신뢰 불만이 1위(P1) |
| ⑤ 행동 | 광고주 · 증권사 | 돈의 시작점 | — |
