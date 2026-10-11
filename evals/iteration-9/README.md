# iteration-9：thesis-roadmap 的觸發評測（2026-10-11）

## 問題

0.5.0 新增 `thesis-roadmap`。要確認兩件事：該叫用它的提問會叫用它，而它不會搶走原本三個 SKILL 的觸發。

這一輪只測觸發，不評輸出品質。

## 做法

- `run_trigger.py` 用 `claude -p --plugin-dir` 載入 repo 裡的 plugin，記錄模型第一個 Skill 工具呼叫叫了哪一個 SKILL。
- 參數：`--setting-sources project,local`（不載入使用者設定，所以已安裝的舊版 plugin 不會載入），`--max-turns 2`，在空資料夾執行，`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`。每次都確認 init 訊息載入的是 0.5.0。
- 11 題：5 題應叫用 `thesis-roadmap`（r1 到 r5）。6 題應叫用原本的 SKILL：d1、d2 是 research-direction-finding，q1、q2 是 research-question-audit，w1、w2 是 academic-writing-discipline。d1、d2、q1、w1、w2 取自既有的 `evals.json`，其中 q1 是 research-direction-finding 的邊界題（已經有研究想法，應該交給 research-question-audit）；r1 到 r5 與 q2 是這一輪新寫的。
- 每題 Sonnet 跑 2 次、Opus 跑 1 次，共 33 次。
- 環境是維護者的電腦，除了 thesis-toolkit 之外還載入了約 17 個其他 skill，會跟這四個 SKILL 競爭觸發。
- 原始輸出（`raw/`）含本機路徑和其他已安裝 skill 的名稱，沒有放進 repo。腳本在跑完之後只改了路徑寫法（改成相對於 repo），題目與參數沒變。

## 結果

| 輪次 | description | 正確 | 錯的 |
|---|---|---|---|
| 第一輪（`results_round1.json`） | 初版 | 31/33 | r5 在 Sonnet 2 次都沒叫用任何 SKILL |
| 第二輪（`results_round2.json`） | 補上「問某個階段有沒有工具可用」 | 33/33 | 無 |

r5 是「題目稽核過了，接下來要讀文獻設計問卷，這個階段有工具可以幫我嗎？」。第一輪 Sonnet 的回答內容沒錯，都說了 toolkit 不管讀文獻和問卷，但沒叫用 roadmap，所以沒有附 mis-thesis-guide 的對應頁面。初版 description 只寫了「不知道下一步」「不確定在哪個階段」「SKILL 該先用哪個」，沒有涵蓋這種問法。第二輪的 description 加上「或問某個階段（讀文獻、設計問卷、跑統計、準備口試）有沒有工具可用」和一個例句。

兩輪的 6 題反例都正確叫用原本的 SKILL：第一輪 18/18，第二輪 18/18。反例裡的 `error_max_turns` 是因為叫用 SKILL 之後還要讀 references，被 `--max-turns 2` 截斷，不影響「第一個叫用哪個 SKILL」的判定。

## 限制

- 題目由維護者設計，每題最多 3 次，只能說這 11 種問法在這個環境下的觸發方向，不是穩定的觸發率。
- 第二輪的 description 是看了第一輪 r5 的失敗才改的，r5 在第二輪通過，不能當成獨立驗證。
- 沒有測 Claude.ai 網頁版：網頁版的 `description` 上限 200 字元，這個 SKILL 的 description 比較長，上傳前要精簡。
