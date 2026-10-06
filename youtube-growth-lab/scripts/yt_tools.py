#!/usr/bin/env python3
"""Local, dependency-free YouTube analysis tools. Run with --help.

Outputs are descriptive checks, never predictions of views. No network,
credentials, publishing, media modification, or third-party dependencies.
"""
import argparse
import bisect
import csv
import html
import json
import math
from pathlib import Path
import re
import statistics
import sys
import unicodedata


class InputError(ValueError):
    pass


def number(value, label, minimum=0, maximum=None):
    if isinstance(value, bool):
        raise InputError(f"{label}: expected a finite number, not a boolean")
    try:
        n = float(value)
    except (ValueError, TypeError):
        raise InputError(f"{label}: expected a number") from None
    if not math.isfinite(n) or n < minimum or (maximum is not None and n > maximum):
        raise InputError(f"{label}: outside allowed range or non-finite")
    return n


def positive(value, label):
    n = number(value, label)
    if n == 0:
        raise InputError(f"{label}: must be greater than zero")
    return n


def text_field(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label}: expected nonempty text")
    return value.strip()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def tokens(text):
    """Preserve Unicode letters and combining marks, including Hindi matras."""
    out, current = [], []
    for c in unicodedata.normalize("NFC", text).casefold():
        if unicodedata.category(c)[0] in "LNM" or (c in "'’" and current):
            current.append(c)
        elif current:
            out.append("".join(current).strip("'’"))
            current = []
    if current:
        out.append("".join(current).strip("'’"))
    return [w for w in out if w]


def package_check(title, thumb="", language="en"):
    title = text_field(title, "title")
    errors, review = [], []
    if len(title) > 100:
        errors.append("Title exceeds 100 Unicode code points; shorten and verify in Studio.")
    if "<" in title or ">" in title:
        errors.append("Remove angle brackets from the title.")
    if len(title) > 60:
        review.append("Preview the title on intended devices; truncation varies by surface and font.")
    if len(thumb.split()) > 4:
        review.append("Check thumbnail text at feed size; there is no universal word-count limit.")
    stop = set("the a an of for to in on and or is are with you your my i this that it how what why".split()) if language == "en" else set()
    shared = sorted((set(tokens(title)) & set(tokens(thumb))) - stop)
    if shared:
        review.append("Repeated terms may be useful for recognition; inspect whether image and title add distinct information.")
    if language == "en":
        vague = sorted(set(tokens(title)) & {"amazing", "insane", "crazy", "secret", "best", "ultimate"})
        if vague:
            review.append("Substantiate or replace broad claims: " + ", ".join(vague))
    return {"title": title, "thumbnail_text": thumb, "title_code_points": len(title),
            "errors": errors, "review_notes": review, "shared_terms": shared,
            "manual_checks": ["Audience understands the promise", "Video delivers the promise",
                              "Actual thumbnail remains readable at feed size", "Claims have evidence"],
            "visual_review_performed": False, "predicts_views": False}


def hook_check(hook, language="en", wpm_low=120, wpm_high=170):
    hook = text_field(hook, "hook")
    low, high = positive(wpm_low, "wpm-low"), positive(wpm_high, "wpm-high")
    if low > high:
        raise InputError("wpm-low must not exceed wpm-high")
    wc = len(hook.split())
    warnings = []
    if language in {"zh", "ja", "th"}:
        warnings.append("Whitespace word timing is unreliable for this language; use a timed read.")
    if language == "en" and re.match(r"(?i)^(hey guys|welcome back|before we get started)\b", hook):
        warnings.append("Consider opening with the viewer's purpose or the promised result.")
    return {"hook": hook, "whitespace_words": wc,
            "spoken_seconds_estimate": [round(wc * 60 / high, 1), round(wc * 60 / low, 1)],
            "wpm_assumptions": [low, high], "review_notes": warnings,
            "manual_checks": ["Matches title and thumbnail", "Names a relevant question or outcome",
                              "Has a real payoff", "Sounds natural in the creator's language"],
            "timing_note": "Estimate only; pauses and delivery need a timed read.", "predicts_views": False}


