"""Day 04: voc_tagged.csv 집계 → 차트 3개 + 표본 10건 + 요약 수치(JSON).

사용법:
    python scripts/analyze_voc.py
출력: research/users_competitors/charts/*.png, sample10.csv, voc_stats.json
"""
import json
import sys
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "research" / "users_competitors"
CH = D / "charts"
plt.rcParams["font.family"] = ["Malgun Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False
NEG, POS, NEU = "#D9480F", "#2B8A3E", "#ADB5BD"
STAGES = ["가입·계정", "정보 탐색", "판단", "거래", "관리"]


def stacked(ax, table, order, title):
    t = table.reindex(order).fillna(0)
    n = t.sum(axis=1)
    left = pd.Series(0, index=t.index, dtype=float)
    for col, color, label in [("-", NEG, "부정"), ("0", NEU, "중립"), ("+", POS, "긍정")]:
        v = t.get(col, 0)
        ax.barh(t.index, v, left=left, color=color, label=label)
        left += v
    for i, (k, total) in enumerate(n.items()):
        ax.text(total + 0.3, i, f"n={int(total)}", va="center", fontsize=9)
    ax.invert_yaxis()
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="lower right", fontsize=9)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    CH.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(D / "voc_tagged.csv", dtype=str)
    df["sentiment"] = df["sentiment"].replace({"0": "0"})

    # 1) 주제별 감정 분포
    topic = pd.crosstab(df["topic"], df["sentiment"])
    order = topic.sum(axis=1).sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    stacked(ax, topic, order, "주제별 감정 분포 (전체 110건)")
    fig.tight_layout(); fig.savefig(CH / "01_topic_sentiment.png", dpi=150); plt.close(fig)

    # 2) 여정 단계별 감정 (관련 리뷰만)
    rel = df[df["relevant"] == "Y"]
    stage = pd.crosstab(rel["stage"], rel["sentiment"])
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    stacked(ax, stage, [s for s in STAGES if s in stage.index], f"여정 단계별 감정 (질문 관련 {len(rel)}건)")
    fig.tight_layout(); fig.savefig(CH / "02_stage_sentiment.png", dpi=150); plt.close(fig)

    # 3) 앱별 × 반기별 부정 비율
    df["half"] = df["month"].str[:4] + "-H" + df["month"].str[5:7].astype(int).map(lambda m: "1" if m <= 6 else "2")
    app_neg = df.groupby("app")["sentiment"].apply(lambda s: (s == "-").mean() * 100).round(0)
    app_n = df.groupby("app").size()
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    names = {"investing_com": "Investing.com", "kiwoom_heroS": "키움 영웅문S#", "toss": "토스(증권)", "yahoo_finance": "Yahoo Finance"}
    labels = [f"{names[a]} (n={app_n[a]})" for a in app_neg.index]
    ax.barh(labels, app_neg.values, color=[NEG if v >= 60 else "#F08C00" if v >= 40 else POS for v in app_neg.values])
    for i, v in enumerate(app_neg.values):
        ax.text(v + 1, i, f"{v:.0f}%", va="center", fontsize=9)
    ax.set_xlim(0, 100); ax.invert_yaxis()
    ax.set_title("앱별 부정 리뷰 비율", loc="left", fontsize=12, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(CH / "03_app_negative.png", dpi=150); plt.close(fig)

    # 표본 10건 (무작위, 고정 시드)
    sample = df.sample(10, random_state=20261110)[["id", "app", "stage", "topic", "sentiment", "summary"]]
    sample.to_csv(D / "sample10.csv", index=False, encoding="utf-8")

    # 질문 관련 리뷰의 주제 × 감정 매트릭스 (인사이트 재료)
    rel_topic = pd.crosstab(rel["topic"], rel["sentiment"])
    rel_stage_topic = pd.crosstab([rel["stage"]], rel["topic"])
    stats = {
        "total": len(df), "relevant": len(rel),
        "months": [df["month"].min(), df["month"].max()],
        "by_app": app_n.to_dict(),
        "neg_rate_by_app": app_neg.to_dict(),
        "sentiment_total": df["sentiment"].value_counts().to_dict(),
        "topic_counts": df["topic"].value_counts().to_dict(),
        "relevant_topic_sentiment": {k: v for k, v in rel_topic.to_dict(orient="index").items()},
        "relevant_stage_counts": rel["stage"].value_counts().to_dict(),
        "relevant_stage_neg": rel.groupby("stage")["sentiment"].apply(lambda s: int((s == "-").sum())).to_dict(),
        "relevant_stage_topic": rel_stage_topic.to_dict(orient="index"),
    }
    (D / "voc_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=1))
    print(sample.to_string(index=False))


if __name__ == "__main__":
    main()
