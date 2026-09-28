---
created: 2026-09-28
tags: [mis-thesis-skills, thesis-toolkit, eval, 計畫]
---

# iteration-6 測試規格：thesis-toolkit v0.3.0 與改版候選

> 時間軸：2026-09-28 16:50 建立（本日第 3 份）。
> 接在一份內容調整評估（10 條提案）後面。09-28 維護者只收 R1、R2，已改在分支 `v0.4-candidate`（commit `8611e4c`，本機，未 push），其餘提案暫不收。所以候選版只有 RQA 跟 v0.3.0 不同，AWD、RDF 兩版完全一樣。
> 模型只測 Sonnet 與 Opus。
> 這份只是規格，還沒跑。執行時複製到 `mis-thesis-skills\evals\iteration-6\SPEC.md`（內容不含個人資訊，可以進公開 repo）。

## 一、要回答的三個問題

1. v0.3.0 在現在的模型上還有沒有效益？iteration-5 量的是 v0.2.0，執行模型是 sonnet。
2. 改版候選（暫稱 v0.4.0）有沒有比 v0.3.0 好，至少不能變差？
3. 效益會不會因模型而異？同學可能用 Sonnet，也可能用 Opus，兩個都要量。

## 二、設計原則（取自 Anthropic〈Demystifying evals for AI agents〉，逐字比對過原文）

- 每題跑多次：「Because model outputs vary between runs, we run multiple trials to produce more consistent results.」iteration-5 每題只跑 1 次，這輪每題至少 3 次。
- 評產出，不評路徑：「it's often better to grade what the agent produced, not the path」。斷言分成兩類並分開計分，見第四節。
- 正反案例都要有：「Test both the cases where a behavior should occur and where it shouldn't. One-sided evals create one-sided optimization.」每個 skill 至少一題「文字或題目本來就合格，不該被挑毛病」。
- 斷言要讓兩個專家獨立判得一樣：「A good task is one where two domain experts would independently reach the same pass/fail verdict.」寫不到這個程度的斷言不收。
- 讀逐字紀錄：「You won't know if your graders are working well unless you read the transcripts」。每一條失敗的斷言都要回去看回應原文，判斷是模型錯還是斷言錯。
- 注意飽和：Opus 5.5 沒裝 skill 可能已經接近滿分，那時 delta 小不代表 skill 沒用，要看在地規則類的斷言。

## 三、實驗矩陣

