# 乾淨重跑規格（2026-09-20 擬定，待 tkit session 執行）

## 這份規格要解決什麼

`academic-writing-discipline`（AWD）與 `research-question-audit`（RQA）在 iteration-4 的
benchmark 數字目前不可解讀，原因是同一組數字裡混了兩個變因：

1. **skill 版本不一致**。2026-09-12 跑的既有 case，當時全域 plugin 快取還停在 09-08 版
   （`claude plugin update` 因版號沒變而誤報已是最新），用的是修正前的 skill；09-19 補跑的
   4 個 case 用的是修正後的 `7f59510`。
2. **兩臂 CLI 設定不對稱**。09-19 的 without_skill 加了 `--setting-sources project,local`
   以擋掉 user 層 hook 注入，with_skill 與更早的既有 case 都沒加。

所以 AWD 的 delta +0.00 無法判斷是「skill 沒有效益」還是「題目太簡單，沒有 skill 也答得出來」。
重跑的目的就是讓這個數字能回答那個問題。

## 範圍

8 個 case × 2 臂 = 16 次執行，全部用同一套設定：

| skill | case |
|---|---|
| academic-writing-discipline | eval-1-causal-verb-and-existence-abuse、eval-2-bloated-middle-sentence、eval-3a-clean-lit-review-false-positive、eval-3b-lit-review-argument-gap |
| research-question-audit | eval-1-bad-title-no-dv、eval-2-too-many-dvs、eval-3-gai-dependency、eval-4-mature-thesis |

`research-direction-finding` 的 5 個 case 不在這次範圍內（09-12 首次評測，沒有混版問題）。

## 執行前必做的兩件事

### 1. 確認 skill 版本

比對 `C:\Users\user\.claude\plugins\installed_plugins.json` 裡 `thesis-toolkit` 的
`gitCommitSha` 與 repo HEAD。

**已於 2026-09-20 查證**：快取停在 `7f59510`，repo HEAD 是 `82160b9`，但 `git diff --name-only
7f59510..HEAD -- plugins/` 為空，也就是這個落差只影響 `evals/` 資料，skill 本體兩者相同。
執行前重新確認一次即可；若期間 `plugins/` 有新 commit，要先 `claude plugin update` 並再次比對
sha，不要只看它回報「已是最新」（版號沒變時會誤報）。

### 2. 小測 with_skill 的載入方式（這是唯一沒解決的技術問題）

without_skill 用 `--setting-sources project,local` 排除 user 層設定，是為了擋掉 user 層 hook
注入干擾輸出。問題是這個參數**同時會讓 user 層安裝的 plugin 載不到**，所以 with_skill 不能
照抄，否則兩臂都變成沒有 skill。

候選做法是 with_skill 也用 `--setting-sources project,local`，另外加 `--plugin-dir` 指向
repo 內的 `plugins/`，讓 skill 從 repo 直接載入。**這個做法尚未驗證**，正式重跑前先跑一次
小測確認：

- 用 `--setting-sources project,local --plugin-dir <repo>/plugins` 起一次對話，
  確認 `thesis-toolkit` 的三個 skill 真的出現在可用清單裡，而且叫用得起來。
- 確認載入的是 repo 內容而非全域快取（改一個字串當標記，或比對 skill 輸出的特徵）。

小測不通過就停下來回報，不要用「兩臂設定不同」的方式硬跑完，那會重蹈這次要修的錯。

## 執行步驟

1. `PYTHONIOENCODING=utf-8 python3 evals/tools/extract_prompts.py <暫存目錄>`
   把每個 case 的 prompt 抽成獨立 .txt。這一步的用意是讓執行 eval 的 subagent 物理上拿不到
   同一份 `eval_metadata.json` 裡的 assertions（那是正確答案）。暫存目錄放 repo 外。
2. 對 8 個 case 各跑 with_skill 與 without_skill 兩臂，兩臂除了 skill 載入方式之外，
   其餘參數、模型、effort 全部相同。每次執行產出 `outputs/response.md` 與 `timing.json`，
   照 iteration-4 既有目錄結構存放。
3. 評分產生 `grading.json`。評分者**不可以是產出該回應的同一個 agent**，且要拿得到 assertions。
4. `python3 evals/tools/aggregate_results.py evals/iteration-4/<skill目錄> [--force]`
   彙整成 `benchmark.json`。
5. 評分完成後，另派 fresh-context verifier 重評一次，比對判定是否一致（09-19 那次是 36 條全一致，
   可當基準）。

## 注意事項

- RQA eval-1 的 a3 assertion 已於 2026-09-20 修正（commit `014bd53`），重跑時用的是新版本。
  舊的 eval-1 評分結果已失效，不要拿來比較。
- 本 repo 是公開發布的 plugin，**不要在 repo 裡新建 `TODO.md`**（會被推上公開 repo）。
  跨 session 待辦記在 `D:\github-repo\Obsidian Vault\日常對話\TODO.md`。
- 16 次執行是這批工作裡最大的額度支出，跑之前先確認額度夠，不要跑到一半斷掉留下半套資料。

## 驗收條件

- [ ] 16 次執行全部完成，每個 case 的兩臂都有 `grading.json` 與 `timing.json`
- [ ] 抽驗 3 次執行的紀錄，確認兩臂的 CLI 參數除 skill 載入方式外完全相同（貼出實際參數）
- [ ] AWD 與 RQA 各產出一份新的 `benchmark.json`，數字與舊版本並列比較
- [ ] fresh-context verifier 重評結果與原評分的一致率有紀錄
- [ ] 依新數字回答：AWD 的 delta 是題目太簡單，還是 skill 沒有效益？結論寫進 README 的「評測」段落
- [ ] 舊的混版數字要保留或標註失效，由執行者判斷後明講採用了哪一種

## 完成後

回頭更新 `D:\github-repo\Obsidian Vault\日常對話\TODO.md` 的該項，並把 commit `014bd53`
（a3 修正）連同新結果一起 push。
