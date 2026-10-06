# Provenance and primary references

Reviewed 2026-10-05. Recheck current pages for live platform instructions.
These links are references, not integrations or permission to access an account.

## Upstream

This is a rewritten, extended adaptation of the workflow concepts in
Jake Schincariol's MIT-licensed [youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill).
The upstream copyright and license notice are retained in `../LICENSE`.
The numerical tools in this version were rewritten. Do not import upstream
hook scores as calibrated performance probabilities or treat unverified
example statistics as facts.

## Current platform guidance

- [A/B test titles and thumbnails](https://support.google.com/youtube/answer/16391400?hl=en):
  eligibility, concurrent alternatives, test outcome, watch time, and duration.
- [Impressions and CTR FAQs](https://support.google.com/youtube/answer/7628154?hl=en):
  audience/source effects, counted-impression scope, and limits of benchmarks.
- [Retention key moments](https://support.google.com/youtube/answer/9314415?hl=en):
  intro metric, skips, rewatching, comparison groups, and processing delay.
- [Video chapters](https://support.google.com/youtube/answer/9884579?hl=en):
  start at zero, three or more ascending chapters, minimum ten seconds, and
  feature availability. Confirm the final chapter against the media duration.
- [Impressions and watch time](https://support.google.com/youtube/answer/9314486?hl=en):
  counted impressions, attributed views, and attributed watch time.
- [Content performance definitions](https://support.google.com/youtube/answer/12220281?hl=en):
  format-specific reports and metric definitions. On the review date, this
  page describes an August 24, 2026 change to views across formats. Preserve
  each export's actual definition; do not assume older and newer series match.
- [Creating Shorts](https://support.google.com/youtube/answer/10059070?hl=en):
  current format and duration guidance; verify for the user's planned upload.
- [Video settings](https://support.google.com/youtube/answer/57404?hl=en) and
  [video resource reference](https://developers.google.com/youtube/v3/docs/videos#snippet.title):
  title and metadata constraints.

Treat official guidance as platform documentation, not a guarantee for a
particular video. Workflow defaults such as sample-size gates, duration
tolerances, and writing pace are transparent design choices in this skill.
