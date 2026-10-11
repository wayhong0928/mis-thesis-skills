"""thesis-roadmap 觸發評測：每題看模型第一個 Skill 工具呼叫叫了哪個 skill。"""
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
PLUGIN = str(HERE.resolve().parents[1] / "plugins" / "thesis-toolkit")
P = "thesis-toolkit:"

CASES = [
    # 應觸發 thesis-roadmap
    ("r1", "thesis-roadmap", "我論文卡住了，不知道下一步要做什麼"),
    ("r2", "thesis-roadmap", "thesis-toolkit 這幾個工具要照什麼順序用？"),
    ("r3", "thesis-roadmap", "我不確定自己現在算在論文的哪個階段，該先做什麼？"),
    ("r4", "thesis-roadmap", "碩士論文從零到寫完大概要經過哪些步驟？我該從哪個 skill 開始用"),
    ("r5", "thesis-roadmap", "題目稽核過了，接下來要讀文獻設計問卷，這個階段有工具可以幫我嗎？"),
    # 不應觸發 thesis-roadmap，應觸發原本的 skill
    ("d1", "research-direction-finding", "我碩一下了，老師叫我自己想論文題目，但我完全不知道要做什麼，坐在電腦前面兩個禮拜了還是一片空白。可以幫我想一個題目嗎？"),
    ("d2", "research-direction-finding", "我想做 AI 相關的研究，但這個範圍太大了不知道怎麼縮小。"),
    ("q1", "research-question-audit", "我想研究生成式 AI 素養如何影響大學生在程式設計課程的學習績效，這個方向你覺得可以嗎？"),
    ("q2", "research-question-audit", "我想研究遠距工作對員工倦怠的影響，幫我看這個題目站不站得住"),
    ("w1", "academic-writing-discipline", "幫我看看這段話寫得好不好：『本研究之數據顯示，人工智能之使用行為對受試者之學習成效具有顯著之影響，因此可以得知兩者之間存在正向關係。』"),
    ("w2", "academic-writing-discipline", "我這句話會不會有『中間肥大』的問題：『由於近年來生成式AI技術的快速發展與普及，使得越來越多的大學生開始在課業與報告撰寫的過程中，對於這類工具的使用產生了高度的依賴性，因此本研究希望能夠深入探討這樣的依賴傾向究竟會對學生的學習成效造成什麼樣的影響。』"),
]
RUNS = [("sonnet", 1), ("sonnet", 2), ("opus", 1)]
# 在空資料夾執行，避免讀到 repo 的設定
WORK = HERE / "work"


def run(job):
    cid, expect, prompt, model, rep = job
    out = HERE / "raw" / f"{cid}_{model}_{rep}.jsonl"
    out.parent.mkdir(exist_ok=True)
    env = dict(os.environ, CLAUDE_CODE_DISABLE_CLAUDE_MDS="1")
    cmd = ["claude", "-p", prompt, "--model", model, "--setting-sources", "project,local",
           "--plugin-dir", PLUGIN, "--output-format", "stream-json", "--verbose", "--max-turns", "2"]
    with open(out, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                       cwd=WORK, env=env, timeout=600)
    first_skill, loaded, result_sub = None, False, None
    for line in open(out, encoding="utf-8"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "system" and d.get("subtype") == "init":
            loaded = any(p.get("version") == "0.5.0" for p in d.get("plugins", []))
        if d.get("type") == "assistant" and first_skill is None:
            for c in d["message"]["content"]:
                if c.get("type") == "tool_use" and c["name"] == "Skill":
                    first_skill = c["input"].get("skill")
                    break
        if d.get("type") == "result":
            result_sub = d.get("subtype")
    return dict(case=cid, expect=expect, model=model, rep=rep, first_skill=first_skill,
                ok=first_skill == P + expect, plugin_050=loaded, result=result_sub)


if __name__ == "__main__":
    WORK.mkdir(exist_ok=True)
    jobs = [(c, e, p, m, r) for c, e, p in CASES for m, r in RUNS]
    with ThreadPoolExecutor(max_workers=3) as ex:
        rows = list(ex.map(run, jobs))
    (HERE / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in rows:
        print(r["case"], r["model"], r["rep"], "OK " if r["ok"] else "XX ", r["first_skill"], r["result"], "" if r["plugin_050"] else "PLUGIN-NOT-LOADED")
