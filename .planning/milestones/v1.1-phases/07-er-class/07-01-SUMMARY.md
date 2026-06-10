---
phase: 07-er-class
plan: "01"
subsystem: kb-primitives
tags: [relationship-endpoint, arrowhead-validation, er, class, kb-primitive]
dependency_graph:
  requires:
    - .claude/agents/excalidraw/diagram-types/notation-conventions.md
    - .claude/agents/excalidraw/diagram-types/compartmented-box.md
    - .claude/agents/excalidraw/scripts/render/excalidraw_validator.py
  provides:
    - .claude/agents/excalidraw/kb/relationship-endpoint.md (shared glyph primitive)
    - arrowhead-enum deny-list check in excalidraw_validator.py
  affects:
    - .claude/agents/excalidraw/diagram-types/er.md (Plan 02 — will @-reference this primitive)
    - .claude/agents/excalidraw/diagram-types/class.md (Plan 03 — will @-reference this primitive)
tech_stack:
  added: []
  patterns:
    - "Composed diamond/ellipse glyph overlaid on an anchored connector (Pattern 3)"
    - "kb/ primitive referenced by multiple type files (mirrors tree-hierarchy / snowflake pattern)"
    - "Additive deny-list hardening of frozen Phase-1 validator"
key_files:
  created:
    - .claude/agents/excalidraw/kb/relationship-endpoint.md
  modified:
    - .claude/agents/excalidraw/scripts/render/excalidraw_validator.py
decisions:
  - "Task 1 (add-check): Arrowhead-enum deny-list added to excalidraw_validator.py as permitted additive hardening — rejects any startArrowhead/endArrowhead outside {arrow,bar,dot,triangle,null} with exit code 1"
metrics:
  duration: "~15 minutes"
  completed: "2026-06-07T19:44:34Z"
  tasks_completed: 2
  files_created: 1
  files_modified: 1
requirements: [DM-02, UML-02]
---

# Phase 07 Plan 01: Relationship-Endpoint Primitive + Validator Hardening Summary

Shared endpoint-glyph primitive `kb/relationship-endpoint.md` pins deferred diamond/ellipse/multiplicity geometry once for both ER and UML class types; arrowhead-enum deny-list added to validator converts silent bare-line failures into loud Phase-1 errors.

## Tasks Completed

| Task | Description | Commit | Files |
|------|-------------|--------|-------|
| 1 | Decision: add-check (resolved at checkpoint) | — | — |
| 2 | Arrowhead deny-list check in excalidraw_validator.py | db9486a | excalidraw_validator.py |
| 3 | Author kb/relationship-endpoint.md primitive | 4760645 | kb/relationship-endpoint.md |

## Decisions Made

### Task 1: add-check — Arrowhead-enum deny-list adopted

**Decision:** Add the deny-list check (option `add-check`).

**Rationale:** Neither `excalidraw_validator.py` nor `verifier_structural.py` inspected
arrowhead-token legality before this plan. An illegal token (`crowsfoot`, `diamond`, `hollow`)
renders silently as a plain line in 0.17.3 — no error, no warning. Success Criterion 1 ("no
illegal arrowhead value appears in any authored JSON") had zero automated guard. The check is
purely additive: it rejects what was always illegal by appending to the existing `errors` list
without touching the report/exit-code machinery (lines 54-69). The RESEARCH recommended this
as high-value, low-cost hardening; it was accepted explicitly as a permitted additive exception
to the "validator FROZEN" rule.

**SC-1 coverage after this plan:** Automated — the Phase-1 validator now rejects any authored
JSON that contains an illegal arrowhead token, exiting with code 1 before render is attempted.

## What Was Built

### Task 2: Arrowhead deny-list in excalidraw_validator.py

Added a new check block (after the existing "label" deny-list, before standalone-text check)
that iterates all elements and inspects both `startArrowhead` and `endArrowhead` keys. Legal
set: `{"arrow", "bar", "dot", "triangle", None}`. Any value outside the set appends a
descriptive error message naming the element id, the offending key, the illegal value, and the
legal set. Appending to `errors` drives the existing non-zero exit — no change to report
machinery.

**Verification passed:**
- `crowsfoot` arrowhead → exit code 1, error names element id + illegal value.
- Legal arrowheads (arrow/bar/dot/triangle/None, mixed) → exit code 0, no arrowhead error.

### Task 3: kb/relationship-endpoint.md primitive

Created the shared endpoint-glyph primitive following tree-hierarchy.md's section layout:
back-ref header, When to use, Geometry, JSON skeleton, See in examples, Notes.

**Pinned geometry (deferred from notation-conventions.md lines 55-58):**
- Diamond glyph: `width: 14px`, `height: 14px`; aggregation = white fill (`#ffffff`); composition = solid fill (`#1e1e1e`)
- Ellipse glyph: `10px x 10px` for ER optional endpoint (alternative to `dot` arrowhead)
- Textual multiplicity label: `fontFamily: 3`, `fontSize: 16`, placed 20-40px from endpoint outside all box bboxes; `strokeColor: "#1e1e1e"`

**Anchoring rule (Pattern 3):** Connector `arrow` binds to box rectangle border; composed glyph is a separate element overlaid at owner end, added to connector's `groupIds`. Keeps `check_arrow_endpoint_unanchored` green.

**JSON skeletons provided for:**
- ER: one (bar), zero/optional (dot), many (textual label + null arrowhead)
- UML: aggregation (white diamond), composition (solid diamond), generalization (triangle+solid), realization (triangle+dashed), association (arrow+solid), dependency (arrow+dashed)

**Back-ref line:** `> Used by types: er, class` present on line 3.

**References:** `@../diagram-types/notation-conventions.md` and `@../diagram-types/compartmented-box.md` referenced — neither is re-derived.

**Non-blank lines:** 220 (requirement: ≥ 40 — satisfied by wide margin).

## Deviations from Plan

None — plan executed exactly as directed by the user's `add-check` decision and task specifications.

## Known Stubs

- `See in examples` section in `kb/relationship-endpoint.md` contains placeholders for `er_<subject>.png` and `class_<subject>.png`. These are intentional: the canonical examples are authored in Plans 02 and 03; the real filenames will be filled in when those plans complete.

## Threat Flags

None. This plan authors Markdown and extends a local Python validator. No new network endpoints, auth paths, file access patterns, or schema changes at trust boundaries were introduced.

## Self-Check: PASSED

| Check | Result |
|-------|--------|
| kb/relationship-endpoint.md exists | FOUND |
| excalidraw_validator.py exists | FOUND |
| 07-01-SUMMARY.md exists | FOUND |
| Commit db9486a (validator) exists | FOUND |
| Commit 4760645 (primitive) exists | FOUND |
| Back-ref line "> Used by types: er, class" present | PASS |
| "crowsfoot" named as illegal in primitive | PASS |
| LEGAL_ARROWHEADS deny-list variable in validator | PASS |
