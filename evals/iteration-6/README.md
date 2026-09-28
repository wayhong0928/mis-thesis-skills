# iteration-6：v0.3.0 與 v0.4.0 候選版（2026-09-28）

三個 SKILL、18 個案例，Sonnet 5 與 Opus 5.5 兩個模型，總共 300 次執行（含階段 0 的 36 次，不含評分）。規格與執行時的調整見 `SPEC.md`，第十二節記錄了跑之前小測發現、因此改掉的設定。

## 結論

1. **三個 SKILL 在兩個模型上都有明顯效益。** 最終版（下表 v0.4.0）的 outcome 斷言通過率比沒裝高 0.20 到 0.43。Opus 5.5 沒裝 SKILL 也答得不差，但差距沒有縮到可以忽略的程度（決策規則 4 的門檻是 +0.05）。
2. **發布的是第二輪候選版，不是原本的候選版。** 原本的候選版（只改 R1、R2）在 Opus 上勝過 v0.3.0，在 Sonnet 上卻低一點（0.931 對 0.958），不符合決策規則 1。落差來自 RQA 的 `question-forms.md` 裡兩節規則互相矛盾（R3），兩版都有這個矛盾。第二輪候選版修掉它，另外依第 1 階段讀到的失敗補了幾處，在兩個模型上都不低於 v0.3.0，假陽性為 0。
3. **有一項預先定好的刪減被測試推翻。** 規則 5 說：n5 沒有差距就移除 `chapter-structure.md`。n5 確實沒有差距（沒裝的模型本來就抓得到），但移除後重跑，Sonnet 三次都沒抓到緒論缺研究缺口，回應寫「不在本次檢查內」。SKILL 的範圍一縮小，模型就把範圍外的問題略過，結果比沒裝還差。依規則 2 撤回移除。
4. **觸發沒有問題。** 階段 0 的 36 句全部正確：24 句應觸發的都叫用了對應的 SKILL，12 句不應觸發的都沒有誤觸發，其中一句稽核需求被正確導到 research-question-audit。iteration-5 那種「使用者用了 SKILL 術語、問題很窄就不觸發」的情況沒有再出現。

## 主要數字

評分：Sonnet 主評分，與 Opus 盲評判定不同的 outcome 斷言由另一個 Opus 讀原文裁決（31 條）。主要數字只算 `outcome` 斷言；`procedure`（有沒有照 SKILL 流程走）另列，`compliance`（版權排除清單）全部通過，不列入。

Sonnet 每題 3 次，Opus 每題 1 次。

| SKILL | 模型 | 沒裝 | v0.3.0 | v0.4.0 | v0.4.0 − 沒裝 | 案例數 |
|---|---|---|---|---|---|---|
| academic-writing-discipline | Sonnet | 0.708 | 0.952 | 0.988 | +0.28 | 7 |
| | Opus | 0.768 | 0.964 | 0.964 | +0.20 | 7 |
| research-question-audit | Sonnet | 0.669 | 0.958 | 1.000 | +0.33 | 6 |
| | Opus | 0.733 | 0.925 | 1.000 | +0.27 | 6 |
| research-direction-finding | Sonnet | 0.545 | 0.933 | 0.978 | +0.43 | 5 |
| | Opus | 0.647 | 1.000 | 1.000 | +0.35 | 5 |

表中的 v0.4.0 是 `v0.4.0c2` 這一臂的數字。最終發布版與它只差 academic-writing-discipline 的 SKILL.md 一行說明文字（`chapter-structure.md` 的評測狀態），最終版另外重跑了 n5（Sonnet 3 次、Opus 1 次）與 n1（Sonnet 1 次），結果與 `v0.4.0c2` 相同。

research-question-audit 另有原本的候選版（R1、R2）：Sonnet 0.931、Opus 1.000。有 3 條斷言標了 `tests_change`，專門測 R1、R3 要修的已知落差，舊版照自己文件字面走一定會錯。扣掉這 3 條，RQA 的 v0.3.0 在兩個模型上都是 1.000，沒裝的是 0.556 與 0.625。所以 v0.3.0 在 RQA 上輸給候選版的部分，全部落在這兩個已知落差上。

