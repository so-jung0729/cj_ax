# 화면 시안 생성 기록 (Day 08 과제)

- 도구: Claude Code (Claude Design 대신 — 이 환경에서 접속 불가)
- 결과: [screens_v0.html](screens_v0.html) — 7화면, 화면마다 생기는 데이터(이벤트) 표시
- 날짜: 2026-11-09

## 입력
1. plan/onepager.md (한 장 기획서)
2. storyboard/storyboard_v1.md (7컷 표)
3. storyboard/screen_flow.md (화면 · 입력 · 데이터 · 지표)
4. `brand-sugeup-radar` 스킬 (톤·금칙어), research/metrics.csv · 산지 상위 5곳 계산값

## 프롬프트

```text
plan/onepager.md, storyboard/storyboard_v1.md, storyboard/screen_flow.md를 읽고
brand-sugeup-radar 스킬로 모바일 7화면 흐름 시안을 HTML 한 파일로 만들어 줘.
- 화면마다 storyboard_v1.md의 화면 문구를 그대로 쓰고 숫자는 research/metrics.csv에서만
- 화면당 주 버튼은 1개
- 화면 아래에 생기는 데이터(events.md의 이벤트 이름)를 표시
- 전환 화면(컷 6)은 어두운 바탕으로 앞 화면과 대비
```

## 수정 이력
- 컷 4 그래프에 "첫 주 740원" 기준선 추가 — 화면 문구의 비교 기준을 그래프에서도 보이게
- 컷 7에서 배추는 "규격 정리 후 제공"으로 표시 — 배추 소포장 혼재 리스크(top3_rationale) 반영
