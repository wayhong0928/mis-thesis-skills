# mis-thesis-skills

論文研究方法與學術寫作的稽核工具組，把 [mis-thesis-guide](https://github.com/wayhong0928/mis-thesis-guide) 網站的部分內容做成可安裝的 Claude Code SKILL，取代同學自己複製貼上提示詞的方式。

這是一個 [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)，收錄一個 plugin（`thesis-toolkit`），裡面包含三個 SKILL，對應論文 0→1 的三個階段：

## 內含的 SKILL

| SKILL | 管什麼 | 不管什麼 |
|---|---|---|
| `research-direction-finding` | 完全沒有研究方向、或只有一個大到不能當題目的領域興趣時，用起步策略與收斂漏斗（領域→主題→子題→題目→研究問題）一次推進一層，收出一句話的研究想法；每輪寫進度筆記 | 不稽核收出來的題目站不站得住腳（那是下一個 SKILL）；不代替使用者讀文獻 |
| `research-question-audit` | 稽核已經想出來的研究問題／研究想法，抓邏輯、方法論、可行性上的漏洞；跑完稽核後可進入逐項引導模式，一項一項幫你想清楚該怎麼回答 | 不會替你從零發想題目；不涉及問卷題項編寫、統計分析實跑等執行細節 |
| `academic-writing-discipline` | 稽核一段中文學術論述的文字與論證品質：因果動詞紀律、構句原則、台灣學術用語、APA 7、去 AI 感、文獻是否真的對話（而非只是並列）、章節結構寫法 | 不處理研究設計邏輯（那是上面那個 SKILL 的範圍） |

三者的判準都可獨立溯源於公開學術方法學資源（詳見各 SKILL 的 `references/` 與 [mis-thesis-guide](https://github.com/wayhong0928/mis-thesis-guide) 網站上的 [「把教材做成可安裝的 SKILL」](https://github.com/wayhong0928/mis-thesis-guide) 一文，記錄了完整的設計與提煉過程）。

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

### Codex（OpenAI）

Codex 也支援開放的 [Agent Skills](https://agentskills.io/) 格式，讀取路徑是 `.agents/skills/`（而不是 Claude Code 用的 `.claude/skills/`）。可以把 SKILL 資料夾複製過去，或建 symlink 讓兩邊共用同一份檔案。這不是走 plugin marketplace 機制（那是 Claude 生態系專屬的打包方式），只是 SKILL.md 本身的開放格式。

## 評測

`research-question-audit` 與 `academic-writing-discipline` 兩個 SKILL 都用 Anthropic 官方的 [skill-creator](https://github.com/anthropics/skills) 流程跑過完整評測（設計測試案例、平行比較「有無 SKILL」的輸出差異、量化評分），過程與誠實的發現（包括一次「SKILL 反而漏抓 baseline 抓到的問題」的真實案例）記錄在 [`evals/`](evals/) 目錄與網站的實作紀錄文章裡。`research-direction-finding` 於 2026-09-07 新增，測試案例已定義在該 SKILL 的 `evals/evals.json`，但**尚未實際跑過評測**。

## 授權

MIT License，詳見 [LICENSE](LICENSE)。授權範圍僅限站方原創、可獨立溯源的判準與程式碼，不含任何書籍、講座或未經授權的第三方框架與專有用語。

## 相關連結

- [mis-thesis-guide](https://github.com/wayhong0928/mis-thesis-guide) — 這個工具組的來源網站，含完整的研究方法與學術寫作教材
