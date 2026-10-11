[繁體中文](README.md) | English

# mis-thesis-skills

Audit tools for thesis research design and academic writing. They turn part of the [mis-thesis-guide](https://wayhong0928.github.io/mis-thesis-guide/) website into installable Claude Code skills, so students don't have to copy and paste prompts by hand.

**The skills are written for Traditional Chinese.** They answer in Traditional Chinese, the writing audit checks Taiwanese academic usage and the Chinese adaptation of APA 7, and the instructions and reference files are all in Chinese.

This repo is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) with one plugin, `thesis-toolkit`. It holds three audit skills, one for each of the three stages of a thesis from 0 to 1, plus a roadmap skill that tells you which one to use next.

## Skills

| Skill | What it does | What it doesn't do |
|---|---|---|
| `research-direction-finding` | For students with no research direction, or only a field too broad to be a topic. It uses starter strategies and a narrowing funnel (field → topic → subtopic → research topic → research question), moving one level per round until you have a one-sentence research idea. Each round goes into a progress note | Doesn't judge whether the resulting topic holds up (that's the next skill). Doesn't read the literature for you |
| `research-question-audit` | Audits a research question or idea you already have for gaps in logic, methodology, and feasibility. After the audit, it can walk you through the failed items one at a time | Won't come up with a topic from scratch. Doesn't cover execution details such as writing survey items or running statistics |
| `academic-writing-discipline` | Audits Chinese academic prose at the sentence and word level: causal verbs, sentence structure, Taiwanese academic usage, APA 7, AI-sounding text, and how each chapter is usually written | Doesn't judge research design (that's the skill above). **No longer checks the argument chain in literature reviews**; this was removed in v0.3.0 based on eval results, see the 0.3.0 section of the [CHANGELOG](plugins/thesis-toolkit/CHANGELOG.md) |
| `thesis-roadmap` | For when you don't know which stage you're in or which skill to use next. It works out your stage, names the next skill, and gives a sample opening line. For things none of the three skills cover (finding literature, statistics, the oral defense), it points to the matching mis-thesis-guide page | Runs no audits. Doesn't enforce an order; each audit skill works on its own |

The criteria in every skill trace back to public research methods sources, listed in each skill's `references/`. How they were designed and distilled is written up in [Turning course material into a skill](https://wayhong0928.github.io/ai-agent-notes/pages/skill-build.html) (Chinese).

## Usage

Once installed, there are no commands to memorize. Say what you want in Chinese and Claude picks the skill. To call one directly, type its name, for example `/thesis-toolkit:research-question-audit`.

| You say | Skill | What you get |
|---|---|---|
| "My advisor wants me to find my own topic and I have no idea where to start" | `research-direction-finding` | It first asks whether you have no direction at all, a broad field, or a topic to carve out of your advisor's project. With no direction, it gives you one task you can do today, then moves down one level per round and records the conclusion and the rejected options in the progress note |
| "I want to study how remote work affects employee burnout. Does this topic hold up?" | `research-question-audit` | An audit report: seven checkpoints, each marked pass, fail, unsure, or not applicable, with reasons. Failed and unsure items are rewritten as questions a committee member might ask. It ends by offering to work through them one at a time |
| "I'm stuck on my thesis and don't know what to do next" | `thesis-roadmap` | It works out whether you're finding a direction, auditing a topic, or writing chapters, says what it based that on, then tells you which skill to use next and how to ask |
| Paste a literature review paragraph and say "check how this is written" | `academic-writing-discipline` | Issues sorted into fatal, error, and minor, each with the original sentence, the problem, and a fix (for example, "導致" (cause) used on cross-sectional data, or mainland Chinese terms such as "通過問卷收集數據"). It ends with a revised version that applies the fixes and is ready to use |

## Installation

### Claude Code

```
/plugin marketplace add wayhong0928/mis-thesis-skills
/plugin install thesis-toolkit@mis-thesis-skills
```

### Claude Cowork

Customize → Plugins → Add marketplace, enter `wayhong0928/mis-thesis-skills`, then install `thesis-toolkit`.

### Claude.ai (web)

The web app doesn't support plugin marketplaces. Zip a single skill folder (for example `plugins/thesis-toolkit/skills/research-question-audit/`) and upload it under Customize → Skills. Claude.ai caps the `description` field at 200 characters, shorter than Claude Code allows, so you may need to trim it before uploading.

