# thesis-toolkit SKILL description 審查（2026-10）

這份文件只做檢查，沒有修改任何 SKILL。

- **審查對象**：`plugins/thesis-toolkit/skills/` 底下四個 SKILL，版本 0.5.4（commit `ca763e0`，即本分支的起點 `main`）
- **對照基準**：Anthropic 官方的 skill 撰寫指引三頁，2026-10-23 讀取（見第一節）
- **審查日期**：2026-10-23
- **限制**：第四節的觸發測試題**還沒有實際跑過**，「預期」欄是審查者依各 SKILL 的範圍判斷的結果，不是觀測值。要拿到觸發率，請用 `evals/iteration-9/run_trigger.py` 的做法實跑。字數用 Python `len()` 計算（以 Unicode 字元為單位）。

---

## 目錄

- 一、官方指引摘錄
- 二、問題數總表
- 三、逐個 SKILL 對照
  - 3.1 academic-writing-discipline
  - 3.2 research-direction-finding
  - 3.3 research-question-audit
  - 3.4 thesis-roadmap
- 四、觸發測試題（80 題）
- 五、相鄰 SKILL 容易混淆的情境與歸屬
- 六、待實測與未計入問題數的觀察

---

## 一、官方指引摘錄

讀取的三頁：

| 代號 | 頁面 | 網址 |
|---|---|---|
| CC | Claude Code 文件：Extend Claude with skills | https://code.claude.com/docs/en/skills |
| BP | Skill authoring best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices （`docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices` 會轉址到這裡） |
| OV | Agent Skills overview | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview |

以下每條附來源網址、段落名稱與逐字原文，中文是審查者的摘要。

### 1. name

| # | 規定（摘要） | 來源 | 逐字原文 |
|---|---|---|---|
| N1 | 最多 64 字元，只能用小寫英文、數字、連字號，不能有 XML 標籤，不能含保留字 | BP「Skill structure」；OV「Skill structure」 | "Maximum 64 characters" / "Must contain only lowercase letters, numbers, and hyphens" / "Cannot contain XML tags" / "Cannot contain reserved words: "anthropic", "claude"" |
| N2 | 建議用動名詞形式，名詞片語也可以；避免同一組 skill 命名風格不一 | BP「Naming conventions」 | "Consider using **gerund form** (verb + -ing) for Skill names, as this clearly describes the activity or capability the Skill provides." / "Acceptable alternatives: … Noun phrases: `pdf-processing`, `spreadsheet-analysis`" / "Avoid: … Inconsistent patterns within your skill collection" |
| N3 | 在 Claude Code 裡，name 是選填，預設用目錄名稱；plugin skill 會加上 plugin 前綴 | CC「Frontmatter reference」 | "Command name shown in the `/` menu. Defaults to the directory name." / "In a plugin skill, `name` sets the last segment of the command and the plugin prefix stays in place." |

### 2. description

| # | 規定（摘要） | 來源 | 逐字原文 |
|---|---|---|---|
| D1 | 不可空白，最多 1,024 字元，不能有 XML 標籤，要寫做什麼與何時用 | BP「Skill structure」 | "Must be non-empty" / "Maximum 1,024 characters" / "Cannot contain XML tags" / "Should describe what the Skill does and when to use it" |
| D2 | description 是觸發比對的依據，必須同時寫做什麼與何時用 | OV「Level 1: Metadata (always loaded)」 | "The `description` is what Claude matches your request against when determining whether to trigger the Skill, so it must say both what the Skill does and when to use it." |
| D3 | 一律用第三人稱 | BP「Writing effective descriptions」 | "**Always write in third person**. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems." |
| D4 | 要具體、放關鍵詞，寫出觸發情境 | BP「Writing effective descriptions」 | "**Be specific and include key terms**. Include both what the Skill does and specific triggers/contexts for when to use it." |
| D5 | Claude 要從上百個 skill 裡靠 description 選，description 要足以判斷何時選它；實作細節放本文 | BP「Writing effective descriptions」 | "The description is critical for skill selection: Claude uses it to choose the right Skill from potentially 100+ available Skills. Your description must provide enough detail for Claude to determine when to select this Skill, whereas the rest of `SKILL.md` provides the implementation details." |
| D6 | 主要用途放最前面；Claude Code 的 skill 清單裡，`description` 加 `when_to_use` 超過 1,536 字元會被截斷 | CC「Frontmatter reference」 | "Put the key use case first: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing to reduce context usage." |
| D7 | skill 很多時，清單會依字元預算捨棄部分 description，預算是 context window 的 1% | CC「Skill descriptions are cut short」 | "if you have many skills, Claude Code drops some descriptions to fit the listing's character budget, which removes the keywords Claude needs to match your request. The budget scales at 1% of the model's context window." |

### 3. 觸發條件寫法

| # | 規定（摘要） | 來源 | 逐字原文 |
|---|---|---|---|
| T1 | 觸發片語或範例請求可以放在 `when_to_use`（Claude Code 專屬欄位），一樣算進 1,536 字元 | CC「Frontmatter reference」 | "Additional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to `description` in the skill listing and counts toward the 1,536-character cap." |
| T2 | 沒觸發時，先檢查 description 有沒有使用者自然會講的關鍵詞 | CC「Skill not triggering」 | "Check the description includes keywords users would naturally say" |
| T3 | 觸發太頻繁時，把 description 寫得更具體 | CC「Skill triggers too often」 | "Make the description more specific" |
| T4 | 避免空泛 description | BP「Writing effective descriptions」 | "Avoid vague descriptions such as these:" （例：`description: Helps with documents`） |
| T5 | 官方範例的句型：先寫做什麼，再寫「Use when …」 | BP「Writing effective descriptions」 | "description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction." |
| T6 | plugin 的 skill 可以用 `claude plugin eval` 配 `tool_used: Skill` grader 量測觸發率 | CC「Skill not triggering」 | "If the skill ships in a plugin, you can measure how often it triggers across realistic prompts rather than checking one at a time: write an eval case with a `tool_used: Skill` grader and run it with `claude plugin eval` after each description change." |