**一致性（pass^k）**：Sonnet 每題 3 次裡，outcome 斷言三次都通過的比例。v0.4.0 在 AWD、RQA、RDF 分別是 0.964、1.000、0.933；v0.3.0 是 0.893、0.875、0.933；沒裝的是 0.661、0.614、0.467。

**假陽性**：負向斷言（「沒有把合格的地方判成錯」）的失敗次數。Sonnet 上，沒裝的 AWD 有 4 次，v0.3.0 的 RQA 有 2 次，原候選版的 RQA 有 3 次，v0.4.0 三個 SKILL 都是 0。

**成本**：裝 SKILL 的執行平均 4 到 9 萬 tokens（多數是快取讀取），沒裝的約 1 到 2 萬；耗時約為沒裝的 1.4 到 4.6 倍，RQA 最慢，Sonnet 平均約 100 秒。

完整逐題、逐條數字在 `results.md`，由 `tools/aggregate.py --final final` 產生。

## 各 SKILL 看到什麼

### academic-writing-discipline

- 效益集中在在地規則與假陽性。沒裝 SKILL 時，Sonnet 在 n2（已經改好的段落）3 次都挑出不存在的錯誤，在 n3 三次都把三條件齊備的「具有顯著正向影響」判成因果越線，n4 的大陸統計術語（判別效度、模型擬合）三次都沒抓到。裝了之後這些題全對。
- v0.3.0 的失誤：21 次執行有 2 次只叫用 SKILL、沒讀 references，其中一次漏掉「人工智能」與「存在」濫用，整合修改版還把「人工智能」原樣留著。v0.4.0 在 SKILL.md 加了一份必掃清單，規定先讀 references，整合修改版寫完再掃一次。
- 沒裝 SKILL 的 Sonnet 回應，28 份裡有 5 份混了簡體字（例如「从」「据」「数」「实」「确」）；裝了 SKILL 的 0 份。
- 探查題：iteration-5 的乾淨文獻回顧丟給沒裝 SKILL 的 Opus 跑 3 次，3 次都自己抓到因應分類的前後矛盾，也提出「AI 在前文是壓力源、在後文變成因應資源」這種有實質內容的論證批評。論證鏈檢查不需要加回來。

### research-question-audit

- R1（戰線過長改判斷題）有效：v0.3.0 在 Opus 上兩題都照字面把「一個構念的兩個指標」判成戰線過長，Sonnet 上 n1 的 3 次有 1 次；候選版沒有再判成命中（原候選版有一次標成「不確定」，見下面 R2）。
- R3（是非問句紅線看方向）有效：沒修之前，「X 是否正向預測 Y」會被判成是非問句，兩版都有；修了之後 Sonnet 3 次都放行，沒方向的「是否影響」仍然抓到。
- R2（加「不確定」選項）有副作用的跡象：原候選版有一次把戰線過長標成「判定為不確定，需你澄清」，被裁決為不通過。v0.4.0 沒有再發生，但樣本少，要繼續觀察。

### research-direction-finding

- 效益最大的一個 SKILL。沒裝的模型在「題目來自老師的計畫」（eval-3）與「資訊不足」（eval-5）兩題幾乎全錯：繼續追問，或直接給題目。
- v0.3.0 在起點 A（完全空白）時會先問三到五個背景問題、承諾「回答完再開始」，3 次都沒給能做的起步動作。v0.4.0 改成第一個回應就給作業。
- 檢索範本原本只寫頁名，模型從來沒提過；v0.4.0 附上網址後 Sonnet 3 次都提了。
- 唯一比 v0.3.0 少的一條：eval-2（「想做 AI 但範圍太大」）的 a2，v0.4.0 在 Sonnet 上 3 次有 1 次問「AI 要落在哪個學術子領域」，被判成重新問領域（兩位評分者都標低信心）。v0.3.0 是 3/3。
- eval-2 的 a4（第一個回應就產出進度筆記）各版都是 0。v0.4.0 把 SKILL 改成「從使用者第一次回答開始記」，這條 procedure 斷言因此跟 SKILL 的新寫法不一致，下一輪要改。