**三個臂**：沒裝 skill／v0.3.0（commit `87a599b`）／v0.4.0 候選（分支 `v0.4-candidate`，commit `8611e4c`）。兩個版本各用一個 `git worktree`，`--plugin-dir` 指向各自的 `plugins\`，避免跑到一半切分支。AWD、RDF 的候選版與 v0.3.0 一模一樣，這兩個 skill 只跑「沒裝」與「v0.3.0」兩臂。

**兩個模型**：`--model sonnet`、`--model opus`。每次執行都要從原始輸出確認實際用到的模型 id，寫進 `timing.json` 旁邊。

**分三個階段**，前一段有問題就停，不要一路跑完：

| 階段 | 內容 | 臂 × 模型 × 次數 | 大約次數 |
|---|---|---|---|
| 0 觸發 | 每個 skill 4 句應觸發、2 句不應觸發（例如英文段落、跟論文無關的中文問題），只看有沒有呼叫 Skill 工具。description 兩版相同，只跑 v0.3.0 | v0.3.0 × 兩模型 × 1 | 36 |
| 1 主測 | 第五節全部案例 | RQA 三臂、AWD 與 RDF 兩臂 × sonnet × 3 | 126 |
| 2 對照 | 同一批案例 | 同上 × opus × 1（有疑問的題再補到 3 次） | 42 |

算法：階段 1 是 RQA 6 題 × 3 臂 × 3 次＝54，AWD 7 題 × 2 臂 × 3 次＝42，RDF 5 題 × 2 臂 × 3 次＝30；階段 2 是 18＋14＋10。另加第五節的 AWD 探查題 3 次。

成本粗估：iteration-5 每次執行平均約 3 萬到 10 萬 tokens（多數是快取讀取），平均 20 到 60 秒，個別執行會超出這個範圍。階段 1 依序跑約 1.5 到 2 小時。一次跑完會吃掉當天不少用量。

## 四、斷言規則

沿用 `evals\RUBRIC.md`（每條要有 `based_on`；分類類斷言要引用 reference 章節），另外加兩條：

1. 每條斷言標 `kind`：
   - `outcome`：使用者實際拿到的東西對不對。例如「有指出『存在正向關係』可改成『顯著正相關』」「沒有把合格的依變數判成不通過」。
   - `procedure`：有沒有照 skill 的流程走。例如「有用五種缺口的名稱分類」「結尾有逐項引導的邀請句」。沒裝 skill 的那一臂本來就不可能知道這些流程，這類斷言只拿來看 skill 有沒有被正確執行，不算進效益。
2. 報告的主要數字只用 `outcome` 斷言算。`procedure` 另外列一欄。

RDF eval-4 的斷言照這個原則改成 outcome：「使用者拿到了針對既有題目的稽核，而不是被帶回去重新找方向」。有沒有寫出「交棒」兩字不再計分。

## 五、案例

### academic-writing-discipline（7 題）

| 案例 | 來源 | 測什麼 | 對應提案 |
|---|---|---|---|
| eval-1 因果動詞與「存在」濫用 | 沿用 | 用詞規則 | 基準 |
| eval-2 中間肥大 | 沿用，句尾探問那條斷言照 09-20 覆核版 | 構句；因果語言的階段判斷 | A1 |
| n1 未經整理的長草稿 | 新 | 一段約 600 字、問題混雜的草稿：埋 2 個致命、3 個錯誤，另放 2 句看起來可疑但其實合格的句子。看它能不能排出輕重、不誤判那 2 句 | A2、A3 |
| n2 乾淨段落 | 新 | 已經改好的段落，正確答案是「可用」或只有瑕疵級。負向案例 | R2 精神、假陽性 |
| n3 研究問題與結果章的因果語言 | 新 | 同一段落裡，研究問題用探問、結果章用「影響」且三條件齊全、討論章寫「導致」。只有最後一處該抓 | A1 |
| n4 台灣用語與 APA 中文化 | 新 | 大陸用語、統計術語、「等人」與「& 」混用、中英文標點 | 在地知識，預期 skill 優勢最大 |
| n5 緒論草稿 | 新 | CARS 三個 move 缺一個 | 決定 `chapter-structure.md` 去留 |

eval-3a、3b 測的功能已經移除，不跑。

AWD 這輪沒有改，「對應提案」欄的 A1 到 A3 是暫不收的提案：這幾題的結果只當作以後要不要收的證據。RQA 的 n2 對應的 R3 也一樣。

另加一題探查（不算進任何臂的分數）：把 eval-3a 的乾淨文獻回顧丟給沒裝 skill 的 Opus 5.5 跑 3 次，看它自己會不會把站得住的過渡判成論證斷裂。結果只拿來判斷「論證鏈檢查有沒有必要加回來」。

### research-question-audit（6 題）

| 案例 | 來源 | 測什麼 | 對應提案 |
|---|---|---|---|
| eval-1 沒有依變數的題目 | 沿用 | 基準 | |
| eval-2 依變數太多 | 沿用 | 戰線過長該抓的情況 | R1（改版後仍要抓得到） |
| eval-3 GAI 依賴 | 沿用 | 缺口分類 | |
| eval-4 成熟題目 | 沿用，斷言依 `ASSERTION_AUDIT_2026-09-20.md` 修：a1、a4 重新裁定案例文本是否真的合格，裁定不了就改寫案例文本 | 假陽性 | R1、R2 |
| n1 兩個指標量同一構念 | 新 | 依變數用兩個指標測同一個構念，不該標戰線過長 | R1 |
| n2 有方向的是非問句 | 新 | 研究問題寫「X 是否正向預測 Y」，不該觸發是非問句紅線；另一句「X 是否影響 Y」該觸發 | R3 |

### research-direction-finding（5 題，外加 1 題選做）

沿用 iteration-4 的 5 題，只改 eval-4 的斷言（見第四節）。選做：eval-2 改成三輪對話，事先寫好使用者的三句回覆，用 `claude -p --resume <session-id>` 依序餵，看它每輪是不是只推進一層、有沒有產出進度筆記。多輪做法要先小測能不能穩定接續，不行就放棄這題。

## 六、指標

- 各臂 `outcome` 斷言平均通過率，以及三臂兩兩的差距。
- 一致性：同一題 3 次執行裡，致命級問題每次都有抓到的比例（官方文章的 pass^k 概念，k＝3）。
- 假陽性：負向案例（AWD n2、RQA eval-4 與 n1）被挑出的不實問題數。
- 觸發率：階段 0 應觸發句的觸發比例、不應觸發句的誤觸發比例。
- 成本：每臂平均 tokens 與秒數。改版如果效果一樣但更省，也算改善。

## 七、執行設定

- CLI 照 `iteration-5\README.md` 的那一組（隔離 cwd、`--setting-sources project,local`、工具白名單），加上 `--model`。階段 0 要看有沒有呼叫 Skill 工具，改用 `--output-format stream-json`；這個格式是否要搭配 `--verbose`，執行前先小測確認，不要照記憶寫。
- `--allowedTools` 用逗號分隔的單一參數（09-20 踩過：空白分隔會把後面的位置參數吃掉）。
- 開跑前重做 iteration-5 的三項小測（載得到、對照組載不到、載的是 repo 不是全域快取），兩個 worktree 各做一次。
- prompt 抽成獨立 .txt 放 repo 外，執行行程拿不到斷言。
- 產出放 `evals\iteration-6\`，格式同 iteration-5。

## 八、評分

- 主評分：sonnet，拿得到斷言。
- 盲評：opus，只拿 prompt、斷言、回應三樣，計算逐條一致率，照 iteration-5 的做法。
- 判定分歧、或兩臂都失敗的斷言，主對話逐條讀回應原文裁決，並記錄是模型錯還是斷言錯。

## 九、決策規則（跑之前先定好，跑完不改）

1. 候選版在 sonnet 與 opus 兩個模型上，`outcome` 通過率都不低於 v0.3.0，而且負向案例的假陽性沒有增加 → 收成 v0.4.0。
2. 候選版任一模型上有一題比 v0.3.0 平均少 1 條以上 `outcome` 斷言 → 那一題對應的提案退回，其他照收。
3. 效果相同、但較短或較省 → 收（官方文章以「no measurable loss」為刪減標準）。
4. 某個 skill 在 opus 上與沒裝的差距不到 +0.05 → README 寫明「在較強模型上效益有限，主要價值在在地規則」，不刪 skill。
5. AWD n5 沒有差距 → 移除 `chapter-structure.md`。
6. README 的評測段落改成 iteration-6 的數字，並寫清楚量的是哪個版本、哪兩個模型、每題幾次。

## 十、執行順序

1. ~~維護者對評估檔的提案拍板~~（09-28 完成：收 R1、R2）。
2. ~~開 `v0.4-candidate` 分支改 skill，派 fresh verifier 核對改動與提案一致~~（09-28 完成，`8611e4c`）。
3. 寫新案例與斷言，派 verifier 用「兩個專家會不會判得一樣」的標準審一次斷言。
4. 階段 0 → 階段 1 → 階段 2，每階段結束回報一次再往下。
5. 彙整、更新 README、決定合併與版號。

在本機執行，要呼叫本機的 claude CLI。

## 十一、模型換代時的例行檢查

維護者 09-28 的顧慮：照模型能力調 skill，每出一代新模型就得重調一次，時效太短。做法是把 skill 內容分成兩層，只有一層會過期，再拿這套案例當換代時的例行檢查。

立場層不會過期。五種缺口、台灣用語、APA 中文化、因果三條件、交棒流程、國內期刊清單，都是論文圈的慣例或站方的立場，模型再強也不會自己知道，換代不用動。

補強層會過期。寫死的門檻、固定必填的格式、重複叮嚀，是在補模型的不足；模型變強以後，這些可能變成過度限制，R1 就是一例。新寫的規則一律附理由，像本輪 R1、R2 那樣：強模型會依理由判斷例外，弱模型照規則走也不會錯，同一份內容兩種模型都適用。

新的 Sonnet 或 Opus 推出時，只跑一小輪：用新模型跑階段 1 的「沒裝」與「目前版本」兩臂，每題 1 次，約 36 次，一小時內跑完。判讀方式：

- 沒裝的一臂在某條規則上已經穩定答對，那條規則屬補強層，可以考慮刪。
- 裝了的一臂在某題變差（通常是假陽性變多），代表某條硬規則開始綁住新模型，改成附理由的寫法。
- 兩臂都沒變化就不動，README 補一行「某日以某模型重跑，結果一致」。

設計時以 Sonnet 為底。Sonnet 答得好的，Opus 通常也行；Opus 那一臂主要用來抓「規則太硬，把強模型綁住」的情況。

換代的成本因此只剩一小輪測試加少量修改。要長期維護的是案例與斷言。

## 十二、執行時的調整（2026-09-28 執行當天補記）

規格寫好之後、正式跑之前，小測發現幾件事，照下面改：

1. **使用者層的 CLAUDE.md 與 rules 會被讀進執行行程。** `--setting-sources project,local` 擋掉的是 settings 與 hook，擋不掉使用者層的 CLAUDE.md 與 `rules/`。維護者本機的全域守則裡有因果動詞、APA 之類的寫作提示，會讓沒裝 skill 的一臂拿到額外線索。本輪所有執行（含評分）都加上環境變數 `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`，小測回 `NONE`。iteration-5 沒有這一條：它的 without_skill 每次輸入約 27.7k tokens，本輪同樣設定約 15k，差距跟全域守則的大小相符，所以 iteration-5 的沒裝那一臂很可能讀到了維護者的守則。這是從 token 數推論，沒有直接證據。
2. **工具白名單改用 `--tools`。** `--allowedTools` 只管權限，模型仍看得到其他內建工具與帳號層的 MCP connector。本輪改成 `--tools Skill,Read,Glob,Grep` 加 `--strict-mcp-config`，init 事件確認只剩這四個工具、MCP 清單為空。`--disallowedTools` 因此拿掉。
3. **`--output-format stream-json` 必須搭配 `--verbose`**，不加會直接報錯。所有執行都用 stream-json，順便從 `tool_use` 事件記下有沒有叫用 Skill。
4. **三項小測**（兩個 worktree 各做）：init 事件的 skills 清單有三個 skill，沒掛 plugin 的一臂沒有；plugin 路徑指向各自的 worktree；在 AWD `SKILL.md` 插入標記字串後實跑，回應第一行分別是 `MARKER-v030`、`MARKER-v040c`。標記已還原。
5. **effort 用預設值。** 使用者層 settings 被排除，所以執行行程跑的是各模型的預設 effort，跟一般同學裝 plugin 後的情況一致。
6. **評分改成腳本呼叫。** 主評分（sonnet）與盲評（opus）都用不帶工具的 `claude -p`，只拿 prompt、斷言、回應三樣，不知道回應來自哪一臂。兩者拿到的資料相同，差別在模型與執行個體。
7. **斷言多一類 `compliance`**：版權排除清單那條（`../RUBRIC.md` 第 3 節）單獨列，不算進 outcome 也不算進 procedure，避免這條永遠通過的斷言稀釋差距。
8. **RQA eval-4 改寫了案例文本**（見該案例 `source` 欄），RQA eval-2 的 a3 改成反向的假陽性檢查，AWD eval-1 a1 改成接受兩種理由。理由都寫在各自的 `eval_metadata.json`。
9. RDF eval-2 的多輪選做題沒有做。

`build_cases.py`（本目錄）產生案例；`tools/` 裡 `run_eval.py` 執行、`grade.py` 評分、`agreement.py` 算評分者一致率、`build_final.py` 套用裁決、`aggregate.py` 彙整。結果見 `README.md`。