官方三頁都**沒有**規定要寫「何時不用」。本文件第三節把「何時不用」列為檢查項，是因為這四個 SKILL 範圍相鄰，D5 要求 description「足以判斷何時選它」，而相鄰 SKILL 之間要靠排除條件才分得開。

### 4. 檔案長度

| # | 規定（摘要） | 來源 | 逐字原文 |
|---|---|---|---|
| L1 | SKILL.md 本文 500 行以內，接近時拆檔 | BP「Progressive disclosure patterns」 | "Keep the `SKILL.md` body under 500 lines for optimal performance." / "Split content into separate files when approaching this limit." |
| L2 | 同上（Claude Code 版） | CC「Add supporting files」 | "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files." |
| L3 | 本文觸發後才載入，建議 5k token 以內 | OV「How Skills work」表格 | "Level 2: Instructions | When Skill is triggered | Under 5k tokens | `SKILL.md` body with instructions and guidance" |
| L4 | 對話壓縮後只保留每個 skill 前 5,000 token，重要指示放前面 | CC「Skill content lifecycle」「Claude stops following a skill」 | "Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each." / "so put the most important instructions near the top of `SKILL.md`." |
| L5 | 不要放會過時的資訊，歷史放「舊做法」區塊 | BP「Avoid time-sensitive information」 | "Don't include information that will become outdated" / "No time-sensitive information (or in "old patterns" section)" |

### 5. references 拆分

| # | 規定（摘要） | 來源 | 逐字原文 |
|---|---|---|---|
| R1 | 從 SKILL.md 指到每個支援檔，並說明內容與何時讀 | CC「Add supporting files」 | "Reference supporting files from `SKILL.md` so Claude knows what each file contains and when to load it" |
| R2 | references 只往下一層，每個檔都直接從 SKILL.md 連過去 | BP「Avoid deeply nested references」 | "**Keep references one level deep from `SKILL.md`**. All reference files should link directly from `SKILL.md` to ensure Claude reads complete files when needed." |
| R3 | 超過 100 行的 reference 開頭要放目錄 | BP「Structure longer reference files with a table of contents」 | "For reference files longer than 100 lines, include a table of contents at the top. This ensures Claude can see the full scope of available information even when previewing with partial reads." |
| R4 | 術語前後一致 | BP「Use consistent terminology」 | "Choose one term and use it throughout the Skill" |
| R5 | 先建評測再寫長文件，至少三個評測 | BP「Build evaluations first」與檢查清單 | "**Create evaluations BEFORE writing extensive documentation.**" / "At least three evaluations created" |

---

## 二、問題數總表

| SKILL | 問題數 | 主要問題 |
|---|---|---|
| academic-writing-discipline | 6 | description 沒寫到章節結構稽核；沒排除「論證撐不撐得住」；起草與稽核的範圍沒說清楚；本文含版本與評測歷史及安裝後不存在的路徑；兩份 reference 超過 100 行沒有目錄；與 research-question-audit 在變數名稱一致性上重疊 |
| research-direction-finding | 5 | description 沒寫「老師計畫延伸」這種起點；用第二人稱；沒標明期刊清單偏資管；排除條件只列 research-question-audit；venues.md 超過 100 行沒有目錄 |
| research-question-audit | 4 | 「何時不用」沒點名 research-direction-finding（本文也沒點名）；沒排除寫作品質與研究設計後段；缺使用者會講的關鍵詞；用第二人稱 |
| thesis-roadmap | 2 | 「某階段有沒有工具可用」可能誤觸實質方法、統計問題；沒有輸出品質評測 |
| **合計** | **17** | |

硬性規定（N1、D1）四個 SKILL 全部符合；本文行數（L1）全部遠低於 500 行；references 沒有孤兒檔，也沒有超過一層的引用（R2）。

---

## 三、逐個 SKILL 對照

### 3.1 academic-writing-discipline

**基本數據**

| 項目 | 值 | 對照 |
|---|---|---|
| name | `academic-writing-discipline`（27 字元） | N1 符合；名詞片語，N2 可接受 |
| description 字數 | 307 字元（UTF-8 811 bytes） | D1 符合（< 1,024）；D6 符合（< 1,536） |
| 主要用途在最前面 | 是（「當使用者要檢查或潤飾中文學術論述的寫作品質時套用」） | D6 符合 |
| 人稱 | 第三人稱 | D3 符合 |
| SKILL.md 本文行數 | 126 行（約 5,200 字元） | L1 符合；L3 見第六節 |

**references 指向檢查（孤兒檔）**

| 檔案 | 行數 | SKILL.md 提到次數 | 超過 100 行有目錄？ |
|---|---|---|---|
| `ai-flavor-and-common-errors.md` | 71 | 3 | 不適用 |
| `chapter-structure.md` | 59 | 5 | 不適用 |
| `grep-checks.sh` | 125 | 2 | 腳本，給使用者在本機執行，不適用 R3 |
| `sentence-and-causal.md` | 181 | 6 | **沒有**（只有 `##` 標題） |
| `taiwan-usage-apa.md` | 182 | 4 | **沒有**（只有 `##` 標題） |

孤兒檔：無。`taiwan-usage-apa.md` 第 163 行指到 `ai-flavor-and-common-errors.md`、`sentence-and-causal.md` 第 175 行指到 `grep-checks.sh`，但這兩個檔 SKILL.md 本身也都直接指到，不算 R2 的多層引用。

**逐項對照**

| 檢查項 | 結果 |
|---|---|
| 何時用 | 清楚：檢查或潤飾中文學術文字，一句到一整段，並舉三個單項問法 |
| 何時不用 | 部分：只排除研究設計邏輯（交給 research-question-audit）；本文 §0 另外排除的「文獻回顧論證鏈」沒寫進 description |
| 與其他 SKILL 分界 | 與 research-question-audit 有兩處重疊（研究缺口、變數名稱），見問題 1、6 |
| 長度與拆分 | 本文長度符合；兩份 reference 缺目錄 |

**問題**

