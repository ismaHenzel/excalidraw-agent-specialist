---
phase: 08-sequence-use-case
plan: "01"
subsystem: kb-primitive + verifier-hardening
tags: [uml, sequence, lifeline, activation-bar, verifier, structural-check]
dependency_graph:
  requires: []
  provides:
    - kb/lifeline-activation.md (sequence geometry primitive)
    - verifier_structural.py check_sequence_activation_center_x
  affects:
    - diagram-types/sequence.md (can now @-reference lifeline-activation.md)
    - UML-01 Success Criterion 1 (activation bars centered on lifeline x now has automated guard)
tech_stack:
  added: []
  patterns:
    - KB two-layer primitive-first pattern (mirrors kb/relationship-endpoint.md from Phase 7)
    - Additive verifier hardening (mirrors Phase 7 arrowhead check precedent)
key_files:
  created:
    - .claude/agents/excalidraw/kb/lifeline-activation.md
  modified:
    - .claude/agents/excalidraw/scripts/verifier/verifier_structural.py
decisions:
  - "Task 1 decision: add-center-x — add check_sequence_activation_center_x to verifier_structural.py (RESEARCH Open Question 1 recommendation selected by user)"
  - "Monotonic-Y verifier check deferred — enforced by KB discipline + visual review only (RESEARCH recommendation)"
  - "All pixel values in lifeline-activation.md marked [ASSUMED] per RESEARCH.md A1 — first-pass from 20-grid convention, confirmed empirically through the render loop"
metrics:
  duration: "< 10 min"
  completed: "2026-06-08"
  tasks_completed: 3
  files_modified: 2
---

# Phase 08 Plan 01: Lifeline-Activation Primitive + Center-X Verifier Check Summary

Authored the sequence-diagram geometry primitive `kb/lifeline-activation.md` — the exact structural analog of Phase 7's `kb/relationship-endpoint.md` — and added the `check_sequence_activation_center_x` structural verifier check to `verifier_structural.py` per the user's `add-center-x` decision on Task 1.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Decide center-x structural check | checkpoint resolved (add-center-x) | decision recorded |
| 2 | Author kb/lifeline-activation.md primitive | 9337e26 | .claude/agents/excalidraw/kb/lifeline-activation.md |
| 3 | Apply center-x verifier check decision | e526f9c | .claude/agents/excalidraw/scripts/verifier/verifier_structural.py |

## Center-X Decision (Task 1) — Explicit Record

**Decision selected:** `add-center-x` (RESEARCH recommendation)

**Consequence for UML-01 Success Criterion 1:** "Activation bars centered on lifeline x"
now has an automated structural guard: `check_sequence_activation_center_x` in
`verifier_structural.py`. The check runs on every diagram passing through the structural
verifier — any activation-bar rectangle (10–16px wide) whose center-x differs by more
than 1px from the nearest dashed zero-width lifeline line will raise
`activation_bar_center_x_mismatch` (severity: `error`).

**Consequence for monotonic-Y:** The monotonic message-Y check was NOT added (RESEARCH
also recommended deferring it as too complex). SC-1's "message Y values monotonically
non-decreasing" requirement is enforced by `kb/lifeline-activation.md` discipline + verifier
visual review only. No automated guard exists for message Y ordering.

## Key Decisions

1. **add-center-x** — user selected the RESEARCH-recommended option; adds ~55 lines to
   `verifier_structural.py`; heuristic (10–16px width) could in theory false-positive on
   non-activation narrow rectangles but this is low risk for the canonical sequence example.
2. **Monotonic-Y deferred** — complex check, visual review catches it; not adding now.
3. **All geometry values [ASSUMED]** — participant head 120×40, lifeline pitch 180px,
   activation bar 12px, message Y pitch 40px — derived from 20-grid convention and
   compartmented-box precedent; confirmed empirically through the render loop.

## Artifacts Produced

### kb/lifeline-activation.md (new)

- Title: `# Pattern: Lifeline + Activation Bar`
- Back-ref: `> Used by types: sequence`
- Sections: When to use, Legal arrowhead tokens (deny-list callout verbatim from
  relationship-endpoint.md), Geometry (5 sub-sections), JSON skeleton (5 skeletons),
  See in examples, Notes (3 hard rules)
- Forward-references: `@../diagram-types/notation-conventions.md` (DTKB-04) and
  `@../diagram-types/compartmented-box.md` (INT-02) — no re-derivation of either
- Activation bar centering formula pinned: `x = lifeline_center_x - 6`
  (= `lifeline_center_x - ACTIVATION_BAR_WIDTH / 2`)
- Notes hard rules:
  1. Message arrows MUST bind to activation-bar `rectangle` (or participant-head `rectangle`),
     NEVER to the lifeline `line` element — `check_arrow_endpoint_unanchored` does not accept
     `line` elements as anchor targets
  2. `lifeline_center_x = line.x` (width is 0; left edge IS the center)
  3. Self-message route: 3-point elbow from activation bar right edge (+40px x, +40px y,
     back to bar right edge at lower y)
- 200 lines (well above 60-line minimum)

### verifier_structural.py (modified — additive only)

- New function: `check_sequence_activation_center_x(elements)`
- Issue key: `activation_bar_center_x_mismatch` / severity: `error`
- Heuristic: dashed `line` elements with `width == 0` = lifelines; `rectangle` elements
  with `10 <= width <= 16` = activation bars; search radius 8px; tolerance 1px
- Registered in the check-runner aggregation list (after `check_arrow_not_elbow`)
- Pre-existing check count: 9 → post-edit: 10 (no existing check removed or modified)
- Verifier exits 0 on `activity_order_fulfillment.excalidraw` (known-good example)

## Deviations from Plan

None — plan executed exactly as written (after the Task 1 checkpoint resolved to
`add-center-x`).

## Threat Surface Scan

No new network endpoints, auth paths, file access patterns, or schema changes introduced.
The only surface change is an additive Python function in the structural verifier (local
file processing, no I/O beyond reading the already-opened `.excalidraw` JSON).

T-08-01 (verifier tampering) mitigated: additive-only edit; all 9 pre-existing `def check_`
functions present; known-good example still exits 0.
T-08-02 (illegal arrowhead in primitive) mitigated: `grep -vE '^#' | grep -ciE
'endArrowhead.*(crowsfoot|hollow|open)'` returns 0.

## Self-Check: PASSED

- [x] `.claude/agents/excalidraw/kb/lifeline-activation.md` exists (200 lines)
- [x] Commit 9337e26 exists (`feat(08-01): author kb/lifeline-activation.md...`)
- [x] Commit e526f9c exists (`feat(08-01): add check_sequence_activation_center_x...`)
- [x] `grep -c 'def check_sequence_activation_center_x'` = 1
- [x] `grep -c 'activation_bar_center_x_mismatch'` = 2
- [x] `grep -c 'def check_'` = 10 (was 9, none removed)
- [x] Verifier exits 0 on activity_order_fulfillment.excalidraw