def timestamp(value):
    s = str(value).strip().replace(",", ".")
    if ":" not in s:
        return number(s, "timestamp")
    parts = s.split(":")
    if len(parts) not in (2, 3) or not all(re.fullmatch(r"\d+", p) for p in parts[:-1]):
        raise InputError(f"Invalid timestamp: {value}")
    secs = number(parts[-1], "timestamp seconds", maximum=59.999999)
    minutes = int(parts[-2])
    if len(parts) == 3:
        if minutes >= 60:
            raise InputError(f"Invalid timestamp minutes: {value}")
        return int(parts[0]) * 3600 + minutes * 60 + secs
    return minutes * 60 + secs


def clean_caption(value):
    if not isinstance(value, str):
        raise InputError("Transcript text must be a string")
    return html.unescape(re.sub(r"<[^>]*>", "", value)).strip()


def load_cues(path):
    path = Path(path)
    raw = path.read_text(encoding="utf-8-sig")
    rows, warnings = [], []
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = data.get("segments")
        if not isinstance(data, list):
            raise InputError("Transcript JSON must be a segment list or an object with segments")
        for idx, row in enumerate(data, 1):
            if not isinstance(row, dict) or not {"start", "end", "text"} <= row.keys():
                raise InputError(f"Transcript segment {idx}: needs start, end, text")
            rows.append((number(row["start"], "start"), number(row["end"], "end"), clean_caption(row["text"])))
    elif path.suffix.lower() in {".srt", ".vtt"}:
        for block in re.split(r"\n\s*\n", raw.replace("\r\n", "\n").strip()):
            lines = block.splitlines()
            if not lines:
                continue
            if re.match(r"^(NOTE(?:\s|$)|STYLE$|REGION$)", lines[0].strip()):
                continue
            timing = [i for i, line in enumerate(lines) if "-->" in line]
            if not timing:
                if lines[0].strip().startswith("WEBVTT"):
                    continue
                raise InputError("Caption block has no timing; use blank lines between cues")
            if len(timing) != 1:
                raise InputError("Caption block contains multiple timings; separate cues with blank lines")
            i = timing[0]
            match = re.fullmatch(r"\s*([\d:.,]+)\s*-->\s*([\d:.,]+)(?:\s+.*)?", lines[i])
            if not match:
                raise InputError("Invalid caption timing line")
            rows.append((timestamp(match[1]), timestamp(match[2]), clean_caption(" ".join(lines[i + 1:]))))
    else:
        raise InputError("Use .srt, .vtt or .json for timestamped transcripts")
    for idx, (start, end, _) in enumerate(rows, 1):
        if end <= start:
            raise InputError(f"Cue {idx}: end must be greater than start")
    if not rows:
        raise InputError("No transcript cues found")
    if rows != sorted(rows, key=lambda r: (r[0], r[1])):
        warnings.append("Cues were reordered by timestamp.")
    rows.sort(key=lambda r: (r[0], r[1]))
    end_so_far = 0
    for start, end, _ in rows:
        if start < end_so_far:
            warnings.append("Overlapping cues detected; review rolling captions and speaker overlap.")
            break
        end_so_far = max(end_so_far, end)
    return rows, warnings


def union_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def edit_report(path, duration, gap_threshold=0.6, padding=0.15, language="en"):
    duration = positive(duration, "duration")
    threshold, pad = positive(gap_threshold, "gap-threshold"), number(padding, "padding")
    if threshold <= 2 * pad:
        raise InputError("gap-threshold must exceed twice padding")
    cues, warnings = load_cues(path)
    if max(c[1] for c in cues) > duration + 1e-6:
        raise InputError("Transcript ends after the supplied media duration")
    candidates, last_speech = [], None
    covered_until = cues[0][1]
    for idx, (start, end, text) in enumerate(cues):
        if idx and start - covered_until > threshold:
            candidates.append({"kind": "CAPTION_GAP", "start": covered_until + pad, "end": start - pad,
                               "reason": "No caption here; check for music, demonstration, or untranscribed speech."})
        covered_until = max(covered_until, end)
        words = tokens(text)
        filler = language == "en" and bool(re.fullmatch(r"(?:um+|uh+|erm+)(?:[\s,.!?]+(?:um+|uh+|erm+))*[\s,.!?]*", text, re.I))
        if filler:
            candidates.append({"kind": "FILLER_CANDIDATE", "start": start, "end": end, "reason": text})
        elif words:
            if last_speech is not None:
                old_start, old_end, old_text = last_speech
                if 0 <= start - old_end <= 5 and len(words) >= 3 and words == tokens(old_text):
                    candidates.append({"kind": "EXACT_REPEAT_CANDIDATE", "start": old_start, "end": old_end,
                                       "reason": "Repeated wording may be a retake or intentional emphasis."})
            last_speech = (start, end, text)
    candidates.sort(key=lambda c: (c["start"], c["end"], c["kind"]))
    merged = union_intervals((c["start"], c["end"]) for c in candidates)
    removed = sum(end - start for start, end in merged)
    return {"duration_seconds": duration, "candidates": candidates, "union_intervals": merged,
            "candidate_union_seconds": round(removed, 3),
            "hypothetical_duration_if_all_accepted": round(duration - removed, 3),
            "warnings": warnings, "media_modified": False,
            "note": "Review every candidate against media. Caption absence is not evidence of silence; no cut is approved."}


