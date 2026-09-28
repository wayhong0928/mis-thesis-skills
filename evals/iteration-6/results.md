# iteration-6 結果（評分：final）

## academic-writing-discipline

| 模型 | 臂 | outcome | outcome（不含 tests_change） | pass^k | procedure | 假陽性 | tokens | 秒 |
|---|---|---|---|---|---|---|---|---|
| opus | v0.3.0 | 0.964 | 0.964 | 0.964 | 1.0 | 1 | 50429.143 | 38.615 |
| opus | v0.4.0-nochapter | 0.964 | 0.964 | 0.964 | 0.5 | 1 | 49668.857 | 37.455 |
| opus | v0.4.0c2 | 0.964 | 0.964 | 0.964 | 0.5 | 1 | 51522.143 | 37.984 |
| opus | v0.4.0rc | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 53953 | 50.575 |
| opus | without_skill | 0.768 | 0.768 | 0.768 | 0.25 | 2 | 10689.714 | 27.047 |
| sonnet | v0.3.0 | 0.952 | 0.952 | 0.893 | 0.916 | 0 | 74656.191 | 62.869 |
| sonnet | v0.4.0-nochapter | 0.857 | 0.857 | 0.857 | 0.25 | 0 | 81082.429 | 59.613 |
| sonnet | v0.4.0c2 | 0.988 | 0.988 | 0.964 | 1.0 | 0 | 85484.143 | 59.324 |
| sonnet | v0.4.0rc | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 84954 | 87.373 |
| sonnet | without_skill | 0.708 | 0.708 | 0.661 | 0.0 | 4 | 17251.572 | 26.334 |

