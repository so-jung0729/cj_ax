# 데이터 복원·수집·실행 안내

프로젝트 소개는 [README](../README.md), 데이터의 범위·계산 방법·한계는 [데이터 명세](../research/data/data_spec.md)를 먼저 확인하세요.

## 실행 위치

Node.js 18 이상이 필요합니다. **모든 명령은 `README.md`와 `scripts/`가 있는 저장소 루트에서 실행합니다.** `docs/` 안에서 실행하지 않습니다.

다른 컴퓨터에 새로 복제하는 경우:

```powershell
git clone https://github.com/so-jung0729/cj_ax.git
cd cj_ax
```

폴더 통합 변경은 GitHub에 반영되기 전까지 로컬에만 있습니다. 아직 이전 구조의 커밋을 받은 경우에는 해당 커밋의 실행 안내를 따릅니다.

## 저장된 원본 복원과 CSV 생성

```powershell
node scripts/raw_archive.mjs restore
node scripts/build_auction_daily.mjs
```

API 키나 네트워크 호출 없이 저장된 압축본에서 복원합니다. 원본은 `research/data/raw/auction/`, 정리본은 `research/data/`에 생성됩니다.

복원은 같은 이름의 원본을 덮어씁니다. 보관된 압축본은 2026-10-06~2026-11-05의 스냅샷이며, 이후에 수집한 날짜를 자동으로 포함하지 않습니다.

## API 키 설정

새 데이터를 받을 때는 본인이 해당 API 활용 신청을 완료하고 프로젝트 루트 `.env`에 키를 넣습니다. 기존 `.env`가 없다면:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

`DATA_GO_KR_SERVICE_KEY`에 값을 입력합니다. 키 값은 코드·문서·대화·로그·커밋에 쓰지 않습니다. `.env`와 작업용 원본은 Git에서 제외됩니다.

## 수집과 재집계

아래는 보관된 데이터 기간의 예시입니다. 실제로 새로 받을 때는 API에서 조회 가능한 날짜로 바꾸고, 종료일은 경매가 끝난 날짜로 지정하세요.

```powershell
node scripts/backfill_auction.mjs 2026-10-06 2026-11-05
node scripts/build_auction_daily.mjs
```

현재 수집기는 메타데이터가 있는 날짜·품목을 건너뜁니다. `manifest.json`에는 이번 실행에서 지정한 기간을 기록하며, 일별 집계기는 이 목록을 읽습니다. 따라서 **새 날짜만 지정하면 CSV도 그 기간만으로 다시 만들어질 수 있습니다.** 매일 누적 수집을 자동화하기 전, 기간 목록 병합과 늦게 수정된 거래의 재수집 처리를 보완해야 합니다.

정확한 과거 조회 가능 기간과 API별 권한·호출 한도는 확인 중입니다. aT 경매에서 확인한 결과를 정산·KAMIS·기상 API에도 적용할 수 있다고 가정하지 않습니다.

## API 시험 스크립트

| 스크립트 | 목적 |
|---|---|
| `scripts/probe_at.mjs` | 경매·정산 API 호출 시험 |
| `scripts/probe_at_retention.mjs` | 과거 날짜 조회 범위 측정 |
| `scripts/probe_at_scope.mjs` | 시장·품목 범위 측정 |
| `scripts/backfill_auction.mjs` | 날짜·품목별 원본 수집 |
| `scripts/build_auction_daily.mjs` | 중복·오류 처리와 일별·산지별 집계 |
| `scripts/raw_archive.mjs` | 고정 경로의 원본 압축본 생성·복원 |

시험·수집 스크립트는 실제 API를 호출합니다. 폴더 정리 검증에서는 원본 복원·CSV 생성만 실행하고 API를 호출하지 않습니다.