def csv_number(cell, unit, label):
    value = cell.strip()
    if not value:
        raise InputError(f"{label}: missing value; do not fill missing data with zero")
    if value.endswith("%"):
        if unit != "percent":
            raise InputError(f"{label}: percent sign conflicts with declared {unit} unit")
        value = value[:-1]
    if "," in value:
        raise InputError(f"{label}: normalize decimal/grouping separators explicitly first")
    return number(value, label)


def retention_points(path, x_col, y_col, x_unit, y_unit, duration):
    duration = positive(duration, "duration")
    points = []
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise InputError("Retention CSV contains duplicate column names")
        if x_col not in fields or y_col not in fields or x_col == y_col:
            raise InputError(f"Choose distinct existing columns; found {fields}")
        for line, row in enumerate(reader, 2):
            if None in row or row[x_col] is None or row[y_col] is None:
                raise InputError(f"CSV row {line}: malformed column count")
            x = csv_number(row[x_col], x_unit, f"row {line}, {x_col}")
            y = csv_number(row[y_col], y_unit, f"row {line}, {y_col}")
            if x_unit == "fraction":
                if x > 1:
                    raise InputError("Position fraction exceeds 1")
                x *= duration
            elif x_unit == "percent":
                if x > 100:
                    raise InputError("Position percent exceeds 100")
                x *= duration / 100
            if x > duration + 1e-6:
                raise InputError("Retention position exceeds media duration")
            if y_unit == "fraction":
                y *= 100
            points.append((x, y))
    if len(points) < 2:
        raise InputError("At least two retention points are required")
    if any(b[0] <= a[0] for a, b in zip(points, points[1:])):
        raise InputError("Retention positions must be strictly increasing; resolve duplicates or sort explicitly")
    return points


def interpolate(points, at):
    if at < points[0][0] or at > points[-1][0]:
        return None
    idx = bisect.bisect_left([p[0] for p in points], at)
    if points[idx][0] == at:
        return {"value_pct": points[idx][1], "method": "observed", "bracket_seconds": [at, at]}
    x0, y0 = points[idx - 1]
    x1, y1 = points[idx]
    return {"value_pct": y0 + (at - x0) / (x1 - x0) * (y1 - y0),
            "method": "linear_interpolation", "bracket_seconds": [x0, x1]}


def retention_report(path, x_col, y_col, x_unit, y_unit, duration, transcript=None):
    duration = positive(duration, "duration")
    points = retention_points(path, x_col, y_col, x_unit, y_unit, duration)
    cues, warnings = load_cues(transcript) if transcript else ([], [])
    if cues and max(c[1] for c in cues) > duration + 1e-6:
        raise InputError("Transcript exceeds media duration")
    if any(p[1] > 100 for p in points):
        warnings.append("Retention exceeds 100%; preserve possible repeat viewing and verify source units.")
    if points[0][0] != 0 or points[-1][0] != duration:
        warnings.append("Partial curve: no extrapolation to missing endpoints.")
    intro = interpolate(points, 30) if duration >= 30 else None
    if intro and intro["method"] != "observed":
        warnings.append("The 30-second value is interpolated; inspect its reported sample interval.")
    drop = points[0][1] - intro["value_pct"] if intro and points[0][0] == 0 else None
    intervals = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        delta = y1 - y0
        if delta < 0:
            intervals.append({"start_seconds": x0, "end_seconds": x1,
                              "drop_pp": -delta, "drop_pp_per_second": -delta / (x1 - x0),
                              "transcript_context": " ".join(c[2] for c in cues if c[0] < x1 and c[1] > x0)[:800]})
    intervals.sort(key=lambda r: (-r["drop_pp"], r["start_seconds"]))
    return {"points": len(points), "duration_seconds": duration,
            "input_units": {"position": x_unit, "retention": y_unit},
            "observed_span_seconds": [points[0][0], points[-1][0]],
            "retention_at_30_seconds": intro, "start_to_30_change_pp": drop,
            "largest_drop_intervals": intervals[:5], "warnings": warnings,
            "interpretation": "Percentage-point changes over sampled intervals, not counts of people or proof of cause. Compare like-for-like videos and inspect media."}


