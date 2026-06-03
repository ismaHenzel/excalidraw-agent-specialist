# Plan 01-01 — Summary

**Status:** Complete.

## File Created

- `.claude/agents/excalidraw/scripts/verifier_structural.py` (479 lines)

## Check Functions

| Function                              | Severity   | Check name                       |
|---------------------------------------|------------|----------------------------------|
| `check_raw_emoji_in_text`             | error      | `raw_emoji_in_text`              |
| `check_text_overflow_static`          | error      | `text_overflow_static`           |
| `check_arrow_endpoint_unanchored`     | error      | `arrow_endpoint_unanchored`      |
| `check_image_path_unresolvable`       | error      | `image_path_unresolvable`        |
| `check_roughness_nonzero`             | warning    | `roughness_nonzero`              |
| `check_fontfamily_nonmonospace`       | warning    | `fontfamily_nonmonospace`        |
| `check_arrow_points_too_few`          | warning    | `arrow_points_too_few`           |
| `check_arrow_missing_elbow_roundness` | warning    | `arrow_missing_elbow_roundness`  |
| (fallback in `main`)                  | error      | `verifier_internal_error`        |

## EMOJI_TO_ICON Mapping

Only emojis with verified PNGs in `.claude/agents/excalidraw/icons/`:

| Emoji | Codepoint | Icon file |
|-------|-----------|-----------|
| ✅    | U+2705    | `success_icon.png` |
| ❌    | U+274C    | `failure_icon.png` |
| ⚠     | U+26A0    | `failure_icon.png` (no dedicated warning icon exists; closest available) |

For any other emoji, the `suggested_fix` falls back to the generic "Replace with an image element pointing to a matching PNG in .claude/agents/excalidraw/icons/."

## Tuning Constants

- `MONOSPACE_ADVANCE_RATIO = 0.6` — Cascadia/Fira Code average advance width per em at `fontFamily: 3`.
- `ENDPOINT_TOLERANCE_PX = 8` — arrow endpoint within 8 px of shape border counts as anchored.

## Contract

- Invocation: `python3 scripts/verifier_structural.py <absolute-path-to-excalidraw>`
- Exit code: **0 always** (even on missing arg, missing file, invalid JSON, uncaught exception).
- Stdout: single line of JSON — a JSON array (possibly empty) of issue objects with the 5 mandatory keys (`check`, `element_id`, `severity`, `detail`, `suggested_fix`).
- Stderr: empty.

## Image-Path Resolution

Verbatim mirror of `scripts/render_excalidraw.py` lines 69-94: absolute → `excalidraw_parent_dir` → `$EXCALIDRAW_ASSETS_DIR`. Implemented in `_resolve_image_path`.

## Deviations

- The plan's two-task split (skeleton → checks) was executed as a single Write because the file is small enough to validate end-to-end in one shot. All Plan-01 acceptance criteria still pass (verified inline with the planned test cases).
- `check_roughness_nonzero` and `check_fontfamily_nonmonospace` only fire when the field is **present** and non-conforming. Elements with the field absent are not flagged. This is a defensive interpretation of the spec's "for each element with X != Y" wording — fixtures explicitly set `roughness: 0` / `fontFamily: 3` to keep the contract clear.
