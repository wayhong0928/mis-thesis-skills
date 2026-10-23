# thesis-toolkit 基準檢查（2026-10）

- 對象：`main` @ `ca763e0`（thesis-toolkit 0.5.4，2026-10-17）
- 檢查日：2026-10-23，為 10/24 新版發布前的基準
- 範圍：只讀不改。本分支只新增這一個檔案，沒有動任何既有檔案
- 環境：Ubuntu 24.04.5 LTS、glibc 2.39、GNU bash 5.2.21、GNU grep 3.11、Claude Code CLI 2.1.309；系統預設 locale 是 `POSIX`（`LANG` 未設定）

## 總結

| 嚴重度 | 件數 |
|---|---|
| 致命 | 0 |
| 錯誤 | 4 |
| 瑕疵 | 11 |

- 安裝：**成功**。README 原文的 `/plugin` 斜線指令在非互動模式（`claude -p`）跑不了；改用同義的 `claude plugin` CLI 子指令，在全新設定目錄下裝成 0.5.4，4 個 SKILL 都載入。README「更新到新版」的兩條 CLI 指令也實跑成功。
- 結構：JSON 全部合法，`claude plugin validate` 通過（只有缺 author 的警告）；版號 0.5.4 與 CHANGELOG 最新一筆一致；4 個 SKILL 的 frontmatter 齊全、name 與資料夾名一致；SKILL.md 引用的 references 檔案全部存在。
- 腳本：24 條規則在 UTF-8 locale 下大多照設計運作。主要問題有兩個：預設 POSIX locale 下 0.5.3 加的 locale 修正反而讓 3 條規則直接報錯；幾條標「應為空」的規則有漏抓或誤抓。
- README：SKILL 清單、指令與相對路徑都對得上實際檔案，評測表數字也和 `evals/iteration-6/README.md` 一致（四捨五入到小數兩位）。不一致的只有幾處說明文字。

## 發現清單

嚴重度定義沿用 `academic-writing-discipline` 的三級：致命＝裝不起來或功能整個失效；錯誤＝會讓使用者得到錯的結果，應在發版前修；瑕疵＝說明不精確或涵蓋不足，可排進後續版本。

