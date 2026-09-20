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

三個 SKILL 都用 Anthropic 官方的 [skill-creator](https://github.com/anthropics/skills) 流程跑過評測：設計測試案例、比較「有無 SKILL」兩臂的輸出、逐條斷言評分。過程與發現記錄在 [`evals/`](evals/) 目錄，包括一次真實的「SKILL 反而漏抓 baseline 抓到的問題」案例（`academic-writing-discipline` 的文獻回顧論證鏈稽核，發現後已修正並重跑驗證）。

最新一輪是 2026-09-20 的 [`evals/iteration-5/`](evals/iteration-5/)，把 `academic-writing-discipline` 與 `research-question-audit` 的 8 個案例用同一套設定重跑（先前的數字混了 SKILL 版本與兩臂 CLI 設定兩個變因，不可解讀）。兩臂唯一差異是 `--plugin-dir` 有沒有指向本 repo 的 plugin。通過率差異：`research-question-audit` +0.31，四個案例一致有正向效果；`academic-writing-discipline` +0.10，但效益集中在用詞規則類的案例，在需要判斷論證鏈成不成立的兩個案例上兩臂同分。評分另由一個不同模型的評分者盲評覆核，78 條逐條判定一致率 96.2%，兩套評分算出的 delta 分別是 +0.31／+0.20 與 +0.10／+0.05，方向一致、大小對寬嚴標準敏感。

`research-direction-finding` 於 2026-09-12 完成首次評測，5 個案例的整體效果差異為正向，沒有上述混版問題。

**v0.3.0 依這批數字縮小了 `academic-writing-discipline` 的範圍。** 逐條拆開看，該 SKILL 四個案例共 20 條斷言裡，有無 SKILL 判定不同的只有 2 條，其中一條還是在 SKILL 沒被觸發的情況下贏的（觸發問題已另外修掉並實測驗證）。效益全部集中在用詞與句子層級的判準；兩個需要判斷文獻回顧論證鏈的案例兩臂同分，而且在專門測假陽性的那個案例上，有 SKILL 的那一臂把本來站得住的段落過渡誤判為論證斷裂。對使用者來說，一個會對乾淨文字發出自信誤判的檢查比沒有更糟，所以論證鏈四步與文獻對話四測試整塊移除。`references/chapter-structure.md` 沒有被任何案例測過，留下來的理由是性質接近清單比對，不是因為有數據支持，SKILL.md 裡已標註。

**上面那些數字量的是 v0.2.0，不是現在發布的 v0.3.0。** 移除論證鏈之後，四個案例裡有兩個測的是已經不存在的功能，所以 +0.10 這個數字描述的是一個不再發布的版本，v0.3.0 尚未重新評測。不補跑的理由是：剩下兩個仍在範圍內的案例樣本太少，而且其中一個的差距來自 SKILL 未被觸發時的隨機波動，補跑得出的數字一樣不能用。要重新量應該另外設計案例，並改測目前量不到的兩個軸：同一段文字重跑的一致性，以及使用者丟未經聚焦的草稿時的表現。

每個案例只跑 1 次，樣本數也只有 4 個案例，這些數字是方向性觀察，不是穩定的效果估計。`evals/iteration-5/README.md` 記錄了完整設定、逐案例數字，以及三個還沒解決的問題（其中一個案例的 SKILL 根本沒被觸發，兩個假陽性防呆案例的斷言可能與案例文本不符）。

## 授權

MIT License，詳見 [LICENSE](LICENSE)。授權範圍僅限站方原創、可獨立溯源的判準與程式碼，不含任何書籍、講座或未經授權的第三方框架與專有用語。

## 相關連結

- [mis-thesis-guide](https://github.com/wayhong0928/mis-thesis-guide) — 這個工具組的來源網站，含完整的研究方法與學術寫作教材
