# Skill Benchmark: research-question-audit (iteration-3)

**Model**: claude-sonnet-5
**Date**: 2026-09-07
**Evals**: 4 test cases, 1 run each per configuration (with_skill / without_skill)

> 對照組：iteration-1（n=2, delta +0.25, 未跑計時/token）、iteration-2（未完成，無 benchmark）。本輪是 SKILL.md 新增「引導完成」一節、論證鏈判準修正之後，第一次跑出的乾淨當前版本數據。

## Summary

| Metric | with_skill | without_skill | Delta |
|---|---|---|---|
| Pass Rate | 95.8% ± 8.3% | 70.4% ± 24.7% | +0.25 |
| Time | 208.7s ± 96.3s | 78.3s ± 31.0s | +130.4s |
| Tokens | 89,393 ± 7,444 | 66,284 ± 2,097 | +23,109 |

## Per-case breakdown

| Case | with_skill | without_skill | delta | 備註 |
|---|---|---|---|---|
| eval-1 bad-title-no-dv（沿用iter1） | 1.00 | 1.00 | 0.00 | 舊4條assertion鑑別力弱，真正差異（情境缺口兩欄判準）未被測到 |
| eval-2 too-many-dvs（沿用iter1） | 1.00 | 0.75 | +0.25 | 差距乾淨落在「是非問句紅線」這條skill特有規則 |
| eval-3 gai-dependency-vague-dv（沿用iter2 prompt，補齊assertions與without組） | 1.00 | 0.40 | +0.60 | 本輪最大delta，差距集中在三個結構化框架（五缺口/六長相/引導邀請句） |
| eval-4 mature-thesis-false-positive-check（本輪全新設計） | 0.83 | 0.67 | +0.17 | baseline意外很強，獨立抓到班級層級混淆這個專業問題 |

## 重要觀察

1. **without_skill 的變異度（stddev 24.7%）遠高於 with_skill（8.3%）**：baseline 在不同案例上表現從 1.00 到 0.40 都有，波動很大；with_skill 穩定落在 0.83-1.00。這比單看平均 delta 更能說明 skill 的實際價值——不是每次都讓輸出變好一點，而是把「表現隨案例大幅波動」收斂成穩定的高水準結構化輸出。
2. **skill 的邊際價值集中在三個 SKILL.md 明文規定的結構化機制**：五種缺口分類框架、六種壞題目長相具名比對、是非問句紅線。這些是規則性強、需要照著特定文件跑一遍才會系統性覆蓋的判準，baseline（一般研究方法知識）不會自發產生。
3. **baseline 本身的研究方法論判斷力不弱**：eval-4 的 without_skill 獨立抓到一個相當專業的方法論問題（k=2 班級層級混淆／pseudoreplication），顯示 Sonnet 本身在方法論審查上已有一定水準，skill 的加值不是「從零到有」，而是「把隱性判斷力轉成系統性、不遺漏的檢查清單」。
4. **eval-4 的一條 assertion 判定「不通過」，經覆核是我設計 test case 時的判斷誤差（我以為自己寫的是理論缺口，但對照 gap-and-innovation.md 的定義，更貼近情境缺口），with_skill 的重分類其實是正確遵照 references 文件的表現，不宜解讀為 skill 缺陷。

## 樣本數與可信度

n=4 個 case，每案例只跑 1 次，無法做統計推論。eval-2 與 eval-3 的 delta 是本輪最乾淨、最可信的正向訊號（差距可歸因到明確的 SKILL 規則）；eval-1 與 eval-4 各自有測試設計上的局限（見上方觀察 1、4），解讀時需要一併參考。

## Rubric

見 `../RUBRIC.md`（兩個 skill 共用）。
