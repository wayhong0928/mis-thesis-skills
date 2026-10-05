# -*- coding: utf-8 -*-
"""列出某案例某斷言在各 run 的判定與證據：python show.py <skill> <case> <aid> [arm] [grader]"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
RUNS = Path(__file__).resolve().parent.parent / "runs"
skill, case, aid = sys.argv[1:4]
arm = sys.argv[4] if len(sys.argv) > 4 else "*"
grader = sys.argv[5] if len(sys.argv) > 5 else "sonnet"
for g in sorted((RUNS / skill / case).glob(f"{arm}/*/run-*/grading_{grader}.json")):
    v = {x["id"]: x for x in json.loads(g.read_text(encoding="utf-8"))["verdicts"]}[aid]
    t = json.loads((g.parent / "timing.json").read_text(encoding="utf-8"))
    print(f"{g.parent.relative_to(RUNS / skill / case)} {v['passed']} [{v.get('confidence')}] skills={t['skill_calls']} | {v['evidence'][:150]} | {v.get('note','')[:200]}")
