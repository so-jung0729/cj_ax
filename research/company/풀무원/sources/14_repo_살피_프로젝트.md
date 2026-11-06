# 살피 프로젝트 저장소 (요약 메모)

- 제목: team 장바구니 '살피' 프로젝트
- 저장소: https://github.com/k-1026/jangbaguni
- 확인한 커밋: fc373e5
- 확인한 파일: `brand/살피_브랜드키트_기획서.md`, `salpi_agent/README.md`, `salpi_agent/foodspring.py`, `research/industry_food/업체선정.md`, `research/industry_food/1028_topic_pitch.md`, `simulation/README.md`
- 자료원: 팀 내부 프로젝트 자료. 사실의 외부 근거가 아니라 '우리 자산'의 근거로만 씀.
- 수집일: 2026-11-05 (CJ프레시웨이 폴더에서 복사)

---

- 자산: 시세를 살피는 미어캣 캐릭터 '살피'와, 대구 외식업 사장님을 위한 메뉴 원가 관리 AI.
- 포지셔닝: 식자재몰은 어디서 싸게 살까, 살피는 이 메뉴로 얼마 남을까. 아무것도 팔지 않으며 '기다리기'도 제안함.
- 메인 페르소나: 대구 달서구 한식당 사장님 (가상).
- 웹 기능: 대구 야채 시세 대시보드, 7일 예측, 식봄 상품 표시와 상품 페이지 연결.
- 외부 데이터: aT 도매 경락가·거래량, KAMIS, 기상청, 특일, 대구 행사.
- 설계한 행동 기록: `order_placed`, `stockout_report`, `waste_report`, `deeplink_click` 등.
- 한계: 페르소나와 세그먼트는 가상 설계이고, 실제 매장 판매 데이터로 검증하지 않음.
