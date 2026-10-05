# -*- coding: utf-8 -*-
"""iteration-7 執行腳本（從 iteration-6 的 run_eval.py 精簡而來，只留主測）。

用法：
  python run_eval.py --models sonnet --trials 3 [--cases ...] [--arms ...]

已有 response.md 的 run 會跳過，可以中斷後續跑。
執行設定同 ../../iteration-6/SPEC.md 第十二節：隔離 cwd、--setting-sources project,local、
CLAUDE_CODE_DISABLE_CLAUDE_MDS=1、--tools 白名單加 --strict-mcp-config、stream-json 加 --verbose。
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
IT = HERE.parent
CASES = IT / "cases"
RUNS = IT / "runs"

# 執行環境：repo 外的空目錄、兩個版本各一個 worktree、prompt 放 repo 外
WORK = Path(os.environ["IT7_WORK"])
CWD = WORK / "workdir"
PROMPTS = WORK / "prompts"
WT = {"v0.4.0": WORK / "wt" / "v040", "v0.4.2": WORK / "wt" / "v042", "v0.4.3": WORK / "wt" / "v043"}
ARMS = ["without_skill", "v0.4.0", "v0.4.2", "v0.4.3"]
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
                "read_files": [str((c.get("input") or {}).get("file_path", "")).replace("\\", "/").split("/")[-1]
                               for c in calls if c["name"] == "Read"],
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
        if args.cases and case not in args.cases:
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        pf = write_prompt(f"{skill}__{case}", meta["prompt"])
        for arm in ARMS:
            if args.arms and arm not in args.arms:
                continue
            for model in args.models:
                for n in range(1, args.trials + 1):
                    od = RUNS / skill / case / arm / model / f"run-{n}"
                    jobs.append((pf, od, model, arm, f"{case}/{arm}/{model}/{n}"))
    return jobs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="sonnet")
    ap.add_argument("--trials", type=int, default=1)
    ap.add_argument("--cases", default="")
    ap.add_argument("--arms", default="")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()
    for k in ("models", "cases", "arms"):
        v = getattr(args, k)
        setattr(args, k, [x for x in v.split(",") if x])
    CWD.mkdir(parents=True, exist_ok=True)
    jobs = jobs_main(args)
    print(f"{len(jobs)} jobs", flush=True)
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = [ex.submit(run_one, *j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            label, status = f.result()
            print(f"[{i}/{len(jobs)}] {label}: {status}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
