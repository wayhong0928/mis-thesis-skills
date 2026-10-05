# iteration-7 結果（評分：final）

## academic-writing-discipline

| 模型 | 臂 | outcome | outcome（不含 tests_change） | pass^k | procedure | 假陽性 | tokens | 秒 |
|---|---|---|---|---|---|---|---|---|
| opus | v0.4.0 | 0.985 | 1.0 | 0.985 | 1.0 | 1 | 48820.615 | 37.382 |
| opus | v0.4.2 | 0.936 | 0.818 | 0.936 | 1.0 | 1 | 46250.692 | 35.033 |
| opus | v0.4.3 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 54535.889 | 45.711 |
| opus | without_skill | 0.832 | 0.75 | 0.832 | 0.0 | 2 | 10218.615 | 20.6 |
| sonnet | v0.4.0 | 0.95 | 0.919 | 0.908 | 1.0 | 4 | 49671.872 | 30.994 |
| sonnet | v0.4.2 | 0.962 | 0.899 | 0.91 | 1.0 | 1 | 51608.308 | 31.477 |
| sonnet | v0.4.3 | 0.963 | 0.889 | 0.945 | 1.0 | 0 | 48992.5 | 32.789 |
| sonnet | without_skill | 0.787 | 0.692 | 0.742 | 0.084 | 10 | 9885.667 | 14.403 |

