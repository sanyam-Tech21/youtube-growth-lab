# Tool contracts

Contents: execution; text checks; transcript edits; retention; chapters;
matched comparisons; impressions funnel; regression checks.

## Execution

Use Python 3.10+ and the absolute path to `scripts/yt_tools.py` in this skill.
The examples below assume the current directory is this skill's root; resolve
paths explicitly in other contexts. No package installation is required.
All commands emit JSON. Exit code 0 means the command completed; code 2 means
invalid input or a failed chapter/title constraint. Review notes are not errors.
The tools do not fetch analytics, render video, see images, or publish content.

## Text checks

```bash
python3 scripts/yt_tools.py package --title 'Why your room feels cluttered' --thumb 'ONE SMALL CHANGE' --language en
python3 scripts/yt_tools.py hook --hook 'Aapki table par jagah kam hai? Yeh setup try karo.' --language hi --wpm-low 110 --wpm-high 150
```

Neither command scores likely views. `package` checks text only and preserves
Unicode. English-language wording warnings run only with `--language en`.
Character length uses Unicode code points; verify edge cases such as complex
emoji in Studio. `hook` estimates time from whitespace words and the supplied
speaking-rate range; use a timed read for delivery, pauses, or languages without
word spacing. An editorial preference is not a tested winner.

## Transcript edits

Accept `.srt`, `.vtt`, or JSON in either of these shapes:

```json
[{"start": 0, "end": 3.5, "text": "The actual spoken words."}]
```

```json
{"segments": [{"start": 0, "end": 3.5, "text": "The actual spoken words."}]}
```

Use numeric seconds in JSON. Caption files need valid timing lines and blank
lines between cues. Cues may overlap; that produces a warning. Preserve actual
cue text, including numeric-only speech. Malformed timings and negative or
non-finite numbers fail. JSON with a different schema must be explicitly
normalized into a separate file first.

```bash
python3 scripts/yt_tools.py edit recording.srt --duration 600 --language en
```

`--duration` is actual media length, not the last caption timestamp. Optional
`--gap-threshold` defaults to 0.6 seconds and `--padding` to 0.15 seconds on
each side of a gap. These are adjustable editing preferences, not scientific
thresholds. The tool flags caption gaps, narrow English filler-only cues, and
nearby exact repeated utterances. Review all against media. It unions
overlapping candidate intervals before calculating hypothetical runtime.
It does not flag uncaptioned leading/trailing media for automatic removal.

## Retention

Require a header row, explicit column names, position units, retention units,
and actual video duration. For example, a normalized 60-second curve:

```csv
seconds,retention
0,100
15,85
30,72
45,68
60,61
```

```bash
python3 scripts/yt_tools.py retention curve.csv --duration 60 --x-col seconds --y-col retention --x-unit seconds --y-unit percent --transcript recording.srt
```

Omit `--transcript` when unavailable. `--x-unit` accepts `seconds`, `percent`,
or `fraction`. `--y-unit` accepts `percent` or `fraction`. In fraction mode,
0.72 means 72%; in percent mode, 0.72 means 0.72%. Never guess units from max
values. Percent signs are accepted only for declared percent columns.
Retention above 100% is preserved with a units/repeat-viewing note.

Reject missing/invalid values, duplicate column names, duplicate or decreasing
positions, and positions outside the media. Decimal-comma or thousands-grouped
numbers need an explicit locale conversion first. Keep the original file.
The result reports sampled intervals and whether 30-second retention was
observed, interpolated, or unavailable. It does not classify a curve as
universally healthy or infer exact individual exits. If rows were normalized
from a screenshot, identify their approximate nature in the analysis.

## Chapters

Read the transcript and author semantic boundaries as whole seconds or
timestamps. Use real titles, not a bag of frequent words:

```json
[
  {"start": "00:00", "title": "The problem"},
  {"start": "00:25", "title": "A worked example"},
  {"start": "00:50", "title": "What to try next"}
]
```

```bash
python3 scripts/yt_tools.py chapters chapters.json --duration 75
```

Validation requires at least three entries, zero as the first start,
increasing starts, and at least ten seconds per chapter including the final
one. Invalid input has no paste block and returns code 2. Valid timings still
need semantic review and available channel features.

## Matched comparisons

Pass a JSON list with one observed metric per video per run. Each row needs:

```json
{
  "id": "illustrative-video-id",
  "channel": "illustrative-channel",
  "format": "long",
  "metric": "views",
  "metric_definition": "exact definition from the source report",
  "window": "first_168_hours",
  "traffic_source": "organic_all",
  "cohort": "same-language tutorials in a comparable period",
  "duration_seconds": 480,
  "value": 1200,
  "source": "export filename or public source URL",
  "captured_at": "2026-10-05"
}
```

This row is a schema example, not real channel evidence. `format` is `long`,
`short`, or `live`. A window is `first_N_hours`, where N is a positive integer,
or `lifetime_snapshot`; the latter also requires positive `age_days` at capture.
For first-N-hour data, verify the video actually reached that age and the
export covers that interval. Do not relabel lifetime data as first-week data.
Use `traffic_source: public_unknown` for public totals when appropriate;
do not assert they are organic if paid promotion is unknown.

```bash
python3 scripts/yt_tools.py compare videos.json --min-peers 5 --duration-ratio 1.5 --age-ratio 1.5
```

Rows match on channel, format, metric, metric definition, window, traffic
source, and user-defined cohort. Peers must have similar duration; lifetime
snapshots also require similar age. The subject is excluded from its own
baseline. Duplicate IDs or missing metadata fail. A small peer group yields
`insufficient_comparable_data`, not a ratio. A zero peer median yields an
undefined ratio. The tool returns peer IDs for checking, median, and linearly
interpolated quartiles. It does not assess sample representativeness, dates,
topic labels, or truth of source data: review these before interpreting it.

## Impressions funnel

```bash
python3 scripts/yt_tools.py funnel --impressions 10000 --views-from-impressions 500 --watch-seconds-from-impressions 90000
```

These illustrative inputs yield 5% CTR, 180 seconds per attributed view, and
9 watch seconds per impression. Require the same window/source scope for
every input. Use only views and watch time attributed to counted impressions.
Unknown denominators stay unknown. Do not treat these numbers as a forecast,
a native experiment verdict, or a universal performance target.

## Regression checks

Run `python3 scripts/test_yt_tools.py` after modifying the numerical tools.
These tests validate parsing, arithmetic, failure handling, and CLI behavior;
they do not establish effectiveness at gaining views.