| 案例 | 模型 | 臂 | n | outcome | pass^k | procedure | 假陽性 | 觸發 skill | turns | 逐條 |
|---|---|---|---|---|---|---|---|---|---|---|
| eval-1-causal-verb-and-existence-abuse | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | opus | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | opus | without_skill | 1 | 0.75 | 0.75 | None | 0 | 0/1 | [1] | a1=1/1 a2=0/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | sonnet | v0.3.0 | 3 | 0.75 | 0.5 | None | 0 | 3/3 | [5, 6, 3] | a1=3/3 a2=1/3 a3=2/3 a4=3/3 a5=3/3 |
| eval-1-causal-verb-and-existence-abuse | sonnet | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-causal-verb-and-existence-abuse | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| eval-1-causal-verb-and-existence-abuse | sonnet | without_skill | 3 | 0.417 | 0.25 | None | 0 | 0/3 | [1, 1, 1] | a1=2/3 a2=0/3 a3=0/3 a4=3/3 a5=3/3 |
| eval-2-bloated-middle-sentence | opus | v0.3.0 | 1 | 0.75 | 0.75 | None | 1 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a6=1/1 |
| eval-2-bloated-middle-sentence | opus | v0.4.0-nochapter | 1 | 0.75 | 0.75 | None | 1 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a6=1/1 |
| eval-2-bloated-middle-sentence | opus | v0.4.0c2 | 1 | 0.75 | 0.75 | None | 1 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a6=1/1 |
| eval-2-bloated-middle-sentence | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a6=1/1 |
| eval-2-bloated-middle-sentence | sonnet | v0.3.0 | 3 | 0.917 | 0.75 | None | 0 | 3/3 | [4, 5, 4] | a1=3/3 a2=3/3 a3=2/3 a4=3/3 a6=3/3 |
| eval-2-bloated-middle-sentence | sonnet | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [4] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a6=1/1 |
| eval-2-bloated-middle-sentence | sonnet | v0.4.0c2 | 3 | 0.917 | 0.75 | None | 0 | 3/3 | [4, 4, 4] | a1=3/3 a2=3/3 a3=2/3 a4=3/3 a6=3/3 |
| eval-2-bloated-middle-sentence | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a6=3/3 |
| n1-messy-long-draft | opus | v0.3.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | opus | v0.4.0-nochapter | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | opus | without_skill | 1 | 0.625 | 0.625 | 0.5 | 1 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a5=0/1 a6=1/1 a7=0/1 a8=1/1 a9=0/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 0.833 | 0 | 3/3 | [6, 7, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 a8=3/3 a9=2/3 a10=3/3 a11=3/3 |
| n1-messy-long-draft | sonnet | v0.4.0-nochapter | 1 | 1.0 | 1.0 | 0.5 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=0/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 6, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 a8=3/3 a9=3/3 a10=3/3 a11=3/3 |
| n1-messy-long-draft | sonnet | v0.4.0rc | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 a8=1/1 a9=1/1 a10=1/1 a11=1/1 |
| n1-messy-long-draft | sonnet | without_skill | 3 | 0.542 | 0.375 | 0.0 | 1 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=1/3 a4=0/3 a5=0/3 a6=1/3 a7=2/3 a8=3/3 a9=0/3 a10=0/3 a11=3/3 |
| n2-clean-paragraph | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n2-clean-paragraph | opus | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n2-clean-paragraph | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n2-clean-paragraph | opus | without_skill | 1 | 0.0 | 0.0 | None | 1 | 0/1 | [1] | a1=0/1 a2=0/1 a3=1/1 |
| n2-clean-paragraph | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 |
| n2-clean-paragraph | sonnet | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 |
| n2-clean-paragraph | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=3/3 |
| n2-clean-paragraph | sonnet | without_skill | 3 | 0.5 | 0.5 | None | 0 | 0/3 | [1, 1, 1] | a1=0/3 a2=3/3 a3=3/3 |
| n3-causal-language-across-chapters | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [4] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | opus | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [4, 4, 3] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n3-causal-language-across-chapters | sonnet | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n3-causal-language-across-chapters | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [8, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n3-causal-language-across-chapters | sonnet | without_skill | 3 | 0.667 | 0.667 | None | 3 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=0/3 a4=3/3 |
| n4-taiwan-usage-and-apa | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [7] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | opus | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 |
| n4-taiwan-usage-and-apa | sonnet | v0.4.0-nochapter | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 a7=1/1 |
| n4-taiwan-usage-and-apa | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 5, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 |
| n4-taiwan-usage-and-apa | sonnet | without_skill | 3 | 0.833 | 0.833 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=0/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 a7=3/3 |
| n5-intro-missing-niche | opus | v0.3.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [7] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n5-intro-missing-niche | opus | v0.4.0-nochapter | 1 | 1.0 | 1.0 | 0.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=0/1 a4=1/1 |
| n5-intro-missing-niche | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 0.0 | 0 | 1/1 | [7] | a1=1/1 a2=1/1 a3=0/1 a4=1/1 |
| n5-intro-missing-niche | opus | v0.4.0rc | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| n5-intro-missing-niche | opus | without_skill | 1 | 1.0 | 1.0 | 0.0 | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=0/1 a4=1/1 |
| n5-intro-missing-niche | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 7, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n5-intro-missing-niche | sonnet | v0.4.0-nochapter | 3 | 0.0 | 0.0 | 0.0 | 0 | 3/3 | [6, 6, 6] | a1=0/3 a2=0/3 a3=0/3 a4=3/3 |
| n5-intro-missing-niche | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 7, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n5-intro-missing-niche | sonnet | v0.4.0rc | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 7, 8] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| n5-intro-missing-niche | sonnet | without_skill | 3 | 1.0 | 1.0 | 0.0 | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=0/3 a4=3/3 |

## research-direction-finding

| 模型 | 臂 | outcome | outcome（不含 tests_change） | pass^k | procedure | 假陽性 | tokens | 秒 |
|---|---|---|---|---|---|---|---|---|
| opus | v0.3.0 | 1.0 | 1.0 | 1.0 | 0.767 | 0 | 41469.8 | 30.739 |
| opus | v0.4.0c2 | 1.0 | 1.0 | 1.0 | 0.9 | 0 | 39118.6 | 30.649 |
| opus | without_skill | 0.647 | 0.647 | 0.647 | 0.5 | 1 | 9336.8 | 16.618 |
| sonnet | v0.3.0 | 0.933 | 0.933 | 0.933 | 0.678 | 0 | 68349.8 | 38.23 |
| sonnet | v0.4.0c2 | 0.978 | 0.978 | 0.933 | 0.878 | 0 | 71054.067 | 37.817 |
| sonnet | without_skill | 0.545 | 0.545 | 0.467 | 0.422 | 0 | 19191.0 | 14.754 |

| 案例 | 模型 | 臂 | n | outcome | pass^k | procedure | 假陽性 | 觸發 skill | turns | 逐條 |
|---|---|---|---|---|---|---|---|---|---|---|
| eval-1-blank-slate | opus | v0.3.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-blank-slate | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [3] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-blank-slate | opus | without_skill | 1 | 1.0 | 1.0 | 1.0 | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-1-blank-slate | sonnet | v0.3.0 | 3 | 0.667 | 0.667 | 1.0 | 0 | 3/3 | [5, 5, 5] | a1=3/3 a2=3/3 a3=0/3 a4=3/3 a5=3/3 |
| eval-1-blank-slate | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [3, 5, 3] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| eval-1-blank-slate | sonnet | without_skill | 3 | 0.667 | 0.667 | 0.667 | 0 | 0/3 | [1, 1, 1] | a1=2/3 a2=3/3 a3=0/3 a4=3/3 a5=3/3 |
| eval-2-broad-domain-ai | opus | v0.3.0 | 1 | 1.0 | 1.0 | 0.5 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a5=1/1 a6=1/1 |
| eval-2-broad-domain-ai | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 0.5 | 0 | 1/1 | [5] | a1=1/1 a2=1/1 a3=1/1 a4=0/1 a5=1/1 a6=1/1 |
| eval-2-broad-domain-ai | opus | without_skill | 1 | 0.333 | 0.333 | 0.5 | 1 | 0/1 | [1] | a1=1/1 a2=1/1 a3=0/1 a4=0/1 a5=0/1 a6=1/1 |
| eval-2-broad-domain-ai | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 0.5 | 0 | 3/3 | [5, 4, 5] | a1=3/3 a2=3/3 a3=3/3 a4=0/3 a5=3/3 a6=3/3 |
| eval-2-broad-domain-ai | sonnet | v0.4.0c2 | 3 | 0.889 | 0.667 | 0.5 | 0 | 3/3 | [5, 6, 5] | a1=3/3 a2=2/3 a3=3/3 a4=0/3 a5=3/3 a6=3/3 |
| eval-2-broad-domain-ai | sonnet | without_skill | 3 | 0.889 | 0.667 | 0.333 | 0 | 0/3 | [2, 1, 1] | a1=2/3 a2=3/3 a3=2/3 a4=0/3 a5=3/3 a6=3/3 |
| eval-3-advisor-project-topic | opus | v0.3.0 | 1 | 1.0 | 1.0 | 0.333 | 0 | 1/1 | [3] | a1=1/1 a2=0/1 a3=1/1 a4=1/1 a6=0/1 a5=1/1 |
| eval-3-advisor-project-topic | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [3] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a6=1/1 a5=1/1 |
| eval-3-advisor-project-topic | opus | without_skill | 1 | 0.5 | 0.5 | 0.0 | 0 | 0/1 | [1] | a1=0/1 a2=0/1 a3=1/1 a4=0/1 a6=0/1 a5=1/1 |
| eval-3-advisor-project-topic | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 0.889 | 0 | 3/3 | [3, 3, 3] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a6=2/3 a5=3/3 |
| eval-3-advisor-project-topic | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 0.889 | 0 | 3/3 | [3, 3, 3] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a6=2/3 a5=3/3 |
| eval-3-advisor-project-topic | sonnet | without_skill | 3 | 0.167 | 0.0 | 0.111 | 0 | 0/3 | [1, 1, 1] | a1=1/3 a2=0/3 a3=1/3 a4=0/3 a6=0/3 a5=3/3 |
| eval-4-already-has-idea-boundary | opus | v0.3.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-4-already-has-idea-boundary | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-4-already-has-idea-boundary | opus | without_skill | 1 | 1.0 | 1.0 | 1.0 | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-4-already-has-idea-boundary | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [6, 7, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-4-already-has-idea-boundary | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-4-already-has-idea-boundary | sonnet | without_skill | 3 | 1.0 | 1.0 | 1.0 | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-5-insufficient-information | opus | v0.3.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a7=1/1 a6=1/1 |
| eval-5-insufficient-information | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [7] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a7=1/1 a6=1/1 |
| eval-5-insufficient-information | opus | without_skill | 1 | 0.4 | 0.4 | 0.0 | 0 | 0/1 | [1] | a1=0/1 a2=0/1 a3=1/1 a4=1/1 a5=0/1 a6=1/1 a7=0/1 |
| eval-5-insufficient-information | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 0.0 | 0 | 3/3 | [8, 6, 5] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a7=0/3 a6=3/3 |
| eval-5-insufficient-information | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 7, 9] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a7=3/3 a6=3/3 |
| eval-5-insufficient-information | sonnet | without_skill | 3 | 0.0 | 0.0 | 0.0 | 0 | 0/3 | [2, 2, 1] | a1=0/3 a2=0/3 a3=0/3 a4=0/3 a5=0/3 a7=0/3 a6=3/3 |

## research-question-audit

| 模型 | 臂 | outcome | outcome（不含 tests_change） | pass^k | procedure | 假陽性 | tokens | 秒 |
|---|---|---|---|---|---|---|---|---|
| opus | v0.3.0 | 0.925 | 1.0 | 0.925 | 1.0 | 2 | 51976.167 | 58.688 |
| opus | v0.4.0c | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 53542 | 68.145 |
| opus | v0.4.0c2 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 54009.667 | 70.108 |
| opus | without_skill | 0.733 | 0.625 | 0.733 | 1.0 | 1 | 10547.667 | 28.484 |
| sonnet | v0.3.0 | 0.958 | 1.0 | 0.875 | 1.0 | 2 | 80913.056 | 101.712 |
| sonnet | v0.4.0c | 0.931 | 1.0 | 0.875 | 1.0 | 3 | 85988.5 | 100.592 |
| sonnet | v0.4.0c2 | 1.0 | 1.0 | 1.0 | 1.0 | 0 | 92713.5 | 106.825 |
| sonnet | without_skill | 0.669 | 0.556 | 0.614 | 0.667 | 0 | 19430.166 | 22.998 |

| 案例 | 模型 | 臂 | n | outcome | pass^k | procedure | 假陽性 | 觸發 skill | turns | 逐條 |
|---|---|---|---|---|---|---|---|---|---|---|
| eval-1-bad-title-no-dv | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-1-bad-title-no-dv | opus | v0.4.0c | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-1-bad-title-no-dv | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-1-bad-title-no-dv | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-1-bad-title-no-dv | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-1-bad-title-no-dv | sonnet | v0.4.0c | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 7, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-1-bad-title-no-dv | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [9, 6, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-1-bad-title-no-dv | sonnet | without_skill | 3 | 0.667 | 0.333 | None | 0 | 0/3 | [1, 1, 1] | a1=2/3 a2=1/3 a3=3/3 a4=3/3 |
| eval-2-too-many-dvs | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-2-too-many-dvs | opus | v0.4.0c | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-2-too-many-dvs | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-2-too-many-dvs | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 |
| eval-2-too-many-dvs | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-2-too-many-dvs | sonnet | v0.4.0c | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-2-too-many-dvs | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 7, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-2-too-many-dvs | sonnet | without_skill | 3 | 1.0 | 1.0 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 |
| eval-3-gai-dependency | opus | v0.3.0 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-3-gai-dependency | opus | v0.4.0c | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-3-gai-dependency | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | 1.0 | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-3-gai-dependency | opus | without_skill | 1 | 0.5 | 0.5 | 1.0 | 0 | 0/1 | [1] | a1=0/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| eval-3-gai-dependency | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [6, 7, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| eval-3-gai-dependency | sonnet | v0.4.0c | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [6, 7, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| eval-3-gai-dependency | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | 1.0 | 0 | 3/3 | [7, 6, 7] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| eval-3-gai-dependency | sonnet | without_skill | 3 | 0.5 | 0.5 | 0.667 | 0 | 0/3 | [1, 1, 1] | a1=0/3 a2=3/3 a3=2/3 a4=2/3 a5=3/3 |
| eval-4-mature-thesis | opus | v0.3.0 | 1 | 0.8 | 0.8 | None | 1 | 1/1 | [6] | a1=0/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 |
| eval-4-mature-thesis | opus | v0.4.0c | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 |
| eval-4-mature-thesis | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 a6=1/1 |
| eval-4-mature-thesis | opus | without_skill | 1 | 0.4 | 0.4 | None | 1 | 0/1 | [1] | a1=1/1 a2=0/1 a3=0/1 a4=0/1 a5=1/1 a6=1/1 |
| eval-4-mature-thesis | sonnet | v0.3.0 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 |
| eval-4-mature-thesis | sonnet | v0.4.0c | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [7, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 |
| eval-4-mature-thesis | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 7, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 a6=3/3 |
| eval-4-mature-thesis | sonnet | without_skill | 3 | 0.6 | 0.6 | None | 0 | 0/3 | [1, 1, 2] | a1=3/3 a2=0/3 a3=0/3 a4=3/3 a5=3/3 a6=3/3 |
| n1-two-indicators-one-construct | opus | v0.3.0 | 1 | 0.75 | 0.75 | None | 1 | 1/1 | [6] | a1=0/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| n1-two-indicators-one-construct | opus | v0.4.0c | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| n1-two-indicators-one-construct | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| n1-two-indicators-one-construct | opus | without_skill | 1 | 1.0 | 1.0 | None | 0 | 0/1 | [1] | a1=1/1 a2=1/1 a3=1/1 a4=1/1 a5=1/1 |
| n1-two-indicators-one-construct | sonnet | v0.3.0 | 3 | 0.917 | 0.75 | None | 1 | 3/3 | [6, 6, 6] | a1=2/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| n1-two-indicators-one-construct | sonnet | v0.4.0c | 3 | 0.917 | 0.75 | None | 1 | 3/3 | [6, 6, 7] | a1=2/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| n1-two-indicators-one-construct | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 6, 6] | a1=3/3 a2=3/3 a3=3/3 a4=3/3 a5=3/3 |
| n1-two-indicators-one-construct | sonnet | without_skill | 3 | 0.75 | 0.75 | None | 0 | 0/3 | [1, 1, 1] | a1=3/3 a2=0/3 a3=3/3 a4=3/3 a5=3/3 |
| n2-directional-yes-no-question | opus | v0.3.0 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n2-directional-yes-no-question | opus | v0.4.0c | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n2-directional-yes-no-question | opus | v0.4.0c2 | 1 | 1.0 | 1.0 | None | 0 | 1/1 | [6] | a1=1/1 a2=1/1 a3=1/1 |
| n2-directional-yes-no-question | opus | without_skill | 1 | 0.5 | 0.5 | None | 0 | 0/1 | [1] | a1=0/1 a2=1/1 a3=1/1 |
| n2-directional-yes-no-question | sonnet | v0.3.0 | 3 | 0.833 | 0.5 | None | 1 | 3/3 | [6, 6, 7] | a1=3/3 a2=2/3 a3=3/3 |
| n2-directional-yes-no-question | sonnet | v0.4.0c | 3 | 0.667 | 0.5 | None | 2 | 3/3 | [6, 7, 6] | a1=3/3 a2=1/3 a3=3/3 |
| n2-directional-yes-no-question | sonnet | v0.4.0c2 | 3 | 1.0 | 1.0 | None | 0 | 3/3 | [6, 7, 6] | a1=3/3 a2=3/3 a3=3/3 |
| n2-directional-yes-no-question | sonnet | without_skill | 3 | 0.5 | 0.5 | None | 0 | 0/3 | [1, 3, 1] | a1=0/3 a2=3/3 a3=3/3 |

## 階段 0 觸發

| id | 預期 | 模型 | 叫用的 skill |
|---|---|---|---|
| academic-writing-discipline__should-1 | 應觸發 | opus | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-1 | 應觸發 | sonnet | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-2 | 應觸發 | opus | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-2 | 應觸發 | sonnet | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-3 | 應觸發 | opus | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-3 | 應觸發 | sonnet | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-4 | 應觸發 | opus | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should-4 | 應觸發 | sonnet | thesis-toolkit:academic-writing-discipline |
| academic-writing-discipline__should_not-1 | 不應觸發 | opus | 無 |
| academic-writing-discipline__should_not-1 | 不應觸發 | sonnet | 無 |
| academic-writing-discipline__should_not-2 | 不應觸發 | opus | 無 |
| academic-writing-discipline__should_not-2 | 不應觸發 | sonnet | 無 |
| research-question-audit__should-1 | 應觸發 | opus | thesis-toolkit:research-question-audit |
| research-question-audit__should-1 | 應觸發 | sonnet | thesis-toolkit:research-question-audit |
| research-question-audit__should-2 | 應觸發 | opus | thesis-toolkit:research-question-audit |
| research-question-audit__should-2 | 應觸發 | sonnet | thesis-toolkit:research-question-audit |
| research-question-audit__should-3 | 應觸發 | opus | thesis-toolkit:research-question-audit |
| research-question-audit__should-3 | 應觸發 | sonnet | thesis-toolkit:research-question-audit |
| research-question-audit__should-4 | 應觸發 | opus | thesis-toolkit:research-question-audit |
| research-question-audit__should-4 | 應觸發 | sonnet | thesis-toolkit:research-question-audit |
| research-question-audit__should_not-1 | 不應觸發 | opus | 無 |
| research-question-audit__should_not-1 | 不應觸發 | sonnet | 無 |
| research-question-audit__should_not-2 | 不應觸發 | opus | 無 |
| research-question-audit__should_not-2 | 不應觸發 | sonnet | 無 |
| research-direction-finding__should-1 | 應觸發 | opus | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-1 | 應觸發 | sonnet | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-2 | 應觸發 | opus | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-2 | 應觸發 | sonnet | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-3 | 應觸發 | opus | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-3 | 應觸發 | sonnet | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-4 | 應觸發 | opus | thesis-toolkit:research-direction-finding |
| research-direction-finding__should-4 | 應觸發 | sonnet | thesis-toolkit:research-direction-finding |
| research-direction-finding__should_not-1 | 不應觸發 | opus | thesis-toolkit:research-question-audit |
| research-direction-finding__should_not-1 | 不應觸發 | sonnet | thesis-toolkit:research-question-audit |
| research-direction-finding__should_not-2 | 不應觸發 | opus | 無 |
| research-direction-finding__should_not-2 | 不應觸發 | sonnet | 無 |
