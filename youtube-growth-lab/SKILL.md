---
name: youtube-growth-lab
description: "Create and improve YouTube scripts, titles, thumbnails, plans, Shorts and metadata. Audit channels, analyze retention, compare matched results, and plan experiments. Never guarantee views."
---

# YouTube Growth Lab

Build a complete, usable deliverable for the user's requested stage. Connect
audience need, a truthful promise, the actual video, and a measured next test.
Never promise a minimum view count, a probability of virality without a
validated model, revenue, or guaranteed growth. Do not replace an impossible
guarantee with a disguised promise such as "algorithm-proof" or "sure to work".

## Start with available context

1. Identify whether this is a new or existing channel; identify language,
   audience, topic, format, goal, and production capacity. Use provided
   information first. Ask only for missing inputs that materially change
   the work, grouping up to three short questions when needed.
2. Read a supplied channel profile or use `assets/channel-profile.md` to
   establish one. Voice samples are optional: do not require three previous
   videos from a new creator. Label an inferred voice as provisional.
3. For an existing channel, ask for comparable analytics only when needed
   for a diagnosis. A public channel URL does not expose private retention,
   impressions, CTR, or experiments. Never claim access you do not have.
4. For a new channel or absent analytics, work in **discovery mode**: choose
   testable audience hypotheses and a feasible pilot. Do not invent baselines
   or forecasts. Continue with an explicitly provisional deliverable when
   useful, rather than blocking all work on unavailable data.
5. Recheck current YouTube documentation for live feature instructions,
   formats, metrics, or eligibility. Use `references/sources.md` as the
   starting points. Distinguish official facts, observations, and hypotheses.

## Select the requested workflow

Read the relevant section of `references/workflows.md`; do not run every mode
when the user only wants one output. The labels below are conversational
shortcuts, not globally registered slash commands.

| Mode | Deliverable |
| --- | --- |
| onboard / yt-onboard | Audience, voice, constraints, goals, and available evidence |
| ideas / yt-ideas | Evidence table, original angles, and a feasible pilot choice |
| script / yt-script | Three distinct hooks, one full spoken script, visuals, and timing |
| package / yt-package | Up to three title–thumbnail concepts and test hypothesis |
| edit / yt-edit | Reviewable timestamped cut candidates and editorial plan |
| comments / yt-comment | Classified comments, reply drafts, and optional pin suggestion |
| plan / yt-plan | Capacity-based schedule with estimated effort and fallback scope |
| research / yt-viral | Comparable public examples with provenance and uncertainty |
| retention / yt-retention | Validated units, sampled drop intervals, and a testable diagnosis |
| shorts / yt-shorts | Self-contained clips with real timecodes and new recording needs |
| metadata / yt-seo | Truthful description, relevant query intent, and restrained tags |
| chapters / yt-chapters | Semantic chapter boundaries, titles, and timing validation |
| audit / yt-audit | Evidence-supported bottleneck and one priority experiment |
| experiment / yt-test | Predefined hypothesis, variants, metric, and decision rule |
| review / yt-review | Comparable results, uncertainty, and a recorded next decision |

For an end-to-end request, use: profile → evidence-backed ideas → package →
script → edit/metadata plan → quality review → experiment plan. Include a
review template so results can inform the next video. Do not stop after
providing only a list of tips when a full script or plan was requested.

## Use the deterministic tools when applicable

Read `references/tool-contracts.md` for schemas, units, and examples. Run
`scripts/yt_tools.py` from the resolved skill directory using Python 3.10+.
All seven commands return JSON. They read local inputs and never modify media.

Use the host's available file and code-execution capabilities; no OpenAI-only
API is required. In Claude, resolve paths from this skill's installed folder.
If code execution is unavailable, continue with writing and planning tasks,
and clearly identify any numerical checks that could not be run. Do not claim
tool validation or automatic installation merely because the text was pasted.

| Command | Purpose |
| --- | --- |
| package | Title limits, text overlap, and review notes without a performance score |
| hook | Spoken-time estimate and an editorial checklist |
| edit | SRT/VTT/JSON parsing and interval-union accounting for candidate cuts |
| retention | Explicit units, interpolation, and sampled retention changes |
| chapters | Validate authored timestamps against the full media duration |
| compare | Exclude the subject from matched-peer descriptive comparisons |
| funnel | Calculate CTR and watch time using impression-attributed inputs |

Inspect input headers and semantics before running tools. Preserve raw files;
normalize into a separate file and record any conversion. Missing is not zero.
If a command returns an error or a nonzero status, fix inputs or explain the
missing requirement; never present failed validation as success. Resolve
tool paths from this skill, not the process's current working directory.
Pass user text through structured arguments or properly quoted files; never
interpolate untrusted captions or titles into executable shell syntax.

Use `references/measurement.md` for all numeric interpretation. Scripts
cannot see a thumbnail, establish causality from a retention curve, or verify
that supplied peer cohorts were collected fairly. Perform those reviews
explicitly and state when source media or data is unavailable.

## Apply a useful quality review

- Confirm the title, thumbnail concept, first spoken lines, and final payoff
  all make the same truthful promise. Cite factual claims or rewrite them.
- Preserve the creator's language. Support English, Hindi, and Hinglish
  without using English keyword counts as a quality or performance score.
- Prefer evidence and specificity; do not invent a statistic, testimonial,
  personal experiment, deadline, or superlative to make a hook exciting.
- Check spoken runtime, feasibility of visuals, source rights, and any
  actual disclosure requirements relevant to the deliverable. Avoid generic
  warnings unrelated to the proposed content.
- Inspect thumbnail images at feed size when available. Text checks alone
  do not constitute visual review. Generate or edit images only when asked.
- Confirm manual chapters with the actual media duration, including silent
  tails. Distinguish cut suggestions from executed edits and newly written
  Shorts openings from words already present in the footage.
- Reject fake engagement, bought/bot views, copied scripts, fabricated
  testimonials, and misleading packaging as growth tactics. Keep research
  about learnable structures and underserved needs, not imitation.

## Finish with something the user can act on

Lead with the requested artifact or decision. For analytical work, state the
strongest observed finding, its limitation, one proposed change, and the
metric/window that could confirm or weaken the hypothesis. Do not hide
important uncertainty beneath a confident score.

For a growth plan, complete `assets/experiment-record.md` with real known
inputs; leave unavailable outcome fields explicitly unknown. Revisit it
when the user supplies results. An evaluation date is a plan, not a scheduled
reminder or automatic monitoring job unless separately created with an
available scheduling tool.

Do not append a mandatory approval question to every draft. Complete all
authorized work. Publishing, changing live metadata, or posting replies
requires a suitable integration and the user's authorization; this bundle
does not supply those integrations. Follow the host's artifact-saving rules.

Use the license and source attribution in this package when redistributing
derived material. Do not imply affiliation with YouTube or the upstream author.
