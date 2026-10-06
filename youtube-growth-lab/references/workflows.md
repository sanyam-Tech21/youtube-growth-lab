# Workflow playbook

Contents: onboarding; ideas/research; packaging; scripts; editing; retention;
Shorts; metadata/chapters; comments; planning; audit; experiments/review.

## Onboarding

Capture audience and one job the channel serves, language, topic boundaries,
creator strengths, time/budget, footage/equipment, preferred formats, and goal.
For a business channel, ask whether success means qualified enquiries,
subscribers, or reach; do not optimize raw views at the expense of that goal.
Use the user's actual preferences. Do not import unrelated personal details
into a public channel profile. Label assumptions and make the profile editable.

## Ideas and public research

1. Define the viewer's question, desired experience, or problem. Name why the
   creator can add something useful or entertaining.
2. Browse current public examples when tools are available. Record source URL,
   capture date, publication date, language, format, duration, and exactly
   which metric was observed. Mark unavailable counts as unknown.
3. Include ordinary and weak examples, not just search's popular results.
   Prefer a bounded set such as recent eligible uploads per channel and record
   that sampling rule. Exclude or label promotions, livestreams, and Shorts
   when researching long-form organic content.
4. For observed outliers, use `compare` only with compatible rows. Public
   lifetime views at different ages are not first-week performance. Even an
   age-matched multiple is descriptive and affected by selection and timing.
5. Present an evidence table: viewer need | source/date | observed pattern |
   original angle | evidence gaps | estimated effort. With only one useful
   example, call it an anecdote rather than a validated pattern.
6. Choose one pilot based on audience fit, originality, evidence, and ability
   to deliver. Explain tradeoffs in words; do not turn an arbitrary weighted
   rubric into a "viral probability". Never invent keyword search volumes.

If live browsing fails, use supplied examples or mark ideas as unresearched
hypotheses. Do not claim to have discovered a current trend. A pilot is not
a commitment to endless uploads; define what result would change the plan.

## Titles and thumbnails

Write up to three substantially different title–thumbnail combinations:
for example, outcome, question, and surprising documented contrast. For each,
provide title, image composition, optional thumbnail text, the viewer promise,
the actual evidence/payoff, and why the alternative is meaningfully different.

Run `package` for text checks; inspect images separately when supplied. Do not
force a number into every title or ban useful repetition of a product name.
Treat text length and word-count advice as layout choices. Test readability
on intended screens. If there is no image, clearly call the output a concept.

Read the experiment section before recommending a live test. A preferred
editorial concept is not an experimentally established winner.

## Scripts and hooks

Write three plausible openings with different mechanisms. Useful mechanisms
include: a viewer's question, an immediate demonstration, a real before/after,
an evidenced comparison, a bounded challenge actually performed, or a precise
problem. The mechanism is an option, not a required formula or ranking signal.

Select one through the promise/payoff check and the creator's voice. Run
`hook` for timing, not a score. Supply the full requested spoken body with:

- Immediate orientation to the promised value and appropriate tone.
- Early tangible evidence or a useful partial answer where the topic allows.
- A sequence of meaningful beats; each has an objective and feasible visual.
- Timely resolution of questions introduced earlier. Never withhold the sole
  answer just to stretch watch time.
- A satisfying payoff and one relevant next action if a call to action fits.

Separate spoken words from production directions. Count only spoken words for
runtime; use a range or the creator's measured rate, and include planned pauses
or demonstrations. The first 15 seconds are not the only determinant of a
video's performance. A talking-head format may be entirely appropriate.

## Editing from transcripts

Require a timestamped transcript and actual media duration for precise cuts.
If the transcript is untimed, supply structural editing notes and ask for
timing only when needed. Do not invent timestamps or transcribe inaccessible
video. Use actual transcription tools only when available and authorized.

Run `edit`; review candidates in context. Caption gaps can contain essential
demonstrations, music, or missed speech. Repeated lines can be emphasis or
rolling-caption artifacts. Keep purposeful pauses and meaning intact. Report
union duration, not a sum that counts overlaps twice. Treat projected runtime
as hypothetical until cuts are accepted and the media is rendered. This tool
does not generate a rendered video or an NLE-compatible EDL.

## Retention

