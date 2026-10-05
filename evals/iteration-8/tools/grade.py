# -*- coding: utf-8 -*-
"""iteration-8 評分腳本（沿用 iteration-7）（同 iteration-6，只拿掉探查題）。

每份 response.md 交給一個不帶工具的 claude -p 評分，評分者只拿到 prompt、斷言、回應三樣，
不知道回應來自哪一臂、哪個模型。主評分用 sonnet，盲評用 opus，兩者各自獨立執行。

用法：
  python grade.py --grader sonnet [--glob "research-question-audit/*"]
  python grade.py --grader opus
結果寫在各 run 目錄的 grading_<grader>.json。已存在就跳過。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
IT6 = HERE.parent
RUNS = IT6 / "runs"
CASES = IT6 / "cases"
WORK = Path(os.environ["IT7_WORK"])
CWD = WORK / "workdir"
GP = WORK / "grade_prompts"

INSTR = """你是論文寫作評測的評分者。下面有一個使用者提問、一份 AI 回應、以及一組斷言。請逐條判定這份回應是否符合每一條斷言。

判定規則：
1. 二元判定，passed 只能是 true 或 false，不給部分分。
2. 每條都要附 evidence：從回應裡逐字摘出支持你判定的句子（60 字以內）。判 pass 卻找不到可摘的句子，就改判 fail。
3. 斷言寫「沒有……」「沒有把……判為……」的是假陽性檢查：回應裡找不到那種錯誤指控就判 pass，evidence 寫「回應未出現此指控」並簡述回應對該處的處理（若有提到）。
4. 斷言寫「至少其一」「例如」的，照字面：例子只是舉例，回應用不同說法講到同一件實質內容也算。
5. 只判斷言本身，不要因為回應的其他優缺點加分或扣分。
6. 另外給 confidence：high（判定明確）或 low（斷言本身可有兩種讀法，或回應處在邊界）。low 時在 note 寫出兩種讀法。

只輸出一個 JSON 陣列，不要有任何其他文字，格式：
[{"id": "a1", "passed": true, "evidence": "...", "confidence": "high", "note": ""}, ...]
"""


def packet(prompt, assertions, response):
    al = "\n".join(f'- {a["id"]}：{a["text"]}' for a in assertions)
    return f"{INSTR}\n=== 使用者提問 ===\n{prompt}\n\n=== AI 回應 ===\n{response}\n\n=== 斷言 ===\n{al}\n"


def extract_json(text):
    m = re.search(r"\[\s*\{.*\}\s*\]", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def grade_one(run_dir, meta, grader):
    out = run_dir / f"grading_{grader}.json"
    if out.exists():
        return run_dir, "skip"
    resp = (run_dir / "response.md").read_text(encoding="utf-8")
    scored = meta["assertions"]
    GP.mkdir(parents=True, exist_ok=True)
    pf = GP / (re.sub(r"[^A-Za-z0-9._-]", "_", str(run_dir.relative_to(RUNS))) + f"_{grader}.txt")
    pf.write_bytes(packet(meta["prompt"], scored, resp).encode("utf-8"))
    cmd = ["claude", "-p", "--model", grader, "--output-format", "json", "--setting-sources", "project,local",
           "--strict-mcp-config", "--tools", ""]
    env = dict(os.environ, CLAUDE_CODE_DISABLE_CLAUDE_MDS="1")
    for attempt in range(3):
        with open(pf, "rb") as fin:
            p = subprocess.run(cmd, stdin=fin, capture_output=True, cwd=CWD, env=env, timeout=900)
        try:
            res = json.loads(p.stdout.decode("utf-8", errors="replace"))
            verdicts = extract_json(res.get("result", ""))
        except json.JSONDecodeError:
            res, verdicts = {}, None
        ids = {a["id"] for a in scored}
        if verdicts and {v.get("id") for v in verdicts} >= ids:
            kinds = {a["id"]: a.get("kind", "outcome") for a in scored}
            for v in verdicts:
                v["kind"] = kinds.get(v["id"])
            out.write_text(json.dumps({"grader": grader, "models_used": sorted((res.get("modelUsage") or {}).keys()),
                                       "verdicts": verdicts}, ensure_ascii=False, indent=2), encoding="utf-8")
            return run_dir, "ok"
        time.sleep(10)
    (run_dir / f"grading_{grader}.error.txt").write_text(p.stdout.decode("utf-8", errors="replace")[-3000:], encoding="utf-8")
    return run_dir, "FAIL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grader", required=True)
    ap.add_argument("--glob", default="*")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    CWD.mkdir(parents=True, exist_ok=True)
    jobs = []
    for resp in sorted(RUNS.glob(f"{args.glob}/**/response.md")):
        rd = resp.parent
        rel = rd.relative_to(RUNS).parts
        meta = json.loads((CASES / rel[0] / rel[1] / "eval_metadata.json").read_text(encoding="utf-8"))
        jobs.append((rd, meta, args.grader))
    print(f"{len(jobs)} to grade with {args.grader}", flush=True)
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = [ex.submit(grade_one, *j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            rd, st = f.result()
            print(f"[{i}/{len(jobs)}] {rd.relative_to(RUNS)}: {st}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
