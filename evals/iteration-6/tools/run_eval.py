# -*- coding: utf-8 -*-
"""iteration-6 執行腳本。

用法：
  python run_eval.py trigger --models sonnet,opus
  python run_eval.py main --models sonnet --trials 3 [--skills ...] [--cases ...] [--arms ...]
  python run_eval.py probe --models opus --trials 3

已有 response.md 的 run 會跳過，可以中斷後續跑。
設定見 ../SPEC.md 第七節。
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
IT6 = HERE.parent
CASES = IT6 / "cases"
RUNS = IT6 / "runs"

# 執行環境：repo 外的空目錄、兩個版本各一個 worktree、prompt 放 repo 外
WORK = Path(os.environ["IT6_WORK"])          # 例如 <scratchpad>
CWD = WORK / "workdir"
PROMPTS = WORK / "prompts"
WT = {"v0.3.0": WORK / "wt" / "v030", "v0.4.0c": WORK / "wt" / "v040c", "v0.4.0c2": WORK / "wt" / "v040c2", "v0.4.0rc": WORK / "wt" / "v040c2"}

# v0.4.0c2 是第 1 階段之後的第二輪修正（commit ca619ac）。v0.4.0-nochapter 是移除 chapter-structure.md 的版本（bf397d7），
# 回歸測試後撤回，資料只留紀錄。v0.4.0rc 是撤回後的最終版（3a3b856）。三者共用同一個 worktree，只在用 --arms 指定時才跑
ARMS_BY_SKILL = {
    "academic-writing-discipline": ["without_skill", "v0.3.0", "v0.4.0c2", "v0.4.0rc"],
    "research-direction-finding": ["without_skill", "v0.3.0", "v0.4.0c2"],
    "research-question-audit": ["without_skill", "v0.3.0", "v0.4.0c", "v0.4.0c2"],
}
TOOLS = "Skill,Read,Glob,Grep"


def build_cmd(model, arm):
    cmd = ["claude", "-p", "--model", model, "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project,local", "--strict-mcp-config",
           "--tools", TOOLS, "--allowedTools", TOOLS]
    if arm != "without_skill":
        cmd += ["--plugin-dir", str(WT[arm] / "plugins")]
    return cmd


def parse_stream(raw):
    result, init, tool_calls = None, None, []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "system" and d.get("subtype") == "init":
            init = d
        elif d.get("type") == "assistant":
            for c in d.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tool_calls.append({"name": c.get("name"), "input": c.get("input")})
        elif d.get("type") == "result":
            result = d
    return init, tool_calls, result


def run_one(prompt_file, outdir, model, arm, label):
    outdir.mkdir(parents=True, exist_ok=True)
    if (outdir / "response.md").exists():
        return label, "skip"
    cmd = build_cmd(model, arm)
    env = dict(os.environ, CLAUDE_CODE_DISABLE_CLAUDE_MDS="1")
    (outdir / "cli_command.txt").write_text(
        "CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 " + " ".join(cmd) + f"\n(stdin: {prompt_file.name}; cwd: {CWD})\n", encoding="utf-8")
    last_err = ""
    for attempt in range(2):
        t0 = time.time()
        with open(prompt_file, "rb") as fin:
            p = subprocess.run(cmd, stdin=fin, capture_output=True, cwd=CWD, env=env, timeout=1200)
        wall = time.time() - t0
        raw = p.stdout.decode("utf-8", errors="replace")
        init, calls, res = parse_stream(raw)
        limited = res and any(s in (res.get("result") or "") for s in ("hit your session limit", "usage limit", "rate limit"))
        if res and res.get("subtype") == "success" and res.get("result") and not limited:
            (outdir / "stream.jsonl").write_text(raw, encoding="utf-8")
            skills = [c["input"].get("skill") for c in calls if c["name"] == "Skill" and isinstance(c.get("input"), dict)]
            timing = {
                "model_requested": model,
                "models_used": sorted((res.get("modelUsage") or {}).keys()),
                "init_model": init.get("model") if init else None,
                "arm": arm,
                "num_turns": res.get("num_turns"),
                "duration_ms": res.get("duration_ms"),
                "wall_seconds": round(wall, 1),
                "total_cost_usd": res.get("total_cost_usd"),
                "usage": res.get("usage"),
                "skill_calls": skills,
                "tool_calls": [c["name"] for c in calls],
                "plugins": [pl.get("path") for pl in (init or {}).get("plugins", []) if pl.get("path") != "builtin"],
            }
            (outdir / "timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding="utf-8")
            (outdir / "response.md").write_text(res["result"], encoding="utf-8")
            return label, f"ok turns={res.get('num_turns')} skills={skills} {wall:.0f}s"
        last_err = (p.stderr.decode("utf-8", errors="replace")[-1500:] + "\n" + raw[-1500:])
        time.sleep(300 if limited else 20)
    (outdir / "error.txt").write_text(last_err, encoding="utf-8")
    return label, "FAIL"


def write_prompt(key, text):
    PROMPTS.mkdir(parents=True, exist_ok=True)
    f = PROMPTS / f"{key}.txt"
    f.write_bytes(text.encode("utf-8"))
    return f


def jobs_main(args):
    jobs = []
    for meta_file in sorted(CASES.glob("*/*/eval_metadata.json")):
        skill, case = meta_file.parent.parent.name, meta_file.parent.name
        if args.skills and skill not in args.skills:
            continue
        if args.cases and case not in args.cases:
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        pf = write_prompt(f"{skill}__{case}", meta["prompt"])
        for arm in ARMS_BY_SKILL[skill]:
            if args.arms and arm not in args.arms:
                continue
            if not args.arms and arm in ("v0.4.0c2", "v0.4.0rc"):
                continue
            for model in args.models:
                for n in range(1, args.trials + 1):
                    od = RUNS / skill / case / arm / model / f"run-{n}"
                    jobs.append((pf, od, model, arm, f"{skill[:3]}/{case}/{arm}/{model}/{n}"))
    return jobs


def jobs_trigger(args):
    jobs = []
    for t in json.loads((IT6 / "trigger_prompts.json").read_text(encoding="utf-8")):
        pf = write_prompt("trigger__" + t["id"], t["prompt"])
        for model in args.models:
            od = RUNS / "trigger" / model / t["id"]
            jobs.append((pf, od, model, "v0.3.0", f"trigger/{model}/{t['id']}"))
    return jobs


def jobs_probe(args):
    # AWD 探查：iteration-5 的 eval-3a 乾淨文獻回顧，只丟給沒裝 skill 的一臂
    src = IT6.parent / "iteration-5" / "academic-writing-discipline" / "eval-3a-clean-lit-review-false-positive" / "eval_metadata.json"
    meta = json.loads(src.read_text(encoding="utf-8"))
    pf = write_prompt("probe__eval-3a", meta["prompt"])
    return [(pf, RUNS / "probe-eval-3a" / "without_skill" / m / f"run-{n}", m, "without_skill", f"probe/{m}/{n}")
            for m in args.models for n in range(1, args.trials + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["main", "trigger", "probe"])
    ap.add_argument("--models", default="sonnet")
    ap.add_argument("--trials", type=int, default=1)
    ap.add_argument("--skills", default="")
    ap.add_argument("--cases", default="")
    ap.add_argument("--arms", default="")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    for k in ("models", "skills", "cases", "arms"):
        v = getattr(args, k)
        setattr(args, k, [x for x in v.split(",") if x])
    CWD.mkdir(parents=True, exist_ok=True)
    jobs = {"main": jobs_main, "trigger": jobs_trigger, "probe": jobs_probe}[args.phase](args)
    print(f"{len(jobs)} jobs", flush=True)
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = [ex.submit(run_one, *j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            label, status = f.result()
            print(f"[{i}/{len(jobs)}] {label}: {status}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