| # | 檔案:行號 | 問題 | 嚴重度 | 建議修法 |
|---|---|---|---|---|
| 1 | `plugins/thesis-toolkit/skills/academic-writing-discipline/references/grep-checks.sh:19-22`（影響第 48、104、108 行） | 使用者的 locale 不是 UTF-8 時，腳本會改設 `LC_ALL=C.UTF-8`。但 glibc 2.39 的 `C.UTF-8` 不支援 `[一-龥]` 這類非 ASCII 範圍，GNU grep 回 `Invalid collation character`（exit 2），「歐化：弱動詞＋抽象名詞」「流水帳式 Author (Year) 指出」「句中冒號」3 條規則不會輸出任何結果。本次在預設 POSIX locale 下實跑重現；換成 `localedef` 產生的 `en_US.UTF-8` 後 3 條都正常。使用者本來就設 `LANG=C.UTF-8` 時也會出錯，很多 Docker 映像的預設值就是這個；這種情況 case 判斷直接放行，不會改 locale | 錯誤 | 不要假設 `C.UTF-8` 能用，先實測範圍比對：`printf '一\n' \| grep -qE '[一-龥]' 2>/dev/null`；測不過就從 `locale -a` 挑一個非 `C.` 開頭的 UTF-8 locale 重試；都沒有的話，含中文範圍的 3 條改用 `grep -P '[\x{4E00}-\x{9FA5}]'`，或印出明確警告說這 3 條跳過。修完在 Ubuntu 24.04 的 POSIX 與 C.UTF-8 兩種 locale 下各跑一次 |
| 2 | `.../academic-writing-discipline/references/grep-checks.sh:68` | 「引用『等』後缺『人』（應為空）」的樣式 `等[，,;；)]` 抓不到敘述引用。實測 `王小明等(2020)指出此現象。` 沒被抓到；這是最常見的寫法，`taiwan-usage-apa.md:98` 的範例也是敘述引用 | 錯誤 | 加上敘述引用的樣式，例如 `等[（(][0-9]{4}`。和第 3 列一起改 |
| 3 | `.../academic-writing-discipline/references/grep-checks.sh:68` | 同一條規則會誤抓一般列舉。`受訪者每日使用手機、平板等，平均…` 被標出來，但這條規則標「應為空」，腳本開頭第 9 行的說明是「跑出結果代表有問題，逐條修正」，使用者可能把正確的句子也改掉 | 瑕疵 | 只在引用的語境下比對，例如 `[（(][^）)]*等[，,] ?[0-9]{4}`（括號引用）加上 `等[（(][0-9]{4}`（敘述引用），不要比對單獨的「等，」。本次實測這組樣式：R11 與 `（王小明等，2020）` 都抓到，F01、B3 不再誤抓 |
| 4 | `.../academic-writing-discipline/references/grep-checks.sh:80` 對照 `.../references/taiwan-usage-apa.md:96,102,107` | 「半形標點誤用於中文行文（應為空）」會抓所有半形 `,` 與 `;`。但 `taiwan-usage-apa.md` 第 107 行規定「括號引用時，英文文獻用半形逗號和分號」，第 96、102 行的範例也是 `（Davis, 1989）`、`（Davis, 1989; Venkatesh et al., 2012）`。實測 `…科技接受模式（Davis, 1989）。` 被抓。照 references 寫的正確引用，在腳本裡會被判成要修 | 錯誤 | 排除英文引用括號裡的半形標點，例如只抓緊鄰中文字的 `[一-龥][,;]\|[,;] ?[一-龥]`（本次實測：R14、B1 抓到，F02、B3 的英文引用不再誤抓）；或先用 `grep -vE '[A-Za-z]+( et al\.)?, [0-9]{4}'` 濾掉再比對。至少把標記從「應為空」改成「需人工判讀」，並註明英文引用除外 |
| 5 | `.../academic-writing-discipline/references/grep-checks.sh:64` 對照 `.../academic-writing-discipline/SKILL.md:68` | SKILL.md 第 2.1 節必掃清單列了「數據→資料、收集→蒐集、回歸→迴歸、判別效度→區辨效度」，腳本的大陸用語詞表只有「數據收集」「數據庫」「回歸分析」，沒有單獨的「數據」「收集」「回歸」「判別效度」。實測：repo 自己的範例句（`evals/evals.json` 第 1 題）`本研究之數據顯示…` 的「數據」沒被抓；`本研究以問卷收集數據並採用判別效度檢驗。`、`邏輯回歸結果顯示兩者相關。` 兩句都沒有任何輸出。這組標「應為空」，沒輸出會讓使用者以為已經通過 | 錯誤 | 詞表補上 `數據\|收集\|回歸\|判別效度`。「回歸」補了之後，「回歸分析」那一項就可以刪掉 |
| 6 | `.../academic-writing-discipline/references/grep-checks.sh:64` 對照 `.../references/taiwan-usage-apa.md:16-17,31-33` | 對照表裡幾個沒有歧義的大陸用語不在腳本詞表裡：軟件、硬件、網絡、互聯網、正態分佈、效應量、自變量、因變量。不含「研究」「框架」「程序」這類台灣也常用的詞 | 瑕疵 | 把上述 8 個詞補進詞表。或在第 63 行的標題註明「只涵蓋高頻詞，完整對照見 taiwan-usage-apa.md」 |
| 7 | `.../academic-writing-discipline/references/grep-checks.sh:96` | 「不是X而是Y」標題寫「句型計數（每份檔案應 ≤1）」，但 `grep -c` 算的是行數，不是出現次數。同一行出現 2 次只算 1，實測 `而非、而非。` 輸出 1。第 88 行「值得注意的是」用的是 `grep -o \| wc -l`，算的是次數，兩條規則的計數方式不一致 | 瑕疵 | 改成 `grep -oE "…" "$FILE" \| wc -l`，和第 88 行一致 |
| 8 | `.../academic-writing-discipline/references/grep-checks.sh:104` | 流水帳規則 `^[A-Za-z一-龥]+(（\|\()` 不允許作者名和括號之間有空白。實測 `Venkatesh 等人（2012）指出…`（就是 `taiwan-usage-apa.md:98` 的範例格式）和 `Davis (1989) 指出…` 都沒被抓到，`王小明等人（2020）發現…` 有抓到 | 瑕疵 | 樣式放寬成 `^[A-Za-z一-龥][A-Za-z一-龥 、.&]*(（\|\()[0-9]{4}[a-z]?(）\|\)) ?(指出\|發現\|提出\|認為)`（本次用上面三句實測，三句都抓到） |
| 9 | `.../academic-writing-discipline/references/grep-checks.sh:15` | 沒檢查檔案存不存在。不帶參數執行時，會對預設的 `檔案.md` 跑出 21 次 `No such file or directory`，兩條計數規則又印 `0`，看起來像通過，結束碼還是 0 | 瑕疵 | 在第 15 行後加 `[ -f "$FILE" ] \|\| { echo "找不到檔案：$FILE" >&2; echo "用法：bash grep-checks.sh 檔案.md" >&2; exit 1; }` |
| 10 | `.../academic-writing-discipline/SKILL.md:81`（也涉及 `grep-checks.sh:4-5`） | 第 3 節第 5 步要 Claude 告訴使用者「可使用 `references/grep-checks.sh`」在本機跑，但沒說安裝後檔案在哪裡。實際位置是 `~/.claude/plugins/cache/mis-thesis-skills/thesis-toolkit/<版號>/skills/academic-writing-discipline/references/grep-checks.sh`，而且版號一更新路徑就變；使用者照字面在自己的論文資料夾跑 `bash references/grep-checks.sh` 會找不到檔案 | 瑕疵 | 第 5 步補一句：給使用者完整的絕對路徑（從本 SKILL 的 base directory 組出來），或建議先複製到論文資料夾再跑 |
| 11 | `.../academic-writing-discipline/SKILL.md:28,30` | SKILL 正文引用 `evals/iteration-5/`、`evals/iteration-6/` 當證據，但 plugin 安裝時只複製 `plugins/thesis-toolkit/`。實際檢查安裝快取，裡面沒有 `evals/`，模型或使用者照路徑找會撲空 | 瑕疵 | 改成完整的 GitHub 網址，例如 `https://github.com/wayhong0928/mis-thesis-skills/tree/main/evals/iteration-5` |
| 12 | `plugins/thesis-toolkit/.claude-plugin/plugin.json:1-5` | `claude plugin validate` 對 marketplace 和 plugin 都發出警告「No author information provided」；plugin 目錄檢查另外提示沒有 icon | 瑕疵 | 加 `"author": { "name": "wayhong0928" }`。icon 只有要上架 plugin 目錄時才需要，可以不處理 |
| 13 | `README.md:46`、`README.en.md:48` | 寫 Claude.ai 的 `description` 上限 200 字元，「上傳前可能需要精簡」。實測 4 個 SKILL 的 description 字元數：academic-writing-discipline 307、research-direction-finding 212、research-question-audit 183、thesis-roadmap 312。除了範例用的 research-question-audit，另外 3 個都一定要精簡，不是「可能」 | 瑕疵 | 改寫成「research-question-audit 以外的三個都超過，需先精簡」，或在 repo 另附一份 ≤200 字元的短版 description |
| 14 | `README.md:18`、`README.en.md:20` | 「三者的判準都可獨立溯源…詳見各 SKILL 的 `references/`」（英文版是 "every skill … each skill's `references/`"）。現在有 4 個 SKILL，`thesis-roadmap` 沒有 `references/` 資料夾，也不含判準 | 瑕疵 | 改成「三個稽核 SKILL 的判準…；thesis-roadmap 只做導覽，不含判準」 |
| 15 | `README.md:35-38`、`README.en.md:37-40` | 安裝段只給互動模式的 `/plugin` 斜線指令。在非互動模式（`claude -p "/plugin marketplace add …"`）實跑，回的是 `/plugin isn't available in this environment.`。同義的 CLI 指令可以裝，「更新到新版」那段也已經用 CLI 寫法，安裝段卻沒有 | 瑕疵 | 安裝段補上終端機寫法：`claude plugin marketplace add wayhong0928/mis-thesis-skills`、`claude plugin install thesis-toolkit@mis-thesis-skills` |