1. **description 沒寫到章節結構稽核，且和 research-question-audit 的「研究缺口」字面重疊。** 本文 §0 與 §2 有「緒論是否完成 CARS 三個 move（含研究缺口）、方法章是否交代 How 與 Why」，但 description 完全沒提。description 反而寫「研究缺口怎麼分類，那是 research-question-audit 的範圍」，使用者問「我緒論有沒有把研究缺口講出來」時，Claude 依 description 可能判給 research-question-audit 或不叫用。依據：D4、D5、T2。
2. **沒有排除「文獻回顧論證撐不撐得住」。** 本文 §0 第 2 點明說 v0.3.0 起不管論證鏈，但 description 沒寫。使用者問「我這段文獻回顧的論證通不通」時會觸發本 SKILL，拿到的是用語與構句檢查，容易誤以為論證也檢查過了。依據：D5、T3。
3. **起草與稽核的範圍沒有說清楚。** 0.5.2 起 `sentence-and-causal.md` §一.4 有「起草當下就對原文」等起草端規則，但 description 只寫「檢查或潤飾」，本文 §1 的互動形態也是「使用者貼一段文字進來」。使用者說「幫我寫一段 TAM 的文獻回顧」時不會觸發，起草端規則實際上用不到。要擴大到起草還是明確排除起草，需要維護者決定（改寫版先依現行本文寫成排除，見下方說明）。依據：D2、D5。
4. **本文含版本與評測歷史，以及安裝後不存在的路徑。** §0 寫「v0.3.0 起移除」「2026-09-20 的評測」「Sonnet 3 次都沒抓到」，§3 第 2 步寫「21 次執行有 2 次」，並指向 `evals/iteration-5/`、`evals/iteration-6/`。這兩個路徑在 repo 根目錄，不在 plugin 裡；從 SKILL 目錄看，`evals/` 底下只有 `evals.json`，Claude 照路徑去讀會找不到。依據：L5（歷史資訊建議移到「舊做法」區塊或 CHANGELOG）、L4（壓縮後只留前 5,000 token，§0 的歷史說明佔了最前面的位置）。
5. **兩份 reference 超過 100 行，開頭沒有目錄。** `sentence-and-causal.md` 181 行、`taiwan-usage-apa.md` 182 行。依據：R3。
6. **變數名稱一致性與 research-question-audit 重疊。** 本 SKILL 的必掃清單有「同一構念前後出現兩個譯名」、`sentence-and-causal.md` 有「依變項名稱不同也要交代」；research-question-audit 的常見錯誤第 8 條是「題目、問題、假說三處變數名稱不一致」。兩邊 description 都沒劃界，使用者問「題目寫使用意圖、假說寫使用意願可以嗎」時兩邊都說得通。建議分界：段落內同一構念譯名不一歸本 SKILL；題目、研究問題、假說三處對不上歸 research-question-audit。依據：D5、R4。

**description 原文與改寫版**

| 原文（307 字元） | 改寫版（364 字元） |
|---|---|
| 當使用者要檢查或潤飾中文學術論述的寫作品質時套用，一句話或一整段都算（論文段落、研究計畫書、期刊投稿、口試講稿）。稽核因果動詞紀律、構句原則（中間肥大、話題漂移、弱動詞與「存在」濫用、由於…因此等易爆句型）、台灣學術用語、APA 7 中文化格式、連接詞與標點、去 AI 感特徵。使用者只問其中單一項目時也要套用，例如「這句有沒有中間肥大」「這樣寫算不算因果越線」「這個詞是不是大陸用語」；問題範圍窄不是略過本 SKILL 自己回答的理由，判準與替換表在 references/ 裡，憑印象答會漏。不處理研究設計邏輯（研究問題怎麼問、研究缺口怎麼分類，那是 research-question-audit 的範圍）。 | 檢查或潤飾使用者已經寫好的中文學術文字，一句話到一整章都算（論文段落、研究計畫書、期刊投稿、口試講稿）。稽核因果動詞紀律、構句原則（中間肥大、話題漂移、弱動詞與「存在」濫用、由於…因此等易爆句型）、台灣學術用語、APA 7 中文化格式、連接詞與標點、去 AI 感特徵，以及緒論有沒有交代研究缺口（CARS 三個 move）、方法章有沒有同時寫怎麼做與為何這麼做。使用者只問其中單一項目時也要套用，例如「這句有沒有中間肥大」「這樣寫算不算因果越線」「這個詞是不是大陸用語」；判準與替換表在 references/ 裡，憑印象答會漏。不處理：研究問題怎麼問、缺口屬於哪一類、題目與假說的變數對不對得上（用 research-question-audit）；文獻回顧的論證撐不撐得住（本 SKILL 不檢查）；還沒有文字、要從零起草。 |

改了什麼：

- 開頭從「當使用者要…時套用」改成先寫做什麼（T5 句型），並加「已經寫好的」把稽核與起草分開（問題 3）。
- 補上緒論 CARS 與方法章 How／Why（問題 1）。
- 「不處理」拆成三項：研究設計交給 research-question-audit 並補上變數對應（問題 6）、論證鏈明講不檢查（問題 2）、從零起草（問題 3）。
- 刪掉「問題範圍窄不是略過本 SKILL 自己回答的理由」這半句，保留「憑印象答會漏」，省下字數放排除條件。CHANGELOG「修掉窄問題不觸發」一節記載，舊 description 遇到單句加單一項目的問法不會叫用，改寫後才觸發（佐證在 `evals/iteration-5/`），刪之前請先重跑單項問法的觸發測試（第四節 A-1 到 A-3、A-7）。
- 如果維護者決定讓起草端規則也生效，把最後一項改成「使用者要起草文獻回顧或緒論段落時也套用」，並同步修改本文 §1 的互動形態。

---

### 3.2 research-direction-finding

**基本數據**

| 項目 | 值 | 對照 |
|---|---|---|
| name | `research-direction-finding`（26 字元） | N1 符合；名詞片語，N2 可接受 |
| description 字數 | 212 字元（UTF-8 566 bytes） | D1、D6 符合 |
| 主要用途在最前面 | 是 | D6 符合 |
| 人稱 | 混用：「陪你從零把方向收出來」「稽核你已經有的想法」用第二人稱 | **D3 不符** |
| SKILL.md 本文行數 | 106 行（約 3,600 字元） | L1、L3 符合 |

