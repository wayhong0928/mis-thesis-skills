# iteration-10 結果（評分：final）

| 方 | 偵測 G | 偵測 N | 偵測合計 | 誤報 | 沒叫用 Skill 的執行 | low confidence 判定 |
|---|---|---|---|---|---|---|
| grep 基線 | 6/6 | 0/6 | 6/12 | 見 VERDICT | — | — |
| without_skill | 9/18 | 18/18 | 27/36 | 0/21 | 15/15 | 13 |
| v0.5.2 | 13/18 | 16/18 | 29/36 | 0/21 | 0/15 | 8 |

0.5.2 只算有叫用 Skill 的執行：植入題 9 次、乾淨題 6 次；偵測 G 13、N 16，誤報 0。

| 案例 | 斷言 | without_skill | v0.5.2 |
|---|---|---|---|
| c1-litreview-clean | f1 | 3/3 | 3/3 |
| c1-litreview-clean | f2 | 3/3 | 3/3 |
| c1-litreview-clean | f9 | 3/3 | 3/3 |
| c2-discussion-clean | f1 | 3/3 | 3/3 |
| c2-discussion-clean | f2 | 3/3 | 3/3 |
| c2-discussion-clean | f3 | 3/3 | 3/3 |
| c2-discussion-clean | f9 | 3/3 | 3/3 |
| p1-litreview-planted | d1 | 3/3 | 3/3 |
| p1-litreview-planted | d2 | 3/3 | 3/3 |
| p1-litreview-planted | d3 | 3/3 | 1/3 |
| p1-litreview-planted | d4 | 3/3 | 3/3 |
| p2-discussion-planted | d1 | 3/3 | 3/3 |
| p2-discussion-planted | d2 | 1/3 | 0/3 |
| p2-discussion-planted | d3 | 1/3 | 3/3 |
| p2-discussion-planted | d4 | 3/3 | 3/3 |
| p3-implication-planted | d1 | 3/3 | 3/3 |
| p3-implication-planted | d2 | 1/3 | 1/3 |
| p3-implication-planted | d3 | 0/3 | 3/3 |
| p3-implication-planted | d4 | 3/3 | 3/3 |

問題一：0.5.2 偵測率 0.806，grep 0.500，G 類 13/18 → **勝過 grep**
問題二：0.5.2 比沒裝多 2 條（G +4、N -2），誤報 0 vs 0 → **方向一致但不足**