## 1. 安裝紀錄

全新設定目錄：`HOME` 與 `CLAUDE_CONFIG_DIR` 都指到空資料夾，不沿用既有的 Claude 設定。這個執行環境的帳號登入仍有效，所以 `claude plugin list` 另外列出 7 個從 claude.ai 同步來的 plugin（productivity、design 等）。它們和 thesis-toolkit 無關，名稱也沒有重疊。

| 步驟 | 指令 | 結果 |
|---|---|---|
| README 原文第 1 步 | `claude -p "/plugin marketplace add wayhong0928/mis-thesis-skills"` | **做不到**。輸出 `/plugin isn't available in this environment.`，exit 0。`/plugin` 是互動式 TUI 指令，這個環境沒有互動終端機。README 第 2 步 `/plugin install …` 同理沒跑 |
| 同義 CLI，第 1 步 | `claude plugin marketplace add wayhong0928/mis-thesis-skills` | 成功：`Successfully added marketplace: mis-thesis-skills`（從 GitHub HTTPS clone，validate 通過） |
| 同義 CLI，第 2 步 | `claude plugin install thesis-toolkit@mis-thesis-skills` | 成功：`Successfully installed plugin: thesis-toolkit@mis-thesis-skills (scope: user)` |
| 確認 | `claude plugin list`、`claude plugin details thesis-toolkit@mis-thesis-skills` | Version 0.5.4、enabled；Skills (4)：academic-writing-discipline、research-direction-finding、research-question-audit、thesis-roadmap；常駐 token 約 1,076 |
| README「更新到新版」 | `claude plugin marketplace update mis-thesis-skills`、`claude plugin update thesis-toolkit@mis-thesis-skills` | 都成功，第二條回 `already at the latest version (0.5.4)` |

Claude Cowork、Claude.ai 網頁版、Codex 三段需要圖形介面或其他產品，本次沒有驗證。

## 2. 結構檢查

### JSON 與版號

| 檔案 | 結果 |
|---|---|
| `.claude-plugin/marketplace.json` | 合法（`python3 -m json.tool`）；`claude plugin validate .` 通過，1 個警告（見第 12 列） |
| `plugins/thesis-toolkit/.claude-plugin/plugin.json` | 合法；`"version": "0.5.4"` |
| `plugins/thesis-toolkit/CHANGELOG.md:3` | 最新一筆 `## 0.5.4（2026-10-17）`，**和 plugin.json 一致** |
| 3 個 `skills/*/evals/evals.json` | 都合法（`thesis-roadmap` 沒有這個檔，和 README 寫的「只跑了觸發評測」一致） |

marketplace.json 的 plugin 項目沒有 `version`，版號只寫在 plugin.json，不會有兩邊不一致的問題。repo 目前沒有任何 git tag。

### SKILL.md frontmatter

| 資料夾 | `name` | name＝資料夾名 | `description` 字元數（UTF-8 bytes） | 其他欄位 |
|---|---|---|---|---|
| academic-writing-discipline | 有 | 是 | 307（811） | 無 |
| research-direction-finding | 有 | 是 | 212（566） | 無 |
| research-question-audit | 有 | 是 | 183（513） | 無 |
| thesis-roadmap | 有 | 是 | 312（718） | 無 |

4 個都在 Agent Skills 規格的 description 上限 1,024 字元內。超過 Claude.ai 200 字元上限的問題見第 13 列。

### references 路徑

用 `grep -o 'references/…'` 抽出每個 SKILL.md 引用的路徑，逐一檢查是否存在：

- academic-writing-discipline：20 處引用、5 個檔案，**全部存在**；資料夾裡沒有未被引用的檔案。
- research-direction-finding：9 處引用、4 個檔案，**全部存在**。
- research-question-audit：13 處引用、3 個檔案，**全部存在**。
- thesis-roadmap：沒有 `references/`，SKILL.md 也沒引用。

另外核對了跨 SKILL 的引用。`thesis-roadmap/SKILL.md:36` 寫的「research-direction-finding 第 5 節」確實是〈什麼時候停下來，交給誰〉；第 39 行的三種總結和 `research-question-audit/SKILL.md:141` 一致。

