# Local 결과 패키지 — 수급 레이더

- 정리일: 2026-11-09 · 강의 Day 04~08 산출물을 한 줄기로 묶은 패키지
- 진행: 개인 프로젝트 (팀 → 1인). 수업의 "지역 자산"을 **품목·산지·데이터 자산**으로 바꿔 적용 ([ROADMAP](../ROADMAP.md))
- HTML로 보기: 루트 [index.html](../index.html) 한 곳에서 봅니다 (Day 04~10 한 줄기 카드 → 카드를 누르면 Day별 상세·기업 원페이지). 만들기: `python scripts/build_index.py` (이 폴더의 day04~08·journey.html도 함께 갱신)

## 한 줄
**자산** 양파·무·배추 (aT 경매 데이터) → **고객** 식자재 유통사 농산 구매 담당자 → **메시지** "평소와 달라진 품목을, 이유와 함께 먼저 보여 드립니다." → **화면** 무 알림 → 이유 카드 → 알림 받기

## 파일 안내

| 단계 | 파일 | 역할 |
|---|---|---|
| Day 04 | [research/fieldwork_plan.md](../research/fieldwork_plan.md) · [voices/report.md](../research/voices/report.md) · [insights.md](../research/insights.md) · [metrics.md](../research/metrics.md) | 필드워크 계획, 사람들의 말 분석, 인사이트 3, 지표 후보 6 |
| Day 05 | [archive/metadata.csv](../archive/metadata.csv) · [tags.md](../archive/tags.md) · [check_report.md](../archive/check_report.md) · [collect_sheet.csv](../archive/collect_sheet.csv) · [questions.md](../archive/questions.md) | 수집물 25건 아카이브와 점검 |
| Day 06 | [inventory/inventory_v1.xlsx](../inventory/inventory_v1.xlsx) · [top3_rationale.md](../inventory/top3_rationale.md) · [evidence_check.md](../inventory/evidence_check.md) | 자산 30개, 점수, Top 3 근거 |
| Day 07 | [brand/persona_sheet.md](../brand/persona_sheet.md) · [customer_persona.md](../brand/customer_persona.md) · [SKILL.md](../.claude/skills/brand-sugeup-radar/SKILL.md) · [worldview.md](../.claude/skills/brand-sugeup-radar/worldview.md) · [segment_definition.md](../plan/segment_definition.md) · [onepager.md](../plan/onepager.md) | 브랜드·고객 페르소나, 세계관, 브랜드 스킬, 세그먼트, 한 장 기획서 |
| Day 08 | [storyboard/storyboard_v1.md](../storyboard/storyboard_v1.md) · [review_v1.md](../storyboard/review_v1.md) · [screen_flow.md](../storyboard/screen_flow.md) · [events.md](../storyboard/events.md) · [screens/screens_v0.html](../storyboard/screens/screens_v0.html) | 7컷 스토리보드, 화면 흐름, 이벤트 명세, 화면 시안 |
| Day 09 | [research/company/compare.md](../research/company/compare.md) · [companies.csv](../research/company/companies.csv) · 기업별 `research/company/<기업>/onepager.html` | 기업 6곳 원페이지·비교 (feedback #1) |
| Day 10 | [valuechain/industry/valuechain_v1.md](../valuechain/industry/valuechain_v1.md) · [analysis.md](../valuechain/industry/analysis.md) · [valuechain_v1.html](../valuechain/industry/valuechain_v1.html) | 6곳을 겹친 산업 밸류체인 v1 (feedback #1) |
| Day 11 | [feedback.md](feedback.md) · [painpoint/](../painpoint/painpoint_def.md) | 자가 점검 피드백, 고객 여정·페인포인트 Top 3 |

수업 양식의 `01_inventory/ … 03_storyboard/` 사본은 만들지 않고 원본 위치로 연결했습니다 (같은 파일이 두 곳에 생기지 않게).

## 세 산출물이 같은 곳을 가리키는가

| 점검 | 결과 |
|---|---|
| 자산 | 인벤토리 Top 3(양파·무·배추) = 스토리보드 소재(무)·브랜드 핵심 자산(양파) ✅ |
| 메시지 | 스킬 핵심 메시지 ① = 스토리보드 전환 컷 6 문구 ✅ |
| 대상 | 페르소나(구매 담당자)가 행동유도(알림 받기)를 할 사람 ✅ |
| 근거 | 화면 숫자 4개 모두 research/metrics.csv와 일치 ([review_v1.md](../storyboard/review_v1.md)) ✅ |
| AI 흔적 | 프롬프트·생성 기록: fieldwork_plan(표준 프롬프트), scripts/build_inventory.py, brand/test/, storyboard/screens/prompt.md ✅ |

## 미완 항목과 보완 계획

| 항목 | 막힌 이유 | 다음 |
|---|---|---|
| 유튜브 자막 5건 · 커뮤니티 10건 | yt-dlp·Node 없음, 수집 미실시 | Node 설치 후 Aside로 수집 |
| 검색 요약 15건 원문 대조 | 시간 | 인벤토리 근거로 쓰는 행부터 |
| 2인 채점 캘리브레이션 | 혼자 진행 | AI 점수와 본인 점수 비교, 2점 이상 차이 항목 척도 수정 |
| 스킬 호출 확인 | 새 세션 필요 | 새 Claude Code 세션에서 `brand-sugeup-radar` 확인 |
| Claude Design 시안 | 이 환경에서 접속 불가 | HTML 시안으로 대체, 접속되면 같은 표로 다시 생성 |
