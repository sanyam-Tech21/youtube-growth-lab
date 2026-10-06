#!/usr/bin/env python3
"""Regression tests for data mistakes that can change editorial decisions."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import yt_tools as yt


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def file(self, name, contents):
        p = self.root / name
        p.write_text(contents, encoding="utf-8")
        return str(p)

    def curve(self, content, duration=60, x_unit="seconds", y_unit="percent"):
        return yt.retention_report(self.file("curve.csv", "x,y\n" + content), "x", "y", x_unit, y_unit, duration)

    def row(self, i, value=100, **kwargs):
        row = dict(id=str(i), channel="sample", format="long", metric="views",
                   metric_definition="sample_definition", window="first_168_hours",
                   traffic_source="organic_all", cohort="English tutorial", duration_seconds=300,
                   value=value, source="synthetic fixture", captured_at="2026-10-05")
        row.update(kwargs)
        return row

    def test_top_level_json_list_and_object(self):
        segment = dict(start=0, end=2, text="123")
        for data in ([segment], {"segments": [segment]}):
            cues, _ = yt.load_cues(self.file("sample.json", json.dumps(data)))
            self.assertEqual(cues, [(0, 2, "123")])

    def test_srt_preserves_numeric_speech(self):
        cues, _ = yt.load_cues(self.file("sample.srt", "1\n00:00:00,000 --> 00:00:02,000\n123\n\n2\n00:00:03,000 --> 00:00:04,000\nहाँ\n"))
        self.assertEqual([c[2] for c in cues], ["123", "हाँ"])

    def test_vtt_ignores_notes_and_settings(self):
        raw = "WEBVTT\n\nNOTE editor note\nnot speech\n\ncue-a\n00:00.000 --> 00:02.000 align:start\n<v Me>Hello &amp; welcome</v>\n\nSTYLE\n::cue { color: red; }\n"
        cues, _ = yt.load_cues(self.file("sample.vtt", raw))
        self.assertEqual(cues[0][2], "Hello & welcome")

    def test_invalid_transcript_times_fail(self):
        for segment in [dict(start=2, end=1, text="x"), dict(start=-1, end=1, text="x"),
                        dict(start=0, end=float("nan"), text="x")]:
            with self.assertRaises(yt.InputError):
                yt.load_cues(self.file("sample.json", json.dumps([segment])))

    def test_invalid_timestamp_components_fail(self):
        for value in ["00:61", "01:60:00", "a:b:c", "1:2:3:4", "inf"]:
            with self.assertRaises(yt.InputError):
                yt.timestamp(value)

    def test_sort_and_overlap_warning(self):
        data = [dict(start=2, end=4, text="second"), dict(start=0, end=3, text="first")]
        cues, warnings = yt.load_cues(self.file("s.json", json.dumps(data)))
        self.assertEqual(cues[0][0], 0)
        self.assertEqual(len(warnings), 2)

    def test_edit_uses_interval_union(self):
        data = [dict(start=0, end=2, text="um"), dict(start=1, end=3, text="uh")]
        out = yt.edit_report(self.file("s.json", json.dumps(data)), 5)
        self.assertEqual(out["candidate_union_seconds"], 3)
        self.assertEqual(out["hypothetical_duration_if_all_accepted"], 2)

    def test_edit_gap_uses_covered_extent(self):
        data = [dict(start=0, end=10, text="long caption"), dict(start=2, end=3, text="overlap"),
                dict(start=4, end=5, text="still covered")]
        out = yt.edit_report(self.file("s.json", json.dumps(data)), 12)
        self.assertFalse(any(c["kind"] == "CAPTION_GAP" for c in out["candidates"]))

    def test_edit_does_not_cut_meaningful_single_word(self):
        data = [dict(start=0, end=1, text="Right."), dict(start=1, end=2, text="Okay.")]
        self.assertEqual(yt.edit_report(self.file("s.json", json.dumps(data)), 2)["candidates"], [])

    def test_edit_full_duration_and_media_bounds(self):
        path = self.file("s.json", json.dumps([dict(start=0, end=2, text="words")]))
        self.assertEqual(yt.edit_report(path, 10)["hypothetical_duration_if_all_accepted"], 10)
        with self.assertRaises(yt.InputError):
            yt.edit_report(path, 1)

    def test_edit_padded_gap_and_repeat(self):
        data = [dict(start=0, end=2, text="Here is the result"),
                dict(start=3, end=4, text="um"), dict(start=4, end=6, text="Here is the result")]
        out = yt.edit_report(self.file("s.json", json.dumps(data)), 6)
        self.assertAlmostEqual(out["candidate_union_seconds"], 3.7)

    def test_seconds_axis_not_guessed_as_percent(self):
        out = self.curve("0,100\n15,80\n30,70\n45,65\n", duration=45)
        self.assertEqual(out["retention_at_30_seconds"]["value_pct"], 70)
        self.assertEqual(out["start_to_30_change_pp"], 30)

    def test_fraction_and_percentage_equivalence(self):
        a = self.curve("0,1\n0.5,0.7\n1,0.6\n", x_unit="fraction", y_unit="fraction")
        b = self.curve("0%,100%\n50%,70%\n100%,60%\n", x_unit="percent")
        self.assertEqual(a["retention_at_30_seconds"], b["retention_at_30_seconds"])

    def test_intro_is_value_at_30_not_minimum_before_it(self):
        out = self.curve("0,100\n10,50\n30,80\n60,60\n")
        self.assertEqual(out["retention_at_30_seconds"]["value_pct"], 80)

    def test_interpolation_has_bracket(self):
        out = self.curve("0,100\n20,80\n40,60\n60,50\n")
        self.assertEqual(out["retention_at_30_seconds"]["value_pct"], 70)
        self.assertEqual(out["retention_at_30_seconds"]["bracket_seconds"], [20, 40])

    def test_short_video_no_fake_30s_value(self):
        self.assertIsNone(self.curve("0,100\n20,50\n", duration=20)["retention_at_30_seconds"])

    def test_partial_curve_no_extrapolation(self):
        out = self.curve("5,90\n20,70\n")
        self.assertIsNone(out["retention_at_30_seconds"])
        self.assertIsNone(out["start_to_30_change_pp"])

    def test_retention_above_100_preserved(self):
        self.assertEqual(self.curve("0,100\n30,130\n60,105\n")["retention_at_30_seconds"]["value_pct"], 130)

    def test_zero_start_is_not_replaced_with_100(self):
        self.assertEqual(self.curve("0,0\n30,10\n60,5\n")["start_to_30_change_pp"], -10)

    def test_bad_curve_fails(self):
        for body in ["0,100\n0,90\n", "30,80\n0,100\n", "0,100\n10,\n", "0,100\n30,nan\n",
                     "0,100\n80,50\n", "0,100\n10,-20\n"]:
            with self.assertRaises(yt.InputError):
                self.curve(body)

    def test_retention_unit_conflict_and_extra_numeric_columns(self):
        with self.assertRaises(yt.InputError):
            self.curve("0,100%\n1,80%\n", x_unit="fraction", y_unit="fraction")
        path = self.file("columns.csv", "junk,x,y\n999,0,100\n888,30,70\n777,60,60\n")
        self.assertEqual(yt.retention_report(path, "x", "y", "seconds", "percent", 60)["retention_at_30_seconds"]["value_pct"], 70)

    def test_valid_chapters_with_full_duration(self):
        rows = [dict(start=0, title="One"), dict(start=10, title="Two"), dict(start=20, title="Three")]
        out = yt.chapters_check(rows, 30)
        self.assertTrue(out["valid"])
        self.assertTrue(out["paste_block"].startswith("00:00 "))

    def test_invalid_chapter_tail_no_paste(self):
        rows = [dict(start=0, title="One"), dict(start=10, title="Two"), dict(start=20, title="Three")]
        out = yt.chapters_check(rows, 29.9)
        self.assertFalse(out["valid"])
        self.assertIsNone(out["paste_block"])

    def test_fractional_chapters_rejected(self):
        with self.assertRaises(yt.InputError):
            yt.chapters_check([dict(start=0.1, title="One")], 50)

    def test_chapter_order_rejected(self):
        out = yt.chapters_check([dict(start=x, title="Section") for x in [0, 30, 20]], 60)
        self.assertFalse(out["valid"])

    def test_compare_excludes_self(self):
        rows = [self.row(i, x) for i, x in enumerate([10, 20, 30, 40, 50, 1000])]
        out = yt.compare_rows(rows)["results"][0]
        self.assertEqual(out["id"], "5")
        self.assertEqual(out["median"], 30)
        self.assertNotIn("5", out["peer_ids"])
        self.assertEqual(out["multiple"], 1000 / 30)

    def test_compare_rejects_incompatible_formats_windows_definitions(self):
        rows = [self.row(i) for i in range(6)]
        rows += [self.row("short", format="short"), self.row("window", window="first_24_hours"),
                 self.row("definition", metric_definition="another"), self.row("source", traffic_source="paid")]
        out = next(r for r in yt.compare_rows(rows)["results"] if r["id"] == "0")
        self.assertEqual(out["peer_count"], 5)

    def test_compare_lifetime_age_and_duration_filters(self):
        rows = [self.row(i, window="lifetime_snapshot", age_days=10) for i in range(6)]
        rows += [self.row("old", window="lifetime_snapshot", age_days=1000),
                 self.row("length", window="lifetime_snapshot", age_days=10, duration_seconds=5000)]
        out = next(r for r in yt.compare_rows(rows)["results"] if r["id"] == "0")
        self.assertEqual(out["peer_count"], 5)

    def test_compare_zero_median_and_sparse_data(self):
        rows = [self.row(i, 0) for i in range(6)]
        out = yt.compare_rows(rows)["results"][0]
        self.assertEqual(out["status"], "zero_peer_median")
        self.assertIsNone(out["multiple"])
        self.assertEqual(yt.compare_rows(rows[:3])["results"][0]["status"], "insufficient_comparable_data")

    def test_compare_bad_values_or_missing_metadata_fail(self):
        for rows in [[self.row(1), self.row(1)], [self.row(1, None)], [self.row(1, source="")],
                     [self.row(1, window="lifetime_snapshot")], [self.row(1, float("inf"))]]:
            with self.assertRaises(yt.InputError):
                yt.compare_rows(rows)

    def test_unicode_text_not_english_scored(self):
        self.assertEqual(yt.tokens("मेरी किताब"), ["मेरी", "किताब"])
        out = yt.package_check("मेरी किताब", "नया तरीका", "hi")
        self.assertEqual(out["errors"], [])
        self.assertNotIn("score", out)

    def test_titles_dont_need_numbers(self):
        out = yt.package_check("Why small rooms feel cluttered", "ONE CHANGE")
        self.assertEqual(out["errors"], [])
        self.assertEqual(out["review_notes"], [])

    def test_hook_timing_uses_rate_bounds(self):
        out = yt.hook_check("one two three four five six", wpm_low=120, wpm_high=180)
        self.assertEqual(out["spoken_seconds_estimate"], [2, 3])
        with self.assertRaises(yt.InputError):
            yt.hook_check("hello", wpm_low=180, wpm_high=120)

    def test_funnel_correct_scope_math(self):
        out = yt.funnel(10000, 500, 90000)
        self.assertEqual((out["ctr_pct"], out["average_seconds_for_impression_views"], out["watch_seconds_per_impression"]), (5, 180, 9))

    def test_funnel_zeros_invalid_counts(self):
        self.assertIsNone(yt.funnel(0, 0, 0)["ctr_pct"])
        for args in [(100, 101, 100), (100, 1.5, 10), (100, 0, 1), (float("nan"), 0, 0)]:
            with self.assertRaises(yt.InputError):
                yt.funnel(*args)

    def test_cli_errors_are_nonzero(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(yt.main(["package", "--title", "x" * 101]), 2)
            self.assertEqual(yt.main(["edit", str(self.root / "missing.srt"), "--duration", "60"]), 2)

    def test_cli_all_subcommands(self):
        transcript = self.file("s.json", '[{"start":0,"end":2,"text":"Hello there everyone"}]')
        curve = self.file("r.csv", "x,y\n0,100\n30,70\n60,50\n")
        chapters = self.file("c.json", json.dumps([dict(start=x, title="Section") for x in [0, 10, 20]]))
        peers = self.file("p.json", json.dumps([self.row(i) for i in range(6)]))
        cases = [["package", "--title", "Helpful tutorial"], ["hook", "--hook", "Here is the result"],
                 ["edit", transcript, "--duration", "10"],
                 ["retention", curve, "--duration", "60", "--x-col", "x", "--y-col", "y", "--x-unit", "seconds", "--y-unit", "percent"],
                 ["chapters", chapters, "--duration", "30"], ["compare", peers],
                 ["funnel", "--impressions", "10", "--views-from-impressions", "1", "--watch-seconds-from-impressions", "20"]]
        for args in cases:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(yt.main(args), 0)
            self.assertIsInstance(json.loads(out.getvalue()), dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