## 3. grep-checks.sh 實跑

腳本：`plugins/thesis-toolkit/skills/academic-writing-discipline/references/grep-checks.sh`，`bash -n` 語法檢查通過，一共 24 條規則。測試文字放在 repo 以外的暫存資料夾，沒有加進 repo。

### 3.1 測試文字

**A. repo 現有範例**：`academic-writing-discipline/evals/evals.json` 兩題 prompt 裡『』括起來的句子。

```
1 本研究之數據顯示，人工智能之使用行為對受試者之學習成效具有顯著之影響，因此可以得知兩者之間存在正向關係。
2 由於近年來生成式AI技術的快速發展與普及，使得越來越多的大學生開始在課業與報告撰寫的過程中，對於這類工具的使用產生了高度的依賴性，因此本研究希望能夠深入探討這樣的依賴傾向究竟會對學生的學習成效造成什麼樣的影響。
```

**B. 自寫三句**：第 1 句明顯違規，第 2 句乾淨，第 3 句是符合 references 寫法的邊界句。

```
1 本研究通過問卷收集數據,結果表明知覺有用性導致使用意圖上升，值得注意的是，兩者之間存在著顯著的正向關係。
2 本研究以問卷蒐集資料，分析結果顯示知覺有用性與使用意圖顯著正相關。
3 受訪者每日使用手機、平板等，平均使用時間為 3.2 小時（Davis, 1989）。
```

**C. 逐條探針**（附錄）：每條規則各寫一句應命中的句子（R01–R24），再加 6 句誤抓／漏抓探針（F01–F06）。

### 3.2 輸出：B 三句，本機預設 locale（POSIX）

這是使用者在預設 POSIX locale 的 Linux 上直接跑會看到的結果，3 條規則報錯。

```
=== 稽核對象：three.md ===

--- [因果動詞紀律] 高門檻越線動詞（需人工判讀：區分「引用別人的實驗」與「自己的橫斷面宣稱」） ---
1:本研究通過問卷收集數據,結果表明知覺有用性導致使用意圖上升，值得注意的是，兩者之間存在著顯著的正向關係。

--- [因果動詞紀律] 「影響」（商管慣例可用，不視為錯誤——只人工檢查同一句或同一節內因果與相關語言是否前後一致） ---

--- [因果動詞紀律] 自創路徑名稱殘留（需人工判讀是否偽裝成既有構念，例如「⟨X⟩侵蝕路徑」「⟨X⟩固化路徑」這類非既有構念的自造詞） ---

--- [主張強度] 強度詞（需人工判讀：出現時確認有一句原文直接支撐；這是提示，不是錯誤清單） ---

--- [主張強度] 全稱句（需人工判讀：加「就本研究回顧的文獻而言」這類限定或刪） ---

--- [構句原則] 歐化：弱動詞＋抽象名詞（需人工判讀能否還原為單純動詞） ---
grep: Invalid collation character

--- [構句原則] 「存在」濫用（應為空，或改直接陳述） ---
1:本研究通過問卷收集數據,結果表明知覺有用性導致使用意圖上升，值得注意的是，兩者之間存在著顯著的正向關係。

--- [構句原則] 抽象名詞化主語（需人工判讀能否還原為動作短語） ---

--- [構句原則] 中間肥大易發句型（需人工判讀中間修飾是否過長） ---

--- [台灣學術用語] 大陸用語 / 地區用語混用（應為空） ---
1:本研究通過問卷收集數據,結果表明知覺有用性導致使用意圖上升，值得注意的是，兩者之間存在著顯著的正向關係。

--- [APA 7] 引用「等」後缺「人」（應為空） ---
3:受訪者每日使用手機、平板等，平均使用時間為 3.2 小時（Davis, 1989）。

--- [APA 7] 全形破折號用於頁碼（應改半形 en dash –） ---

--- [連接詞與標點] 破折號插說（應為空，專有名詞除外） ---

--- [連接詞與標點] 半形標點誤用於中文行文（應為空） ---
1:本研究通過問卷收集數據,結果表明知覺有用性導致使用意圖上升，值得注意的是，兩者之間存在著顯著的正向關係。
3:受訪者每日使用手機、平板等，平均使用時間為 3.2 小時（Davis, 1989）。

--- [去 AI 感] AI 套話 / 空泛結語（應為空） ---

--- [去 AI 感] 「值得注意的是」出現次數（每份檔案應 ≤2） ---
1

--- [去 AI 感] 「首先/其次/第一/第二」連用列舉（需人工判讀是否連用超過三段） ---

--- [去 AI 感] 「不是X而是Y」句型計數（每份檔案應 ≤1） ---
0

--- [去 AI 感] 過度 hedging 連疊（需人工判讀是否四連疊） ---

--- [去 AI 感] 流水帳式「Author (Year) 指出」開頭（需人工判讀是否連續三段以上） ---
grep: Invalid collation character

--- [去 AI 感] 句中冒號（需人工判讀：列舉、定義、引用前的冒號照用；引出解釋或結論的改成完整句） ---
grep: Invalid collation character

--- [APA 7] 同一句敘述引用後又加括號引用（需人工判讀：括號裡是同一篇就刪） ---

--- [連接詞] 「因」開頭的句子（需人工判讀：後面要有結果） ---

--- [文獻回顧] 他人研究的統計數字（需人工判讀：文獻回顧章轉述別人的研究時，寫方向與顯著與否即可） ---

=== 稽核完畢 ===
「需人工判讀」的項目請對照 references/sentence-and-causal.md、references/taiwan-usage-apa.md、
references/ai-flavor-and-common-errors.md 逐條確認是否真的違規。
```

