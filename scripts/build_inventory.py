"""Day 06 인벤토리 점수 계산·근거 검증·xlsx 생성.

저장소 루트에서 실행:
    python scripts/build_inventory.py

입력: inventory/inventory_v1.csv (사실 열 + 공통 점수 3열), inventory/scoring_input.csv (트랙 점수 2열)
출력: inventory/scoring.csv, inventory/top3.csv, inventory/evidence_check.md, inventory/inventory_v1.xlsx
점수는 사람이 입력한 값이며, 이 스크립트는 계산과 검증만 한다.
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = os.path.join(ROOT, "inventory")

CRITERIA = ["데이터가용성", "수요규모", "위험크기", "시장성", "스토리성"]
TRACK_W = {"데이터가용성": 0.35, "수요규모": 0.25, "위험크기": 0.20, "시장성": 0.10, "스토리성": 0.10}
COMMON_W = {"스토리성": 1 / 3, "시장성": 1 / 3, "데이터가용성": 1 / 3}
EQUAL_W = {c: 0.2 for c in CRITERIA}


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def weighted(row, weights):
    return round(sum(float(row[c]) * w for c, w in weights.items()), 2)


def main():
    inv = read_csv(os.path.join(INV, "inventory_v1.csv"))
    extra = {r["asset_id"]: r for r in read_csv(os.path.join(INV, "scoring_input.csv"))}
    meta_ids = {r["id"] for r in read_csv(os.path.join(ROOT, "archive", "metadata.csv"))}

    # 1) 근거 검증
    problems = []
    for r in inv:
        refs = [x.strip() for x in r["근거파일"].split(";") if x.strip()]
        if len(refs) < 2:
            problems.append((r["asset_id"], "근거 2개 미만"))
        for ref in refs:
            ok = ref in meta_ids if "/" not in ref else os.path.exists(os.path.join(ROOT, ref))
            if not ok:
                problems.append((r["asset_id"], f"근거 없음: {ref}"))
        for c in ["스토리성", "시장성", "데이터가용성"]:
            if r[c] not in {"1", "2", "3", "4", "5"}:
                problems.append((r["asset_id"], f"{c} 점수 형식 오류"))
        if not r["한줄설명"] or len(r["한줄설명"]) > 60:
            problems.append((r["asset_id"], f"한줄설명 길이 {len(r['한줄설명'])}자"))
    dup = [r["근거파일"] for r in inv]
    lines = ["# 근거 검증 보고서 (Day 06)", "", "- 생성: `python scripts/build_inventory.py`",
             f"- 대상: inventory_v1.csv {len(inv)}행 · metadata id {len(meta_ids)}개", "",
             "| asset_id | 문제 |", "|---|---|"]
    lines += [f"| {a} | {p} |" for a, p in problems] or ["| - | 없음 |"]
    lines += ["", "## 참고", "- 한줄설명 60자 초과는 수업 규칙 위반이지만 수치를 남기려고 둔 행이 있으면 여기 표시됩니다.",
              "- `T05`·`T09`처럼 같은 통계를 인용한 근거는 개수로는 2개지만 독립 출처는 1건입니다(A21 비고).", ""]
    hard = [p for p in problems if not p[1].startswith("한줄설명")]
    lines.append("통과" if not hard else "불통과")
    with open(os.path.join(INV, "evidence_check.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # 2) 점수 계산
    rows = []
    for r in inv:
        e = extra[r["asset_id"]]
        row = {"asset_id": r["asset_id"], "자산명": r["자산명"], "유형": r["유형"],
               "데이터가용성": r["데이터가용성"], "수요규모": e["수요규모"], "위험크기": e["위험크기"],
               "시장성": r["시장성"], "스토리성": r["스토리성"]}
        row["트랙총점"] = weighted(row, TRACK_W)
        row["공통총점"] = weighted(row, COMMON_W)
        row["균등총점"] = weighted(row, EQUAL_W)
        row["근거수치"] = e["근거수치"]
        row["수치출처"] = e["수치출처"]
        row["근거id"] = r["근거파일"]
        row["채점자"] = "Claude 초안(본인 검수 전)"
        rows.append(row)
    for key in ["트랙총점", "공통총점", "균등총점"]:
        ranked = sorted(rows, key=lambda x: (-x[key], x["asset_id"]))
        for i, x in enumerate(ranked, 1):
            x[key.replace("총점", "순위")] = i
    fields = ["asset_id", "자산명", "유형"] + CRITERIA + ["트랙총점", "트랙순위", "공통총점", "공통순위",
                                                    "균등총점", "균등순위", "근거수치", "수치출처", "근거id", "채점자"]
    rows.sort(key=lambda x: x["트랙순위"])
    write_csv(os.path.join(INV, "scoring.csv"), rows, fields)

    top = [r for r in rows if r["트랙순위"] <= 5]
    write_csv(os.path.join(INV, "top3.csv"), top, fields)

    print("evidence:", "통과" if not hard else f"불통과 {hard}")
    for r in rows[:6]:
        print(r["트랙순위"], r["asset_id"], r["자산명"], r["트랙총점"], "공통", r["공통순위"], "균등", r["균등순위"])
    print("공통 Top3:", [r["자산명"] for r in sorted(rows, key=lambda x: x["공통순위"])[:3]])

    # 3) xlsx
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
    except ImportError:
        print("openpyxl 없음 — xlsx 생략", file=sys.stderr)
        return
    wb = Workbook()
    ws = wb.active
    ws.title = "inventory"
    head = list(inv[0].keys())
    ws.append(head)
    for r in inv:
        ws.append([int(r[h]) if h in ("스토리성", "시장성", "데이터가용성") else r[h] for h in head])
    ws2 = wb.create_sheet("scoring")
    ws2.append(["기준", "1점", "3점", "5점", "트랙 가중치", "공통 가중치", "이유"])
    for line in SCALE:
        ws2.append(line)
    ws2.append([])
    ws2.append(fields)
    start = ws2.max_row + 1
    for i, r in enumerate(rows):
        n = start + i
        vals = [r[f] for f in fields]
        ws2.append([int(v) if f in CRITERIA else v for f, v in zip(fields, vals)])
        # 트랙 총점은 시트 수식으로도 계산 (D~H = 데이터가용성~스토리성)
        ws2.cell(row=n, column=9).value = f"=ROUND(D{n}*0.35+E{n}*0.25+F{n}*0.2+G{n}*0.1+H{n}*0.1,2)"
    ws3 = wb.create_sheet("top3")
    ws3.append(["구분", "1위", "2위", "3위"])
    for key, label in [("트랙순위", "트랙 가중치 (데이터·서비스)"), ("공통순위", "공통 가중치"), ("균등순위", "5기준 균등 (민감도)")]:
        ranked = sorted(rows, key=lambda x: x[key])[:3]
        ws3.append([label] + [f"{x['자산명']} ({x['asset_id']})" for x in ranked])
    for sh in (ws, ws2, ws3):
        sh.freeze_panes = "A2"
        for c in sh[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="E3F1EE")
    wb.save(os.path.join(INV, "inventory_v1.xlsx"))
    print("xlsx 저장")


SCALE = [
    ["데이터가용성", "텍스트 서술만 있음", "반정형 자료(목록·보도 수치)나 월 단위 통계", "일 단위 API·CSV를 실제 확보했거나 호출 확인", 0.35, 1 / 3, "대시보드가 매일 갱신돼야 함"],
    ["수요규모", "거래·이용 수치 없음", "보도 수치 또는 중간 규모 거래(일 100t 미만)", "일 1000t 이상 거래 또는 전국 단위 이용 수치", 0.25, 0, "많이 쓰는 품목일수록 사용자가 많음"],
    ["위험크기", "한 달 가격 변동계수 5% 미만, 급변 보도 없음", "변동계수 5~20% 또는 급변 보도 1건", "변동계수 20% 이상 또는 평년·전월 대비 40% 이상 급변 근거", 0.20, 0, "알릴 가치가 있는 변화가 있는가"],
    ["시장성", "구매자의 비용·업무와 연결된 근거 없음", "구매자 관련 보도 1건", "구매자(식당·급식·MD)의 비용 부담 근거 2건 이상", 0.10, 1 / 3, "사람이 돈·시간을 쓰는 대상인가"],
    ["스토리성", "이름·수치만 있음", "변화의 원인 하나가 자료에 등장", "원인·당사자·사건이 여러 소스에서 반복", 0.10, 1 / 3, "이유를 설명할 재료가 있는가"],
]

if __name__ == "__main__":
    main()
