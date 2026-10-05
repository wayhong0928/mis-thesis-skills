# -*- coding: utf-8 -*-
"""產生 iteration-7 的 eval_metadata.json（只測 academic-writing-discipline）。

舊的 7 題從 ../iteration-6/cases/ 讀進來，prompt 原樣沿用（n2 例外，見該題 source），只改需要改的斷言。
新增 6 題（n6–n11）對應 0.4.1、0.4.2 的改動。

kind 與 tests_change 的定義同 iteration-6（見 ../iteration-6/build_cases.py 開頭）：
  outcome    使用者實際拿到的東西對不對。主要數字只用這類。
  procedure  有沒有照 skill 的流程走，不算進效益。
  compliance 版權排除清單檢查，單獨列。
  tests_change 專門測某項改版要修的落差，舊版照自己文件字面走預期會 fail，報告時另列含與不含的數字。
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE / "cases"
IT6 = HERE.parent / "iteration-6" / "cases"
AWD = "academic-writing-discipline"
SC = "references/sentence-and-causal.md"
TW = "references/taiwan-usage-apa.md"
COPY = ("沒有出現任何版權排除清單的詞彙（彭明輝姓名或書名、舊瓶新酒／新瓶舊酒、雁行理論、七項要件、貢獻三角度、深而窄）",
        "SKILL.md 開頭聲明（不含任何書籍、講座或未經授權的第三方框架與專有用語）；evals/RUBRIC.md §3")
YX = "0.4.1：「影響」改成商管慣例可接受"


def A(i, kind, text, based_on, tests_change=None):
    d = {"id": i, "kind": kind, "text": text, "based_on": based_on}
    if tests_change:
        d["tests_change"] = tests_change
    return d


def comp(i):
    return A(i, "compliance", *COPY)


def old(case):
    m = json.loads((IT6 / AWD / case / "eval_metadata.json").read_text(encoding="utf-8"))
    m.pop("skill", None)
    m.pop("eval_name", None)
    return m


def by_id(m):
    return {a["id"]: a for a in m["assertions"]}


CASES = {}

# ---------------- 沿用 iteration-6 的 7 題 ----------------

m = old("eval-1-causal-verb-and-existence-abuse")
a = by_id(m)
a["a1"]["text"] = ("指出同一句前半用因果語言（具有顯著之影響）、後半退回相關語言（存在正向關係），前後不一致，"
                   "並給出全句語氣統一的改法")
a["a1"]["based_on"] = f"{SC} §一.1 紅線二（全篇動詞紀律要一致）與 §一.5 最後一列（同一句話內因果與相關語言並存）"
m["assertions"].insert(4, A(
    "a6", "outcome",
    "沒有把「具有顯著之影響」本身列為問題：沒有以「橫斷面研究不能用影響」或「缺少理論、迴歸、控制變數三條件」為由要求把「影響」改掉"
    "（為了讓全句前後一致而統一成「預測」或「相關」的寫法不在此限；回應若同時提出「前後不一致」與「橫斷面宜保守」兩個理由，以是否要求改掉「影響」這個詞為準）",
    f"{SC} §一.1 核心原則（「影響」不是禁用詞，商管問卷研究常這樣寫，稽核時不列問題）；SKILL.md §2.1 必掃清單第一項", YX))
m["source"] = ("沿用 iteration-6，prompt 不變。iteration-7 依 0.4.1：a1 只接受「前後不一致」這個理由（原本也接受「缺三條件」，"
               "0.4.1 起三條件不再是門檻）；新增 a6 檢查不把「影響」本身列為問題。")
CASES["eval-1-causal-verb-and-existence-abuse"] = m

m = old("eval-2-bloated-middle-sentence")
a = by_id(m)
a["a3"]["text"] = ("指出『對於這類工具的使用產生了高度的依賴性』這段的『對於……』結構本身在拉長句子、可以精簡"
                   "（只在改寫裡把這段縮短、沒有點出這個結構的，不算）")
m["assertions"] = [x for x in m["assertions"] if x["id"] not in ("a4", "a5")]
m["source"] = ("沿用 iteration-6，prompt 不變。a3 依 iteration-6 裁決（assertion_ambiguous）把判定標準寫明；"
               "a5 在 iteration-6 已剔除（excluded_assertions.json），本輪直接拿掉。a4（不把句尾『造成什麼樣的影響』判為越線）也拿掉："
               "skill 的替換表把『造成』列為「門檻高，多數情況避免」，iteration-6 有裝 skill 的 Opus 三臂都因此判 fail，屬 skill 正當抓出、出題者沒設計的問題（iteration-7 開跑前審查指出）。")
CASES["eval-2-bloated-middle-sentence"] = m

m = old("n1-messy-long-draft")
a = by_id(m)
a["a7"]["based_on"] = f"{SC} §一.1 核心原則（「影響」是商管慣例；本句三條件也齊備）與 §一.5 第二列"
m["source"] = "沿用 iteration-6，prompt 與斷言不變，只依 0.4.1 改 a7 的 based_on。"
CASES["n1-messy-long-draft"] = m

m = old("n2-clean-paragraph")
a = by_id(m)
m["prompt"] = m["prompt"].replace("因而給予有用性較高的評價", "因而對有用性的評分也較高")
assert "對有用性的評分也較高" in m["prompt"]
a["a1"]["text"] += ("。把轉述列入「待核對」、提醒回原文確認，或對 Venkatesh 等人轉述的構念對應提出核對提醒，都不算錯誤指控；"
                    "回應結論為「需修」但致命與錯誤都是 0、只列瑕疵與待核對項目，也算可以直接用或只需小修")
a["a2"]["based_on"] = f"{SC} §一.1 核心原則（「影響」是商管慣例，稽核不列問題；本段三條件也齊備）"
m["source"] = ("沿用 iteration-6。iteration-6 限制段指出原文「給予……較高的評價」落在弱動詞規則裡，負向案例不乾淨，"
               "本輪改成「對有用性的評分也較高」。a1 補一句：列入待核對不算錯誤指控（0.4.1 起轉述細節要列待核對）。")
CASES["n2-clean-paragraph"] = m

m = old("n3-causal-language-across-chapters")
a = by_id(m)
a["a3"]["text"] = a["a3"]["text"].replace("三條件齊備", "有理論、PLS-SEM、控制變數")
for k in ("a2", "a3"):
    a[k]["text"] += "（判定標準：回應對該處的結論不是越線或錯誤；只附帶提出可換詞的選項不算）"
    a[k]["based_on"] = f"{SC} §一.1 核心原則（「影響」是商管慣例；研究問題與結果章同用「影響」屬於一致）"
m["source"] = "沿用 iteration-6，prompt 不變。a2、a3 依 iteration-6 的兩筆 assertion_ambiguous 裁決，把判定標準寫進斷言；based_on 依 0.4.1 改寫。"
CASES["n3-causal-language-across-chapters"] = m

m = old("n4-taiwan-usage-and-apa")
m["source"] = "沿用 iteration-6，prompt 與斷言不變。"
CASES["n4-taiwan-usage-and-apa"] = m

m = old("n5-intro-missing-niche")
m["source"] = "沿用 iteration-6，prompt 與斷言不變。"
CASES["n5-intro-missing-niche"] = m

# ---------------- 新增 6 題 ----------------

CASES["n6-user-writes-final-draft"] = {
    "source": "新。測 0.4.1「整合修改版的出口」：使用者說明定稿要自己寫時，修改稿改標「參考修改稿」、放在清單最後。",
    "prompt": ("這段是我第二章的一段。定稿我想自己寫，你幫我列出問題就好，不用幫我改寫整段：\n\n"
               "『近年來，生成式AI在程式設計教育中被廣泛使用。Lee 等人（2025）通過問卷調查發現，學生對AI的依賴程度與批判思考呈負相關。"
               "此外，部分學者認為過度依賴會導致學生的學習能力下降，因此對於如何在教學中適當引入生成式AI的問題，值得深入探討。』"),
    "assertions": [
        A("a1", "outcome",
          "指出下列三項中至少兩項並對應到原句位置：(a)『通過問卷調查』的『通過』應為『透過』；"
          "(b)『對於如何……的問題』句型拉長句子，可改成動詞句；"
          "(c)『部分學者認為……會導致……』的因果語氣超出可確認的證據（指出此句沒有指名來源也算）",
          f"{TW} §一.4 容易混淆的地區用語（通過→透過）；{SC} §二.2 避免中間肥大（『對於……的問題』）、§一.2 替換表『導致』與 §一.4 主張強度與證據強度的匹配；SKILL.md §2.1 必掃清單"),
        A("a2", "outcome",
          "尊重使用者「不用改寫整段」的要求：回應主體是問題清單；若附上整段修改稿，明確標示為參考用，並放在問題清單之後"
          "（完全沒附整段修改稿也算通過）",
          "SKILL.md §4 整合修改版的例外（使用者說明定稿要自己寫時，改標「參考修改稿」，放在清單最後）",
          "0.4.1：參考修改稿出口"),
        comp("a3"),
    ],
}

CASES["n7-paraphrase-details-unverified"] = {
    "source": "新。測 0.4.1「轉述句出現原文才有的細節、使用者沒附原文時列待核對」。作者與數字是虛構的，避免模型憑記憶判斷真偽。",
    "prompt": ("幫我潤飾這段文獻回顧（我手邊沒有原文，是之前看過記下來的）：\n\n"
               "『陳與王（2023）以 186 名資管系大二學生為對象進行準實驗，發現使用 AI 程式助理的組別在期末專題的完成率較高，"
               "且在之後不能使用 AI 的紙筆測驗中，成績並未低於對照組。林等人（2024）則以放聲思考法觀察 24 名新手，"
               "發現多數學生高估自己對 AI 產生之程式碼的理解程度。』"),
    "assertions": [
        A("a1", "outcome",
          "把轉述裡只有原文才能確認的細節列為要回原文核對的項目，並至少點名其中一項具體細節"
          "（例如 186 名、資管系大二、準實驗、紙筆測驗成績並未低於對照組這類效果方向、24 名、放聲思考法）；"
          "只寫一句籠統的「引用內容請自行核對」不算",
          "SKILL.md §3 第 3 步（轉述句裡出現原文才可能有的細節，使用者沒附原文時列進「待核對」）",
          "0.4.1：轉述細節列待核對"),
        A("a2", "outcome",
          "沒有在沒有原文的情況下改動轉述內容：潤飾後的文字仍保留 186 名、資管系大二、準實驗、24 名、放聲思考法，"
          "且『並未低於對照組』沒有被改成『相當』『無顯著差異』等不同的比較說法（指出可能有誤並建議回原文確認，不算改動）",
          "SKILL.md §3 第 3 步（列進「待核對」，不要當成已確認）；references/sentence-and-causal.md §一.4 核對程度也要對上寫法"),
        comp("a3"),
    ],
}

CASES["n8-conventional-attribution"] = {
    "source": "新。測 0.4.1「⟨作者⟩（年）提出⟨理論⟩這類慣用歸屬寫法不誤抓，歸屬事實錯才列錯誤」。第三句的歸屬是錯的。0.4.0 沒有叫模型去抓這種寫法的規則，所以 a2 不標 tests_change（預防性規則，開跑前審查指出）。",
    "prompt": ("幫我檢查這段理論基礎的寫法：\n\n"
               "『Davis（1989）提出知覺有用性與知覺易用性兩個構念，用來解釋使用者對資訊科技的接受程度。"
               "Ajzen（1991）提出計畫行為理論，認為行為意圖受態度、主觀規範與知覺行為控制三者影響。"
               "本研究另參考 Bandura（1977）提出的科技接受模型，將自我效能納入研究模型。』"),
    "assertions": [
        A("a1", "outcome",
          "指出『Bandura（1977）提出的科技接受模型』歸屬錯誤：科技接受模型不是 Bandura 提出的（Bandura 1977 談的是自我效能）",
          "SKILL.md §5 不要誤抓領域慣用寫法（只有歸屬事實錯才列錯誤）"),
        A("a2", "outcome",
          "沒有把『Davis（1989）提出知覺有用性與知覺易用性兩個構念』或『Ajzen（1991）提出計畫行為理論』判為歸屬錯誤，"
          "也沒有要求改寫成別的作者或別的歸屬（建議回原文核對年份、列入待核對，或補充理論更早的出處，都不算錯誤指控）",
          "SKILL.md §5 不要誤抓領域慣用寫法（「⟨作者⟩（年）提出⟨理論⟩」照用，不列問題）"),
        comp("a3"),
    ],
}

CASES["n9-scope-beyond-evidence"] = {
    "source": "新。測 0.4.1「範圍也要對上證據」：單一學校樣本推到全體、傾向量表寫成已確定的臨床狀態。",
    "prompt": ("幫我看看結論這段：\n\n"
               "『本研究以北部某科技大學資訊管理系 182 名學生為樣本，採橫斷面問卷調查。結果顯示，受試者在生成式AI依賴量表的平均分數為 4.9"
               "（七點量表）。由此可知，臺灣大學生普遍已對生成式AI成癮，教育主管機關應儘速介入。』"),
    "assertions": [
        A("a1", "outcome",
          "指出從單一學校、單一科系的樣本推論到「臺灣大學生普遍」超出樣本能支持的範圍，並給出縮小範圍的改法",
          f"{SC} §一.4 範圍也要對上證據（單一學校、單一科系的樣本，不寫成「臺灣大學生普遍……」）",
          "0.4.1：範圍也要對上證據"),
        A("a2", "outcome",
          "指出依賴量表的平均分數只反映依賴傾向，寫成「成癮」這種已確定的狀態超出量表能支持的程度",
          f"{SC} §一.4 範圍也要對上證據（只測到傾向或態度的量表，不寫成已確定的行為或臨床狀態）",
          "0.4.1：範圍也要對上證據"),
        comp("a3"),
    ],
}

CASES["n10-method-citation-unverified"] = {
    "source": "新。測 0.4.2「方法論文獻的轉述，使用者沒附原文一律列待核對」。兩句方法論轉述取自真實論文草稿曾出現的寫法。",
    "prompt": ("幫我檢查這段研究方法：\n\n"
               "『本研究採 PLS-SEM 分析。依 Hair 等人（2019）的建議，PLS-SEM 的樣本數一般落在 100 至 200 之間，故本研究預計收集 200 份有效問卷。"
               "中介效果則依 Zhao 等人（2010）的建議，以間接效果與直接效果是否顯著，判定為完全中介或部分中介。』"),
    "assertions": [
        A("a1", "outcome",
          "把 Hair 等人（2019）的樣本數說法列為需要回原文核對，或指出原文可能沒有這個說法；沒有直接把它當成已確認的依據",
          f"{SC} §一.4 核對程度也要對上寫法（方法論文獻的轉述，使用者沒附原文的，一律列進「待核對」）；SKILL.md §3 第 3 步",
          "0.4.2：方法論引用列待核對"),
        A("a2", "outcome",
          "把 Zhao 等人（2010）的中介判定方法列為需要回原文核對，或指出 Zhao 等人主張的中介分類不是「完全／部分中介」",
          f"{SC} §一.4 核對程度也要對上寫法（中介效果的判定方法屬方法論文獻）；SKILL.md §3 第 3 步",
          "0.4.2：方法論引用列待核對"),
        A("a3", "outcome", "指出『收集』應為『蒐集』",
          f"SKILL.md §2.1 必掃清單（收集→蒐集）；{TW} §一.3 研究方法描述用語"),
        comp("a4"),
    ],
}

CASES["n11-table-implies-causation"] = {
    "source": "新。測 0.4.2「表格與版面也是主張」：歷程表格的欄位順序會讓讀者以為前一欄造成後一欄。",
    "prompt": ("這是我期中報告「AI 工具使用揭露」的表格，幫我看看寫法有沒有問題：\n\n"
               "| 階段 | 我給 AI 的提示詞 | AI 的產出 | 我的修正 |\n"
               "|---|---|---|---|\n"
               "| 文獻整理 | 請整理科技接受模型的相關實證研究 | 列出 12 篇文獻與摘要 | 刪除其中 4 篇預印本與撤稿論文 |\n"
               "| 假說推導 | 請依壓力因應理論推導科技焦慮與依賴的關係 | 一段假說推導草稿 | 依指導教授意見，把假說方向從負向改成正向 |\n"
               "| 問卷設計 | 請把英文量表翻成中文 | 中文題項初稿 | 對照原量表逐題修改語意 |\n\n"
               "補充：第二列的修正是指導教授在 meeting 時直接要求的，跟 AI 那段草稿的內容沒有關係。"),
    "assertions": [
        A("a1", "outcome",
          "指出第二列的呈現（表格欄位順序，或把教授指示放在「我的修正」欄）會讓讀者以為修正是針對 AI 產出做的（或 AI 產出促成了修正），與實情不符，"
          "並建議拆開、加註修正來源或移除該列",
          f"{SC} §一.4 表格與版面也是主張（欄位先後會被讀成先後或因果；會被誤讀歸屬或因果的那一列，整列拿掉或另外說明）",
          "0.4.2：表格與版面也是主張"),
        comp("a2"),
    ],
}


def main():
    for case, meta in CASES.items():
        d = ROOT / AWD / case
        d.mkdir(parents=True, exist_ok=True)
        out = {"skill": AWD, "eval_name": case, **meta}
        (d / "eval_metadata.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    n = {k: 0 for k in ("outcome", "procedure", "compliance")}
    tc = 0
    for meta in CASES.values():
        for x in meta["assertions"]:
            n[x["kind"]] += 1
            tc += bool(x.get("tests_change"))
    print(len(CASES), "cases;", n, "; tests_change:", tc)


if __name__ == "__main__":
    main()