**references 指向檢查（孤兒檔）**

| 檔案 | 行數 | SKILL.md 提到次數 | 超過 100 行有目錄？ |
|---|---|---|---|
| `convergence-funnel.md` | 98 | 2 | 不適用 |
| `handoff-to-literature.md` | 69 | 2 | 不適用 |
| `progress-note-template.md` | 96 | 2 | 不適用 |
| `venues.md` | 111 | 3 | **沒有**（開頭是用法說明，章節標題從第 20 行之後才出現） |

孤兒檔：無。`convergence-funnel.md` 指到 `venues.md` 與 `handoff-to-literature.md`，兩者 SKILL.md 都直接指到，不算 R2 的多層引用。

**逐項對照**

| 檢查項 | 結果 |
|---|---|
| 何時用 | 清楚：完全沒方向、只有模糊領域興趣，並舉「我想做 AI 相關的」「我想做資安」 |
| 何時不用 | 部分：只排除「已經寫得出一句話研究想法」；沒排除只問流程（thesis-roadmap）、找文獻 |
| 與其他 SKILL 分界 | 與 thesis-roadmap 的「不知道論文下一步做什麼」字面接近；起點 C 在 description 缺席 |
| 長度與拆分 | 本文符合；venues.md 缺目錄 |

**問題**

1. **description 沒寫「老師計畫延伸」這種起點。** 本文 §1 的起點 C 與 §2.3、thesis-roadmap 第 1 節的表格都把「老師給了研究計畫，要從裡面找題目」導到本 SKILL，但 description 只寫「完全沒有方向、模糊領域興趣」。使用者說「老師叫我從他的國科會計畫找一塊當論文」時，依 description 不一定會觸發。依據：D4、D5。
2. **用第二人稱。**「陪你從零把方向收出來」「稽核你已經有的想法」。依據：D3。
3. **沒標明期刊與研討會清單偏資管。** 策略一用的 `venues.md` 標題是「資訊管理（MIS/IS）領域期刊與研討會清單」，description 沒提領域。非資管背景的研究生觸發後，策略一給的是資管期刊。不必限制觸發，但 description 寫一句可以讓 Claude 預期這件事。依據：D4。
4. **排除條件只列 research-question-audit。** 沒寫只問「下一步該做什麼、工具順序」時用 thesis-roadmap，也沒寫本 SKILL 不幫忙找文獻（本文 §0 寫「不代替使用者讀文獻」）。「我論文不知道要做什麼」這種話，本 SKILL 與 thesis-roadmap 都說得通；thesis-roadmap 的 description 已寫「完全沒方向直接用 research-direction-finding」，這邊對稱補上會更穩。依據：D5、T3。
5. **`venues.md` 111 行，開頭沒有目錄。** 依據：R3。

**description 原文與改寫版**

| 原文（212 字元） | 改寫版（366 字元） |
|---|---|
| 當使用者完全沒有研究方向、或只有一個模糊的領域興趣（例如「我想做 AI 相關的」「我想做資安」），想要收斂出一個具體到能寫成一句話的研究想法時使用。本 SKILL 做的是「陪你從零把方向收出來」，不是「稽核你已經有的想法」——已經寫得出一句話研究想法的人，請改用 research-question-audit。適用於還沒決定題目、面對空白文件不知道從哪裡開始的階段，例如碩一下要開始想論文題目、或換過一次題目要重新找方向。 | 帶研究生從沒有方向收斂出一句話的研究想法：依「領域→主題→子題→題目→研究問題」一輪推進一層，每輪結論寫成可貼進 Notion 或 Obsidian 的進度筆記，資訊不夠時請使用者先去讀文獻。使用者完全沒有題目、只有大到不能當題目的領域興趣（「我想做 AI 相關的」「想做資安但不知道做什麼」「老師叫我自己想題目」），或指導教授給了研究計畫、要從計畫切出自己的題目時使用；例如碩一下開始想題目、題目被打槍要重找方向。期刊與研討會清單以資管（MIS/IS）領域為主。不用於：已經寫得出一句話研究想法、要看站不站得住（用 research-question-audit）；只問下一步、工具該照什麼順序用（用 thesis-roadmap）；檢查文字寫法（用 academic-writing-discipline）；直接找某主題的文獻。 |

改了什麼：先寫做什麼（T5）；第二人稱改成第三人稱（問題 2）；補老師計畫（問題 1）；補資管範圍（問題 3）；排除條件補 thesis-roadmap、academic-writing-discipline、找文獻（問題 4）。

---

### 3.3 research-question-audit

**基本數據**

| 項目 | 值 | 對照 |
|---|---|---|
| name | `research-question-audit`（23 字元） | N1 符合；名詞片語，N2 可接受 |
| description 字數 | 183 字元（UTF-8 513 bytes） | D1、D6 符合 |
| 主要用途在最前面 | 是 | D6 符合 |
| 人稱 | 混用：「陪你從零想題目」用第二人稱 | **D3 不符** |
| SKILL.md 本文行數 | 168 行（約 5,500 字元） | L1 符合；L3 見第六節 |

**references 指向檢查（孤兒檔）**

| 檔案 | 行數 | SKILL.md 提到次數 | 超過 100 行有目錄？ |
|---|---|---|---|
| `audit-checklist.md` | 67 | 7 | 不適用 |
| `gap-and-innovation.md` | 58 | 2 | 不適用 |
| `question-forms.md` | 58 | 4 | 不適用 |

孤兒檔：無。`audit-checklist.md` 指到 `gap-and-innovation.md`、`question-forms.md` 指到 `audit-checklist.md`，SKILL.md 都直接指到，不算 R2 的多層引用。

**逐項對照**

| 檢查項 | 結果 |
|---|---|
| 何時用 | 清楚：已經有具體研究問題或想法（哪怕一句話雛型），想知道站不站得住 |
| 何時不用 | 模糊：「本 SKILL 會建議先做別的事再回來」沒點名該用哪個 SKILL；沒排除寫作品質與研究設計後段 |
| 與其他 SKILL 分界 | 與 academic-writing-discipline 在「研究問題句子怎麼寫」「變數名稱」重疊；與 research-direction-finding 的交棒不對稱 |
| 長度與拆分 | 符合 |

