# -*- coding: utf-8 -*-
"""把 evals/iteration-4/ 底下每個 case 的 prompt 抽成獨立的 .txt。

為什麼要這一步：跑 eval 的 subagent 只能看到 prompt，不能看到同一份
eval_metadata.json 裡的 assertions——那是這次評測的正確答案，看了等於作弊。
與其靠 prompt 叮嚀「不要讀那個欄位」，不如讓它物理上拿不到。

用法（在 repo 根目錄）：
    PYTHONIOENCODING=utf-8 python3 evals/tools/extract_prompts.py [輸出目錄]
不給輸出目錄就寫到 evals/tools/_prompts/（已列入 .gitignore 考量，是暫存產物）。
"""
import io, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "iteration-4"
SCRATCH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "_prompts"
SCRATCH.mkdir(parents=True, exist_ok=True)

manifest = []
for skill_dir in sorted(ROOT.iterdir()):
    if not skill_dir.is_dir():
        continue
    for case_dir in sorted(skill_dir.iterdir()):
        md = case_dir / "eval_metadata.json"
        if not md.is_file():
            continue
        d = json.load(io.open(md, encoding="utf-8"))
        pf = SCRATCH / f"{skill_dir.name}__{case_dir.name}.txt"
        io.open(pf, "w", encoding="utf-8", newline="\n").write(d["prompt"])
        manifest.append({
            "skill": skill_dir.name,
            "case": case_dir.name,
            "prompt_file": str(pf),
            "prompt_chars": len(d["prompt"]),
            "assertions": len(d.get("assertions", [])),
        })

io.open(SCRATCH / "manifest.json", "w", encoding="utf-8", newline="\n").write(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

for m in manifest:
    print(f"{m['skill']:28} {m['case']:42} prompt {m['prompt_chars']:5} 字元  {m['assertions']} 條 assertion")
print("\nprompt 檔目錄:", SCRATCH)
