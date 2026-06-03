# Phase 1: Verifier Subagent - Context

**Gathered:** 2026-05-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver a **standalone, exercisable `excalidraw_verifier` subagent** that:

1. Accepts a single input: an absolute path to a `.excalidraw` file. It infers the sibling rendered PNG path by replacing the `.excalidraw` extension with `.png`.
2. Runs a **structural pre-check** of the JSON (cheap, no vision tokens) covering: arrow endpoint anchoring, text-width fits container width given monospace metrics, image `file_path` resolves, no raw emoji codepoints in `text` elements that use `fontFamily: 3`, plus a small set of Architect's Precision style checks (`roughness: 0`, `fontFamily: 3`, arrow `points` length ≥ 3, arrow `roundness: { type: 2 }`).
3. Runs a **multimodal visual review** of the rendered PNG covering: text overflow at render time, arrows visibly connecting their anchors, icons present and non-blank, no missing-glyph boxes, overall layout coherence.
4. Emits a **structured pass/fail report** as a sibling JSON file (`<basename>.verifier-report.json`) AND a fenced ```json block in its final assistant message. The sibling file is the canonical machine-readable artefact; the in-message block is a redundancy for in-context inspection.
5. Is exercisable in isolation against three committed fixtures (good, raw-emoji, text-overflow) under `.claude/agents/excalidraw/fixtures/verifier/`.

Out of this phase: the auto-fix loop (Phase 2), the main specialist's always-render mandate (Phase 2), iteration artefact discipline at the specialist level (Phase 2). This phase ONLY ships the verifier — nothing wires it into the main specialist yet.

</domain>

<decisions>
## Implementation Decisions

### Report Transport & Parsing
- **D-01:** The verifier writes the canonical report to `<basename>.verifier-report.json` as a sibling of the `.excalidraw` file. Phase 2's auto-fix loop reads this file rather than parsing the LLM's message. The file is overwritten on every verifier run (no version suffix) — consistent with LOOP-03's "no versioned history clutter" rule.
- **D-02:** The verifier ALSO echoes the same JSON object inside a ```json ... ``` fenced block as the last segment of its assistant message. This is the human-debugging path; the file is the machine-parsing path. Both must be byte-identical (same `json.dumps` invocation feeds both).
- **D-03:** Schema:
  ```json
  {
    "passed": false,
    "checked_at": "2026-05-20T22:38:00Z",
    "source": ".../diagram.excalidraw",
    "png": ".../diagram.png",
    "issues": [
      {
        "check": "text_overflow",
        "element_id": "label_3",
        "severity": "error",
        "detail": "Text 'Databricks Workspace' (236px @ fontSize 20) exceeds rectangle width (180px).",
        "suggested_fix": "Increase rectangle width to ≥260, or shorten label."
      }
    ]
  }
  ```
  `passed` is `true` iff `issues` is empty OR every issue has `severity: "warning"` (warnings do not fail). All five issue keys are mandatory.

### Structural Check Scope
- **D-04:** Required structural checks (must produce `severity: "error"` when violated):
  - `arrow_endpoint_unanchored` — arrow `points` end coordinate does not land on the border of any rectangle/ellipse/diamond within a small tolerance (8 px).
  - `text_overflow_static` — text element estimated rendered width (using monospace metric `0.6 × fontSize` per character at `fontFamily: 3`) exceeds the width of the containing shape, where "containing" means the smallest rectangle/ellipse/diamond whose bounding box encloses the text element's bounding box.
  - `image_path_unresolvable` — image element's `file_path` (or implicit path) does not resolve to a file under `.claude/agents/excalidraw/icons/` or to an absolute path that exists.
  - `raw_emoji_in_text` — text element contains a Unicode codepoint in the emoji ranges (`U+1F300`–`U+1FAFF`, `U+2600`–`U+27BF`, plus regional indicators) and `fontFamily == 3`.
- **D-05:** Required style checks (must produce `severity: "warning"` when violated — flagged but do not fail the diagram):
  - `roughness_nonzero` — any element with `roughness != 0`.
  - `fontfamily_nonmonospace` — any text element with `fontFamily != 3`.
  - `arrow_points_too_few` — arrow with fewer than 3 entries in `points` (violates elbow rule).
  - `arrow_missing_elbow_roundness` — arrow without `roundness: { type: 2 }`.
- **D-06:** The verifier MUST NOT duplicate the rules of the existing static `scripts/excalidraw_validator.py` (label-on-shape, metadata, color contrast). The pre-render `validate_and_render.sh` pipeline already runs that validator. The verifier extends it with structural defects that the static validator never knew about.

### Visual Review Strategy
- **D-07:** **Per-diagram judgment, not example-comparison.** PROJECT.md explicitly excludes pixel-diff regression against `examples/*.png`. The verifier reads the PNG and judges absolute correctness: does this image, on its own, contain text overflowing a box; arrows that visibly miss their anchor; icons that rendered blank; or boxes/squares where glyphs should be? It does NOT cross-reference any canonical example.
- **D-08:** Visual checks produce these `check` values:
  - `text_overflow_visual` — text visibly extends beyond its container in the rendered image (catches cases the static metric missed, e.g., word-wrap or non-monospace fallback).
  - `arrow_disconnected_visual` — arrow head/tail visibly does not touch its claimed anchor element.
  - `icon_blank` — image element rendered as a blank/transparent rectangle.
  - `missing_glyph_box` — text element renders as one or more tofu boxes (□) instead of real glyphs.
  - `layout_collision` — two elements visibly overlap when they should not (text on text, box on box).
- **D-09:** Severity for visual checks is `error` (visual defects are render-time failures). Visual `suggested_fix` strings reference the JSON, not the PNG (e.g., "Replace text element `id: label_3` with an `image` element pointing to `.claude/agents/excalidraw/icons/checkmark.png`").

### Suggested-Fix Specificity
- **D-10:** `suggested_fix` is **free-text guidance** starting with an imperative verb. Examples:
  - "Increase rectangle `id: db_block` width from 180 to ≥260 to fit the 236-px text."
  - "Replace text element `id: label_3` (raw emoji 'U+2705') with an image element pointing to `.claude/agents/excalidraw/icons/check.png`."
  - "Adjust arrow `id: arrow_4` last point from `[412, 100]` to `[420, 80]` to land on the border of `id: api_block`."
  - Free-text is sufficient because Phase 2's consumer is also an LLM (the main specialist), which can interpret natural-language fix hints reliably. Structured patch hints would impose verifier-side complexity (computing exact offsets, choosing patch types) without buying reliability gains.
- **D-11:** Every fix must reference an `element_id` (already in the issue object's `element_id` field). When a fix touches multiple elements, the additional ids appear inline in the `suggested_fix` text. The single `element_id` field always identifies the primary subject.

### Verifier Tool Set & Inputs
- **D-12:** YAML frontmatter `tools:` list = `Read, Glob, Grep, Bash, Write`.
  - `Read` — open the PNG (multimodal) and the JSON.
  - `Glob` — list `.claude/agents/excalidraw/icons/` to verify icon-path resolution and to suggest emoji-to-icon mappings.
  - `Grep` — search text content for emoji codepoints and reserved-character ranges.
  - `Bash` — invoke `python3` for the structural pre-check helper (`scripts/verifier_structural.py`, NEW) and for resolving paths.
  - `Write` — emit the sibling `.verifier-report.json`.
- **D-13:** Spawn-prompt contract: caller passes a single absolute path to the `.excalidraw` file. The verifier MUST NOT accept the PNG path as a separate argument — it derives `<basename>.png` and errors immediately if missing. This removes ambiguity and forces the caller to render before verification (matches LOOP-01 always-render).
- **D-14:** Helper script `scripts/verifier_structural.py` (new, part of this phase): pure-JSON checks, exit code 0 always, prints a JSON array of `issue` objects to stdout. The verifier subagent reads stdout and merges with its own visual-check issues into the final report. Keeps structural logic deterministic and testable without spawning the subagent.

### Fixture Strategy
- **D-15:** Commit three fixtures under `.claude/agents/excalidraw/fixtures/verifier/`:
  - `good/good.excalidraw` + `good/good.png` — valid icon-block + elbow-arrow diagram, no violations.
  - `raw-emoji/raw-emoji.excalidraw` + `raw-emoji/raw-emoji.png` — contains a text element with `"text": "✅"` and `fontFamily: 3`. Structural pre-check must flag it; visual check would also see the tofu box.
  - `text-overflow/text-overflow.excalidraw` + `text-overflow/text-overflow.png` — `text` of width ≈ 280 px inside a `rectangle` of width 180 px. Static check flags it via the 0.6×fontSize heuristic; visual check confirms.
- **D-16:** Each fixture directory ships an `expected-report.json` next to it. The success-criteria test is: run the verifier on the fixture, compare the generated `.verifier-report.json` against `expected-report.json` (ignoring `checked_at` timestamp). Match → criterion satisfied.

### Claude's Discretion
- Exact severity ordering (`error` > `warning`; no `info` for v1).
- The visual-check prompt wording inside the verifier subagent body (must produce the documented schema; otherwise prompt engineering choices are Claude's).
- Whether to inline the structural-check Python source in the subagent prompt or keep it in `scripts/verifier_structural.py` (decision: keep separate; subagent invokes it via Bash). Cleaner separation, allows host-side unit testing.
- Whether the verifier ever rejects work without producing a report (decision: never; even on internal error it must write a report with a `verifier_internal_error` issue so the caller is never stuck).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase Scope & Requirements
- `.planning/PROJECT.md` — core value, milestone, key decisions table (8 locked decisions)
- `.planning/REQUIREMENTS.md` §v1 Requirements — VRFY-01, VRFY-02, CONT-01 (structural pre-check half)
- `.planning/ROADMAP.md` §Phase 1 — goal + 5 success criteria

### Architecture & Existing Code
- `.planning/codebase/ARCHITECTURE.md` — render pipeline (validate_and_render.sh → validator → Docker → Chromium → SVG → PNG) and visual standards
- `.planning/codebase/STRUCTURE.md` — file layout (`scripts/`, `icons/`, `kb/`, `examples/`)
- `.planning/codebase/CONVENTIONS.md` — pattern-KB rules, subagent definition conventions
- `.planning/codebase/CONCERNS.md` — known fragility points (CDN coupling, path resolver, etc. — out of scope here)
- `excalidraw_specialist.md` — existing subagent file format / YAML frontmatter conventions to mirror
- `scripts/excalidraw_validator.py` — pre-existing static validator; verifier must NOT duplicate its rules
- `scripts/validate_and_render.sh` — pipeline that produces the PNG the verifier consumes

### Pattern KB (informs visual checks — what "correct" looks like for each pattern)
- `kb/README.md` — pattern catalogue index
- `kb/icon-block.md` — atomic node geometry (180×80 rect + 24×24 icon + label) — referenced by `text_overflow_static` width math
- `kb/group-container.md` — outermost frame conventions (brand icon + title at top-left)
- `kb/feedback-loop.md`, `kb/decision-marker.md` — arrow-routing rules referenced by `arrow_endpoint_unanchored`

### Visual Ground Truth (informs the visual-review prompt — what a "good" diagram looks like, NOT for diff comparison)
- `examples/dlt.png`, `examples/governance.png`, `examples/orchestrator.png`, `examples/refresh_bi.png` — only for the verifier-prompt author to set baseline expectations; the verifier itself does NOT read these at runtime.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/excalidraw_validator.py` — JSON-loading pattern, error/warning print format, exit-code convention. The new `scripts/verifier_structural.py` mirrors its structure but outputs JSON instead of human-readable text.
- `scripts/render_excalidraw.py:118` — already validates image-element `file_path` resolution (warns but continues). The new structural check elevates this to `error` severity and reports per-element.
- `excalidraw_specialist.md` frontmatter — exact YAML format for `name`/`description`/`tools` keys. The new `excalidraw_verifier.md` uses the same convention.
- `scripts/validate_and_render.sh` — already runs the static validator then renders. Phase 2 will extend it to spawn the verifier; this phase does NOT touch it.

### Established Patterns
- **Self-contained subagent files.** Both subagents (`excalidraw_specialist.md`, new `excalidraw_verifier.md`) live in the agent's plugin directory and are discovered by Claude Code via YAML `name:` field — no central registry.
- **Relative paths.** All asset paths assume the project's working directory contains `.claude/agents/excalidraw/`. The verifier follows the same convention; the structural Python helper resolves icon paths relative to its own location.
- **Helper scripts in `scripts/`.** Existing convention: Python helpers (`render_excalidraw.py`, `excalidraw_validator.py`) live in `scripts/` and are invoked via `bash` wrappers when orchestration is needed. New `verifier_structural.py` follows this; no bash wrapper needed because the subagent invokes it directly via the Bash tool.
- **Severity vocabulary.** The static validator uses `[X]` errors / `[!]` warnings. The verifier report uses `error` / `warning` strings — same two-tier hierarchy, machine-parseable encoding.

### Integration Points
- **Phase 2 will read the verifier's sibling `.verifier-report.json`.** This phase's report path / schema choices are the contract.
- **The render pipeline produces the PNG.** The verifier assumes `<basename>.png` exists as a sibling of `<basename>.excalidraw`. The orchestrator (Phase 2) guarantees this precondition; this phase only documents the expectation.
- **The icons directory remains the authoritative emoji-replacement source.** The structural emoji check consults `Glob('.claude/agents/excalidraw/icons/*.png')` to suggest a replacement icon when it flags a raw emoji.

</code_context>

<specifics>
## Specific Ideas

- **Emoji-to-icon suggestion table** in the structural check: a small static dict mapping the most common emojis (✅ → check, ❌ → x, ⚠️ → warning, 🔧 → tool, 🚀 → rocket) to the closest filename in `icons/`. When a raw emoji is found, the `suggested_fix` field names the recommended icon path. If no mapping exists, the fix just says "Replace with an `image` element pointing to a matching PNG in `.claude/agents/excalidraw/icons/`."
- **Text-width heuristic constant.** Use `0.6 × fontSize` for monospace fonts at `fontFamily: 3` (Cascadia Code / Fira Code average advance width is ~0.58–0.62 em). Document the constant in `verifier_structural.py` as a module-level `MONOSPACE_ADVANCE_RATIO = 0.6` with a comment explaining the empirical derivation.
- **The verifier's "passed" rule:** passed iff every issue has `severity: "warning"`. A diagram with style warnings still ships. A diagram with even one `error` does not.

</specifics>

<deferred>
## Deferred Ideas

- **Pixel-diff visual regression** against `examples/*.png` — explicitly out of scope per PROJECT.md.
- **A `verifier_internal_error` recovery report** — the verifier should always produce a report, even when it crashes internally. Out of scope as a polish concern; for v1, if the subagent crashes, the caller surfaces the crash. Revisit if Phase 3 (E2E validation) shows verifier crashes occur in normal use.
- **Configurable severity thresholds** — letting the caller decide which warnings should be promoted to errors. Out of scope; the two-tier `error`/`warning` split is fine for v1.
- **A `verifier_self_test.sh`** that runs the verifier against all three fixtures and asserts `expected-report.json` match — implementation polish for Phase 1's success criteria; if not built as a script, the plan-phase agent should still author a manual test recipe in PLAN.md.
- **Multi-page or multi-frame `.excalidraw` files** — current `examples/` are single-frame; out of scope.

</deferred>

---

*Phase: 01-Verifier Subagent*
*Context gathered: 2026-05-20*
