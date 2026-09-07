# Skill Benchmark: academic-writing-discipline (iteration-3)

**Model**: claude-sonnet-5
**Date**: 2026-09-07
**Evals**: 3 test cases, 1 run each per configuration (with_skill / without_skill)

> 對照組：iteration-1（n=2, delta +0.10, 未跑計時/token）、iteration-2（未完成，無 benchmark）。本輪是 SKILL.md 因果動詞規則改寫、新增引導完成一節之後，第一次跑出的乾淨當前版本數據。

## Summary

| Metric | with_skill | without_skill | Delta |
|---|---|---|---|
| Pass Rate | 86.7% ± 11.6% | 66.7% ± 11.6% | +0.20 |
| Time | 164.7s ± 66.8s | 65.7s ± 41.4s | +99.0s |
| Tokens | 81,448 ± 7,040 | 65,800 ± 2,721 | +15,649 |

## Per-case breakdown

| Case | with_skill | without_skill | delta | 備註 |
|---|---|---|---|---|
| eval-1 causal-verb-and-existence-abuse（沿用iter1） | 0.80 | 0.60 | +0.20 | 差距來自台灣用語規則（人工智能→人工智慧） |
| eval-2 bloated-middle-sentence（沿用iter1） | 0.80 | 0.80 | 0.00 | 舊assertion(a4)可能因規則改版失去鑑別力 |
| eval-3 good-lit-review-false-positive-check（本輪重建） | 1.00 | 0.60 | +0.40 | delta解讀需保留，without獨立抓到真實論證缺口，見下方警示 |

## 重要警示（務必先讀再用這份數據）

1. **樣本數極小（n=3），每個 case 只跑 1 次**：無法做統計推論，delta 只是方向性觀察。
2. **eval-3 的『假陽性防呆』測試前提可能不成立**：本案例的文獻回顧段落是本輪重建的（原始 prompt 未保存），重建後意外留下一個真實的論證缺口（「迴避因應」的鋪陳沒有回扣到後續的「認知卸載/求助工具使用」變項分類）。without_skill 獨立抓到這個缺口，with_skill 的伏筆兌現檢查因為只看單一段落而給了通過。這代表 eval-3 的 +0.40 delta 有相當比例可能反映「without_skill 找到真實問題」而非「with_skill 沒有價值」，不應該直接當作「skill 讓假陽性防呆能力變好」的證據使用。
3. **eval-2 的 delta=0 不代表 skill 沒用**：0.8/0.8 平手的原因是其中一條沿用自iteration-1的assertion（因果動詞判準）在規則改寫後可能已經過時，對兩邊都不構成鑑別度；真正的構句判準（易爆句型辨識）兩邊表現相近，反映 Sonnet 本身構句分析能力已經不弱。
4. **可信的正向訊號**：eval-1 顯示的 +0.20 delta 落在「台灣學術用語替換」這條需要 SKILL 明文規則才會被系統性套用的判準上，這是本輪唯一一個「delta 乾淨、可歸因、可信」的案例。

## Rubric

見 `../RUBRIC.md`（兩個 skill 共用）。