| 案例 | 模型 | 臂 | n | outcome | pass^k | procedure | 假陽性 | 觸發 skill | turns | 逐條 |
|---|---|---|---|---|---|---|---|---|---|---|
| eval-1-causal-verb-and-existence-abuse | opus | v0.4.0 | 1 | 0.8 | 0.8 | None | 1 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a6=0/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a6=1/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | opus | without_skill | 1 | 0.4 | 0.4 | None | 1 | 0/1 | [1] | a1=0/1 a2=0/1 a3=1/1 a4=1/1 a6=0/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | sonnet | v0.4.0 | 3 | 0.8 | 0.8 | None | 3 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a6=0/3 a5=3/3 |
| eval-1-causal-verb-and-existence-abuse | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a6=3/3 a5=3/3 |
| eval-1-causal-verb-and-existence-abuse | sonnet | without_skill | 3 | 0.533 | 0.4 | None | 2 | 0/3 | [1, 1, 1] | a1=1/3 a2=0/3 a3=3/3 a4=3/3 a6=1/3 a5=3/3 |
| eval-2-bloated-middle-sentence | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a6=1/1 |
| eval-2-bloated-middle-sentence | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a6=1/1 |
| eval-2-bloated-middle-sentence | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a6=1/1 |
| eval-2-bloated-middle-sentence | sonnet | v0.4.0 | 3 | 0.889 | 0.667 | None | 0 | 3/3 | [5, 5, 6] | a1=3/3 a2=3/3 a3=2/3 a6=3/3 |
| eval-2-bloated-middle-sentence | sonnet | v0.4.2 | 3 | 0.889 | 0.667 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=2/3 a6=3/3 |
| eval-2-bloated-middle-sentence | sonnet | without_skill | 3 | 0.889 | 0.667 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=2/3 a6=3/3 |
| n1-messy-long-draft | opus | v0.4.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | opus | v0.4.2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | opus | v0.4.3 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | opus | without_skill | 1 | 0.75 | 0.75 | 0.0 | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a5=0/1 a6=1/1 a7=1/1 a8=1/1 a9=0/1 a10=0/1 a11=1/1 |
| n1-messy-long-draft | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [5, 7, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 a8=3/3 a9=3/3 a10=3/3 a11=3/3 |
| n1-messy-long-draft | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 a8=3/3 a9=3/3 a10=3/3 a11=3/3 |
| n1-messy-long-draft | sonnet | v0.4.3 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [5, 6, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 a8=3/3 a9=3/3 a10=3/3 a11=3/3 |
| n1-messy-long-draft | sonnet | without_skill | 3 | 0.75 | 0.75 | 0.167 | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 a4=0/3 a5=0/3 a6=3/3 a7=3/3 a8=3/3 a9=0/3 a10=1/3 a11=3/3 |
| n10-method-citation-unverified | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n10-method-citation-unverified | opus | v0.4.2 | 1 | 0.667 | 0.667 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=0/1 a4=1/1 |
| n10-method-citation-unverified | opus | v0.4.3 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n10-method-citation-unverified | opus | without_skill | 1 | 0.667 | 0.667 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=0/1 a4=1/1 |
| n10-method-citation-unverified | sonnet | v0.4.0 | 3 | 0.778 | 0.667 | None | 0 | 1/3 | [1, 6, 1] | a1=3/3 a2=3/3 a3=1/3 a4=3/3 |
| n10-method-citation-unverified | sonnet | v0.4.2 | 3 | 0.778 | 0.667 | None | 0 | 1/3 | [6, 1, 1] | a1=3/3 a2=3/3 a3=1/3 a4=3/3 |
| n10-method-citation-unverified | sonnet | v0.4.3 | 3 | 0.778 | 0.667 | None | 0 | 1/3 | [1, 6, 1] | a1=3/3 a2=3/3 a3=1/3 a4=3/3 |
| n10-method-citation-unverified | sonnet | without_skill | 3 | 0.667 | 0.667 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=0/3 a4=3/3 |
| n11-table-implies-causation | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 |
| n11-table-implies-causation | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 |
| n11-table-implies-causation | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 |
| n11-table-implies-causation | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 5, 5] | a1=3/3 a2=3/3 |
| n11-table-implies-causation | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 |
| n11-table-implies-causation | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 |
| n2-clean-paragraph | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n2-clean-paragraph | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n2-clean-paragraph | opus | without_skill | 1 | 0.0 | 0.0 | None | 1 | 0/1 | [1] | a1=0/1 a2=0/1 a3=1/1 |
| n2-clean-paragraph | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n2-clean-paragraph | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n2-clean-paragraph | sonnet | without_skill | 3 | 0.0 | 0.0 | None | 3 | 0/3 | [1, 1, 1] | a1=0/3 a2=0/3 a3=3/3 |
| n3-causal-language-across-chapters | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | sonnet | v0.4.0 | 3 | 0.889 | 0.667 | None | 1 | 3/3 | [5, 5, 5] | a1=3/3 a2=2/3 a3=3/3 a4=3/3 |
| n3-causal-language-across-chapters | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n3-causal-language-across-chapters | sonnet | without_skill | 3 | 0.444 | 0.333 | None | 5 | 0/3 | [1, 1, 1] | a1=3/3 a2=0/3 a3=1/3 a4=3/3 |
| n4-taiwan-usage-and-apa | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | opus | v0.4.3 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 |
| n4-taiwan-usage-and-apa | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 |
| n4-taiwan-usage-and-apa | sonnet | v0.4.3 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 |
| n4-taiwan-usage-and-apa | sonnet | without_skill | 3 | 0.944 | 0.833 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 a4=2/3 a5=3/3 a6=3/3 a7=3/3 |
| n5-intro-missing-niche | opus | v0.4.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n5-intro-missing-niche | opus | v0.4.2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n5-intro-missing-niche | opus | without_skill | 1 | 1.0 | 1.0 | 0.0 | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=0/1 a4=1/1 |
| n5-intro-missing-niche | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 7, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n5-intro-missing-niche | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 7, 8] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n5-intro-missing-niche | sonnet | without_skill | 3 | 1.0 | 1.0 | 0.0 | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=0/3 a4=3/3 |
| n6-user-writes-final-draft | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n6-user-writes-final-draft | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n6-user-writes-final-draft | opus | v0.4.3 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n6-user-writes-final-draft | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 |
| n6-user-writes-final-draft | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 |
| n6-user-writes-final-draft | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 |
| n6-user-writes-final-draft | sonnet | v0.4.3 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 |
| n6-user-writes-final-draft | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 |
| n7-paraphrase-details-unverified | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n7-paraphrase-details-unverified | opus | v0.4.2 | 1 | 0.5 | 0.5 | None | 1 | 1/1 | [5] | a1=1/1 a2=0/1 a3=1/1 |
| n7-paraphrase-details-unverified | opus | v0.4.3 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n7-paraphrase-details-unverified | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 |
| n7-paraphrase-details-unverified | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n7-paraphrase-details-unverified | sonnet | v0.4.2 | 3 | 0.833 | 0.5 | None | 1 | 3/3 | [5, 5, 5] | a1=3/3 a2=2/3 a3=3/3 |
| n7-paraphrase-details-unverified | sonnet | v0.4.3 | 6 | 1.0 | 1.0 | None | 0 | 6/6 | [5, 5, 5, 5, 5, 5] | a1=6/6 a2=6/6 a3=6/6 |
| n7-paraphrase-details-unverified | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 |
| n8-conventional-attribution | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n8-conventional-attribution | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n8-conventional-attribution | opus | v0.4.3 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n8-conventional-attribution | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 |
| n8-conventional-attribution | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n8-conventional-attribution | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n8-conventional-attribution | sonnet | v0.4.3 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n8-conventional-attribution | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 |
| n9-scope-beyond-evidence | opus | v0.4.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n9-scope-beyond-evidence | opus | v0.4.2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n9-scope-beyond-evidence | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 |
| n9-scope-beyond-evidence | sonnet | v0.4.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 6, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n9-scope-beyond-evidence | sonnet | v0.4.2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 6, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n9-scope-beyond-evidence | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 |