## 評分的可信度

- Sonnet 主評分與 Opus 盲評逐條比對 1,390 條，一致 1,340 條（96.4%）。outcome 斷言的 30 條分歧另派一個 Opus 讀原文裁決，逐字證據全部回查過原文；12 條是評分者看漏，18 條是斷言本身可以兩種讀法。另 1 條（回歸測試新增）由主對話裁決。
- 剔除 2 條斷言，理由寫在 `excluded_assertions.json`：AWD eval-2 的 a5 要求抓出緒論背景句的「使得」，超出 SKILL 規則的範圍，所有臂都失敗；RDF eval-4 的 a5 是 procedure，但模型直接改叫 research-question-audit，這條失去意義。
- 案例與斷言在跑之前由 fresh-context 的審查者看過一次，96 條裡提出 6 條問題，都已處理。

## 限制

- Opus 每題只跑 1 次。Opus 那一欄的差距是方向性觀察。
- 案例都由同一位維護者設計，負向案例也可能藏著出題者沒注意到的真問題：n2（乾淨段落）裡有一句「給予……較高的評價」，正好落在 SKILL 的弱動詞規則裡，被一次回應抓到。下一輪要改寫。
- RQA 與 RDF 補的「用台灣繁體中文回應」看不出效果：v0.3.0 與 v0.4.0 都是 44 份回應裡有 3 份混了簡體字（沒裝的是 1 份）。留著是因為沒有成本，不是因為有數據支持。
- 裁決者建議改寫 11 條斷言的措辭（見 `adjudications.json` 裡 cause 為 assertion_ambiguous 的條目），本輪沒有改，改了會讓已經評完的數字失去對照。下一輪套用。
- RDF eval-2 的多輪對話選做題沒有做。

## iteration-5 的 without_skill 很可能讀到了維護者的全域設定

小測發現，`--setting-sources project,local` 擋掉的是 settings 與 hook，擋不掉使用者層的 CLAUDE.md 與 `rules/`。維護者本機的全域守則裡有因果動詞、APA 之類的寫作提示。iteration-5 的沒裝那一臂每次輸入約 27.7k tokens，本輪同樣的設定加上 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` 之後約 15k，差距跟全域守則的大小相符。這是從 token 數推論，沒有直接證據，但 iteration-5 的數字應該當作「沒裝的一臂可能拿到了額外提示」來讀。

## 檔案

- `SPEC.md`：規格與執行時的調整
- `build_cases.py` → `cases/<skill>/<case>/eval_metadata.json`、`trigger_prompts.json`
- `tools/run_eval.py`（執行）、`tools/grade.py`（評分）、`tools/agreement.py`（評分者一致率）、`tools/build_final.py`（套用裁決）、`tools/aggregate.py`（彙整）、`tools/show.py`（查單條斷言）
- `runs/<skill>/<case>/<臂>/<模型>/run-N/`：`response.md`、`timing.json`（tokens、耗時、叫用了哪些工具與 SKILL）、`cli_command.txt`、`grading_sonnet.json`、`grading_opus.json`、`grading_final.json`。原始的 `stream.jsonl` 約 20MB，沒有進版控。
- `runs/trigger/`：階段 0；`runs/probe-eval-3a/`：探查題
- 臂的名稱：`without_skill`、`v0.3.0`（87a599b）、`v0.4.0c`（原候選版，8611e4c）、`v0.4.0c2`（第二輪候選版，ca619ac，與最終版只差 SKILL.md 一行說明）、`v0.4.0-nochapter`（移除 chapter-structure.md 的版本，已撤回，資料留作紀錄）、`v0.4.0rc`（最終版，只重跑了 n5 與 n1）
- `adjudications.json`、`excluded_assertions.json`、`agreement.json`、`results.json`、`results.md`
