# Measurement and interpretation

## Preserve the meaning of each number

Record metric name, definition, units, source, capture date, reporting window,
format, and traffic source. Record whether views are lifetime snapshots,
first-N-hour totals, engaged views, or another platform metric. Never silently
combine these. Platform definitions can change; consult `sources.md` and the
current report. Historical values may not be comparable across a definition
change without a documented consistent series.

Distinguish observed, calculated, inferred, and unavailable values. Do not
convert missing values to zeros. A publicly visible view count reveals neither
retention nor click-through rate. Paid promotion and organic reach need separate
interpretation. Do not assume a view represents a unique individual.

## Comparable baselines

Prefer a channel's own similar-length, same-format videos, measured over the
same post-publication interval. Match topic/audience and traffic source where
possible. Exclude the target video from its peer baseline. Record sample size
and median/spread. The `compare` tool defaults to five peers and 1.5× age/length
tolerances as transparent workflow settings, not scientific validity thresholds.
Change these settings only with a reason and keep them in the report.

For public lifetime snapshots, require age at capture; age filtering reduces
but does not remove differences in growth curves. A median multiple means
"observed relative to these selected peers," not "expected performance".
Include source and sampling method to expose survivorship bias. With few
comparable videos, say the evidence is sparse. A zero median is undefined
for division and must not produce infinity or a zero performance ratio.

For a new channel, use a discovery pilot rather than invented benchmarks.
Define learning outcomes such as which topics prompt meaningful questions,
whether viewers understand the promise, and whether the creator can sustain
production. Numeric future targets are goals, not forecasts.

## Impressions funnel

Use the same scope and window for all terms:

- CTR = 100 × views attributed to counted impressions / counted impressions.
- Watch seconds per impression = watch seconds attributed to those impressions
  / counted impressions.
- Mean view duration for that subset = attributed watch seconds / attributed
  views.

Never use total views as the CTR numerator, or mix all-view average duration
with impression-only CTR to label an exact watch-time-per-impression result.
If only those mixed-scope values exist, do not run `funnel`; request compatible
data or report each supplied metric separately. A zero denominator yields
unknown, not zero. Public views and Shorts feed starts are not substitutes
for thumbnail impressions. See official definitions in `sources.md`.

## Retention

Require explicit position units (seconds, percent of duration, or fraction)
and retention units (percent or fraction). A 45-second video does not make
its x-axis percentages. Preserve retention above 100% and verify the units;
repeat viewing can matter. Do not cap it merely to fit a percentage range.

Report the observed or interpolated value at 30 seconds only if the video and
data reach that time. Show the interpolation bracket; coarse samples cannot
locate an exact second. Never extrapolate missing endpoints. For shorter
videos, use observed points appropriate to their duration rather than a
fabricated 30-second metric. A change from 80% to 60% is 20 percentage points,
not proof that exactly 20% of unique people exited there.

List sampled drops as intervals, with transcript context when available.
Dips may involve skipping or abandonment. Compare similar content and inspect
media before choosing an explanation. Do not impose a universal 25% "healthy
hook leak" or assume that cutting always fixes a declining curve.

## Controlled packaging tests

As documented on 2026-10-05, YouTube's native tool can compare up to three
title/thumbnail alternatives concurrently for eligible videos through desktop
Studio with advanced features. It excludes Shorts and certain other states
or audiences. Verify current eligibility before giving live instructions.
It may take up to two weeks; changing metadata during a test stops it. Use
its watch-time-based result and retain "Performed Same" or "Inconclusive"
when reported. Do not select a winner solely because raw CTR is higher.

Without a native result or correctly randomized experiment with adequate
underlying data, report descriptive differences only. Aggregated view counts
cannot supply a trustworthy watch-time significance test. Do not invent
p-values, confidence intervals, sample-size sufficiency, or causal attribution.
Changing a video twice on different days is not a concurrent randomized test.

## Decide what to do next

Use the experiment's predeclared metric and guardrails. Consider viewer value,
topic demand, source mix, and returning audience alongside clicks. State one
next action: retain, revise, repeat, or stop. An inconclusive experiment is a
valid result. A passed code test validates calculations, not YouTube growth.
