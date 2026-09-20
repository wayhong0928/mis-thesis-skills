# AWD eval-2 的 skill 觸發測試

## 問題

iteration-5 正式執行時發現這個 case 的 `with_skill` 臂 `num_turns=1`，與 `without_skill`
同一個量級，代表模型沒有叫用 Skill 工具。用完全相同的 CLI 參數另外跑兩次確認不是隨機現象。

| 執行 | num_turns | tokens |
|---|---|---|
| 正式執行（with_skill） | 1 | 29,408 |
| 重現測試 1 | 1 | 29,626 |
| 重現測試 2 | 1 | 29,632 |

三次都是 `num_turns=1`。原因是當時的 `description` 寫的是「檢查**一段**中文學術論述」「一次跑完
全部判準」，而這題的提問是單一句子加單一項目（「我這句話會不會有『中間肥大』的問題」），
兩邊對不上，模型判斷不叫 SKILL 也答得出來。

## 修法與驗證

`SKILL.md` 的 `description` 改了三處：明講一句話也算、把使用者可能引用的內部術語
（中間肥大、話題漂移、「存在」濫用、易爆句型）寫進去讓它們可被比對、以及寫明
「問題範圍窄不是略過本 SKILL 自己回答的理由」。改完用同一個 prompt 與同一組 CLI 參數實測：

| 執行 | num_turns | tokens |
|---|---|---|
| 改 description 後 1 | 5 | 110,839 |
| 改 description 後 2 | 5 | 108,198 |

兩次都觸發。

## 這些檔案的地位

`probe_*` 與 `after_desc_fix_*` 都只是佐證，沒有取代 `with_skill/` 底下的正式執行資料，
也沒有進入 `benchmark.json`。iteration-5 的 AWD 數字仍然是「description 修正前」的結果，
要拿到修正後的數字必須重跑整個 AWD。