def label_time(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def chapters_check(rows, duration):
    duration = positive(duration, "duration")
    if not isinstance(rows, list) or not rows:
        raise InputError("Chapters JSON must be a nonempty list")
    normalized, errors = [], []
    for idx, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not {"start", "title"} <= row.keys():
            raise InputError(f"Chapter {idx}: needs start and title")
        start = timestamp(row["start"])
        title = text_field(row["title"], "chapter title")
        if "\n" in title or "\r" in title:
            raise InputError("Chapter titles must be single lines")
        if start != int(start):
            raise InputError("Use whole-second chapter starts so validation matches rendered timestamps")
        normalized.append({"start": int(start), "title": title})
    if len(rows) < 3:
        errors.append("At least three chapters are required.")
    if normalized[0]["start"] != 0:
        errors.append("First chapter must start at 00:00.")
    for idx, row in enumerate(normalized):
        end = normalized[idx + 1]["start"] if idx + 1 < len(normalized) else duration
        if end - row["start"] < 10:
            errors.append(f"Chapter {idx + 1} must last at least 10 seconds, in increasing order and within the video.")
    return {"valid": not errors, "errors": errors, "chapters": normalized,
            "paste_block": "\n".join(f"{label_time(r['start'])} {r['title']}" for r in normalized) if not errors else None,
            "note": "Timing validation only. Check titles, boundaries, and channel feature eligibility in Studio."}


def quantile(values, fraction):
    ordered = sorted(values)
    point = (len(ordered) - 1) * fraction
    lower, upper = math.floor(point), math.ceil(point)
    return ordered[lower] + (point - lower) * (ordered[upper] - ordered[lower])


def compare_rows(rows, min_peers=5, duration_ratio=1.5, age_ratio=1.5):
    if not isinstance(rows, list) or not rows:
        raise InputError("Comparison JSON must be a nonempty list")
    if min_peers < 2:
        raise InputError("min-peers must be at least 2; small samples remain exploratory")
    duration_ratio = number(duration_ratio, "duration-ratio", minimum=1)
    age_ratio = number(age_ratio, "age-ratio", minimum=1)
    group_fields = ["channel", "format", "metric", "metric_definition", "window", "traffic_source", "cohort"]
    checked, seen = [], set()
    for idx, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise InputError(f"Row {idx} must be an object")
        r = dict(row)
        for key in ["id", "source", "captured_at"] + group_fields:
            r[key] = text_field(r.get(key), f"row {idx}, {key}")
        if r["id"] in seen:
            raise InputError(f"Duplicate video id: {r['id']}; use one metric per video per run")
        seen.add(r["id"])
        if r["format"] not in {"long", "short", "live"}:
            raise InputError("format must be long, short, or live")
        if not re.fullmatch(r"first_[1-9]\d*_hours|lifetime_snapshot", r["window"]):
            raise InputError("window must be first_N_hours (positive integer N) or lifetime_snapshot")
        r["value"] = number(r.get("value"), "value")
        if r["metric"] == "ctr_pct" and r["value"] > 100:
            raise InputError("ctr_pct exceeds 100")
        r["duration_seconds"] = positive(r.get("duration_seconds"), "duration_seconds")
        if r["window"] == "lifetime_snapshot":
            r["age_days"] = positive(r.get("age_days"), "age_days")
        checked.append(r)
    results = []
    for row in checked:
        peers = []
        for p in checked:
            if p["id"] == row["id"] or any(p[k] != row[k] for k in group_fields):
                continue
            if max(p["duration_seconds"], row["duration_seconds"]) / min(p["duration_seconds"], row["duration_seconds"]) > duration_ratio:
                continue
            if row["window"] == "lifetime_snapshot" and max(p["age_days"], row["age_days"]) / min(p["age_days"], row["age_days"]) > age_ratio:
                continue
            peers.append(p)
        result = {"id": row["id"], "value": row["value"], "peer_count": len(peers),
                  "peer_ids": [p["id"] for p in peers], "status": "insufficient_comparable_data",
                  "median": None, "q25": None, "q75": None, "multiple": None}
        if len(peers) >= min_peers:
            values = [p["value"] for p in peers]
            med = statistics.median(values)
            result.update(status="descriptive_only" if med else "zero_peer_median", median=med,
                          q25=quantile(values, 0.25), q75=quantile(values, 0.75),
                          multiple=row["value"] / med if med else None)
        results.append(result)
    results.sort(key=lambda r: (r["multiple"] is None, -(r["multiple"] or 0), r["id"]))
    return {"results": results, "comparison_keys": group_fields,
            "settings": {"min_peers": min_peers, "duration_ratio": duration_ratio, "age_ratio": age_ratio},
            "note": "Leave-one-out descriptive comparisons, not forecasts or causal effects. Thresholds are workflow choices, not statistical significance. Cohort quality, metric changes, age, calendar period, and selection bias need human review."}


def funnel(impressions, views_from_impressions, watch_seconds_from_impressions):
    n = number(impressions, "impressions")
    v = number(views_from_impressions, "views-from-impressions")
    w = number(watch_seconds_from_impressions, "watch-seconds-from-impressions")
    if not n.is_integer() or not v.is_integer() or v > n:
        raise InputError("Impressions and views-from-impressions must be integer counts with views <= impressions")
    if not v and w:
        raise InputError("Watch time cannot be positive with zero views-from-impressions")
    return {"impressions": n, "views_from_impressions": v,
            "ctr_pct": 100 * v / n if n else None,
            "average_seconds_for_impression_views": w / v if v else None,
            "watch_seconds_per_impression": w / n if n else None,
            "note": "All inputs must have the same reporting window and impression-attributed scope. Do not substitute total views or total watch time."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("package", help="Check title and thumbnail text; no performance score")
    p.add_argument("--title", required=True)
    p.add_argument("--thumb", default="")
    p.add_argument("--language", default="en")
    p = sub.add_parser("hook", help="Estimate spoken timing and list editorial checks")
    p.add_argument("--hook", required=True)
    p.add_argument("--language", default="en")
    p.add_argument("--wpm-low", type=float, default=120)
    p.add_argument("--wpm-high", type=float, default=170)
    p = sub.add_parser("edit", help="Suggest reviewable cuts from timestamped captions")
    p.add_argument("path")
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--gap-threshold", type=float, default=0.6)
    p.add_argument("--padding", type=float, default=0.15)
    p.add_argument("--language", default="en")
    p = sub.add_parser("retention", help="Analyze explicit CSV columns and units")
    p.add_argument("path")
    p.add_argument("--duration", type=float, required=True)
    p.add_argument("--x-col", required=True)
    p.add_argument("--y-col", required=True)
    p.add_argument("--x-unit", choices=["seconds", "percent", "fraction"], required=True)
    p.add_argument("--y-unit", choices=["percent", "fraction"], required=True)
    p.add_argument("--transcript")
    p = sub.add_parser("chapters", help="Validate agent-authored chapter boundaries and titles")
    p.add_argument("path")
    p.add_argument("--duration", type=float, required=True)
    p = sub.add_parser("compare", help="Compare videos only against matching peers")
    p.add_argument("path")
    p.add_argument("--min-peers", type=int, default=5)
    p.add_argument("--duration-ratio", type=float, default=1.5)
    p.add_argument("--age-ratio", type=float, default=1.5)
    p = sub.add_parser("funnel", help="Calculate metrics from impression-attributed data")
    p.add_argument("--impressions", type=float, required=True)
    p.add_argument("--views-from-impressions", type=float, required=True)
    p.add_argument("--watch-seconds-from-impressions", type=float, required=True)
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        if command == "package":
            out = package_check(**args)
        elif command == "hook":
            out = hook_check(**args)
        elif command == "edit":
            out = edit_report(**args)
        elif command == "retention":
            out = retention_report(**args)
        elif command == "chapters":
            out = chapters_check(read_json(args.pop("path")), **args)
        elif command == "compare":
            out = compare_rows(read_json(args.pop("path")), **args)
        else:
            out = funnel(**args)
        print(json.dumps(out, ensure_ascii=False, indent=2, allow_nan=False))
        if (command == "chapters" and not out["valid"]) or (command == "package" and out["errors"]):
            return 2
        return 0
    except (InputError, OSError, ValueError, csv.Error) as exc:
        print(json.dumps({"error": str(exc), "command": command}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