### 3.3 輸出：A repo 範例，本機預設 locale（POSIX）

```
=== 稽核對象：repo_sample.md ===

--- [因果動詞紀律] 高門檻越線動詞（需人工判讀：區分「引用別人的實驗」與「自己的橫斷面宣稱」） ---
2:由於近年來生成式AI技術的快速發展與普及，使得越來越多的大學生開始在課業與報告撰寫的過程中，對於這類工具的使用產生了高度的依賴性，因此本研究希望能夠深入探討這樣的依賴傾向究竟會對學生的學習成效造成什麼樣的影響。

--- [因果動詞紀律] 「影響」（商管慣例可用，不視為錯誤——只人工檢查同一句或同一節內因果與相關語言是否前後一致） ---
1:本研究之數據顯示，人工智能之使用行為對受試者之學習成效具有顯著之影響，因此可以得知兩者之間存在正向關係。
2:由於近年來生成式AI技術的快速發展與普及，使得越來越多的大學生開始在課業與報告撰寫的過程中，對於這類工具的使用產生了高度的依賴性，因此本研究希望能夠深入探討這樣的依賴傾向究竟會對學生的學習成效造成什麼樣的影響。

--- [因果動詞紀律] 自創路徑名稱殘留（需人工判讀是否偽裝成既有構念，例如「⟨X⟩侵蝕路徑」「⟨X⟩固化路徑」這類非既有構念的自造詞） ---

--- [主張強度] 強度詞（需人工判讀：出現時確認有一句原文直接支撐；這是提示，不是錯誤清單） ---

--- [主張強度] 全稱句（需人工判讀：加「就本研究回顧的文獻而言」這類限定或刪） ---

--- [構句原則] 歐化：弱動詞＋抽象名詞（需人工判讀能否還原為單純動詞） ---
grep: Invalid collation character

--- [構句原則] 「存在」濫用（應為空，或改直接陳述） ---
1:本研究之數據顯示，人工智能之使用行為對受試者之學習成效具有顯著之影響，因此可以得知兩者之間存在正向關係。

--- [構句原則] 抽象名詞化主語（需人工判讀能否還原為動作短語） ---

--- [構句原則] 中間肥大易發句型（需人工判讀中間修飾是否過長） ---
2:由於近年來生成式AI技術的快速發展與普及，使得越來越多的大學生開始在課業與報告撰寫的過程中，對於這類工具的使用產生了高度的依賴性，因此本研究希望能夠深入探討這樣的依賴傾向究竟會對學生的學習成效造成什麼樣的影響。

--- [台灣學術用語] 大陸用語 / 地區用語混用（應為空） ---
1:本研究之數據顯示，人工智能之使用行為對受試者之學習成效具有顯著之影響，因此可以得知兩者之間存在正向關係。

--- [APA 7] 引用「等」後缺「人」（應為空） ---

--- [APA 7] 全形破折號用於頁碼（應改半形 en dash –） ---

--- [連接詞與標點] 破折號插說（應為空，專有名詞除外） ---

--- [連接詞與標點] 半形標點誤用於中文行文（應為空） ---

--- [去 AI 感] AI 套話 / 空泛結語（應為空） ---

--- [去 AI 感] 「值得注意的是」出現次數（每份檔案應 ≤2） ---
0

--- [去 AI 感] 「首先/其次/第一/第二」連用列舉（需人工判讀是否連用超過三段） ---

--- [去 AI 感] 「不是X而是Y」句型計數（每份檔案應 ≤1） ---
0

--- [去 AI 感] 過度 hedging 連疊（需人工判讀是否四連疊） ---

--- [去 AI 感] 流水帳式「Author (Year) 指出」開頭（需人工判讀是否連續三段以上） ---
grep: Invalid collation character

--- [去 AI 感] 句中冒號（需人工判讀：列舉、定義、引用前的冒號照用；引出解釋或結論的改成完整句） ---
grep: Invalid collation character

--- [APA 7] 同一句敘述引用後又加括號引用（需人工判讀：括號裡是同一篇就刪） ---

--- [連接詞] 「因」開頭的句子（需人工判讀：後面要有結果） ---

--- [文獻回顧] 他人研究的統計數字（需人工判讀：文獻回顧章轉述別人的研究時，寫方向與顯著與否即可） ---

=== 稽核完畢 ===
「需人工判讀」的項目請對照 references/sentence-and-causal.md、references/taiwan-usage-apa.md、
references/ai-flavor-and-common-errors.md 逐條確認是否真的違規。
```

### 3.4 B 三句的判讀

| 句 | 命中規則 | 判讀 |
|---|---|---|
| 1（違規） | 高門檻越線動詞（導致）、「存在」濫用（存在著）、大陸用語（通過問卷、結果表明）、半形標點（`,`）、「值得注意的是」計 1 次 | 該抓的大多抓到。「收集數據」本身沒被抓（第 5 列），這句是靠「通過問卷」才被標出來；1 次「值得注意的是」符合 ≤2 的規則 |
| 2（乾淨） | 無 | 正確，沒有誤報 |
| 3（邊界） | 「等」後缺「人」、半形標點 | **兩條都是誤抓**：「手機、平板等，」是一般列舉（第 3 列）；`（Davis, 1989）` 是 references 要求的英文引用寫法（第 4 列）。兩條都標「應為空」 |

### 3.5 每條規則有沒有抓到

