# 수급 레이더 (가칭)

품목과 산지별 가격·물량 이상과 기상 위험을 공공데이터로 한곳에서 보여 주는 개인 사이드 프로젝트입니다.

> **상태: 기획과 데이터 검증 전입니다.** 아직 동작하는 서비스가 없습니다.

## 문서

- [진행 로드맵](ROADMAP.md)
- [목표](goals.md)
- [결정 기록](DECISIONS.md)
- [병목 분석](../research/bottlenecks.md)
- [공공데이터 목록](../research/opendata_catalog.md)

## 다른 컴퓨터에서 시작하기

Node.js 18 이상이 필요합니다.

```bash
git clone https://github.com/so-jung0729/cj_ax.git
```

```bash
cd cj_ax/sugeup-radar
```

```bash
cp .env.example .env
```

`.env`에 API 키를 넣습니다. `.env`는 Git에 올라가지 않으므로 컴퓨터마다 새로 넣어야 합니다.

경매 원본 데이터를 되돌립니다.

```bash
node scripts/raw_archive.mjs restore
```

새 날짜를 받은 뒤 정리본을 다시 만듭니다. 종료일은 어제 날짜로 넣습니다.

```bash
node scripts/backfill_auction.mjs 2026-10-06 2026-11-06
```

```bash
node scripts/build_auction_daily.mjs
```

> 경매 API는 약 한 달 치만 조회되는 것으로 보입니다. 오래 비워 두면 그 사이 데이터를 받지 못할 수 있습니다. 매일 자동 수집은 아직 설정하지 않았습니다.

## 안내

가격과 위험 정보는 참고용이며, 구매나 투자를 권유하지 않습니다.
