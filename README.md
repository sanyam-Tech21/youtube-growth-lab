# YouTube Growth Lab

A reusable skill for planning, writing, packaging, and improving YouTube videos in Claude and other assistants that support Agent Skills.

It helps turn audience needs into complete scripts and practical experiments. **No skill can guarantee views, virality, or revenue.**

## Install in Claude

1. Open [youtube-growth-lab.zip](downloads/youtube-growth-lab.zip) and use GitHub’s **Download raw file** button to save the ZIP.
2. In Claude, enable **Code execution and file creation** in Settings → Capabilities if it is not already enabled.
3. Open **Customize → Skills → + → Create skill → Upload a skill**.
4. Upload the ZIP and enable **youtube-growth-lab**.

The ZIP contains a single `youtube-growth-lab` folder with `SKILL.md` and its supporting files. Upload this ZIP, rather than the whole repository archive. Organization settings may control skill creation and code execution.

See Claude’s official [skill installation guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude) and [custom skill structure](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills). Installation guidance checked October 6, 2026. This package has not been installed or tested inside your Claude account.

## Try it

> Use YouTube Growth Lab to create a two-week pilot for my new Hinglish technology channel. I can spend four hours per week. Give me video ideas, one complete script, title–thumbnail concepts, and a practical experiment plan. Ask only for information you need.

For an existing channel, supply relevant analytics exports with column definitions and time windows. A public channel URL does not expose private retention, impressions, or CTR.

## What is included

| Workflow | Output |
| --- | --- |
| Onboarding and ideas | Audience profile, evidence, original angles, feasible pilot |
| Scripts and packaging | Complete spoken script, hook options, title–thumbnail concepts |
| Editing, Shorts, metadata, chapters | Reviewable cut suggestions, clip plans, descriptions, valid timestamps |
| Comments and scheduling | Reply drafts and a plan matched to production capacity |
| Research, retention, audits | Evidence-supported findings with uncertainty and data limitations |
| Experiments and reviews | Hypothesis, metric, comparison window, decision rule, next action |

The skill supports English, Hindi, and Hinglish. Its 15 workflows include new-channel planning without invented analytics.

## Numerical tools

Seven standard-library Python commands handle title checks, hook timing, transcript edit candidates, retention, chapters, matched comparisons, and impression-attributed funnels. They need Python 3.10 or later. They read local inputs and produce JSON; they do not modify media or upload videos.

```bash
python3 youtube-growth-lab/scripts/yt_tools.py --help
python3 youtube-growth-lab/scripts/test_yt_tools.py
```

The automated suite contains 37 tests. Two task-based checks covered a new-channel plan and a retention diagnosis. Passing checks verifies the tested behavior, not future video performance.

Read [SKILL.md](youtube-growth-lab/SKILL.md) for the full workflow, [tool contracts](youtube-growth-lab/references/tool-contracts.md) for inputs, and [measurement guidance](youtube-growth-lab/references/measurement.md) for interpretation.

## Improvements over the starting project

- Replaces predictive scores and view promises with observable checks and testable hypotheses.
- Adds new-channel discovery, capacity-based planning, experiments, and structured result reviews.
- Makes retention units explicit and checks comparable metrics, time windows, and peer cohorts.
- Validates chapter endings against actual media duration and avoids double-counting overlapping cuts.
- Keeps writing and planning usable without claiming unavailable analytics, integrations, or code execution.

## Attribution and license

Based on and substantially reworked from [Jake Schincariol’s YouTube Agent Skill](https://github.com/Jakeschincariol/youtube-agent-skill). The original MIT copyright notice is retained in [LICENSE](LICENSE) and inside the downloadable skill.

This is an independent package, not an official YouTube, Anthropic, or upstream-author product.
