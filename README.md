# mis-thesis-skills

論文研究方法與學術寫作的稽核工具組，把 [mis-thesis-guide](https://wayhong0928.github.io/mis-thesis-guide/) 網站的部分內容做成可安裝的 Claude Code SKILL，取代同學自己複製貼上提示詞的方式。

這是一個 [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)，收錄一個 plugin（`thesis-toolkit`），裡面包含三個 SKILL，對應論文 0→1 的三個階段。

## 內含的 SKILL

| SKILL | 管什麼 | 不管什麼 |
|---|---|---|
| `research-direction-finding` | 完全沒有研究方向、或只有一個大到不能當題目的領域興趣時，用起步策略與收斂漏斗（領域→主題→子題→題目→研究問題）一次推進一層，收出一句話的研究想法；每輪寫進度筆記 | 不稽核收出來的題目站不站得住腳（那是下一個 SKILL）；不代替使用者讀文獻 |
| `research-question-audit` | 稽核已經想出來的研究問題／研究想法，抓邏輯、方法論、可行性上的漏洞；跑完稽核後可進入逐項引導模式，一項一項幫你想清楚該怎麼回答 | 不會替你從零發想題目；不涉及問卷題項編寫、統計分析實跑等執行細節 |
| `academic-writing-discipline` | 稽核中文學術論述在句子與用詞層級的品質：因果動詞紀律、構句原則、台灣學術用語、APA 7、去 AI 感、章節結構寫法 | 不處理研究設計邏輯（那是上面那個 SKILL 的範圍）；**不再檢查文獻回顧的論證鏈**，v0.3.0 依評測結果移除，理由見 [CHANGELOG](plugins/thesis-toolkit/CHANGELOG.md) 0.3.0 一節 |

三者的判準都可獨立溯源於公開學術方法學資源，詳見各 SKILL 的 `references/`。設計與提煉過程記錄在[〈把教材做成 SKILL〉](https://wayhong0928.github.io/ai-agent-notes/pages/skill-build.html)。

## 用法

裝好之後不用記指令，用中文講你要做什麼，Claude 會判斷要叫用哪一個 SKILL。想指定的話，可以輸入 `/thesis-toolkit:research-question-audit` 這類名稱。

| 你說 | 叫用 | 它回 |
|---|---|---|
| 「老師叫我自己想題目，我完全沒方向」 | `research-direction-finding` | 先確認你是完全沒方向、有大方向，還是要從老師的計畫延伸。完全沒方向的話，先給一項今天就能做的作業，之後一輪推進一層，每輪把結論和排除的選項寫進進度筆記 |
| 「我想研究遠距工作對員工倦怠的影響，幫我看這個題目站不站得住」 | `research-question-audit` | 一份稽核報告：七個檢查點各標通過、不通過、不確定或不適用，附理由；不通過和不確定的項目再翻成口試委員可能問的話。最後問你要不要一項一項想清楚 |
| 貼一段文獻回顧，說「幫我檢查這段的寫法」 | `academic-writing-discipline` | 分致命、錯誤、瑕疵三級，列出原句、問題、改法，例如橫斷面資料寫「導致」、「通過問卷收集數據」這類大陸用語。最後附一版套好修法、可以直接用的整合修改版 |

## 安裝方式

### Claude Code

```
/plugin marketplace add wayhong0928/mis-thesis-skills
/plugin install thesis-toolkit@mis-thesis-skills
```

### Claude Cowork

Customize → Plugins → Add marketplace，輸入 `wayhong0928/mis-thesis-skills`，安裝 `thesis-toolkit`。

### Claude.ai 網頁版

網頁版不支援 plugin marketplace，需要把單一 SKILL 資料夾（例如 `plugins/thesis-toolkit/skills/research-question-audit/`）另外包成 `.zip`，在 Customize → Skills 手動上傳。注意 Claude.ai 的 `description` 欄位上限是 200 字元，比 Claude Code 短，上傳前可能需要精簡。

只用網頁版（Claude.ai、ChatGPT、Gemini）的話，可以改用 mis-thesis-guide 的[三段網頁簡版提示詞](https://wayhong0928.github.io/mis-thesis-guide/pages/prompts.html#skill-lite)，不必打包上傳。簡版沒有 references 裡的完整判準，差在哪裡寫在該頁各段下方。

### Codex（OpenAI）

Codex 也支援開放的 [Agent Skills](https://agentskills.io/) 格式，讀取路徑是 `.agents/skills/`（而不是 Claude Code 用的 `.claude/skills/`）。可以把 SKILL 資料夾複製過去，或建 symlink 讓兩邊共用同一份檔案。這不是走 plugin marketplace 機制（那是 Claude 生態系專屬的打包方式），只是 SKILL.md 本身的開放格式。

## 更新到新版

第三方 marketplace 預設不會自動更新，有新版時要自己更新。在終端機執行：

```
claude plugin marketplace update mis-thesis-skills
claude plugin update thesis-toolkit@mis-thesis-skills
```

也可以在 Claude Code 裡輸入 `/plugin`，到 Marketplaces 分頁選 `mis-thesis-skills`，選 **Update marketplace**；同一處選 **Enable auto-update**，之後就會自動更新。更新後開新的 session 就會載入新版，正在用的 session 可以輸入 `/reload-plugins` 套用。各版改了什麼見 [CHANGELOG](plugins/thesis-toolkit/CHANGELOG.md)。

## 評測

三個 SKILL 都用 Anthropic 官方的 [skill-creator](https://github.com/anthropics/skills) 流程跑過評測：設計測試案例、比較「有無 SKILL」兩臂的輸出、逐條斷言評分。

三個 SKILL 都跑的最近一輪是 2026-09-28 的 [`evals/iteration-6/`](evals/iteration-6/)：18 個案例，Sonnet 5 每題 3 次、Opus 5.5 每題 1 次。下表只算「使用者實際拿到的東西對不對」這類斷言（outcome）的通過率：

| SKILL | 模型 | 沒裝 | 0.3.0 | 0.4.0 |
|---|---|---|---|---|
| academic-writing-discipline | Sonnet | 0.71 | 0.95 | 0.99 |
| | Opus | 0.77 | 0.96 | 0.96 |
| research-question-audit | Sonnet | 0.67 | 0.96 | 1.00 |
| | Opus | 0.73 | 0.93 | 1.00 |
| research-direction-finding | Sonnet | 0.55 | 0.93 | 0.98 |
| | Opus | 0.65 | 1.00 | 1.00 |

案例由維護者設計，Opus 每題只跑 1 次，這些數字是方向性觀察，不是穩定的效果估計。怎麼讀這張表、0.4.1 之後的評測，以及更早的數字為什麼要保守看待，見 [`evals/README.md`](evals/README.md)。

## 回報問題

判準有錯、SKILL 沒被叫用或輸出不對，請到 [Issues](https://github.com/wayhong0928/mis-thesis-skills/issues) 回報，附上你貼的內容和它的回應。

## 授權

MIT License，詳見 [LICENSE](LICENSE)。授權範圍僅限站方原創、可獨立溯源的判準與程式碼，不含任何書籍、講座或未經授權的第三方框架與專有用語。

## 同系列

| 資源 | 適合誰 |
|---|---|
| [mis-thesis-guide](https://wayhong0928.github.io/mis-thesis-guide/) | 研究方法與論文寫作的知識庫，查觀念、查判準 |
| [一小時上手](https://wayhong0928.github.io/mis-thesis-guide/pages/ai-quickstart.html) | 只用 ChatGPT、Claude、Gemini 網頁版，想在一小時內建好論文助手（另有 [Claude Code、Codex 版](https://wayhong0928.github.io/mis-thesis-guide/pages/ai-quickstart-agent.html)） |
| [thesis-notes-template](https://github.com/wayhong0928/thesis-notes-template) | 想用 Obsidian 做文獻筆記，要現成的模板和填寫規則 |
| [mis-thesis-skills](https://github.com/wayhong0928/mis-thesis-skills) | 用 Claude Code 或 Codex，想讓 AI 照固定判準檢查題目與寫作 |
