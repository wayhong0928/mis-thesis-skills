# thesis-toolkit 變更紀錄

## 0.4.0（2026-09-28）

依 `evals/iteration-6/` 的評測修改。三個 SKILL 在 Sonnet 5 與 Opus 5.5 上都跑過，本版在兩個模型上的 outcome 斷言通過率都不低於 0.3.0，假陽性為 0。

### research-question-audit

- 壞題目②「戰線過長」原本是「依變數達 2 個（含）以上就命中」。改成先看依變數之間的關係：同一個構念的不同指標不算，各自需要一套理論解釋的不同結果才算，並寫出理由。0.3.0 在 Opus 上兩個相關案例都照字面判成戰線過長。
- 稽核流程加一段判定原則：判「通過」也要寫出依據；資訊不足的項目標「不確定」並說明缺什麼。題目定案六問每項都加上「不確定」選項，檢查點 E 的是非問句紅線加上「不適用（使用者還沒寫出研究問題句）」。
- 是非問句紅線改看有沒有方向：「X 是否影響 Y」仍要改寫，「X 是否正向預測 Y」不算命中。原本 `question-forms.md` 第一節列為可用句型、第四節又說任何「是否」句都不通過，兩節互相矛盾，Sonnet 3 次有 1 到 2 次把有方向的句子判成不通過。
- 報告用台灣繁體中文與全形標點。

### academic-writing-discipline

- SKILL.md 加「必掃清單」（2.1 節）：因果動詞、「存在」與弱動詞、最常見的大陸用語、「等人」與「與」、全形標點、譯名一致。完整規則仍在 references，這份是每次都要掃的底線。
- 規定先讀 `sentence-and-causal.md` 與 `taiwan-usage-apa.md` 再輸出，整合修改版寫完再拿必掃清單掃一次。0.3.0 有 2/21 次執行沒讀 references，其中一次漏掉「人工智能」與「存在」濫用，修改版還把「人工智能」留著。
- `references/chapter-structure.md` 保留。評測時試過移除（沒裝 SKILL 的模型本來就抓得到緒論缺研究缺口），但移除後 Sonnet 3 次都沒抓到，回應說「不在本次檢查內」，所以撤回。SKILL.md 的說明改成記錄這個結果。

### research-direction-finding

- 起點 A（完全空白）的第一個回應要給一項今天能做的作業，不先問一串背景問題。0.3.0 在這個案例 3 次都先問三到五個問題、承諾「回答完再開始」。
- 進度筆記從使用者第一次回答開始記，第一個回應不用硬寫。
- 檢索範本附上網址（`mis-thesis-guide` 提示詞範本頁 2.2 節）。0.3.0 只寫頁名，模型從來沒提過這份範本。
- 回應用台灣繁體中文與全形標點。

## 0.3.0（2026-09-20）

### academic-writing-discipline：移除文獻回顧論證鏈檢查（破壞性變更）

拿掉 `references/ai-flavor-and-argument.md` 的 §二 論證鏈四步（含三層結構、文獻對話四測試：
主語掃描、關係詞測試、伏筆兌現檢查、遮住引註總檢），以及 SKILL.md 裡對應的執行步驟、
判準總覽列、等級判斷條文。檔案因此改名為 `references/ai-flavor-and-common-errors.md`。

理由是 2026-09-20 的評測（`evals/iteration-5/`）：四個案例共 20 條斷言，有無 SKILL 判定不同的
只有 2 條，效益全部在用詞與句子層級；兩個測論證鏈的案例兩臂同分，而且在專門測假陽性的
`eval-3a` 上，有 SKILL 的那一臂把站得住的段落過渡誤判為論證斷裂。會對乾淨文字發出自信誤判的
檢查比沒有更糟，所以整塊移除而不是修補。

保留的判準：因果動詞紀律、構句原則、台灣學術用語、APA 7 中文化、連接詞與標點、去 AI 感、
常見錯誤速查表、`references/grep-checks.sh`。

`references/chapter-structure.md` 保留，但它沒有被任何評測案例測過，SKILL.md 已標註為未經驗證。

### academic-writing-discipline：修掉窄問題不觸發

舊 `description` 寫「檢查一段中文學術論述」「一次跑完全部判準」，遇到「這句話會不會有中間肥大」
這種單句加單一項目的提問就不會被叫用（實測三次都是 `num_turns=1`）。改寫後實測兩次都觸發。
佐證在 `evals/iteration-5/academic-writing-discipline/eval-2-bloated-middle-sentence/trigger_probe/`。

新 `description` 長度 307 字元（改寫時是 320，同版本移除論證鏈那句後變成 307），超過 Claude.ai 網頁版的
200 字元上限，網頁版上傳前需另外精簡；Claude Code 與 Cowork 不受影響。

### 升級注意

`claude plugin update` 曾經因為版號沒變而誤報「已是最新」，這次版號有進版，但更新後仍建議
自己比對 `installed_plugins.json` 的 `gitCommitSha` 與 repo HEAD。

## 0.2.0

新增 `research-direction-finding`，三個 SKILL 對應論文 0→1 的三個階段。
