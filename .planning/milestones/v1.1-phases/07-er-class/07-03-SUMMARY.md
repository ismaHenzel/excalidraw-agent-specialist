---
phase: "07-er-class"
plan: "03"
subsystem: "diagram-types/class"
tags: ["uml-class", "compartmented-box", "relationship-glyphs", "example-pair", "EX-03"]
dependency_graph:
  requires:
    - "07-01: kb/relationship-endpoint.md (shared endpoint-glyph primitive)"
    - "Phase 4: compartmented-box.md construction (INT-02)"
    - "Phase 4: notation-conventions.md (legal-encoding table, DTKB-04)"
  provides:
    - "diagram-types/class.md: UML class type recipe (three-compartment boxes, glyph workarounds, guillemet stereotypes)"
    - "examples_excalidraw/class_order_domain.excalidraw: canonical class source (all 5 relationship types)"
    - "examples/class_order_domain.png: rendered sibling passing validator + structural verifier"
  affects:
    - "diagram-types/README.md: resolver row for class will be wired in Plan 04"
    - "REQUIREMENTS.md: UML-02 tick to be applied in Plan 04 after EX-03 approval"
tech_stack:
  added: []
  patterns:
    - "Pattern 3 / Pitfall 2: composed diamond glyph overlaid on anchored connector (connector binds to box rectangle, diamond shares connector groupIds)"
    - "Three-compartment box: header divider at box.y+40, attr divider after last attr row, methods in third compartment"
    - "Guillemet stereotypes (via «» chars) rendered with fontFamily:3 — confirmed not tofu (Assumption A1 verified)"
key_files:
  created:
    - ".claude/agents/excalidraw/diagram-types/class.md"
    - ".claude/agents/excalidraw/examples_excalidraw/class_order_domain.excalidraw"
    - ".claude/agents/excalidraw/examples/class_order_domain.png"
    - ".claude/agents/excalidraw/examples_excalidraw/class_order_domain.png"
  modified: []
decisions:
  - "Attr-divider placement: compartmented-box.md formula 'box.y+40+20*k' bisects the last attribute row mid-cell (bug in formula application). Fix: placed attr divider AFTER the last attr row bottom edge (last_attr_row_y + 20), keeping all rows un-bisected. No change to row x or pitch."
  - "PremiumCustomer box width expanded from 220 to 240 to clear structural verifier text_overflow_static for '+ getDiscount(): Double' (22 chars x 9.6 = 211.2px ~ 220px — within tolerance but flagged as error at w=220; w=240 passes cleanly)."
  - "Arrow elbow points: added 3-point path (start, midpoint, end) to satisfy arrow_points_too_few verifier requirement for all 5 connectors."
metrics:
  duration: "~20 min"
  completed_date: "2026-06-07"
  tasks_completed: 2
  files_count: 4
---

# Phase 07 Plan 03: UML Class Recipe + Canonical Example Summary

**One-liner:** UML class diagram recipe composing three-compartment boxes, five glyph-workaround relationships, and guillemet stereotypes; canonical order-domain example pair passes validator + structural verifier.

## What Was Built

**Task 1 (prior run, already committed):** `diagram-types/class.md` — the UML class type recipe. Mirrors `snowflake-schema.md` section structure (Layer-header, Purpose, How to draw it, Composes, Ground truth). Composes `@./compartmented-box.md`, `@../kb/relationship-endpoint.md`, and `@./notation-conventions.md` by @-reference. Documents three-compartment box construction, full relationship glyph set (association/dependency/generalization/realization/aggregation/composition), guillemet stereotypes, and the composition-glyph-over-anchored-connector rule (Pattern 3 / Pitfall 2). 153 lines, no re-derived geometry.

**Task 2 (this run):** `examples_excalidraw/class_order_domain.excalidraw` — canonical class source with 6 classes:
- `«Payable»` interface (stereotype rendered with `«»` guillemets, fontFamily:3)
- `Order` (3 attrs, 2 methods — implements Payable via realization)
- `Customer` (3 attrs, 2 methods — plain association to Order)
- `OrderLine` (2 attrs, 1 method — composed by Order via solid diamond)
- `PremiumCustomer` (1 attr, 1 method — generalizes Customer via filled triangle)
- `Discount` (2 attrs, 1 method — aggregated by Order via white diamond)

