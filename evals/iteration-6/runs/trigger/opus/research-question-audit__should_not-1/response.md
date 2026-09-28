## PLS-SEM 和 CB-SEM 的差異

兩者都是結構方程模型（SEM），都能同時估計測量模型和結構模型。差別在於估計邏輯和想回答的問題不同。

### 核心差異

| 面向 | CB-SEM（共變數基礎） | PLS-SEM（變異數基礎／偏最小平方） |
|---|---|---|
| 估計目標 | 讓模型隱含的共變數矩陣盡量接近樣本共變數矩陣 | 盡量提高內生構念被解釋的變異（R²） |
| 研究取向 | 理論驗證（confirmatory） | 預測與探索（predictive / exploratory） |
| 構念的本質 | 共同因素（common factor），把構念當成真正的潛在變數 | 合成變數（composite），把構念當成指標的加權組合 |
| 估計方法 | 多用 ML（最大概似法） | 迭代的 OLS 迴歸 |
| 分配假設 | ML 需要多變量常態 | 無分配假設，用 bootstrapping 檢定顯著性 |
| 樣本數 | 需要較大樣本（一般建議 200 以上） | 小樣本也能跑（但「小樣本萬能」是常見的誤解，見下方） |
| 整體模型配適 | 有完整的配適指標（χ²、CFI、TLI、RMSEA、SRMR） | 缺乏公認的整體配適指標（SRMR 可參考但門檻有爭議） |
| 形成性構念 | 處理困難，有識別問題 | 可以直接處理 |
| 模型複雜度 | 構念或指標太多時容易不收斂 | 複雜模型也能估計 |
| 常用軟體 | AMOS、LISREL、Mplus、R lavaan | SmartPLS、R seminr / cSEM、WarpPLS |

### 怎麼選

**選 CB-SEM：**
- 研究目的是檢驗或比較既有理論
- 構念都是反映性（reflective），而且理論上可以視為共同因素
- 樣本夠大、資料大致常態
- 需要用整體模型配適度說服審查者

**選 PLS-SEM：**
- 研究目的是預測關鍵目標構念，或者理論還在發展階段
- 模型含有形成性（formative）構念
- 模型很複雜（構念多、路徑多、有高階構念）
- 會拿構念分數做後續分析（例如 IPMA）

### 常見誤解（口試常被問）

1. **「樣本小所以用 PLS」**：這不是正當理由。PLS 在小樣本下雖然能跑出結果，統計檢定力仍然有限。樣本數應該用 power analysis 或 inverse square root method 估算（Kock & Hadaya, 2018）。
2. **「資料不常態所以用 PLS」**：現在的 CB-SEM 可以用穩健估計（例如 MLR）或 bootstrapping 處理非常態，這個理由也越來越站不住。
3. **參數偏誤**：用 PLS 估計共同因素模型時，因素負荷量會高估、路徑係數會低估。如果理論上構念就是共同因素，可以考慮 PLSc（consistent PLS）來校正。
4. **選擇理由要跟研究目的扣在一起**：審查者最想看到的是「我的研究目的是預測／探索，所以選 PLS」，而不是只列資料條件。

### 經典參考文獻

- Hair, J. F., Hult, G. T. M., Ringle, C. M., & Sarstedt, M. (2022). *A primer on partial least squares structural equation modeling (PLS-SEM)* (3rd ed.). Sage.
- Hair, J. F., Risher, J. J., Sarstedt, M., & Ringle, C. M. (2019). When to use and how to report the results of PLS-SEM. *European Business Review, 31*(1), 2–24.
- Kline, R. B. (2023). *Principles and practice of structural equation modeling* (5th ed.). Guilford.
- Rigdon, E. E. (2012). Rethinking partial least squares path modeling. *Long Range Planning, 45*(5–6), 341–358.

如果你是在替論文選方法，可以告訴我你的研究目的、模型結構和樣本數，我幫你判斷哪一種比較適合，也可以幫你寫方法章節裡說明選擇理由的那一段。