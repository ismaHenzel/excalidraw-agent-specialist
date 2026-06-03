# Plan 01-03 — Summary

**Status:** Tasks 1, 2, 3 complete. Task 4 (manual end-to-end checkpoint) deferred — requires spawning the `excalidraw_verifier` subagent on each fixture inside an interactive Claude Code session.

## Files Created (10 of 10)

| Path | Status |
|------|--------|
| `fixtures/verifier/good/good.excalidraw` | ✓ passes validator + helper returns `[]` |
| `fixtures/verifier/good/expected-report.json` | ✓ `passed: true`, `issues: []` |
| `fixtures/verifier/good/good.png` | ✓ 18 KB, valid PNG, clean render |
| `fixtures/verifier/raw-emoji/raw-emoji.excalidraw` | ✓ helper emits 1 `raw_emoji_in_text` error |
| `fixtures/verifier/raw-emoji/expected-report.json` | ✓ `passed: false`, byte-matches helper output |
| `fixtures/verifier/raw-emoji/raw-emoji.png` | ✓ 11 KB, valid PNG — emoji rendered via fallback font (so visual `missing_glyph_box` will NOT fire; structural check still flags) |
| `fixtures/verifier/text-overflow/text-overflow.excalidraw` | ✓ helper emits 1 `text_overflow_static` error |
| `fixtures/verifier/text-overflow/expected-report.json` | ✓ `passed: false`, byte-matches helper output |
| `fixtures/verifier/text-overflow/text-overflow.png` | ✓ 17 KB, valid PNG — "Databricks Wo" visibly cut off at rectangle's right edge; visual `text_overflow_visual` will fire |
| `scripts/verifier_self_test.sh` | ✓ executable, passes 3/3 |

## Expected-Report Issue Composition

| Fixture        | passed | issue checks emitted |
|----------------|--------|----------------------|
| good           | true   | (none) |
| raw-emoji      | false  | `raw_emoji_in_text` (1) |
| text-overflow  | false  | `text_overflow_static` (1) |

## Self-Test Runner Results

- `bash scripts/verifier_self_test.sh` → `Summary: 3 pass / 0 fail`, exit `0`.
- `bash scripts/verifier_self_test.sh good` → `PASS: good`, exit `0`.
- `bash scripts/verifier_self_test.sh bogus` → `Usage:` to stderr, exit `1`.

## Deferred — Task 4: Manual end-to-end checkpoint

Requires an interactive Claude Code session: spawn the `excalidraw_verifier` subagent on each absolute fixture path and confirm
- The subagent writes `<basename>.verifier-report.json` next to each fixture.
- The final assistant message ends with a fenced ```json block (no trailing prose).
- The structural issues (after `jq 'del(.checked_at,.source,.png)'` normalization) match the committed `expected-report.json`.
- For `good`: `passed: true`.
- For `raw-emoji`: ≥1 issue with `check == "raw_emoji_in_text"`. NOTE: the raw-emoji PNG renders the emoji via a fallback color-emoji font in headless Chromium, so `missing_glyph_box` will likely NOT fire on this image — the structural check carries the load here.
- For `text-overflow`: ≥1 issue with `check == "text_overflow_static"` and (very likely) ≥1 visual issue with `check == "text_overflow_visual"` — the rendered PNG visibly cuts the label off at the rectangle's right edge.

## Deviations

- The text-overflow fixture was authored using the resolution documented in the plan's "PRACTICAL DESIGN" section: the text element carries a stored `width: 100, height: 20` that fits inside the 180×80 rectangle, while the helper's estimated width (26 chars × 0.6 × 20 = 312 px) overflows. This makes the containing-shape lookup succeed AND the overflow check fire, as planned. Confirmed visually — the rendered PNG shows "Databricks Wo" with the rest cut off.
- The renderer prints CORS-failure noise about `unpkg.com/@excalidraw/excalidraw@undefined/.../Cascadia.woff2` during each render. Render still succeeds and produces a valid PNG (~18 KB / ~11 KB / ~17 KB). This is a pre-existing fragility (CONCERNS.md #2 — CDN coupling) and unrelated to Phase 01 — flagging for awareness only.
- The static validator emits a low-contrast `strokeColor` warning on each fixture (text strokes use `#1e40af` / `#047857`, not pure black). Validator still exits `0` — only warnings, not errors — so this does not block.
