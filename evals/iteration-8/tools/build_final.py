# -*- coding: utf-8 -*-
"""以 sonnet 主評分為底，套用 ../adjudications.json 的裁決，寫出每個 run 的 grading_final.json。"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
IT6 = Path(__file__).resolve().parent.parent
RUNS = IT6 / "runs"
adj = {(a["run"].replace("\\", "/"), a["id"]): a for a in json.loads((IT6 / "adjudications.json").read_text(encoding="utf-8"))}
used = 0
for gs in RUNS.glob("**/grading_sonnet.json"):
    run = str(gs.parent.relative_to(RUNS)).replace("\\", "/")
    g = json.loads(gs.read_text(encoding="utf-8"))
    for v in g["verdicts"]:
        a = adj.get((run, v["id"]))
        if a:
            v["passed"] = bool(a["final"]); v["evidence"] = a["evidence"]; v["adjudicated"] = a.get("cause"); used += 1
    g["grader"] = "final (sonnet + adjudications)"
    (gs.parent / "grading_final.json").write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
print("adjudications applied:", used, "of", len(adj))
