# mis-thesis-skills

論文研究方法與學術寫作的稽核工具組，把 [mis-thesis-guide](https://github.com/wayhong0928/mis-thesis-guide) 網站的部分內容做成可安裝的 Claude Code SKILL，取代同學自己複製貼上提示詞的方式。

這是一個 [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)，收錄一個 plugin（`thesis-toolkit`），裡面包含三個 SKILL，對應論文 0→1 的三個階段：

## 內含的 SKILL

| SKILL | 管什麼 | 不管什麼 |
|---|---|---|
| `research-direction-finding` | 完全沒有研究方向、或只有一個大到不能當題目的領域興趣時，用起步策略與收斂漏斗（領域→主題→子題→題目→研究問題）一次推進一層，收出一句話的研究想法；每輪寫進度筆記 | 不稽核收出來的題目站不站得住腳（那是下一個 SKILL）；不代替使用者讀文獻 |
| `research-question-audit` | 稽核已經想出來的研究問題／研究想法，抓邏輯、方法論、可行性上的漏洞；跑完稽核後可進入逐項引導模式，一項一項幫你想清楚該怎麼回答 | 不會替你從零發想題目；不涉及問卷題項編寫、統計分析實跑等執行細節 |
| `academic-writing-discipline` | 稽核中文學術論述在句子與用詞層級的品質：因果動詞紀律、構句原則、台灣學術用語、APA 7、去 AI 感、章節結構寫法 | 不處理研究設計邏輯（那是上面那個 SKILL 的範圍）；**不再檢查文獻回顧的論證鏈**，v0.3.0 依評測結果移除，理由見下方「評測」 |

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

三個 SKILL 都用 Anthropic 官方的 [skill-creator](https://github.com/anthropics/skills) 流程跑過評測：設計測試案例、比較「有無 SKILL」兩臂的輸出、逐條斷言評分。過程與發現記錄在 [`evals/`](evals/) 目錄。

最新一輪是 2026-09-28 的 [`evals/iteration-6/`](evals/iteration-6/)：18 個案例，Sonnet 5 每題 3 次、Opus 5.5 每題 1 次，比較沒裝、0.3.0、0.4.0 三個版本。主要數字只算「使用者實際拿到的東西對不對」這類斷言（outcome）：

| SKILL | 模型 | 沒裝 | 0.3.0 | 0.4.0 |
|---|---|---|---|---|
| academic-writing-discipline | Sonnet | 0.71 | 0.95 | 0.99 |
| | Opus | 0.77 | 0.96 | 0.96 |
| research-question-audit | Sonnet | 0.67 | 0.96 | 1.00 |
| | Opus | 0.73 | 0.93 | 1.00 |
| research-direction-finding | Sonnet | 0.55 | 0.93 | 0.98 |
| | Opus | 0.65 | 1.00 | 1.00 |

幾個讀這張表時要知道的事：

- 效益主要來自在地規則與「不要把合格的地方判成錯」。沒裝 SKILL 的模型會對已經改好的段落挑出不存在的錯誤、把理論與控制變數齊備的「影響」判成因果越線、抓不到「判別效度」「模型擬合」這類大陸統計術語，也會在使用者資訊不足時繼續追問。
- Opus 5.5 沒裝 SKILL 也答得不差，差距比 Sonnet 小，但仍有 +0.20 到 +0.35。
- 案例由維護者設計，Opus 每題只跑 1 次，這些數字是方向性觀察，不是穩定的效果估計。完整設定、逐題數字、評分者一致率（96.4%）與限制，見 `evals/iteration-6/README.md`。

更早的 [`evals/iteration-5/`](evals/iteration-5/) 量的是 0.2.0。本輪發現當時沒裝 SKILL 的一臂很可能讀到了維護者本機的全域設定，那批數字要保守看待，細節同樣在 iteration-6 的 README。

## 授權

MIT License，詳見 [LICENSE](LICENSE)。授權範圍僅限站方原創、可獨立溯源的判準與程式碼，不含任何書籍、講座或未經授權的第三方框架與專有用語。

## 相關連結

- [mis-thesis-guide](https://github.com/wayhong0928/mis-thesis-guide) — 這個工具組的來源網站，含完整的研究方法與學術寫作教材
