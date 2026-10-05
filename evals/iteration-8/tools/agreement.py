# -*- coding: utf-8 -*-
"""比對 sonnet 主評分與 opus 盲評的逐條一致率，列出分歧條目。輸出 ../agreement.json"""
import json, sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
IT6 = Path(__file__).resolve().parent.parent
RUNS = IT6 / "runs"
same = diff = 0
dis = []
by_kind = Counter(); by_kind_same = Counter()
for gs in sorted(RUNS.glob("**/grading_sonnet.json")):
    go = gs.parent / "grading_opus.json"
    if not go.exists():
        continue
    s = {v["id"]: v for v in json.loads(gs.read_text(encoding="utf-8"))["verdicts"]}
    o = {v["id"]: v for v in json.loads(go.read_text(encoding="utf-8"))["verdicts"]}
    for i in s:
        k = s[i].get("kind")
        by_kind[k] += 1
        if bool(s[i]["passed"]) == bool(o[i]["passed"]):
            same += 1; by_kind_same[k] += 1
        else:
            diff += 1
            dis.append({"run": str(gs.parent.relative_to(RUNS)).replace("\\", "/"), "id": i, "kind": k,
                        "sonnet": s[i]["passed"], "opus": o[i]["passed"],
                        "s_conf": s[i].get("confidence"), "o_conf": o[i].get("confidence"),
                        "s_ev": s[i]["evidence"][:120], "o_ev": o[i]["evidence"][:120], "o_note": o[i].get("note", "")[:200]})
print(f"compared {same+diff}, agree {same} ({same/(same+diff):.1%}), disagree {diff}")
for k in by_kind: print(k, f"{by_kind_same[k]}/{by_kind[k]}")
c = Counter((d["run"].split("/")[0][:3], d["run"].split("/")[1], d["id"]) for d in dis)
for k, n in c.most_common(): print(n, k)
(IT6 / "agreement.json").write_text(json.dumps(dis, ensure_ascii=False, indent=2), encoding="utf-8")