**問題**

1. **「何時不用」沒點名 research-direction-finding，本文也沒有。** description 寫「本 SKILL 會建議先做別的事再回來」；本文 §1 對只有領域興趣的使用者說「建議先用收斂漏斗自己收斂」。但 research-direction-finding 與 thesis-roadmap 都寫明沒方向要用 research-direction-finding，這裡是三個 SKILL 中唯一沒對上的交棒。依據：D5；R4（同一件事三處說法不同）。
2. **沒排除寫作品質與研究設計後段。** 本文 §0 寫明不管「問卷題項編寫、量表選取、統計分析實際跑法」，description 沒寫；也沒寫段落寫法交給 academic-writing-discipline。「TAM 量表要用哪個版本」「研究動機這段寫得順不順」可能誤觸。變數名稱的分界見 3.1 問題 6。依據：D5、T3。
3. **缺使用者會講的關鍵詞。** 使用者多半說「研究缺口」「依變數」「口委會怎麼問」「計畫書題目」「會不會做不完」，description 只有「站得住腳」「邏輯漏洞」。依據：D4、T2。
4. **用第二人稱。**「陪你從零想題目」。依據：D3。

**description 原文與改寫版**

| 原文（183 字元） | 改寫版（366 字元） |
|---|---|
| 當使用者已經有一個具體的論文研究問題或研究想法（哪怕只是一句話的雛型），想知道這個題目能不能站得住腳、抓不抓得出邏輯漏洞時使用。本 SKILL 做的是「稽核已有的想法」，不是「陪你從零想題目」——如果使用者完全沒有方向、只想要一個題目，本 SKILL 會建議先做別的事再回來。適用於研究問題發想 0→1 階段的稽核，例如碩士論文計畫書、學期報告題目定案前的自我檢查。 | 稽核使用者已經有的論文研究問題或研究想法（哪怕只是「我想研究 A 對 B 的影響」這種一句話雛型），一次跑完研究缺口分類、收斂程度、題目定案六問、壞題目比對、研究問題句型（含是非問句紅線）、目的到結論的一致性與對抗式審查，輸出稽核報告與口試委員可能的質詢清單。使用者想知道題目站不站得住、缺口講不講得通、依變數清不清楚、資料拿不拿得到、兩年做不做得完、題目與假說的變數對不對得上、口試會被怎麼問時使用，例如計畫書或題目定案前的自我檢查、從老師計畫切出的子題能不能獨立成一篇。不用於：完全沒有方向、只有領域興趣（用 research-direction-finding）；檢查段落文字、用語或 APA 格式（用 academic-writing-discipline）；問卷題項怎麼寫、量表選哪個、統計怎麼跑（本 SKILL 不管）。 |

改了什麼：先寫做什麼並列出檢查點（T5、D4）；補使用者會講的關鍵詞（問題 3）；點名 research-direction-finding（問題 1）；補寫作與研究設計後段的排除（問題 2）；刪掉第二人稱（問題 4）。本文 §1 的交棒說法也建議同步改成點名 research-direction-finding，不過這次只檢查，沒有改。

---

### 3.4 thesis-roadmap

**基本數據**

| 項目 | 值 | 對照 |
|---|---|---|
| name | `thesis-roadmap`（14 字元） | N1 符合；名詞片語，N2 可接受 |
| description 字數 | 312 字元（UTF-8 718 bytes） | D1、D6 符合 |
| 主要用途在最前面 | 是 | D6 符合 |
| 人稱 | 第三人稱（「我論文卡住了」是引用使用者的話） | D3 符合 |
| SKILL.md 本文行數 | 58 行（約 2,200 字元） | L1、L3 符合 |

**references 指向檢查**：沒有 references 目錄，不適用。

**逐項對照**

| 檢查項 | 結果 |
|---|---|
| 何時用 | 清楚：不知道下一步、不確定在哪個階段、問 SKILL 順序、問某階段有沒有工具，並附三個例句 |
| 何時不用 | 清楚：三種情況各自點名對應 SKILL |
| 與其他 SKILL 分界 | 四個 SKILL 裡寫得最完整；風險在與「直接回答」的分界，見問題 1 |
| 長度與拆分 | 符合 |

**問題**

1. **「某個階段有沒有工具可用」可能誤觸實質問題。** 0.5.0 為了讓「這個階段有工具可以幫我嗎」觸發，加了「問某個階段（讀文獻、設計問卷、跑統計、準備口試）有沒有工具可用」。這串關鍵詞很容易跟「Likert 要五點還七點」「CR 不到 0.7 怎麼辦」「口試簡報要幾頁」這類實質問題對上；這些問題使用者要的是答案，叫用本 SKILL 只會得到一個網站連結。description 沒寫這種情況不用。iteration-9 的反例只有原本三個 SKILL 的 6 題，沒有測這類實質問題。依據：T3、D5。
2. **沒有輸出品質評測。** CHANGELOG 0.5.0 寫「只跑了觸發評測，輸出品質還沒有評測」，SKILL 目錄底下也沒有 `evals/evals.json`（其他三個都有）。觸發評測有 5 題正例，R5 的「至少三個評測」就觸發而言算有；輸出品質（判斷階段對不對、有沒有附對頁面）沒有。依據：R5。

**description 原文與改寫版**

