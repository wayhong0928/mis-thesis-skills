# iteration-5：乾淨重跑（2026-09-20）

`academic-writing-discipline`（AWD）與 `research-question-audit`（RQA）兩個 SKILL 的
8 個 test case × 2 臂 = 16 次執行，全部用同一套設定跑完。`research-direction-finding`
不在這一輪範圍，它的資料留在 `iteration-4/`。

## 為什麼要重跑

iteration-4 的 AWD 與 RQA 數字混了兩個變因，delta 無法解讀：

1. skill 版本不一致。2026-09-12 跑的既有 case，全域 plugin 快取還停在 09-08 版
   （`claude plugin update` 因版號沒變而誤報已是最新），用的是修正前的 skill；09-19
   補跑的 4 個 case 用的是修正後的版本。
2. 兩臂 CLI 設定不對稱。09-19 的 without_skill 加了 `--setting-sources project,local`
   擋掉 user 層 hook 注入，with_skill 與更早的既有 case 都沒加。

完整背景見 `../RERUN_SPEC_2026-09-20.md`。

## 這一輪的設定

兩臂唯一的差異是 `--plugin-dir`：

```
claude -p --model sonnet --output-format json   --setting-sources project,local   --allowedTools Skill,Read,Glob,Grep   --disallowedTools Bash,PowerShell,Write,Edit,NotebookEdit,Task,WebFetch,WebSearch   [--plugin-dir <repo>/plugins]        # 只有 with_skill 有
  < <case>.txt
```

cwd 設在 repo 外的空目錄，without_skill 因此看不到 repo 裡的 SKILL 檔案。iteration-4
的 without_skill 是改用 `--disallowedTools` 把包含 Read 在內的全部工具封死來達到同樣目的，
代價是兩臂的工具能力也跟著不一樣；改成隔離 cwd 之後，兩臂可以用同一組工具。

prompt 從 `eval_metadata.json` 抽成獨立 .txt 放在 repo 外，跑 eval 的行程拿不到同一份檔案裡的
assertions。這一步是本輪的執行腳本自己做的，不是用 `../tools/extract_prompts.py`——那支工具的來源
目錄寫死在 `iteration-4`，沒有參數可以指向別的 iteration。本輪的 `eval_metadata.json` 從
`iteration-4` 複製過來（兩邊逐位元組相同，含 2026-09-20 修正過的 RQA eval-1 a3），所以抽出的
prompt 內容與該工具會產生的相同；但日後兩邊的 metadata 若出現差異，那支工具就不能照字面拿來用。

`--plugin-dir` 這個載入方式先跑過三項小測才正式使用：

| 小測 | 做法 | 結果 |
|---|---|---|
| 能不能載到 | `--setting-sources project,local --plugin-dir <repo>/plugins` | 三個 skill 都出現在可用清單 |
| 對照組是否真的載不到 | 同上但拿掉 `--plugin-dir` | 回 `NONE`，確認 user 層安裝的 plugin 已被排除 |
| 載的是 repo 還是全域快取 | 在 repo 的 AWD `SKILL.md` 暫時插一行標記字串後實跑 | 回應第一行就是該標記 |

標記在小測後已還原。

## 結果

每個 case 各跑 1 次 with_skill、1 次 without_skill。`turns` 是該次執行的對話輪數，
1 代表模型沒有叫用任何工具。

### academic-writing-discipline

| case | with | without | delta | turns (w/wo) |
|---|---|---|---|---|
| eval-1-causal-verb-and-existence-abuse | 1.00 | 0.80 | +0.20 | 6/1 |
| eval-2-bloated-middle-sentence | 0.80 | 0.60 | +0.20 | 1/1 |
| eval-3a-clean-lit-review-false-positive | 0.60 | 0.60 | +0.00 | 3/1 |
| eval-3b-lit-review-argument-gap | 0.80 | 0.80 | +0.00 | 6/1 |
| 平均 | 0.80 | 0.70 | +0.10 | |

### research-question-audit

| case | with | without | delta | turns (w/wo) |
|---|---|---|---|---|
| eval-1-bad-title-no-dv | 1.00 | 0.75 | +0.25 | 3/1 |
| eval-2-too-many-dvs | 1.00 | 0.75 | +0.25 | 5/1 |
| eval-3-gai-dependency | 1.00 | 0.60 | +0.40 | 5/1 |
| eval-4-mature-thesis | 0.50 | 0.17 | +0.33 | 6/1 |
| 平均 | 0.88 | 0.57 | +0.31 | |

### 與 iteration-4 的混版數字對照

| skill | iteration-4（混版，已失效） | iteration-5（乾淨） |
|---|---|---|
| academic-writing-discipline | +0.00（0.90 / 0.90） | +0.10（0.80 / 0.70） |
| research-question-audit | +0.23（0.9375 / 0.704） | +0.31（0.875 / 0.567） |

`../RERUN_SPEC_2026-09-20.md` 的步驟 4 原本寫的是用 `--force` 覆蓋 `iteration-4`，本輪改成
新建 `iteration-5`，理由是規格的驗收條件同時要求「數字與舊版本並列比較」與「舊的混版數字要保留或
標註失效，由執行者判斷後明講採用了哪一種」，兩份並存比覆蓋後再從 git 歷史翻出來好對照。

iteration-4 的資料保留在 `../iteration-4/`，不覆蓋也不刪除，但 AWD 與 RQA 的部分不應再
被引用為當前效果的估計。iteration-4 裡 `research-direction-finding` 的 5 個 case 沒有混版
問題，仍然有效。

## 兩位評分者的一致率

