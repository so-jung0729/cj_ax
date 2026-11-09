# 이벤트 데이터 명세 초안 (Day 08)

이벤트 = 사용자 행동 1건의 기록. 개인정보(이름·연락처)는 넣지 않습니다.

| 이벤트 | 발생 시점 | 속성 | 화면 | 쓰는 지표 |
|---|---|---|---|---|
| `alert_open` | 알림을 눌러 앱이 열림 | user_id, item, change_pct, base_date | 1 | 알림 열람률 |
| `app_open` | 알림 없이 앱을 엶 | user_id, source(direct·link) | 1 | 일일 방문자 |
| `segment_set` | 세그먼트 선택 | user_id, segment(SG1·SG2·SG3) | 2 | 세그먼트 분포 |
| `item_follow` | 담당 품목 선택·해제 | user_id, item, action(add·remove) | 2 | 품목별 관심 수 |
| `threshold_set` | 알림 기준 저장 | user_id, item, base(first_week), threshold_pct | 3 | 설정 완료율 |
| `board_view` | 품목 수급판 열기·기간 변경 | user_id, item, period_days | 4 | 품목별 조회 |
| `origin_view` | 산지 탭 보기 | user_id, item, origin | 5 | 산지별 조회 |
| `reason_open` | 이유 카드 열기 | user_id, item, reason_type(supply_up·supply_down·origin) | 6 | 근거 열람률 |
| `source_open` | 출처·기준일 링크 열기 | user_id, item, source(aT 경매 등) | 6 | 출처 확인률 |
| `alert_subscribe` | 이 품목 알림 받기 | user_id, item, threshold_pct | 7 | 알림 구독 전환율 |

## 공통 속성
`event_id`, `event_time`(KST), `app_version`, `data_base_date`(화면에 보인 데이터의 기준일)

## 한계
- `data_base_date`를 이벤트마다 남기는 이유: 경매 데이터가 약 한 달만 조회돼 같은 화면도 날마다 숫자가 달라집니다.
- 실제 저장소(DB)는 아직 정하지 않았습니다.