| 原文（312 字元） | 改寫版（406 字元） |
|---|---|
| 當使用者不知道論文現在該做什麼、不確定自己在哪個階段，或問 thesis-toolkit 的幾個 SKILL 該先用哪個、整體順序怎麼走，或問某個階段（讀文獻、設計問卷、跑統計、準備口試）有沒有工具可用時使用，例如「我論文卡住了，不知道下一步」「這幾個工具要照什麼順序用」「接下來要讀文獻，有工具可以幫我嗎」。本 SKILL 只判斷階段、指出下一步，不做任何稽核。使用者說自己完全沒方向，直接用 research-direction-finding；已經貼出研究想法要人看站不站得住，直接用 research-question-audit；貼出文字要檢查寫法，直接用 academic-writing-discipline。 | 判斷研究生的論文在 0→1 的哪個階段，指出下一個該用的 thesis-toolkit SKILL 並附開口範例，本身不做任何稽核。使用者不知道論文現在該做什麼、不確定自己在哪個階段、問這幾個 SKILL 該先用哪個、整體順序怎麼走，或問某個階段（讀文獻、設計問卷、跑統計、準備口試）有沒有工具可用時使用，例如「我論文卡住了，不知道下一步」「這幾個工具要照什麼順序用」「接下來要讀文獻，有工具可以幫我嗎」。不用於：使用者說自己完全沒方向（用 research-direction-finding）；已經貼出研究想法要人看站不站得住（用 research-question-audit）；貼出文字要檢查寫法（用 academic-writing-discipline）；直接問問卷、統計、文獻檢索或口試的實質問題，例如「Likert 要用五點還七點」「CR 不到 0.7 怎麼辦」（直接回答，不用本 SKILL）。 |

改了什麼：先寫做什麼（T5）；排除條件統一成「不用於：」格式；補實質問題的排除與兩個例句（問題 1）。問題 2 不是 description 的事，需要另外補評測。

---

## 四、觸發測試題（80 題）

每個 SKILL 10 題應觸發、10 題不該觸發。不該觸發的題目「預期」欄寫的是應該叫用的 SKILL，「無」表示應由 Claude 直接回答、不叫用 thesis-toolkit 的任何 SKILL。標「邊界」的題目是目前 description 沒劃清界線、預期會分歧的情境，用來驗證改寫版。

題目沒有實跑過，見文件開頭的限制。

### A. academic-writing-discipline

**應觸發**

| # | 使用者會這樣講 | 測什麼 |
|---|---|---|
| A-1 | 幫我看這句有沒有大陸用語：「本研究通過問卷收集數據，探討用戶對人工智能的接受度。」 | 單項問法：用語 |
| A-2 | 「知覺有用性導致使用意圖上升」這樣寫算不算因果越線？我是發問卷的橫斷面 | 單項問法：因果動詞 |
| A-3 | 這句會不會中間肥大：「本研究以台灣地區曾使用生成式 AI 工具進行課業學習之大學生為研究對象。」 | 單項問法：構句 |
| A-4 | 老師說我第二章讀起來很像 AI 寫的，可以幫我抓一下哪裡 AI 感很重嗎？（附一段文字） | 去 AI 感 |
| A-5 | 我這段寫 Davis et al.（1989）& Venkatesh，中文論文這樣引用可以嗎？ | APA 7 中文化 |
| A-6 | 下禮拜口試，講稿這段幫我順一下，順便看標點有沒有亂用（附講稿） | 口試講稿、標點 |
| A-7 | 「兩者之間存在顯著的正向關係」這樣寫 OK 嗎？ | 單項問法：弱動詞「存在」 |
| A-8 | 幫我看緒論這幾段，有沒有把研究缺口講出來？老師說看不出來我要補什麼（附緒論） | **邊界**：章節結構（CARS move ②）；原 description 沒寫，改寫版補上 |
| A-9 | 方法章這段我只寫了怎麼抽樣，老師說要補為什麼這樣抽，幫我看還缺什麼（附方法章） | 章節結構（How 與 Why）；原 description 沒寫 |
| A-10 | 參考文獻這幾筆格式對不對？中英文混在一起我搞不清楚順序（附參考文獻） | APA 7 參考文獻 |

**不該觸發**

| # | 使用者會這樣講 | 預期 | 為什麼容易混 |
|---|---|---|---|
| A-11 | 我的研究問題寫成「社群媒體使用是否影響幸福感？」，這樣問可以嗎？ | research-question-audit | 看起來是「一句話寫得對不對」，實際是研究問題句型（是非問句紅線） |
| A-12 | 我想研究遠距工作對工作滿意度的影響，這題目會不會太大？ | research-question-audit | 有「影響」一詞，容易聯想到因果動詞 |
| A-13 | 我寫「台灣還沒有人做過」當研究缺口，這樣算情境缺口嗎？ | research-question-audit | 都在講「研究缺口」 |
| A-14 | 我文獻回顧的邏輯到底通不通？論證有沒有撐住我的假說？ | 無（本 SKILL 已移除論證鏈檢查） | **邊界**：貼了文獻回顧，像寫作檢查；原 description 沒排除 |
| A-15 | 題目寫「使用意圖」、假說寫「使用意願」、架構圖又寫「採用意圖」，整份研究會不會對不上？ | research-question-audit | **邊界**：與「同一構念兩個譯名」重疊，見 3.1 問題 6 |
| A-16 | 資管所碩一，完全不知道論文要做什麼 | research-direction-finding | 「論文」「寫」等字眼 |
| A-17 | 論文寫到第二章了，接下來該做什麼？這套工具有東西可以幫我嗎？ | thesis-roadmap | 提到「寫到第二章」 |
| A-18 | SmartPLS 跑出來 AVE 0.48，這樣區辨效度會過嗎？ | 無（統計實質問題） | 「區辨效度」在本 SKILL 的用語替換表裡 |
| A-19 | 幫我把這段中文摘要翻成英文，要投研討會 | 無 | 學術文字、投稿 |
| A-20 | 幫我寫一段 TAM 的文獻回顧，大概 500 字 | 無（起草不在本 SKILL 現行範圍） | **邊界**：references 有起草端規則，見 3.1 問題 3；維護者若決定涵蓋起草，這題要移到「應觸發」 |

### B. research-direction-finding

**應觸發**

