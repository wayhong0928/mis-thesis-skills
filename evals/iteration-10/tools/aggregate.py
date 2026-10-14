# -*- coding: utf-8 -*-
"""彙整 iteration-10：偵測率（G／N 分開）、誤報、與 grep 基線比較，依 SPEC.md 第五節判定。

用法：python -X utf8 aggregate.py [--final final]
  有 grading_final.json（主對話裁決後）就用 --final final 優先採用，否則用 grading_sonnet.json。
輸出 ../results.md（只有彙整數字，可公開）與 ../results.json（含逐條 evidence，不公開）。
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IT = HERE.parent
RUNS = IT / "runs" / "academic-writing-discipline"
CASES = IT / "cases" / "academic-writing-discipline"
ARMS = ["without_skill", "v0.5.2"]


def load(rd, final):
    for g in ([final] if final else []) + ["sonnet"]:
        f = rd / f"grading_{g}.json"
        if f.exists():
            return {v["id"]: v for v in json.loads(f.read_text(encoding="utf-8"))["verdicts"]}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--final", default="")
    args = ap.parse_args()
    grep = json.loads((IT / "local" / "grep_baseline.json").read_text(encoding="utf-8"))["summary"]

    stat = {a: {"G": 0, "N": 0, "fp": 0, "runs": 0, "graded": 0, "no_skill_call": 0, "low": 0,
                "G_called": 0, "N_called": 0, "fp_called": 0, "graded_called": {"planted": 0, "clean": 0}} for a in ARMS}
    per = {}  # (case, aid, arm) -> passes
    for meta_f in sorted(CASES.glob("*/eval_metadata.json")):
        case = meta_f.parent.name
        meta = json.loads(meta_f.read_text(encoding="utf-8"))
        roles = {a["id"]: (a["role"], a.get("defect_class")) for a in meta["assertions"]}
        for arm in ARMS:
            for rd in sorted((RUNS / case / arm / "sonnet").glob("run-*")):
                if not (rd / "response.md").exists():
                    continue
                s = stat[arm]
                s["runs"] += 1
                called = bool(json.loads((rd / "timing.json").read_text(encoding="utf-8")).get("skill_calls"))
                s["no_skill_call"] += 0 if called else 1
                g = load(rd, args.final)
                if not g:
                    continue
                s["graded"] += 1
                if called:
                    s["graded_called"]["planted" if "planted" in case else "clean"] += 1
                for aid, (role, cls) in roles.items():
                    v = g[aid]
                    s["low"] += v.get("confidence") == "low"
                    ok = bool(v["passed"])
                    per[(case, aid, arm)] = per.get((case, aid, arm), 0) + ok
                    if role == "detect" and ok:
                        s[cls] += 1
                        if called:
                            s[cls + "_called"] += 1
                    if role == "false_positive" and not ok:
                        s["fp"] += 1
                        if called:
                            s["fp_called"] += 1

    n_det = {"G": 6 * 3, "N": 6 * 3}
    n_fp = 7 * 3
    L = [f"# iteration-10 結果（評分：{args.final or 'sonnet'}）", "",
         "| 方 | 偵測 G | 偵測 N | 偵測合計 | 誤報 | 沒叫用 Skill 的執行 | low confidence 判定 |", "|---|---|---|---|---|---|---|",
         f"| grep 基線 | {grep['caught']['G']}/{grep['total']['G']} | {grep['caught']['N']}/{grep['total']['N']} | "
         f"{grep['caught']['G'] + grep['caught']['N']}/12 | 見 VERDICT | — | — |"]
    for a in ARMS:
        s = stat[a]
        L.append(f"| {a} | {s['G']}/{n_det['G']} | {s['N']}/{n_det['N']} | {s['G'] + s['N']}/36 | {s['fp']}/{n_fp} | "
                 f"{s['no_skill_call']}/{s['runs']} | {s['low']} |")
    s = stat["v0.5.2"]
    L += ["", f"0.5.2 只算有叫用 Skill 的執行：植入題 {s['graded_called']['planted']} 次、乾淨題 {s['graded_called']['clean']} 次；"
          f"偵測 G {s['G_called']}、N {s['N_called']}，誤報 {s['fp_called']}。", ""]
    L += ["| 案例 | 斷言 | " + " | ".join(ARMS) + " |", "|---|---|" + "---|" * len(ARMS)]
    for (case, aid) in sorted({(c, i) for c, i, _ in per}):
        L.append(f"| {case} | {aid} | " + " | ".join(f"{per.get((case, aid, a), 0)}/3" for a in ARMS) + " |")

    # 決策規則（SPEC 第五節）
    v = stat["v0.5.2"]
    w = stat["without_skill"]
    rate = (v["G"] + v["N"]) / 36
    grate = (grep["caught"]["G"] + grep["caught"]["N"]) / 12
    if rate > grate:
        q1 = "勝過 grep" if v["G"] / 18 >= 2 / 3 else "與 grep 互補"
    else:
        q1 = "沒有勝過 grep"
    diff = (v["G"] + v["N"]) - (w["G"] + w["N"])
    if diff >= 4:
        q2 = "與有效果一致" if v["fp"] <= w["fp"] else "有效果但誤報較多"
    elif diff >= 1:
        q2 = "方向一致但不足"
    else:
        q2 = "看不出效果"
    L += ["", f"問題一：0.5.2 偵測率 {rate:.3f}，grep {grate:.3f}，G 類 {v['G']}/18 → **{q1}**",
          f"問題二：0.5.2 比沒裝多 {diff} 條（G {v['G'] - w['G']:+d}、N {v['N'] - w['N']:+d}），誤報 {v['fp']} vs {w['fp']} → **{q2}**"]
    (IT / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (IT / "results.json").write_text(json.dumps({"stat": stat, "per": {"|".join(k): x for k, x in per.items()}, "q1": q1, "q2": q2},
                                                ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
