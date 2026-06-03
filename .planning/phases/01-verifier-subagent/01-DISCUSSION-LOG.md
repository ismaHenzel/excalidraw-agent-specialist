# Phase 1: Verifier Subagent - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-20
**Phase:** 1-Verifier Subagent
**Areas discussed:** Report transport & parsing, Structural check scope, Visual review strategy, Suggested-fix specificity, Verifier tool set & inputs, Fixture strategy

**Mode note:** User requested non-interactive resolution ("just create the necessary markdowns of the discuss phase, implementing everything that roadmap phase 1 describes"). All four originally-presented gray areas, plus two additional ones surfaced during analysis (verifier tool set & fixture strategy), were resolved by Claude using PROJECT.md key decisions and codebase conventions as the binding constraints. The user did not select individual options; selections recorded below reflect Claude's discretion within the user's mandate.

---

## Report Transport & Parsing

| Option | Description | Selected |
|--------|-------------|----------|
| Assistant-message fenced JSON block only | Verifier returns the report inline in its last message; main agent string-parses ```json ... ``` blocks | |
| Sibling `<basename>.verifier-report.json` file only | Verifier writes a sibling JSON file; main agent reads the file | |
| Both (file is canonical; message is human-debugging) | Verifier writes the sibling file AND echoes the same JSON object in a fenced block | ✓ |

**Selection rationale:** LOOP-03 in PROJECT.md ("verifier report sits as a sibling of the `.excalidraw` file and is overwritten each iteration") makes the sibling file mandatory. The in-message echo is added as a redundancy for human debugging at no extra cost. Phase 2's auto-fix loop will read the sibling file (deterministic) rather than parsing the LLM message (string-handling risk).

**Notes:** Schema fixed as `{ passed, checked_at, source, png, issues[] }`. Every issue object must carry the five keys `check, element_id, severity, detail, suggested_fix` (this is a hard schema, not a suggestion). `passed` is true iff every issue is `severity: "warning"` or there are no issues.

---

## Structural Check Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Only the 4 in PROJECT.md (arrow anchor, text-fit, image path, raw emoji) | Minimum viable; defer style checks to Phase 3 | |
| 4 in PROJECT.md + the Architect's Precision style checks as `warning` severity | Add cheap-to-implement checks for `roughness: 0`, `fontFamily: 3`, arrow elbow conventions, but they only warn (don't fail) | ✓ |
| Maximal: every rule in `excalidraw_specialist.md` enforced | Including color palette, brand stroke colors, container nesting depth, etc. | |

**Selection rationale:** The 4 in PROJECT.md are mandatory and produce `error`. The style checks (`roughness`, `fontFamily`, arrow elbow shape) are cheap and produce `warning` — they're flagged but don't block delivery. The maximal option imposes too much rigidity for a pre-render check (color/brand decisions vary legitimately by request); those judgments stay with the main specialist's generation rules.

**Notes:** The verifier explicitly does NOT duplicate the rules of the existing `scripts/excalidraw_validator.py` (label-on-shape, metadata, contrast warnings). The two checkers are complementary: validator runs pre-render, verifier runs post-render with PNG awareness.

---

## Visual Review Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Per-diagram judgment only | Verifier reads PNG and judges absolute correctness; no comparison to canonical examples | ✓ |
| Compare with matching `examples/*.png` | Verifier identifies which example PNG matches the request and side-by-side compares | |
| Configurable — caller can opt in to comparison | Default per-diagram; comparison-mode added when caller passes a reference PNG path | |

**Selection rationale:** PROJECT.md explicitly excludes "Pixel-diff visual regression against `examples/*.png`" and explicitly notes that "examples remain visual ground truth for the *generator*, not a test oracle for the verifier." Per-diagram judgment is the documented intent. Adding configurable comparison is feature creep beyond the phase scope.

**Notes:** Visual checks emit five `check` values: `text_overflow_visual`, `arrow_disconnected_visual`, `icon_blank`, `missing_glyph_box`, `layout_collision`. All produce `severity: "error"`. Visual `suggested_fix` strings reference JSON element ids, never pixel coordinates in the PNG.