| # | 使用者會這樣講 | 測什麼 |
|---|---|---|
| B-1 | 碩一下了還完全沒有題目，老師叫我自己想，我該從哪裡開始？ | 起點 A |
| B-2 | 我想做 AI 相關的，但範圍好大，不知道怎麼縮小 | 起點 B |
| B-3 | 對資安有點興趣，可是不知道能做什麼研究 | 起點 B |
| B-4 | 題目被老師打槍了，要重找方向，好崩潰 | 換題重找 |
| B-5 | 老師有接一個國科會計畫在做智慧醫療，叫我從裡面找一塊當論文，要怎麼切？ | **邊界**：起點 C；原 description 沒寫，改寫版補上 |
| B-6 | 什麼題目都可以啦，畢得了業就好，有沒有方法幫我生出一個方向？ | 起點 A |
| B-7 | 我對電商跟推薦系統有點興趣，可以陪我一層一層收斂成題目嗎？ | 漏斗 |
| B-8 | 打開空白 Word 檔完全不知道要研究什麼 | 起點 A |
| B-9 | 學長說可以去看 MISQ 的主題分類找方向，那要怎麼看？ | 策略一 |
| B-10 | 上次聊到我想做 ESG 跟資訊揭露，進度筆記貼在下面，接著往下收 | 續接進度筆記 |

**不該觸發**

| # | 使用者會這樣講 | 預期 | 為什麼容易混 |
|---|---|---|---|
| B-11 | 我想研究知覺風險對行動支付使用意圖的影響，這題目站得住嗎？ | research-question-audit | 都在講「題目」 |
| B-12 | 幫我看研究問題有沒有邏輯漏洞：「探討 ChatGPT 使用對大學生學習成效之研究」 | research-question-audit | 題目還很粗，容易被當成「沒方向」 |
| B-13 | 我已經想好要做遠距工作者的科技壓力跟離職傾向，但老師說缺口講不清楚 | research-question-audit | 有「老師說」、像要重找方向 |
| B-14 | 老師計畫裡我負責的子題已經寫成一句了：「探討醫護人員對 AI 診斷輔助的信任與使用意圖」，幫我看站不站得住 | research-question-audit | **邊界**：老師計畫（起點 C），但已經寫成一句話，依本文 §2.3 直接交棒稽核 |
| B-15 | 我論文卡住了，不知道下一步要幹嘛，這幾個工具要照什麼順序用？ | thesis-roadmap | 「不知道要做什麼」 |
| B-16 | 稽核報告說我「需重新收斂」，那我接下來要用哪個工具？ | thesis-roadmap | 「重新收斂」是本 SKILL 的工作，但使用者問的是用哪個工具 |
| B-17 | 幫我找生成式 AI 用在教育的文獻，最好是近五年的 | 無 | 本 SKILL 有「交給使用者去讀文獻」的流程 |
| B-18 | MISQ 跟 ISR 哪個比較好投？ | 無 | 期刊名在 venues.md 裡 |
| B-19 | 這段研究背景是不是寫得太像 AI？（附一段文字） | academic-writing-discipline | 研究背景是緒論，常跟找方向一起出現 |
| B-20 | SEM 跟 PLS-SEM 我該選哪個？ | 無 | 研究設計階段的提問 |

### C. research-question-audit

**應觸發**

| # | 使用者會這樣講 | 測什麼 |
|---|---|---|
| C-1 | 我想研究 IG 使用時間對大學生自尊的影響，幫我看這題目站不站得住 | 基本情境 |
| C-2 | 下個月要報計畫書，題目「探討遠距工作者之科技壓力」可以先幫我抓漏洞嗎？ | 計畫書前自我檢查 |
| C-3 | 我的研究缺口寫「台灣還沒有人做過」，這樣口委會不會電我？ | 情境缺口紅線（關鍵詞「研究缺口」） |
| C-4 | 研究問題寫「員工數位素養是否影響工作績效？」這樣問有沒有問題？ | 是非問句紅線（與 A-11 互為對照） |
| C-5 | 題目是「企業導入 ERP 之研究」，我自己也講不太清楚依變數是什麼 | 壞題目①（關鍵詞「依變數」） |
| C-6 | 我同時想看信任、滿意度、忠誠度、口碑跟回購意圖，這樣會不會做不完？ | 壞題目②、可行性 |
| C-7 | 幫我模擬一下口試委員會怎麼質疑我的題目：「LINE 官方帳號互動對品牌忠誠度的影響」 | 對抗式審查、質詢清單 |
| C-8 | 我要做設計科學研究，研究問題這樣寫合不合 DSR 的格式？（附研究問題） | 句型（DSR） |
| C-9 | 老師計畫切給我的子題我寫成一句了：「探討智慧工廠導入對基層員工工作自主性的影響」，這能獨立撐一篇碩論嗎？ | 起點 C 交棒 |
| C-10 | 我打算發問卷給上市公司的資訊長，這題目兩年做得完嗎？ | 資料可得性、可行性 |

**不該觸發**

| # | 使用者會這樣講 | 預期 | 為什麼容易混 |
|---|---|---|---|
| C-11 | 我還沒有任何方向，只知道想做 AI | research-direction-finding | 原 description 只說「建議先做別的事」，沒點名 |
| C-12 | 題目被打槍了，想整個換方向，不知道去哪找新題目 | research-direction-finding | 都在講「題目」 |
| C-13 | 這段假說推導有沒有因果動詞越線？（附一段文字） | academic-writing-discipline | 假說是一致性檢查鏈的一環 |
| C-14 | 「本研究旨在探討社群媒體使用對大學生學業拖延之影響」這句會不會太長、中間肥大？ | academic-writing-discipline | 句子本身是研究目的，但問的是構句 |
| C-15 | 幫我把研究動機這段改得通順一點，老師說讀起來很卡 | academic-writing-discipline | 研究動機跟研究問題放在同一章 |
| C-16 | 問卷題項要怎麼改，才不會變成一題問兩件事？ | 無（本文 §0：問卷題項編寫不在範圍） | 研究設計相關 |
| C-17 | TAM 的量表要用 Davis 1989 還是 Venkatesh 2003 的版本？ | 無（量表選取不在範圍） | 檢查點 G 有「測量工具信效度」 |
| C-18 | 迴歸跑出來 VIF 很高，要怎麼處理？ | 無（統計跑法不在範圍） | 「分析」是一致性檢查鏈的一環 |
| C-19 | 我現在到底在哪個階段？要先用哪個工具？ | thesis-roadmap | 「階段」 |
| C-20 | 參考文獻裡的期刊名稱要不要斜體？ | academic-writing-discipline | 計畫書格式問題 |

### D. thesis-roadmap

**應觸發**

