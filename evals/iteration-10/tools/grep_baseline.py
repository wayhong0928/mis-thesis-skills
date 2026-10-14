# -*- coding: utf-8 -*-
"""iteration-10 grep 基線：把 grep-checks.sh 的每組模式套在案例文字上。

從腳本讀出每組的標題與 grep -E 模式，用 Python re 逐組比對（模式只用到 ERE 與 re 共通的語法）。
植入處（cases_def.PLANT_SPANS 的定位字串）與某組的命中範圍重疊，就算 grep 抓到。
乾淨對照另外記錄「應為空」各組的命中，當作 grep 的誤報。結果寫到 local/grep_baseline.json（含原文，不公開），
終端只印彙整數字。

用法：python -X utf8 tools/grep_baseline.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IT = HERE.parent
REPO = IT.parent.parent
SCRIPT = REPO / "plugins" / "thesis-toolkit" / "skills" / "academic-writing-discipline" / "references" / "grep-checks.sh"
sys.path.insert(0, str(IT / "local"))
import cases_def as cd  # noqa: E402


def load_groups():
    groups, title = [], None
    for line in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = re.match(r'echo "--- (.+) ---"', line)
        if m:
            title = m.group(1)
            continue
        m = re.match(r"grep -[a-zA-Z]*E ([\"'])(.+)\1 \"\$FILE\"", line)
        if m and title:
            groups.append({"title": title, "pattern": m.group(2), "must_be_empty": "應為空" in title})
            title = None
    return groups


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    groups = load_groups()
    out = {"groups": len(groups), "planted": {}, "clean_hits": {}}
    caught = {"G": 0, "N": 0}
    total = {"G": 0, "N": 0}
    for case, spans in cd.PLANT_SPANS.items():
        text = cd.TEXTS[case]
        cls = {a["id"]: a["defect_class"] for a in cd.CASES[case]["assertions"]}
        for aid, span in spans.items():
            s = text.index(span)
            e = s + len(span)
            hits = [g["title"] for g in groups
                    if any(m.start() < e and m.end() > s for m in re.finditer(g["pattern"], text))]
            total[cls[aid]] += 1
            caught[cls[aid]] += bool(hits)
            out["planted"][f"{case}/{aid}"] = {"class": cls[aid], "caught": bool(hits), "groups": hits}
    for case in ("c1-litreview-clean", "c2-discussion-clean"):
        text = cd.TEXTS[case]
        out["clean_hits"][case] = {g["title"]: [m.group(0) for m in re.finditer(g["pattern"], text)]
                                   for g in groups if re.search(g["pattern"], text)}
    out["summary"] = {"caught": caught, "total": total}
    (IT / "local" / "grep_baseline.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"模式組數 {len(groups)}")
    for k, v in out["planted"].items():
        print(f"  {k} [{v['class']}] {'抓到' if v['caught'] else '沒抓到'}  {'；'.join(v['groups'])}")
    print(f"偵測：G {caught['G']}/{total['G']}，N {caught['N']}/{total['N']}，合計 {caught['G'] + caught['N']}/{total['G'] + total['N']}")
    for case, hits in out["clean_hits"].items():
        fp = sum(len(v) for t, v in hits.items() if "應為空" in t)
        hint = sum(len(v) for t, v in hits.items() if "應為空" not in t)
        print(f"  {case}：應為空組命中 {fp}，需人工判讀組命中 {hint}")


if __name__ == "__main__":
    main()
