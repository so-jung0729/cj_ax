# 자막 추출 테스트 (Day 04 · H)

- 시도일: 2026-11-09
- 결과: **미실시.** 이 PC에서 yt-dlp, Python, Node.js를 찾지 못했습니다 (`py`, `node` 명령 없음).
- 대상 후보: "가락시장 새벽 경매", "양파 산지 출하 인터뷰" 영상 — 웹 검색에서 영상 URL을 찾지 못해 후보도 미확정 [U]

## 다음에 할 일

1. Node.js 18 이상 설치 (README의 데이터 재현에도 필요)
2. `yt-dlp --skip-download --write-auto-sub --sub-lang ko <URL>` 로 자막만 받기
3. 자막 전문은 저장하지 않고 10줄 이내 요약 + 말한 사람의 역할만 `archive/test/<영상ID>.md`에 기록
4. metadata.csv에 `V01` 행 추가 (license는 YouTube 표준 라이선스 → "요약만(저작권)")