Five relationship types demonstrated:
1. Generalization (PremiumCustomer → Customer): `endArrowhead:"triangle"`, solid stroke
2. Realization (Order → «Payable»): `endArrowhead:"triangle"`, dashed stroke
3. Association (Customer → Order): `endArrowhead:"arrow"`, solid stroke
4. Composition (Order → OrderLine): connector with `null` arrowheads + 14px solid dark diamond overlaid at Order end, shared `groupIds`
5. Aggregation (Order → Discount): connector with `null` arrowheads + 14px white diamond overlaid at Order end, shared `groupIds`

`examples/class_order_domain.png` — rendered sibling produced by `validate_and_render.sh`.

## Verification Results

- `excalidraw_validator.py`: PASS (exit 0)
- `verifier_structural.py`: PASS (empty issues array `[]`)
- Arrowhead audit: no illegal tokens (`bad=[]`, `tri=True`, `dia=True`)
- PNG exists: PASS (`examples/class_order_domain.png`, 173 KB)

## EX-03 Visual Gate

**Status: AWAITING HUMAN APPROVAL (Task 3 checkpoint)**

The PNG shows:
- Six sharp three-compartment class boxes with full-width dividers and monospace ASCII rows
- `«Payable»` guillemets render correctly (confirmed not tofu under fontFamily:3 — Assumption A1 verified)
- Realization: filled triangle on dashed line connecting Order to «Payable»
- Generalization: filled triangle on solid line from PremiumCustomer up to Customer
- Composition: solid (dark) diamond at Order end connecting to OrderLine
- Aggregation: white (hollow) diamond at Order end connecting to Discount
- Association: plain arrow from Customer to Order

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Attr-divider bisected last attribute row**
- **Found during:** Task 2 — visual inspection of rendered PNG showed strikethrough artifacts on last attr row in each box
- **Issue:** Placed second (attr/method) divider at `box.y + 40 + 20*k` per compartmented-box.md formula; this lands 10px into the last attr row (row top is at `box.y + 40 + 10 + (k-1)*20`, divider at `box.y + 40 + k*20` is 10px below row top, bisecting the row mid-cell)
- **Fix:** Moved attr divider to `last_attr_row_y + 20` (immediately after last attr row bottom), and adjusted all method row positions accordingly. Box heights were recalculated to remain consistent.
- **Files modified:** `class_order_domain.excalidraw` (divider y values + method row y values)
- **Commit:** 49c630f

**2. [Rule 1 - Bug] text_overflow_static error on PremiumCustomer**
- **Found during:** Task 2 — first structural verifier run
- **Issue:** `+ getDiscount(): Double` (22 chars × 9.6 = 211.2px ~= 220px) at exact container width 220 triggered overflow error
- **Fix:** Expanded `pc-rect` width from 220 to 240; updated all divider and row element widths for PremiumCustomer group
- **Commit:** 49c630f

**3. [Rule 1 - Bug] arrow_points_too_few warnings on all 5 arrows**
- **Found during:** Task 2 — first structural verifier run
- **Issue:** All arrows had 2-point paths `[[0,0],[dx,dy]]`; verifier requires >= 3 points for elbow routing
- **Fix:** Added intermediate midpoint to each arrow, producing 3-point paths with orthogonal segments
- **Commit:** 49c630f

## Known Stubs

None — all class boxes have real attributes and methods; the example exercises the full relationship glyph set. The resolver row and UML-02 REQUIREMENTS tick are intentionally deferred to Plan 04 (not stubs — they are gated on EX-03 human approval).

## Threat Flags

None — no new network endpoints, auth paths, file access patterns, or schema changes introduced.

## Self-Check

- [x] `class.md` exists: `/home/linuxzinho/coding/excaildraw-claude/.claude/agents/excalidraw/diagram-types/class.md` (153 lines, committed in prior run)
- [x] `class_order_domain.excalidraw` exists: committed at 49c630f
- [x] `class_order_domain.png` (examples/) exists: committed at 49c630f
- [x] Validator passes (exit 0)
- [x] Structural verifier passes (empty array)
- [x] Legal arrowheads only: `bad=[]`, `tri=True`, `dia=True`
- [x] `«»` guillemets render correctly (Assumption A1 confirmed)

## Self-Check: PASSED