Read `measurement.md`, inspect units, and run `retention`. If only a graph image
is available, distinguish approximate visual readings from exported points.
If exports are unavailable in the user's Studio interface, use a screenshot or
manual samples with provenance; do not promise a specific download button.

Select the most consequential observed interval. Inspect the footage or
transcript and offer plausible explanations, for example confusing material,
delayed payoff, title mismatch, an ad break, or skipping to a sought answer.
State which explanation is supported versus untested. A spike may be rewatching
because of value or confusion. A flat curve does not prove the topic or edit
is defective, and healthy retention does not by itself prove packaging is bad.

Give one change and a like-for-like comparison plan. Do not treat correlations
as an exact diagnosis of why individuals left.

## Shorts

Select only spans that stand alone and have a useful or entertaining payoff.
Use the requested duration; verify current eligibility for the chosen format
instead of treating 20–55 seconds as a platform limit. Do not force five clips
if the footage contains only two suitable moments.

For each: existing in/out timecodes, original duration, independent premise,
spoken opening, on-screen text suggestion, payoff, crop/accessibility notes,
and whether a new recording is required. Keep the source meaning intact.
Loops are optional creative choices, not a requirement. Distinguish a clip
plan from a cut video. Track Shorts separately from long-form tests.

## Descriptions, search intent, and chapters

Describe what the video actually delivers in natural language. Identify a
primary relevant query and optional related queries without promising rank.
Include confirmed resources/links, an appropriate next video, and only useful
tags such as ambiguous spellings. Avoid stuffing every query into the first
two lines. Do not invent sponsor links or endorsements.

Author chapters by reading semantic transitions, not just counting pauses.
Create JSON objects with `start` and `title`; use `chapters` with the real media
duration. Correct invalid boundaries before presenting a paste block. Do not
manufacture three distinct topics in a video that does not have them. Timing
validity alone does not guarantee chapter availability for the channel.

## Comments

Classify supplied comments as answerable questions, factual corrections,
positive feedback, constructive criticism, abuse/spam, or ambiguous. Do not
label every disagreement as bait. Check corrections before accepting or
rejecting them. Draft brief, specific replies in the creator's voice, allowing
more space for a complex answer. Avoid invented promises and repeated canned
replies. Recommend a pin only if it adds value. Drafting does not send, heart,
delete, hide, or pin anything. Reply speed is not a guaranteed ranking tactic.

## Calendar and capacity

Budget research, writing, filming, editing, packaging, and analysis. Include a
buffer as an explicit planning assumption. Fit upload count and mix to the
hours available; do not impose one anchor, one follow-up, and three Shorts on
everyone. Explain if even one polished video exceeds the budget and reduce
scope. Keep repeatability and audience fit ahead of volume.

For each planned piece: intended viewer, promise, evidence/asset, work estimate,
owner if supplied, release target/timezone, and evaluation window. Treat a
release date as a planning choice, not a universal algorithmic best time.
Only extract Shorts when they serve the audience and the footage supports them.

## Channel audit

Examine audience/topic fit, delivery of the promise, packaging, traffic sources,
viewer engagement, and the creator's production constraints. A public-only
audit must state that private analytics were not checked. Do not declare a
retention bottleneck from a title score or low total views alone.

Lead with one priority supported by available evidence. Show observations,
alternative explanations, what is already working, and one feasible experiment.
If data cannot separate competing explanations, name the next measurement
instead of pretending the bottleneck is known.

## Experiments and review

Read `measurement.md`; complete `assets/experiment-record.md`. Choose a
hypothesis, variants, audience, metric, reporting window, guardrails, and a
decision rule before observing the result. For eligible long-form packaging,
prefer YouTube's native concurrent experiment when available.

Changing both title and thumbnail tests the combination, not each component's
individual contribution. Sequential changes are observational: audience, time,
topic demand, and traffic source can change. Do not declare causal lift or a
statistical winner from a before/after CTR jump.

Review at agreed windows after the relevant data is processed. Use Studio's
reported experiment outcome; if inconclusive, keep that conclusion. For an
observational pilot, report measured differences, confounders, and repeat or
revise based on the predefined rule. Save the result with source and metric
definition. Never promise a view-count floor or imply that a checklist has
been field-validated without actual channel experiments.
