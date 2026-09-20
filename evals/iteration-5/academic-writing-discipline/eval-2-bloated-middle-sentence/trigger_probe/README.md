# AWD eval-2 的 skill 觸發重現測試

正式執行時發現這個 case 的 `with_skill` 臂 `num_turns=1`，與 `without_skill` 同一個量級，
代表模型沒有叫用 Skill 工具。用完全相同的 CLI 參數另外跑兩次確認是否為隨機現象。

| 執行 | num_turns | tokens |
|---|---|---|
| 正式執行（with_skill） | 1 | 29,408 |
| 重現測試 1 | 1 | 29,626 |
| 重現測試 2 | 1 | 29,632 |

三次都是 `num_turns=1`，是穩定現象。這兩次重現測試的產出只作為佐證留檔，沒有取代
`with_skill/` 底下的正式執行資料，也沒有進入 `benchmark.json`。
