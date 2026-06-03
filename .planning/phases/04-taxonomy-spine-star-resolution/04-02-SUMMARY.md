---
phase: 04-taxonomy-spine-star-resolution
plan: 02
subsystem: diagram-type-kb
tags: [kb, notation, arrowhead, compartmented-box, conventions]
requires:
  - "diagram-types/ KB layer (from plan 04-01)"
provides:
  - "Committed arrowhead-workaround notation conventions (DTKB-04)"
  - "Reusable compartmented-box construction recipe (INT-02)"
affects:
  - "All later relationship/compartmented diagram types (UML class, ER, sequence, use-case, star/snowflake/data-vault)"
tech-stack:
  added: []
  patterns:
    - "Embed-verbatim convention table to prevent per-type drift"
    - "Single grouped compartmented-box construction reused across formal-notation types"
key-files:
  created:
    - .claude/agents/excalidraw/diagram-types/notation-conventions.md
    - .claude/agents/excalidraw/diagram-types/compartmented-box.md
  modified: []
decisions:
  - "Crow's-foot 'many': committed to TEXTUAL multiplicity labels (0..*/1..*) as the single house default; grouped 3-line glyph explicitly NOT used"
  - "Actor: committed to LABELLED BOX as the single house default; stick-figure NOT used"
  - "Generalization: committed to FILLED triangle (Excalidraw lacks a hollow head)"
  - "Multi-line single text blocks are a BINDING prohibition for compartments"
metrics:
  duration: ~10m
  completed: 2026-06-03
---

# Phase 4 Plan 02: Notation Conventions & Compartmented-Box Construction Summary

Locked the two reusable conventions that every later relationship/compartmented diagram
type depends on: the arrowhead-workaround notation encodings (DTKB-04) and the single
reusable compartmented-box construction (INT-02), each committing to exactly one
convention per otherwise-ambiguous notation.

## What Was Built

### Task 1 — notation-conventions.md (DTKB-04)
- States the legal arrowhead set verbatim (`arrow | bar | dot | triangle | null`) and
  warns that any other token renders SILENTLY as a plain line (Pitfall 1).
- Provides a committed notation → legal-encoding table with one binding convention each:
  association (arrow, solid), dependency/return (arrow, dashed), generalization (FILLED
  triangle), realization (triangle, dashed), aggregation (white ~14px diamond) /
  composition (solid ~14px diamond), ER one (bar), ER zero/optional (dot or small ellipse),
  ER many (committed to TEXTUAL multiplicity `0..*`/`1..*` — glyph NOT used), actor
  (committed to LABELLED BOX — stick-figure NOT used), general multiplicity (textual).
- Defers exact glyph pixel geometry to Phase 7; instructs later type files to embed the
  table verbatim to prevent drift.
- 48 non-blank lines; no full element JSON blocks.

### Task 2 — compartmented-box.md (INT-02)
- Documents the four-element construction (one sharp rectangle `roundness: null` +
  full-width horizontal line dividers + one bound/centered title text + N separate
  left-aligned monospace `fontFamily: 3` row texts), ALL in a single `groupIds` group.
- States the HARD binding prohibition against multi-line single `text` blocks for
  compartments (defeats dividers + breaks the verifier's per-element width-fit check,
  Pitfall 2).
- States the alignment rules (Pitfall 3): rows share a common left x; divider x-range
  equals box x-range; 20-grid coordinates; row pitch a multiple of 20.
- Notes the legacy `star_schema.excalidraw` (0 groupIds, soft roundness) is NOT a safe
  template, and that parametric offsets are finalized in Phase 6.
- 48 non-blank lines; no full element JSON blocks.

## Verification

Both automated verify commands from the plan passed:
- Task 1: file exists, >=25 non-blank lines (48), all five arrowhead tokens present,
  "filled" + "crow" + "actor" present, no `"type": "arrow"` JSON block. PASS.
- Task 2: file exists, >=25 non-blank lines (48), `groupIds` + `divider` +
  `monospace`/`fontFamily` + `multi-line` + a prohibition word present, no
  `"type": "rectangle"` JSON block. PASS.

## Deviations from Plan

None — plan executed exactly as written.

## Threat Mitigations Applied

- **T-04-04 (Tampering, arrowhead table):** Committed table lists only legal tokens and
  warns illegal tokens render silently; designed for verbatim embedding so no per-type
  re-derivation can drift.
- **T-04-05 (Tampering, multi-line prohibition):** Binding rule against multi-line
  compartment text keeps the verifier's width-fit check valid; the `groupIds` rule keeps
  box units translatable without divider desync.

## Out of Scope (untouched, as instructed)

No changes to `scripts/`, the validator, the verifier, the render pipeline, or any file
outside the plan's `files_modified` list. The pre-existing `diagram-types/README.md` and
`diagram-types/tech-architecture.md` were not modified.

## Self-Check: PASSED
- FOUND: .claude/agents/excalidraw/diagram-types/notation-conventions.md
- FOUND: .claude/agents/excalidraw/diagram-types/compartmented-box.md
- Both automated verify commands returned PASS.
- No git operations performed (project is not a git repository, per instructions).
