# thesis-toolkit 變更紀錄

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