「POSIX」欄是本機預設 locale 的結果。「UTF-8」欄是另外用 `localedef` 產生 `en_US.UTF-8`、以 `LOCPATH=… LANG=en_US.UTF-8` 執行的結果，代表 locale 正確設定時的行為。

| # | 腳本行 | 規則 | POSIX | UTF-8 | 探針結果 |
|---|---|---|---|---|---|
| 1 | 28 | 高門檻越線動詞 | 正常 | 正常 | R01「導致」抓到；B1、A2「造成」抓到 |
| 2 | 32 | 「影響」 | 正常 | 正常 | R02 抓到；A1、A2 抓到 |
| 3 | 36 | 自創路徑名稱 | 正常 | 正常 | R03「侵蝕路徑」抓到 |
| 4 | 40 | 強度詞 | 正常 | 正常 | R04「證實、最強」抓到 |
| 5 | 44 | 全稱句 | 正常 | 正常 | R05「多數研究、普遍認為」抓到 |
| 6 | 48 | 歐化弱動詞 | **報錯** | 正常 | UTF-8 下 R06「進行分析」抓到；POSIX 下 `Invalid collation character`（第 1 列） |
| 7 | 52 | 「存在」濫用 | 正常 | 正常 | R07、B1、A1 抓到 |
| 8 | 56 | 抽象名詞化主語 | 正常 | 正常 | R08「的收集」抓到 |
| 9 | 60 | 中間肥大句型 | 正常 | 正常 | R09、A2「由於…因此」抓到 |
| 10 | 64 | 大陸用語 | 正常 | 正常 | R10（算法、優化、用戶）、B1、A1（人工智能）抓到；**漏抓** A1「數據」、F03「收集數據、判別效度」、F05「邏輯回歸」（第 5、6 列） |
| 11 | 68 | 「等」後缺「人」 | 正常 | 正常 | **漏抓** R11 `王小明等(2020)`（第 2 列）；**誤抓** F01、B3 一般列舉（第 3 列） |
| 12 | 72 | 頁碼用全形破折號 | 正常 | 正常 | R12 抓到 |
| 13 | 76 | 破折號插說 | 正常 | 正常 | R13 抓到（R12 也會出現，合理） |
| 14 | 80 | 半形標點 | 正常 | 正常 | R14、B1 抓到；**誤抓** F02、B3 英文引用（第 4 列） |
| 15 | 84 | AI 套話 | 正常 | 正常 | R15「綜上所述、填補研究缺口」抓到 |
| 16 | 88 | 「值得注意的是」次數 | 正常 | 正常 | R16 輸出 3（>2，正確標出） |
| 17 | 92 | 首先／其次列舉 | 正常 | 正常 | R17 抓到 |
| 18 | 96 | 不是X而是Y 計數 | 正常 | 正常 | R18 輸出 1；F06 同一行 2 次只算 1（第 7 列） |
| 19 | 100 | hedging 連疊 | 正常 | 正常 | R19 抓到 |
| 20 | 104 | 流水帳 Author (Year) | **報錯** | 正常 | UTF-8 下 `Davis（1989）指出` 抓到；**漏抓** `Davis (1989) 指出`、`Venkatesh 等人（2012）指出`（第 8 列） |
| 21 | 108 | 句中冒號 | **報錯** | 正常 | UTF-8 下 R21 抓到 |
| 22 | 112 | 敘述引用後又加括號引用 | 正常 | 正常 | R22 抓到 |
| 23 | 116 | 「因」開頭的句子 | 正常 | 正常 | 行首「因樣本偏小…」抓到 |
| 24 | 120 | 他人統計數字 | 正常 | 正常 | R24「β =、p <」抓到 |

小計：24 條裡有 21 條在 POSIX 下能跑，3 條報錯。在 UTF-8 下 24 條都能跑，其中 5 條有已確認的漏抓、誤抓或計數問題（規則 10、11、14、18、20）。另外，不帶參數執行時會連續印出 21 次 `grep: 檔案.md: No such file or directory`（第 9 列）。

### 3.6 locale 問題的最小重現

```
$ locale -a
C
C.utf8
POSIX
$ echo 進行調查 > x.md
$ LC_ALL=C.UTF-8 grep -nE "進行了?[一-龥]{2}" x.md      # 腳本的 fallback
grep: Invalid collation character                         # exit 2
$ LOCPATH=./loc LC_ALL=en_US.UTF-8 grep -nE "進行了?[一-龥]{2}" x.md
1:進行調查                                                 # exit 0
$ LC_ALL=C.UTF-8 grep -nP "進行了?[\x{4e00}-\x{9fa5}]{2}" x.md
1:進行調查                                                 # exit 0（-P 可當替代方案）
```

## 4. README 對照