| # | 使用者會這樣講 | 測什麼 |
|---|---|---|
| D-1 | 我論文卡住了，不知道下一步要做什麼 | 基本情境 |
| D-2 | thesis-toolkit 這幾個 skill 要照什麼順序用？ | 工具順序 |
| D-3 | 題目稽核過了，接下來要讀文獻，有工具可以幫我嗎？ | 某階段有沒有工具 |
| D-4 | 我現在算在哪個階段？已經有題目，但還沒開始寫 | 判斷階段 |
| D-5 | 準備口試這個階段，這套工具有東西可以用嗎？ | 某階段有沒有工具 |
| D-6 | 稽核報告總結是「需修正後再議」，那我下一步要幹嘛？ | 階段轉換 |
| D-7 | 剛裝這個 plugin，從哪一個開始用比較好？ | 入口 |
| D-8 | 問卷設計有工具可以幫忙嗎？還是要自己來？ | 某階段有沒有工具 |
| D-9 | 寫到一半發現好像是題目本身有問題，要回頭用哪個？ | 退回前一段 |
| D-10 | 跑統計的階段，toolkit 有對應的 SKILL 嗎？ | 某階段有沒有工具 |

**不該觸發**

| # | 使用者會這樣講 | 預期 | 為什麼容易混 |
|---|---|---|---|
| D-11 | 碩一，完全沒方向，老師叫我自己想題目 | research-direction-finding | 「不知道做什麼」 |
| D-12 | 我想做資安，但範圍太大，要怎麼縮？ | research-direction-finding | 像在問下一步 |
| D-13 | 我想研究短影音成癮對學業表現的影響，幫我看站不站得住 | research-question-audit | 題目階段 |
| D-14 | 我的研究問題是是非問句，要怎麼改？ | research-question-audit | 像在問怎麼辦 |
| D-15 | 幫我檢查這段的寫法（附一段文字） | academic-writing-discipline | 寫作階段 |
| D-16 | 這段方法章有沒有交代為什麼選問卷法？（附方法章） | academic-writing-discipline | 「方法」是 thesis-roadmap 第 3 節的項目 |
| D-17 | Likert 量表要用五點還是七點？ | 無 | **邊界**：「設計問卷」是 description 的關鍵詞，見 3.4 問題 1 |
| D-18 | CR 不到 0.7 要怎麼處理？ | 無 | **邊界**：「跑統計」是 description 的關鍵詞 |
| D-19 | 怎麼用 Google Scholar 找高引用的文獻？ | 無 | **邊界**：「讀文獻」是 description 的關鍵詞 |
| D-20 | 口試簡報一般要放幾頁？ | 無 | **邊界**：「準備口試」是 description 的關鍵詞 |

**題數**：應觸發 40 題、不該觸發 40 題，共 80 題；其中 10 題標「邊界」。

---

## 五、相鄰 SKILL 容易混淆的情境與歸屬

| 情境 | 建議歸屬 | 目前 description 有沒有寫清楚 |
|---|---|---|
| 沒方向／只有領域興趣 | research-direction-finding | research-direction-finding、thesis-roadmap 有；research-question-audit 沒點名 |
| 老師計畫，還沒寫成一句話 | research-direction-finding | 只有 thesis-roadmap 的本文有，research-direction-finding 的 description 沒有 |
| 老師計畫，已寫成一句話 | research-question-audit | 都沒寫，靠 research-direction-finding 本文 §2.3 |
| 研究問題句型（是非問句） | research-question-audit | academic-writing-discipline 有排除「研究問題怎麼問」 |
| 緒論有沒有交代研究缺口 | academic-writing-discipline（chapter-structure） | 沒有；academic-writing-discipline 反而把「研究缺口」寫成排除項 |
| 缺口屬於哪一類 | research-question-audit | 有 |
| 段落內同一構念譯名不一 | academic-writing-discipline | 有（但寫在本文必掃清單，不在 description） |
| 題目、研究問題、假說三處變數名稱對不上 | research-question-audit | 都沒寫 |
| 文獻回顧論證撐不撐得住 | 無（已移除） | 沒有 |
| 從零起草段落 | 無（現行範圍）或 academic-writing-discipline（若擴大） | 沒有，待維護者決定 |
| 問卷、量表、統計的實質問題 | 無 | research-question-audit 本文有，description 沒有；thesis-roadmap 沒有 |
| 不知道下一步、工具順序 | thesis-roadmap | 有 |

---

## 六、待實測與未計入問題數的觀察

以下幾項有依據但不確定，沒算進第二節的問題數：

1. **本文 token 數可能接近或超過 5k（L3）。** research-question-audit 本文約 5,500 字元、academic-writing-discipline 約 5,200 字元，中文每字常佔一個以上 token，兩者可能超過 OV 建議的 5k token。這次沒有實際計算 token，要確認請用 token counting API 量。另外 L4 提到壓縮後只保留每個 skill 前 5,000 token，academic-writing-discipline 前面的授權、聲明、評測歷史會佔掉一部分。
2. **網頁版 description 長度上限。** `evals/iteration-9/README.md` 寫「網頁版的 `description` 上限 200 字元」。這次讀的三頁官方文件只寫 1,024 字元（D1），沒有找到 200 字元的規定，這次沒有查證。四個 description 都超過 200 字元，要上傳 claude.ai 前請另外確認。
3. **命名風格（N2）。** 四個 name 都是名詞片語，屬於 BP 列的「Acceptable alternatives」，彼此風格一致，不算問題。
4. **SKILL 目錄的 `evals/evals.json` 沒被 SKILL.md 指到。** 這是開發用的評測檔，不是給 Claude 讀的 reference，不算孤兒檔。
5. **`grep-checks.sh` 125 行沒有目錄。** 它是給使用者在本機執行的腳本，BP 說腳本執行時只有輸出進 context，不適用 R3。
6. **`when_to_use` 欄位（T1）。** 改寫版的觸發例句都放在 description 裡。Claude Code 支援把觸發例句移到 `when_to_use`，但 CC「Using skill frontmatter outside Claude Code」寫明 claude.ai 上傳與 Skills API 只接受 `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools` 六個欄位，這個 plugin 若也要給網頁版用，放在 description 比較保險。