---

## Suggested-Fix Specificity

| Option | Description | Selected |
|--------|-------------|----------|
| Free-text imperative | "Increase rectangle width to ≥260." String-level fix hints. | ✓ |
| Structured patch hint | `{ patch_type: "resize", element_id: "...", new_width: 260 }` — verifier emits JSON ops the main agent applies mechanically | |
| Both — free-text for humans, structured for the loop | Free-text in `detail` + structured `patch` field in each issue | |

**Selection rationale:** Phase 2's auto-fix consumer is the main specialist (an LLM), which can interpret free-text fix hints reliably. Structured patch hints would impose verifier-side complexity (computing exact widths, choosing patch types) without buying determinism gains. If Phase 3 surfaces brittleness, the patch field can be added later without breaking the schema (additive change).

**Notes:** All fixes start with an imperative verb and name an `element_id`. Multi-element fixes name additional ids inline in the text.

---

## Verifier Tool Set & Inputs

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal: `Read` only | Pure-Read subagent; structural checks done in-prompt | |
| Standard: `Read, Glob, Grep, Bash, Write` | Read for PNG/JSON; Glob for icons; Bash to invoke a Python helper; Write for report sibling | ✓ |
| Full: include MCP tools | `Read, Glob, Grep, Bash, Write, mcp__excalidraw__*` for canvas-level inspection | |

**Selection rationale:** Pure-Read can't reliably compute the text-overflow metric or write the report file. MCP tools add nothing for verification (they're authoring tools). The standard set is the minimum for the documented behavior.

**Notes:** Spawn-prompt contract is fixed: caller passes a single absolute path to the `.excalidraw` file. The verifier infers the PNG path; it errors immediately if the PNG is missing (no fallback to "try to render it myself"). This forces Phase 2's orchestrator to render before invoking the verifier, which matches LOOP-01's always-render mandate.

---

## Fixture Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Hand-craft ad-hoc fixtures at test time | Generate fixtures on demand; don't commit them | |
| Reuse `examples/*.excalidraw` if any exist | Use the canonical examples as the test corpus | |
| Commit three small fixtures under `fixtures/verifier/` | One per defect class; each with a sibling `expected-report.json` | ✓ |

**Selection rationale:** `examples/` currently contains only PNGs (no `.excalidraw` source files), so option 2 is moot. Ad-hoc fixtures make the Phase 1 success criteria un-rerunnable. Committed fixtures with `expected-report.json` siblings make success criteria testable as a `diff` operation — a clean acceptance gate.

**Notes:** Three fixture directories: `good/`, `raw-emoji/`, `text-overflow/`. Each contains a `.excalidraw`, a pre-rendered `.png`, and an `expected-report.json`. The success-criteria test ignores the `checked_at` timestamp when comparing.

---

## Claude's Discretion

Areas where Claude's judgment was used inside the user's mandate ("implement everything that roadmap phase 1 describes"):

- **Severity vocabulary** — two-tier `error` / `warning`; no `info` tier for v1.
- **Visual-check prompt wording** inside the subagent body — must produce the documented schema; otherwise prompt engineering is at Claude's discretion.
- **Structural-check helper location** — kept as `scripts/verifier_structural.py` (separate file), invoked via Bash. Cleaner separation; allows host-side unit testing.
- **Internal-error reporting policy** — verifier always produces a report, even on internal failure (a `verifier_internal_error` issue). Documented in Deferred Ideas as Phase 3 polish if needed.
- **Monospace advance ratio constant** — `0.6 × fontSize`; documented in code with empirical derivation comment.

## Deferred Ideas

- **Pixel-diff visual regression vs `examples/*.png`** — explicitly out of scope per PROJECT.md.
- **Configurable severity thresholds** — caller-driven warning→error promotion; not needed for v1.
- **A `verifier_self_test.sh` runner** — manual test recipe acceptable for Phase 1 if the planner does not author this script.
- **Multi-page / multi-frame `.excalidraw` files** — no examples exist; out of scope.
- **`verifier_internal_error` graceful report** — Phase 3 (E2E) will reveal whether this is needed.