`grading.json` 由兩個 sonnet agent 評出（AWD 與 RQA 各一個），拿得到 assertions。
另派一個 opus 盲評，它拿到的是一份只含 prompt、assertions、response 的資料包，
`grading.json` 物理上不在裡面。換模型加上換脈絡，是為了避免同模型同 prompt 的趨同。

78 條逐條比對，一致 75 條，一致率 96.2%。三條分歧全部落在盲評自己標 `confidence: low`
的條目上：

| case | 臂 | id | 評分者 | 盲評 |
|---|---|---|---|---|
| AWD eval-2-bloated-middle-sentence | without_skill | a1 | fail | pass |
| RQA eval-2-too-many-dvs | with_skill | a3 | pass | fail |
| RQA eval-4-mature-thesis | without_skill | a2 | fail | pass |

兩套評分算出來的 delta 都是正的，但大小對寬嚴標準敏感：

| skill | 評分者（sonnet） | 盲評（opus） |
|---|---|---|
| academic-writing-discipline | +0.10 | +0.05 |
| research-question-audit | +0.31 | +0.20 |

盲評對 26 條「回應抓到同一個實質問題但用詞或角度不同」的條目標了寬嚴爭議，逐條寫出兩種讀法
各自的結果，記錄在 `blind_verdicts.json`。

## 三個發現

### AWD eval-2 的 with_skill 沒有觸發 skill

該次執行 `num_turns=1`、約 29k tokens，與 without_skill 完全同一個量級。另外重跑兩次確認，
3 次都一樣，是穩定現象。那題的 prompt 是「我這句話會不會有『中間肥大』的問題」，使用者已經
自己講出 skill 內部術語、問題範圍很窄，模型判斷不叫 skill 也答得出來。

這筆資料原樣保留，沒有重跑到觸發為止再取代。它那 +0.20 的 delta 是兩次獨立執行之間的隨機
差異，不能算進 skill 效益。

### AWD 的效益集中在機械性判準

eval-1 是用詞規則（因果動詞、「存在」濫用、大陸用語），skill 有效，+0.20。eval-3a 與 3b
需要判斷論證鏈成不成立，skill 確實跑了（3 輪與 6 輪，讀了 references），兩臂卻同分。
扣掉沒觸發的 eval-2，skill 真的有跑的三個 case 平均 delta 是 +0.07。

所以 iteration-4 那個 +0.00 不是「題目太簡單」也不是「skill 整體沒效益」，而是三件不同的事
發生在不同 case 上：一個 case 有效、一個 case 沒觸發、兩個 case 在論證判斷上等於零。

### 兩個假陽性防呆案例的 assertion 可能與案例文本不符

AWD eval-3a 的 a5 與 RQA eval-4 的 a1／a4，兩臂都 fail，而且兩個模型是各自獨立提出同樣的
反對意見：

- RQA eval-4 的 prompt 原文同時列了「使用頻率」與「求助深度」兩個測量，兩臂都據此判依變數
  沒有收斂；prompt 也寫了「準實驗做不完就改單一時間點相關設計」，兩臂都指出單一時間點相關
  設計證明不了「降低」這個因果方向。
- AWD eval-3a 的兩臂都判該段文獻回顧需要大幅修改。

assertion 假定這些部分已經合格、不該被標記為問題，照字面判就是 fail。但兩臂獨立踩同一組
地雷，比較像是案例文本裡確實藏了真問題，而不是兩個模型同時虛構。這跟 `../RUBRIC.md` 第 7 節
記錄的 iteration-3 狀況是同一種。RQA eval-4 若判定那兩點不算違規，with_skill 會從 0.50
變成 0.83。

這兩個 case 的 assertion 還沒改，改之前的數字就是上面那張表。逐條覆核結果見`ASSERTION_AUDIT_2026-09-20.md`：三條爭議 assertion 全部是兩臂同時失敗，所以不論怎麼裁決都不影響 delta。

## 限制

- 每個 case 只跑 1 次 with_skill、1 次 without_skill，stddev 無法計算，不是穩定的統計量。
- 每個 skill 只有 4 個 case，delta 只能當作「這一輪、這幾個案例上觀察到的方向性差異」。
- 16 份回應對版權排除清單（彭明輝、舊瓶新酒、雁行理論等）零命中。8 份 without_skill 回應
  對 skill 名稱、`thesis-toolkit`、`SKILL.md` 也是零命中，iteration-4 有兩份點名了 repo 內
  skill 名稱，改成隔離 cwd 之後沒有再發生。

## 檔案

- `<skill>/<case>/{with_skill,without_skill}/outputs/response.md` — 模型回應
- `<skill>/<case>/{with_skill,without_skill}/grading.json` — 評分者的逐條判定
- `<skill>/<case>/{with_skill,without_skill}/timing.json` — token 與耗時
- `<skill>/<case>/{with_skill,without_skill}/cli_command.txt` — 該次執行的完整 CLI 參數
- `<skill>/<case>/{with_skill,without_skill}/raw_cli_output.json` — CLI 原始輸出，含 `num_turns`
- `<skill>/benchmark.json` — `../tools/aggregate_results.py` 彙整的結果
- `blind_verdicts.json` — 盲評的 78 條獨立判定與寬嚴爭議註記
- `academic-writing-discipline/eval-2-bloated-middle-sentence/trigger_probe/` — skill 未觸發的兩次重現測試佐證

`benchmark.json` 的 `metadata` 欄（評分與執行用的模型、時間戳）是彙整後補寫的，
`../tools/aggregate_results.py` 不會產生這些值；重跑那支工具會把它們清回 `null`。
