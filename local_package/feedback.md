# Local 결과 피드백 (Day 11 · 1~2교시)

- 작성일: 2026-11-09
- **이 파일의 성격:** 혼자 진행하는 프로젝트라 다른 팀 발표·피드백이 없습니다. 아래는 Day 11 평가 기준 네 가지(①근거 ②구조화 ③일관성 ④AI 활용)로 **Claude Code가 local_package를 점검한 자가 점검**입니다. 강사·동료 피드백을 받으면 같은 형식으로 위에 추가합니다.
- 형식: 기준 | 관찰 | 근거 | 제안 | 분류(반영/보류/질문) | 담당 | 대상 파일

| # | 기준 | 관찰 | 근거 | 제안 | 분류 | 담당 | 대상 파일 |
|---|---|---|---|---|---|---|---|
| 1 | ① | 00_README에 Day 09 원페이지·Day 10 밸류체인 경로가 없음 | Day 11 점검 질문 "README에 11/5 원페이지 · 11/6 밸류체인 맵 경로까지 있는가" | 파일 안내 표에 Day 09·10 줄 추가 | **반영 완료** (feedback #1) | 본인 | local_package/00_README.md |
| 2 | ① | 수집물 25건 중 원문 확인 4건, 검색 요약 15건 | archive/check_report.md, voices/report.md | 인벤토리 근거로 쓰는 행부터 원문 대조 | 보류 — 11/13 시장 검증 전 | 본인 | archive/metadata.csv |
| 3 | ① | 유튜브 자막·커뮤니티 VOC 0건이라 Day 11 VOC가 기사 위주 | research/fieldwork_plan.md Q5·Q6 | 커뮤니티 Q&A 10건 수집 후 voc_classified.csv에 추가 | 보류 — 11/12 spec 전 | 본인 | painpoint/voc_classified.csv |
| 4 | ② | 인벤토리 점수가 AI 초안 1인 채점 | inventory/scoring.csv 채점자 열 | 본인 채점 후 2점 이상 차이 항목 척도 수정 | 보류 — 11/13 전 | 본인 | inventory/scoring_input.csv |
| 5 | ③ | 스토리보드 전환 컷 문구 = 스킬 핵심 메시지 ①, 금칙어 0 | storyboard/review_v1.md | 유지 (칭찬) | — | — | storyboard/storyboard_v1.md |
| 6 | ④ | 기존 기업별 밸류체인 맵에 팀 프로젝트(살피) 페르소나가 남아 있음 | CLAUDE.md 범위 규칙 | 산업 맵(valuechain/industry)에서는 제거함. 기업별 맵 정리 여부 결정 필요 | 질문 | 본인 | valuechain/*/valuechain_v1.md |
| 7 | ④ | 프롬프트·결과 쌍과 검증 기록은 있으나 사람 검증 표본이 아직 없음 | brand/test/, storyboard/screens/prompt.md, painpoint/review_sample.md | 표본 검수 칸을 사람이 채움 | 보류 — 이번 주 | 본인 | painpoint/review_sample.md |
