# -*- coding: utf-8 -*-
"""iteration-10 案例：用真實碩論段落植入已知錯誤，比較 grep 基線、沒裝 skill、0.5.2。

案例內容在 local/cases_def.py（含未發表論文段落，不進版控），本檔只負責寫出 eval_metadata.json。
cases/ 同樣不進版控。設計見 SPEC.md。
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "local"))
import cases_def as cd  # noqa: E402

OUT = HERE / "cases" / "academic-writing-discipline"
SK = "academic-writing-discipline"

for name, m in cd.CASES.items():
    d = OUT / name
    d.mkdir(parents=True, exist_ok=True)
    meta = {"skill": SK, "eval_name": name, "source": m["source"], "prompt": m["prompt"], "assertions": m["assertions"]}
    (d / "eval_metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(cd.CASES), "cases")
