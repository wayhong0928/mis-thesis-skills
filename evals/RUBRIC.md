# Iteration-3 評分 Rubric（academic-writing-discipline ／ research-question-audit 共用方法論）

> 建立時間：2026-09-07。適用範圍：`academic-writing-discipline/iteration-3/` 與 `research-question-audit/iteration-3/` 底下全部 test case。目的：讓 benchmark.json 裡的 pass_rate 有明確、可重現的判斷依據，而不是憑印象打分。

## 1. 評分單位：assertion（斷言）

每個 test case 在 `eval_metadata.json` 裡列出 3–6 條 `assertions`，每條都是一句**可獨立判定真偽**的敘述（例如「指出橫斷面研究不能用『具有顯著之影響』」）。grading.json 對每一條給出：

- `passed`：true / false（二元判定，不給部分分）
- `evidence`：從 response.md 裡摘出的具體句子或段落，證明為什麼判 pass 或 fail；找不到證據就是 fail，不可用「感覺有做到」帶過。

一個 run 的 `pass_rate = passed 條數 / assertions 總條數`。

## 2. assertion 設計的三種類型（每個 test case 通常混用）

1. **正向抓取型**（多數 assertion 屬此類）：檢查 skill 有沒有抓到某個已知存在的問題（例如因果動詞越線、依變數過多）。這類 assertion 在 without_skill 组通常較容易 fail（沒有 skill 引導，容易漏抓），是量測 skill 「有沒有補上使用者原本不會注意到的判準」的主要依據。
2. **格式／完整性型**：檢查 skill 有沒有照 SKILL.md 規定的輸出結構跑完該有的步驟（例如「有沒有主動提供引導完成邀請句」「有沒有給出整合修改版」）。這類 assertion 是 with_skill 特有的優勢，without_skill 理論上不會有這個格式，此類 assertion 只放在 with_skill 該檢查的清單裡，不強制 without_skill 也要有。
3. **假陽性防呆型**（`eval-3-good-lit-review`、`eval-4-mature-thesis` 這兩個新案例專用）：檢查 skill 會不會對「本來就寫得不錯／想得夠成熟」的內容無中生有出新問題。這類 assertion 的判法反過來——**沒有虛構問題才算 pass**，虛構出任何一條清單裡沒設計進去的致命／錯誤等級指控，就算 fail。這是本輪新增的評分視角，iteration-1 沒有測試過這個面向。

## 3. 版權排除清單檢查（每個 case 都有一條）

因為兩個 SKILL.md 明文聲明「不含任何書籍、講座或未經授權的第三方框架與專有用語」，每個 test case 都固定放一條 assertion 檢查輸出有沒有洩漏版權排除清單詞彙（彭明輝、舊瓶新酒/新瓶舊酒、雁行理論、七項要件、貢獻三角度、深而窄 等）。這條理論上應該永遠 pass（不涉及技能好壞，是版權合規檢查），如果哪個 run 沒過，代表的是嚴重問題（版權外洩），要另外標記，不能只算進 pass_rate 稀釋掉。

## 4. delta 怎麼算

沿用 skill-creator 官方 `benchmark.json` schema 的 `run_summary.delta`：

```
delta.pass_rate = with_skill 组平均 pass_rate − without_skill 组平均 pass_rate
```

每個 skill 各自算一個 delta（跨該 skill 底下所有 test case 的 with_skill 平均 vs. without_skill 平均），不是逐 case 算完再平均兩次（避免權重被 case 數量不均打亂——但本輪兩個 skill 剛好每個 case 都是 1 次 with + 1 次 without，所以兩種算法在本輪數值上會一致）。

## 5. 樣本數與變異性的誠實聲明（寫進最終回報，不得省略）

- 本輪每個 test case 只跑 **1 次** with_skill、**1 次** without_skill（不是官方建議的 3 次重跑取平均），原因是任務有中斷風險（見任務指示的額度警告），優先確保「7 個案例都跑完」而非「少數案例跑 3 次」。
- **這代表 stddev 無法計算（n=1），benchmark.json 的 `run_summary` 只能報告單次數值，不能宣稱這是穩定的統計量。** 同一個 case 換一次跑，pass_rate 有可能因為 LLM 輸出的隨機性而变動一兩條 assertion 的判定。
- 樣本數 3–4 個 case／skill，遠低於能做統計推論的規模，delta 只能當作「這一輪、這幾個案例上觀察到的方向性差異」，不能當作「當前版本 skill 效果的穩定估計值」。
- 因此最終回報必須明講：這份數據回答的問題是「當前版本在既有／新設計的 7 個案例上，有沒有明顯往好的方向改善」，不是「這個 skill 平均而言能提升多少品質」。

## 6. 兩個新案例（good-lit-review、mature-thesis）的特殊性

這兩個案例的 prompt 不是逐字沿用歷史紀錄（historical run 沒有保存原始 prompt，或該次 iteration 資料夾完全是空的），而是本輪重新設計／重建。已在各自 `eval_metadata.json` 的 `source` 欄位註明重建依據與理由，评分时不跟旧版本比較「有沒有变好」（没有旧版本的对照数据），只作为「当前版本单独的假阳性防呆測試」使用，delta 计算时一样纳入 with vs without 的比较，但不跟 iteration-1/2 的旧分数做纵向比较。