| README 寫的 | 實際 | 結果 |
|---|---|---|
| 一個 plugin `thesis-toolkit`，三個稽核 SKILL 加一個流程導覽（`README.md:7`、`README.en.md:9`） | `plugins/thesis-toolkit/skills/` 底下正好 4 個資料夾 | 一致 |
| SKILL 表格 4 列的名稱（`README.md:13-16`、`README.en.md:15-18`） | 和資料夾名、frontmatter `name` 都相同 | 一致 |
| 收斂漏斗「領域→主題→子題→題目→研究問題」 | `research-direction-finding/SKILL.md:75` | 一致 |
| 「七個檢查點，各標通過、不通過、不確定或不適用」 | `research-question-audit/SKILL.md:33`，檢查點 A–G | 一致 |
| 「通過問卷收集數據」範例 | `academic-writing-discipline/SKILL.md:96` | 一致 |
| 指定叫用 `/thesis-toolkit:research-question-audit` | plugin 名稱:SKILL 名稱，符合命名規則 | 一致（非互動模式下無法實測斜線叫用） |
| 安裝、更新指令 | 見第 1 節 | 安裝段只有斜線指令（第 15 列），更新段實跑成功 |
| 評測表數字（`README.md:71-78`、`README.en.md:73-80`） | `evals/iteration-6/README.md` 的表格（0.708→0.71、0.958→0.96…），案例數 7＋6＋5＝18 | 一致 |
| 相對連結：`plugins/thesis-toolkit/CHANGELOG.md`、`evals/iteration-6/`、`evals/iteration-9/`、`evals/README.md`、`LICENSE`、`README.en.md`／`README.md` | 全部存在；CHANGELOG 的 0.3.0 一節在第 102 行 | 一致 |
| 判準都在「各 SKILL 的 `references/`」 | thesis-roadmap 沒有 | 不一致（第 14 列） |
| Claude.ai「可能需要精簡」 | 4 個裡有 3 個超過 200 字元 | 說得太輕（第 13 列） |

順帶一提，`CHANGELOG.md:106` 提到的 `references/ai-flavor-and-argument.md` 已不存在。這是 0.3.0 改名前的舊檔名，屬於歷史紀錄，不算問題。

## 附錄：探針檔與 UTF-8 輸出

<details>
<summary>probe.md（R01–R24）與 fp.md（F01–F06）</summary>

```
R01 本研究發現使用頻率導致倦怠上升。
R02 社群支持對使用意圖具有顯著正向影響。
R03 本研究提出資訊侵蝕路徑來解釋此現象。
R04 結果證實知覺有用性是最強的預測因子。
R05 多數研究普遍認為此效果穩定。
R06 本研究對資料進行分析。
R07 兩組之間存在著顯著差異。
R08 資料的收集採用線上問卷。
R09 由於受訪者多為在學且每日使用超過三小時的大學生因此結果偏高。
R10 本研究利用算法優化用戶體驗。
R11 王小明等(2020)指出此現象。
R12 見期刊第 12—18 頁。
R13 此一概念——即科技焦慮——源自早期研究。
R14 本研究,以問卷進行調查。
R15 綜上所述，本研究填補研究缺口。
R16 值得注意的是，此效果不穩定。值得注意的是，樣本偏小。值得注意的是，期間較短。
R17 首先，回顧文獻；其次，提出假說。
R18 問題不在工具而是使用方式。
R19 此效果可能或許大概存在。
Davis（1989）指出知覺有用性影響使用意圖。
R21 研究結論如下：使用者偏好簡潔介面。
R22 陳美華（2021）發現此效果顯著（陳美華，2021）。
因樣本偏小，結果可能不穩定。
R24 先前研究發現 β = .32，p < .001。
```

```
F01 受訪者每日使用手機、平板等，平均使用時間為 3.2 小時。
F02 此構念源自科技接受模式（Davis, 1989）。
F03 本研究以問卷收集數據並採用判別效度檢驗。
F04 Davis (1989) 指出知覺有用性影響使用意圖。
F05 邏輯回歸結果顯示兩者相關。
F06 而非、而非。
```

</details>

<details>
<summary>probe.md 在 UTF-8 locale 的輸出</summary>

```
=== 稽核對象：probe.md ===

--- [因果動詞紀律] 高門檻越線動詞（需人工判讀：區分「引用別人的實驗」與「自己的橫斷面宣稱」） ---
1:R01 本研究發現使用頻率導致倦怠上升。

--- [因果動詞紀律] 「影響」（商管慣例可用，不視為錯誤——只人工檢查同一句或同一節內因果與相關語言是否前後一致） ---
2:R02 社群支持對使用意圖具有顯著正向影響。
20:Davis（1989）指出知覺有用性影響使用意圖。

--- [因果動詞紀律] 自創路徑名稱殘留（需人工判讀是否偽裝成既有構念，例如「⟨X⟩侵蝕路徑」「⟨X⟩固化路徑」這類非既有構念的自造詞） ---
3:R03 本研究提出資訊侵蝕路徑來解釋此現象。

--- [主張強度] 強度詞（需人工判讀：出現時確認有一句原文直接支撐；這是提示，不是錯誤清單） ---
4:R04 結果證實知覺有用性是最強的預測因子。

--- [主張強度] 全稱句（需人工判讀：加「就本研究回顧的文獻而言」這類限定或刪） ---
5:R05 多數研究普遍認為此效果穩定。

--- [構句原則] 歐化：弱動詞＋抽象名詞（需人工判讀能否還原為單純動詞） ---
6:R06 本研究對資料進行分析。
14:R14 本研究,以問卷進行調查。

--- [構句原則] 「存在」濫用（應為空，或改直接陳述） ---
7:R07 兩組之間存在著顯著差異。

--- [構句原則] 抽象名詞化主語（需人工判讀能否還原為動作短語） ---
8:R08 資料的收集採用線上問卷。

--- [構句原則] 中間肥大易發句型（需人工判讀中間修飾是否過長） ---
9:R09 由於受訪者多為在學且每日使用超過三小時的大學生因此結果偏高。

--- [台灣學術用語] 大陸用語 / 地區用語混用（應為空） ---
10:R10 本研究利用算法優化用戶體驗。

--- [APA 7] 引用「等」後缺「人」（應為空） ---

--- [APA 7] 全形破折號用於頁碼（應改半形 en dash –） ---
12:R12 見期刊第 12—18 頁。

--- [連接詞與標點] 破折號插說（應為空，專有名詞除外） ---
12:R12 見期刊第 12—18 頁。
13:R13 此一概念——即科技焦慮——源自早期研究。

--- [連接詞與標點] 半形標點誤用於中文行文（應為空） ---
14:R14 本研究,以問卷進行調查。

--- [去 AI 感] AI 套話 / 空泛結語（應為空） ---
15:綜上所述
15:填補研究缺口

--- [去 AI 感] 「值得注意的是」出現次數（每份檔案應 ≤2） ---
3

--- [去 AI 感] 「首先/其次/第一/第二」連用列舉（需人工判讀是否連用超過三段） ---
17:R17 首先，回顧文獻；其次，提出假說。

--- [去 AI 感] 「不是X而是Y」句型計數（每份檔案應 ≤1） ---
1

--- [去 AI 感] 過度 hedging 連疊（需人工判讀是否四連疊） ---
19:R19 此效果可能或許大概存在。

--- [去 AI 感] 流水帳式「Author (Year) 指出」開頭（需人工判讀是否連續三段以上） ---
20:Davis（1989）指出知覺有用性影響使用意圖。

--- [去 AI 感] 句中冒號（需人工判讀：列舉、定義、引用前的冒號照用；引出解釋或結論的改成完整句） ---
21:R21 研究結論如下：使用者偏好簡潔介面。

--- [APA 7] 同一句敘述引用後又加括號引用（需人工判讀：括號裡是同一篇就刪） ---
22:R22 陳美華（2021）發現此效果顯著（陳美華，2021）。

--- [連接詞] 「因」開頭的句子（需人工判讀：後面要有結果） ---
23:因樣本偏小，結果可能不穩定。

--- [文獻回顧] 他人研究的統計數字（需人工判讀：文獻回顧章轉述別人的研究時，寫方向與顯著與否即可） ---
24:R24 先前研究發現 β = .32，p < .001。

=== 稽核完畢 ===
「需人工判讀」的項目請對照 references/sentence-and-causal.md、references/taiwan-usage-apa.md、
references/ai-flavor-and-common-errors.md 逐條確認是否真的違規。
```

