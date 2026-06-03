# Plan 02-01 — Summary

**Status:** Complete.

## File Modified

- `.claude/agents/excalidraw/excalidraw_specialist.md` — 151 lines → 291 lines (+140).

## Section Ordering After Edit

`<role>` — `<capabilities>` — `<asset_paths>` — `<visual_standards>` — `<drawing_methodology>` — `<style_principles>` — **`<content_policy>` (NEW)** — **`<verification_loop>` (NEW)** — `<operational_mandates>`

## ROADMAP §Phase 2 Success-Criteria Trace

| # | Success criterion | Where enforced in the prompt |
|---|-------------------|------------------------------|
| 1 | Sibling `.png` exists before completion claim | `<verification_loop>` block A (always-render) + Mandate #5 (no JSON-only path); honest-failure block G blocks the "done" claim on the alternate branch |
| 2 | Re-fix + re-verify up to 3 iterations | `<verification_loop>` block D (3-attempt cap with the explicit flow diagram) + block E (fix mechanics) |
| 3 | 3rd-attempt failure surfaces failed PNG path + structured issues + source path; no "done" | `<verification_loop>` block G (verbatim template with `Failed PNG:`, `Source:`, `Report:`, `Outstanding issues:` labels and the explicit ban on success tokens) |
| 4 | Emoji request → `image` element pointing at `icons/*.png`, not raw text codepoint | `<content_policy>` (raw-emoji ban + 3-row mapping table + `Glob`-and-ask fallback for unmapped emojis) |
| 5 | Only 1 PNG + ≤1 verifier-report sibling per iteration | `<verification_loop>` block F (sibling-only artefact discipline; explicit ban on `.v1`, `_iter`, `.bak`, suffixed siblings) |

## Operational-Mandate Revisions

| # | Before | After |
|---|--------|-------|
| 5 | `Local Creation: Default to writing the .excalidraw file in the current working directory unless a specific path is requested.` | `Local Creation + Mandatory Verification: Write the .excalidraw in the current working directory by default. EVERY delivery turn MUST end by running scripts/validate_and_render.sh and entering the <verification_loop> — there is no JSON-only path. Never claim a diagram is delivered without a verifier-approved sibling PNG (or, on the 3-attempt cap, an honest-failure message per <verification_loop> block G).` |
| 7 | `Iterative Quality: Use mcp__excalidraw__create_view to verify the visual result and fix overlaps or layout issues before finalizing.` | `Verifier is Authority: The excalidraw_verifier subagent (NOT mcp__excalidraw__create_view) is the verification step. Per <verification_loop>, delegate to it after every render and act on the structured <basename>.verifier-report.json. mcp__excalidraw__create_view remains available as an OPTIONAL drafting aid for previewing geometry before the render — it is no longer the verification gate.` |

Mandates #1, #2, #3, #4, #6, #8 are byte-for-byte preserved.

## Grep Witnesses (proof literals landed)

| Literal                  | Occurrences | Section |
|--------------------------|-------------|---------|
| `success_icon.png`       | 1           | `<content_policy>` |
| `failure_icon.png`       | 3           | `<content_policy>` (2 table rows + 1 prose) |
| `validate_and_render.sh` | 2           | `<verification_loop>` block A + mandate #5 |
| `excalidraw_verifier`    | 3           | `<verification_loop>` block B + mandate #7 + prose |
| `.verifier-report.json`  | 5           | `<verification_loop>` blocks B/C/F/G + mandate #7 |
| `Failed PNG:`            | 1           | `<verification_loop>` block G template |
| `Outstanding issues:`    | 1           | `<verification_loop>` block G template |
| `3 attempts`             | 4           | `<verification_loop>` blocks A/C/D/G |

YAML frontmatter byte-for-byte preserved (verified: `head -5 excalidraw_specialist.md` matches pre-edit).

## Deviations

- None from the plan. The prompt content matches the D2-01..D2-16 invariants in `02-CONTEXT.md` and the `<interfaces>` block in `02-01-PLAN.md`. The verification command from `<verify>` passed (`OK\nlines: 291\nmandate_count: 9`).
- The plan estimated ~60-120 added lines; actual additions came to ~140 because the two new sections include the full ASCII flow diagram (block D) and the verbatim honest-failure template (block G) — both are required for the grep-witnesses test, so the over-shoot is intentional.

## Deferred to Phase 3

End-to-end validation that the closed loop actually self-heals representative defect cases (text-overflow request → fixed diagram within 3 attempts; under-specified request → honest-failure delivery; clean artefact directory after any run). Phase 3 is the acceptance gate that exercises this Phase 2 prompt against the Phase 1 verifier + fixtures.
