# -*- coding: utf-8 -*-
"""彙整 iteration-6 的結果，輸出 ../results.json 與 ../results.md。

用法：python aggregate.py [--grader sonnet] [--final final]
  --grader：主要數字用哪一份評分（預設 sonnet）。若 run 目錄有 grading_final.json（主對話裁決後的版本），
  以 --final final 指定優先採用它。
"""
import argparse
import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
IT6 = HERE.parent
RUNS = IT6 / "runs"
CASES = IT6 / "cases"
EXCL = json.loads((IT6 / "excluded_assertions.json").read_text(encoding="utf-8")) if (IT6 / "excluded_assertions.json").exists() else []


def load_grading(rd, grader, final):
    for g in ([final] if final else []) + [grader]:
        f = rd / f"grading_{g}.json"
        if f.exists():
            return {v["id"]: v for v in json.loads(f.read_text(encoding="utf-8"))["verdicts"]}
    return None


def tokens(t):
    u = t.get("usage") or {}
    return sum(u.get(k, 0) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))


def mean(xs):
    return round(st.mean(xs), 3) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grader", default="sonnet")
    ap.add_argument("--final", default="")
    args = ap.parse_args()

    rows = []  # 每個 run 一列
    for meta_f in sorted(CASES.glob("*/*/eval_metadata.json")):
        skill, case = meta_f.parent.parent.name, meta_f.parent.name
        meta = json.loads(meta_f.read_text(encoding="utf-8"))
        excluded = {e["id"] for e in EXCL if e["skill"] == skill and e["case"] == case}
        tc = {a["id"] for a in meta["assertions"] if a.get("tests_change")}
        kinds = {a["id"]: a["kind"] for a in meta["assertions"] if a["id"] not in excluded}
        negative = {a["id"] for a in meta["assertions"] if a["kind"] == "outcome" and a["text"].startswith("沒有")}
        for rd in sorted((RUNS / skill / case).glob("*/*/run-*")):
            if not (rd / "response.md").exists():
                continue
            arm, model = rd.parent.parent.name, rd.parent.name
            t = json.loads((rd / "timing.json").read_text(encoding="utf-8"))
            g = load_grading(rd, args.grader, args.final)
            row = {"skill": skill, "case": case, "arm": arm, "model": model, "run": rd.name,
                   "turns": t.get("num_turns"), "skill_calls": t.get("skill_calls"), "tokens": tokens(t),
                   "seconds": (t.get("duration_ms") or 0) / 1000, "models_used": t.get("models_used")}
            if g:
                def rate(kind):
                    ids = [i for i, k in kinds.items() if k == kind]
                    return sum(bool(g[i]["passed"]) for i in ids) / len(ids) if ids else None
                row["outcome"] = rate("outcome")
                row["procedure"] = rate("procedure")
                row["compliance_fail"] = [i for i, k in kinds.items() if k == "compliance" and not g[i]["passed"]]
                row["fp"] = sum(1 for i in negative if not g[i]["passed"])
                row["verdicts"] = {i: bool(v["passed"]) for i, v in g.items() if i in kinds}
                oids = [i for i, k in kinds.items() if k == "outcome" and i not in tc]
                row["outcome_no_tc"] = sum(row["verdicts"][i] for i in oids) / len(oids) if oids else None
            rows.append(row)

    # 逐題彙整
    by_cell = defaultdict(list)
    for r in rows:
        by_cell[(r["skill"], r["case"], r["model"], r["arm"])].append(r)
    cells = {}
    for key, rs in by_cell.items():
        graded = [r for r in rs if "outcome" in r]
        c = {"n": len(rs), "graded": len(graded),
             "outcome": mean([r["outcome"] for r in graded]),
             "outcome_no_tc": mean([r["outcome_no_tc"] for r in graded if r.get("outcome_no_tc") is not None]),
             "procedure": mean([r["procedure"] for r in graded if r["procedure"] is not None]),
             "fp": sum(r["fp"] for r in graded),
             "compliance_fail": sum(len(r["compliance_fail"]) for r in graded),
             "tokens": mean([r["tokens"] for r in rs]), "seconds": mean([r["seconds"] for r in rs]),
             "turns": [r["turns"] for r in rs], "skill_triggered": sum(1 for r in rs if r["skill_calls"])}
        # pass^k：outcome 斷言在所有 run 都通過的比例
        if graded:
            ids = [i for i in graded[0]["verdicts"]]
            meta = json.loads((CASES / key[0] / key[1] / "eval_metadata.json").read_text(encoding="utf-8"))
            oids = [a["id"] for a in meta["assertions"] if a["kind"] == "outcome" and a["id"] in graded[0]["verdicts"]]
            c["pass_all"] = mean([1.0 if all(r["verdicts"][i] for r in graded) else 0.0 for i in oids])
            c["per_assertion"] = {i: f'{sum(r["verdicts"][i] for r in graded)}/{len(graded)}' for i in ids}
        cells[key] = c

    # 技能層級
    summary = {}
    for (skill, case, model, arm), c in cells.items():
        s = summary.setdefault((skill, model, arm), {"cases": 0, "outcome": [], "outcome_no_tc": [], "procedure": [], "fp": 0, "tokens": [], "seconds": [], "pass_all": []})
        if c.get("outcome_no_tc") is not None:
            s["outcome_no_tc"].append(c["outcome_no_tc"])
        s["cases"] += 1
        if c["outcome"] is not None:
            s["outcome"].append(c["outcome"])
            s["pass_all"].append(c["pass_all"])
        if c["procedure"] is not None:
            s["procedure"].append(c["procedure"])
        s["fp"] += c["fp"]
        s["tokens"].append(c["tokens"])
        s["seconds"].append(c["seconds"])
    for s in summary.values():
        for k in ("outcome", "outcome_no_tc", "procedure", "tokens", "seconds", "pass_all"):
            s[k] = mean(s[k])

    out = {"grader": args.grader, "final": args.final,
           "cells": {"|".join(k): v for k, v in cells.items()},
           "summary": {"|".join(k): v for k, v in summary.items()}}
    (IT6 / "results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    L = [f"# iteration-6 結果（評分：{args.final or args.grader}）", ""]
    for skill in sorted({k[0] for k in summary}):
        L += [f"## {skill}", "", "| 模型 | 臂 | outcome | outcome（不含 tests_change） | pass^k | procedure | 假陽性 | tokens | 秒 |", "|---|---|---|---|---|---|---|---|---|"]
        for (sk, model, arm), s in sorted(summary.items()):
            if sk == skill:
                L.append(f"| {model} | {arm} | {s['outcome']} | {s['outcome_no_tc']} | {s['pass_all']} | {s['procedure']} | {s['fp']} | {s['tokens']} | {s['seconds']} |")
        L += ["", "| 案例 | 模型 | 臂 | n | outcome | pass^k | procedure | 假陽性 | 觸發 skill | turns | 逐條 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for (sk, case, model, arm), c in sorted(cells.items()):
            if sk == skill:
                pa = " ".join(f"{i}={v}" for i, v in c.get("per_assertion", {}).items())
                L.append(f"| {case} | {model} | {arm} | {c['n']} | {c['outcome']} | {c.get('pass_all')} | {c['procedure']} | {c['fp']} | {c['skill_triggered']}/{c['n']} | {c['turns']} | {pa} |")
        L.append("")

    # 觸發
    trig = json.loads((IT6 / "trigger_prompts.json").read_text(encoding="utf-8"))
    L += ["## 階段 0 觸發", "", "| id | 預期 | 模型 | 叫用的 skill |", "|---|---|---|---|"]
    for t in trig:
        for tf in sorted((RUNS / "trigger").glob(f"*/{t['id']}/timing.json")):
            tj = json.loads(tf.read_text(encoding="utf-8"))
            L.append(f"| {t['id']} | {'應觸發' if t['expect'] else '不應觸發'} | {tf.parent.parent.name} | {', '.join(tj['skill_calls']) or '無'} |")
    (IT6 / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:60]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
