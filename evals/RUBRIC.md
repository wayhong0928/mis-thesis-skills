# Iteration-3 評分 Rubric（academic-writing-discipline ／ research-question-audit 共用方法論）

> 建立時間：2026-09-07。適用範圍：`academic-writing-discipline/iteration-3/` 與 `research-question-audit/iteration-3/` 底下全部 test case。目的：讓 benchmark.json 裡的 pass_rate 有明確、可重現的判斷依據，而不是憑印象打分。

## 1. 評分單位：assertion（斷言）

每個 test case 在 `eval_metadata.json` 裡列出 3–6 條 `assertions`，每條都是一句**可獨立判定真偽**的敘述（例如「指出橫斷面研究不能用『具有顯著之影響』」）。grading.json 對每一條給出：

- `passed`：true / false（二元判定，不給部分分）
- `evidence`：從 response.md 裡摘出的具體句子或段落，證明為什麼判 pass 或 fail；找不到證據就是 fail，不可用「感覺有做到」帶過。

一個 run 的 `pass_rate = passed 條數 / assertions 總條數`。

## 2. assertion 設計的三種類型（每個 test case 通常混用）

1. **正向抓取型**（多數 assertion 屬此類）：檢查 skill 有沒有抓到某個已知存在的問題（例如因果動詞越線、依變數過多）。這類 assertion 在 without_skill 組通常較容易 fail（沒有 skill 引導，容易漏抓），是量測 skill 「有沒有補上使用者原本不會注意到的判準」的主要依據。
2. **格式／完整性型**：檢查 skill 有沒有照 SKILL.md 規定的輸出結構跑完該有的步驟（例如「有沒有主動提供引導完成邀請句」「有沒有給出整合修改版」）。這類 assertion 是 with_skill 特有的優勢，without_skill 理論上不會有這個格式，此類 assertion 只放在 with_skill 該檢查的清單裡，不強制 without_skill 也要有。
3. **假陽性防呆型**（`eval-3-good-lit-review`、`eval-4-mature-thesis` 這兩個新案例專用）：檢查 skill 會不會對「本來就寫得不錯／想得夠成熟」的內容無中生有出新問題。這類 assertion 的判法反過來——**沒有虛構問題才算 pass**，虛構出任何一條清單裡沒設計進去的致命／錯誤等級指控，就算 fail。這是本輪新增的評分視角，iteration-1 沒有測試過這個面向。

## 3. 版權排除清單檢查（每個 case 都有一條）

因為兩個 SKILL.md 明文聲明「不含任何書籍、講座或未經授權的第三方框架與專有用語」，每個 test case 都固定放一條 assertion 檢查輸出有沒有洩漏版權排除清單詞彙（彭明輝、舊瓶新酒/新瓶舊酒、雁行理論、七項要件、貢獻三角度、深而窄 等）。這條理論上應該永遠 pass（不涉及技能好壞，是版權合規檢查），如果哪個 run 沒過，代表的是嚴重問題（版權外洩），要另外標記，不能只算進 pass_rate 稀釋掉。

## 4. delta 怎麼算

沿用 skill-creator 官方 `benchmark.json` schema 的 `run_summary.delta`：

```
delta.pass_rate = with_skill 組平均 pass_rate − without_skill 組平均 pass_rate
```

每個 skill 各自算一個 delta（跨該 skill 底下所有 test case 的 with_skill 平均 vs. without_skill 平均），不是逐 case 算完再平均兩次（避免權重被 case 數量不均打亂——但本輪兩個 skill 剛好每個 case 都是 1 次 with + 1 次 without，所以兩種算法在本輪數值上會一致）。

## 5. 樣本數與變異性的誠實聲明（寫進最終回報，不得省略）