</details>

<details>
<summary>fp.md 在 UTF-8 locale 的輸出</summary>

```
=== 稽核對象：fp.md ===

--- [因果動詞紀律] 高門檻越線動詞（需人工判讀：區分「引用別人的實驗」與「自己的橫斷面宣稱」） ---

--- [因果動詞紀律] 「影響」（商管慣例可用，不視為錯誤——只人工檢查同一句或同一節內因果與相關語言是否前後一致） ---
4:F04 Davis (1989) 指出知覺有用性影響使用意圖。

--- [因果動詞紀律] 自創路徑名稱殘留（需人工判讀是否偽裝成既有構念，例如「⟨X⟩侵蝕路徑」「⟨X⟩固化路徑」這類非既有構念的自造詞） ---

--- [主張強度] 強度詞（需人工判讀：出現時確認有一句原文直接支撐；這是提示，不是錯誤清單） ---

--- [主張強度] 全稱句（需人工判讀：加「就本研究回顧的文獻而言」這類限定或刪） ---

--- [構句原則] 歐化：弱動詞＋抽象名詞（需人工判讀能否還原為單純動詞） ---

--- [構句原則] 「存在」濫用（應為空，或改直接陳述） ---

--- [構句原則] 抽象名詞化主語（需人工判讀能否還原為動作短語） ---

--- [構句原則] 中間肥大易發句型（需人工判讀中間修飾是否過長） ---

--- [台灣學術用語] 大陸用語 / 地區用語混用（應為空） ---

--- [APA 7] 引用「等」後缺「人」（應為空） ---
1:F01 受訪者每日使用手機、平板等，平均使用時間為 3.2 小時。

--- [APA 7] 全形破折號用於頁碼（應改半形 en dash –） ---

--- [連接詞與標點] 破折號插說（應為空，專有名詞除外） ---

--- [連接詞與標點] 半形標點誤用於中文行文（應為空） ---
2:F02 此構念源自科技接受模式（Davis, 1989）。

--- [去 AI 感] AI 套話 / 空泛結語（應為空） ---

--- [去 AI 感] 「值得注意的是」出現次數（每份檔案應 ≤2） ---
0

--- [去 AI 感] 「首先/其次/第一/第二」連用列舉（需人工判讀是否連用超過三段） ---

--- [去 AI 感] 「不是X而是Y」句型計數（每份檔案應 ≤1） ---
1

--- [去 AI 感] 過度 hedging 連疊（需人工判讀是否四連疊） ---

--- [去 AI 感] 流水帳式「Author (Year) 指出」開頭（需人工判讀是否連續三段以上） ---

--- [去 AI 感] 句中冒號（需人工判讀：列舉、定義、引用前的冒號照用；引出解釋或結論的改成完整句） ---

--- [APA 7] 同一句敘述引用後又加括號引用（需人工判讀：括號裡是同一篇就刪） ---

--- [連接詞] 「因」開頭的句子（需人工判讀：後面要有結果） ---

--- [文獻回顧] 他人研究的統計數字（需人工判讀：文獻回顧章轉述別人的研究時，寫方向與顯著與否即可） ---

=== 稽核完畢 ===
「需人工判讀」的項目請對照 references/sentence-and-causal.md、references/taiwan-usage-apa.md、
references/ai-flavor-and-common-errors.md 逐條確認是否真的違規。
```

</details>