If you only use web chat apps (Claude.ai, ChatGPT, Gemini), use the [web-lite prompts](https://wayhong0928.github.io/mis-thesis-guide/pages/prompts.html#skill-lite) on mis-thesis-guide instead; nothing to package or upload. The lite versions lack the full criteria in `references/`; what they leave out is noted under each section on that page.

### Codex (OpenAI)

Codex also supports the open [Agent Skills](https://agentskills.io/) format. It reads from `.agents/skills/` rather than Claude Code's `.claude/skills/`. Copy the skill folders there, or symlink them so both tools share one copy. This doesn't go through the plugin marketplace, which is Claude-only packaging; it only relies on the open SKILL.md format.

## Updating

Third-party marketplaces don't update automatically by default. To update, run in a terminal:

```
claude plugin marketplace update mis-thesis-skills
claude plugin update thesis-toolkit@mis-thesis-skills
```

Or type `/plugin` in Claude Code, open the Marketplaces tab, select `mis-thesis-skills`, and choose **Update marketplace**. Choosing **Enable auto-update** in the same place keeps it updated from then on. New sessions load the new version; in a running session, type `/reload-plugins`. See the [CHANGELOG](plugins/thesis-toolkit/CHANGELOG.md) for what each version changed.

## Evals

The three audit skills were evaluated with the workflow from Anthropic's [skill-creator](https://github.com/anthropics/skills): write test cases, compare output with and without the skill, and grade each assertion.

The latest round covering all three is [`evals/iteration-6/`](evals/iteration-6/) from 2026-09-28: 18 cases, Sonnet 5 three runs per case, Opus 5.5 one run per case. The table counts only outcome assertions, the ones about whether what the user actually gets is right. `thesis-roadmap`, added in 0.5.0, has only had a trigger eval ([`evals/iteration-9/`](evals/iteration-9/)); its output quality hasn't been evaluated.

| Skill | Model | Without | 0.3.0 | 0.4.0 |
|---|---|---|---|---|
| academic-writing-discipline | Sonnet | 0.71 | 0.95 | 0.99 |
| | Opus | 0.77 | 0.96 | 0.96 |
| research-question-audit | Sonnet | 0.67 | 0.96 | 1.00 |
| | Opus | 0.73 | 0.93 | 1.00 |
| research-direction-finding | Sonnet | 0.55 | 0.93 | 0.98 |
| | Opus | 0.65 | 1.00 | 1.00 |

The maintainer wrote the cases and Opus ran each only once, so read these numbers as direction, not stable effect sizes. How to read the table, evals after 0.4.1, and why earlier numbers deserve caution are in [`evals/README.md`](evals/README.md) (Chinese).

## Reporting problems

If a criterion is wrong, a skill doesn't trigger, or the output is off, open an [issue](https://github.com/wayhong0928/mis-thesis-skills/issues) with what you pasted and what it returned.

## License

MIT License, see [LICENSE](LICENSE). The license covers only the maintainer's original criteria and code that trace independently to public sources. It doesn't cover any book, lecture, or unlicensed third-party framework or proprietary term.

## Related

| Resource | For |
|---|---|
| [mis-thesis-guide](https://wayhong0928.github.io/mis-thesis-guide/) | A knowledge base on research methods and thesis writing, for looking up concepts and criteria |
| [One-hour quickstart](https://wayhong0928.github.io/mis-thesis-guide/pages/ai-quickstart.html) | Students who only use the ChatGPT, Claude, or Gemini web apps and want a thesis assistant set up in an hour (there's also a [Claude Code and Codex version](https://wayhong0928.github.io/mis-thesis-guide/pages/ai-quickstart-agent.html)) |
| [thesis-notes-template](https://github.com/wayhong0928/thesis-notes-template) | Students who want to take literature notes in Obsidian with a ready-made template and filling rules |
| [mis-thesis-skills](https://github.com/wayhong0928/mis-thesis-skills) | Students using Claude Code or Codex who want AI to check topics and writing against fixed criteria |
| [claude-workflow-template](https://github.com/wayhong0928/claude-workflow-template) | Students using Claude Code on a thesis or research project who want a ready-made workflow setup: session handoff, dispatch templates, independent verification |

All linked sites and templates are in Traditional Chinese.