- 本輪每個 test case 只跑 **1 次** with_skill、**1 次** without_skill（不是官方建議的 3 次重跑取平均），原因是任務有中斷風險（見任務指示的額度警告），優先確保「7 個案例都跑完」而非「少數案例跑 3 次」。
- **這代表 stddev 無法計算（n=1），benchmark.json 的 `run_summary` 只能報告單次數值，不能宣稱這是穩定的統計量。** 同一個 case 換一次跑，pass_rate 有可能因為 LLM 輸出的隨機性而變動一兩條 assertion 的判定。
- 樣本數 3–4 個 case／skill，遠低於能做統計推論的規模，delta 只能當作「這一輪、這幾個案例上觀察到的方向性差異」，不能當作「當前版本 skill 效果的穩定估計值」。
- 因此最終回報必須明講：這份數據回答的問題是「當前版本在既有／新設計的 7 個案例上，有沒有明顯往好的方向改善」，不是「這個 skill 平均而言能提升多少品質」。

## 6. 兩個新案例（good-lit-review、mature-thesis）的特殊性

這兩個案例的 prompt 不是逐字沿用歷史紀錄（historical run 沒有保存原始 prompt，或該次 iteration 資料夾完全是空的），而是本輪重新設計／重建。已在各自 `eval_metadata.json` 的 `source` 欄位註明重建依據與理由，評分時不跟舊版本比較「有沒有變好」（沒有舊版本的對照資料），只作為「當前版本單獨的假陽性防呆測試」使用，delta 計算時一樣納入 with vs without 的比較，但不跟 iteration-1/2 的舊分數做縱向比較。

## 7. 每條 assertion 必須附 `based_on` 欄位（iteration-4 起強制）

從 iteration-4 開始，`eval_metadata.json` 裡每一條 assertion 都要多帶一個 `based_on` 欄位，值是這條 assertion 的判準依據在哪個 reference 檔的哪一節（例：`"based_on": "references/sentence-and-causal.md §一.1 核心原則（三條件）"`）。不只新設計的 assertion 要附，**原樣沿用舊 iteration 的 assertion 也要逐條回去查依據並補上**，不能因為「反正是抄舊的」就跳過。

**為什麼要這樣做**：iteration-3 已經出現至少三個案例的判準本身寫錯或過時（因果動詞規則從舊版一律禁用改成三條件版、研究缺口分類標錯類型、文獻回顧的假陽性案例其實藏了真缺口），追查每一次都要重新讀完整份 reference 檔案才找得到問題所在。有了 `based_on`，日後任一份 reference 檔的判準修改時，直接對該檔案路徑跑一次 grep 就能列出所有受影響的 assertion，不必逐案例重讀猜測——這跟「檔案改名後要 grep 所有引用者」是同一個模式，先例是 `~/.claude/rules/判斷力守則.md` 教訓追加區 2026-08-06 那一條（監控檔案拆分後只改路由表沒同步其他引用者）。

**找不到依據的 assertion 不能算數**：如果一條 assertion 寫完後回頭找不到對應的 reference 章節，代表這條判準本身可能是憑印象寫的，不是本 SKILL 明文規定的東西，這種情況要嘛回去補一條真正的規則到 reference 檔，要嘛承認這條 assertion 不成立、拿掉，不能先放著、之後再補。

## 8. 判斷分類對錯的 assertion，正確答案必須引用 reference 章節

「這屬於哪一種研究缺口」「這句話算不算越線」這類判斷分類正確與否的 assertion，除了第 7 節要求的 `based_on` 欄位以外，assertion 文字本身在陳述「正確答案是什麼」時也必須具體引用該分類依據的 reference 章節與判準內容，不能只寫結論（例如只寫「應判定為情境缺口」）而不附為什麼。

**理由**：分類型判準（缺口五分類、因果動詞三條件、壞題目六長相……）往往有紅線與例外，寫 assertion 的人如果自己講不出「依第幾節第幾條，因為滿足／不滿足什麼條件」，就代表這條判準本身可能沒想清楚，之後跑評測時很容易連出題者自己都不確定對錯，把一個有爭議的題目當成標準答案在打分。寫不出引用，這種 assertion 就不得放進正式評測——要嘛回頭把判斷想清楚並補上引用，要嘛承認自己判斷不出來、誠實標記「無法確定，暫不列入評測」，不能硬湊一個看似合理的答案交差（iteration-3 的 RQA eval-4 就是反面教材：assertion 只寫「應判定為理論缺口」，沒有附上為什麼排除情境缺口的判準依據，才會在 iteration-4 校正時發現分類本身錯了）。
