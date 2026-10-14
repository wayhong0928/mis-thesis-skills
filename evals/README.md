# 評測紀錄

三個 SKILL 都用 Anthropic 官方的 [skill-creator](https://github.com/anthropics/skills) 流程跑過評測：設計測試案例、比較「有無 SKILL」兩臂的輸出、逐條斷言評分。各輪的設定與評分方式寫在該輪資料夾的 README 或 SPEC。

## iteration-6（2026-09-28，三個 SKILL）

18 個案例，Sonnet 5 每題 3 次、Opus 5.5 每題 1 次，比較沒裝、0.3.0、0.4.0 三個版本。數字表在專案根目錄的 README；完整設定、逐題數字、評分者一致率（96.4%）與限制，見 [`iteration-6/README.md`](iteration-6/README.md)。

讀那張表時要知道的事：

- 效益主要來自在地規則與「不要把合格的地方判成錯」。沒裝 SKILL 的模型會對已經改好的段落挑出不存在的錯誤、把合格的「影響」判成因果越線、抓不到「判別效度」「模型擬合」這類大陸統計術語，也會在使用者資訊不足時繼續追問。
- Opus 5.5 沒裝 SKILL 也答得不差，差距比 Sonnet 小，但仍有 +0.20 到 +0.35。
- 案例由維護者設計，Opus 每題只跑 1 次，這些數字是方向性觀察，不是穩定的效果估計。

## iteration-7、iteration-8（2026-10-05，只測 academic-writing-discipline）

0.4.1 到 0.4.3 只改了 academic-writing-discipline，另外跑了兩輪：

- [`iteration-7/`](iteration-7/)：13 個案例，Sonnet 每題 3 次、Opus 每題 1 次。0.4.2 有一個副作用：沒有原文時，會在修改稿裡改寫原作者的比較說法，所以沒有發布。0.4.3 修掉之後重測 6 題，其餘 7 題沿用 0.4.2 的結果。合併後的 outcome 通過率，0.4.0 → 0.4.3 是 Sonnet 0.950 → 0.974、Opus 0.985 → 1.000，假陽性 4 → 0、1 → 0。進步主要來自不再把「影響」誤判成因果越線。
- [`iteration-8/`](iteration-8/)：驗證 0.4.1／0.4.2 新規則本身的效益，只跑 Sonnet，每臂 1 到 3 次。三項規則（轉述細節列待核對、範圍對上證據、方法論引用列待核對）0.4.0 試跑時就做到了。表格與版面那一項，判準寬嚴不同，結論也不同，所以無法判定。評測沒有顯示這四項規則讓 0.4.3 比 0.4.0 好。

## iteration-9（2026-10-11，thesis-roadmap 觸發）

[`iteration-9/`](iteration-9/) 只測 0.5.0 新增的 `thesis-roadmap` 會不會被正確叫用、會不會搶走另外三個 SKILL 的觸發，不評輸出品質。11 題，Sonnet 每題 2 次、Opus 1 次：初版 description 31/33，補一句之後 33/33，兩輪的反例都是 18/18。做法、題目與限制見該資料夾的 README。

## iteration-10（2026-10-14，academic-writing-discipline 與 grep 基線）

[`iteration-10/`](iteration-10/) 用兩篇未發表碩論的三段真實文字，植入 12 個錯（grep 抓得到、抓不到的各 6 個），另放 2 段原文當乾淨對照，比較 `grep-checks.sh`、沒裝 skill、0.5.2 三方。Sonnet 每臂每題 3 次。偵測合計 grep 6/12、沒裝 27/36、0.5.2 29/36；grep 抓得到的那 6 個，grep 全中，0.5.2 是 13/18。依事先寫定的規則，判定是「勝過 grep」與「比沒裝方向一致但不足」：skill 的差距集中在大陸用語，語意層的錯沒裝的模型已經抓得到，模型之外仍要跑 grep。另外發現 skill 內部對「值得注意的是」的規則互相矛盾（grep 清單寫應為空，用語檔寫最多 2 次）。案例、回應與評分只留在維護者本機，別人無法重跑。做法與限制見該資料夾的 SPEC 與 VERDICT。

## iteration-5 以前

[`iteration-5/`](iteration-5/) 量的是 0.2.0。iteration-6 發現當時沒裝 SKILL 的一臂很可能讀到了維護者本機的全域設定，那批數字要保守看待，細節見 [`iteration-6/README.md`](iteration-6/README.md)。academic-writing-discipline 在 0.3.0 移除論證鏈檢查，依據的就是 iteration-5 的數字，見 [`iteration-5/README.md`](iteration-5/README.md) 與 [CHANGELOG](../plugins/thesis-toolkit/CHANGELOG.md)。
