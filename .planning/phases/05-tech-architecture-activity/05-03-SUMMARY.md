---
plan: 05-03
phase: 05-tech-architecture-activity
status: checkpoint
wave: 2
requirements: [UML-04]
checkpoint_task: 3
checkpoint_type: human-verify
---

# Plan 05-03 Summary: Author Activity example pair + promote resolver row

## What was built

Authored `examples_excalidraw/activity_order_fulfillment.excalidraw` — a canonical UML Activity diagram composing existing `kb/` primitives per the Plan 02 recipe. The diagram represents an order-fulfillment workflow with: filled ellipse initial node, four sequential action rectangles (Receive Order, Check Stock, Reorder Items, Charge Payment, Ship Order), one real `diamond` decision gate ("In stock?") with labeled Yes/No branches, a 4-point feedback-loop arrow routing `Reorder Items → Check Stock` around the main flow, and an ellipse ring final node. All arrows use `elbowed: true`, `roundness: null`, and ≥3 orthogonal elbow points. All text elements carry explicit `width`, `height`, `lineHeight`, `textAlign`, `verticalAlign`, and `originalText`.

Rendered the `.excalidraw` to `examples_excalidraw/activity_order_fulfillment.png` via the Docker render pipeline, placed the PNG at `examples/activity_order_fulfillment.png`, and promoted the `activity` resolver row in `diagram-types/README.md` from _(planned — Phase 5)_ to wired.

Stopped at Task 3 (`checkpoint:human-verify`) awaiting visual verification of the rendered PNG (the visual half of EX-03 gate).

## Key files

### Created
- `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` — canonical Activity source (27 elements: 2 ellipses, 5 rectangles, 1 diamond, 9 arrows, 10 text labels)
- `.claude/agents/excalidraw/examples/activity_order_fulfillment.png` — rendered ground-truth PNG (147 KB)

### Modified
- `.claude/agents/excalidraw/diagram-types/README.md` — activity row promoted from _(planned)_ to wired; "Wired rows" note updated to include both tech-architecture and activity

## Automated checks passed

- `excalidraw_validator.py` exits 0, zero warnings
- `verifier_structural.py` returns empty issues list `[]` (zero errors)
- Inline Python check: `diamond`, `ellipse`, `rectangle`, `arrow` all present; all `text` elements have `width` and `height`
- Task 2 verification: `examples/activity_order_fulfillment.png` exists, `diagram-types/README.md` contains `activity_order_fulfillment.png`, no `_(planned)_` in activity row

## Commits

- `f109c72` feat(05-03): author canonical Activity example .excalidraw
- `6b4a620` feat(05-03): render Activity PNG and promote resolver row to wired

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Re-authored excalidraw from previous partial draft**
- **Found during:** Task 1
- **Issue:** The pre-existing `activity_order_fulfillment.excalidraw` (untracked at plan start) had 5 of 7 arrows with only 2 points (violating the house-style "≥3 orthogonal points" requirement) and text elements with low-contrast strokeColor `#1e40af` (validator warning).
- **Fix:** Rewrote the file with all arrows using ≥3 orthogonal elbow points, updated all text strokeColors to `#1e1e1e`, added a new `charge_payment` action node to enrich the flow per the plan's description.
- **Files modified:** `examples_excalidraw/activity_order_fulfillment.excalidraw`
- **Commit:** f109c72

## Checkpoint (Task 3: awaiting human visual verification)

The structural half of EX-03 is satisfied. The visual half requires human inspection of `examples/activity_order_fulfillment.png`:

1. Confirm flow reads: start ellipse → Receive Order → Check Stock → "In stock?" diamond → Yes branch → Charge Payment → Ship Order → end ellipse; No branch → Reorder Items → feedback loop back to Check Stock
2. Confirm arrowheads visibly touch shape borders (no `arrow_disconnected_visual`)
3. Confirm no text spills outside its container (no `text_overflow_visual`)
4. Confirm no missing-glyph boxes (no `missing_glyph_box`)
5. Confirm no layout collisions between elements

## Self-Check: PASSED

- `examples_excalidraw/activity_order_fulfillment.excalidraw` exists ✓
- `examples/activity_order_fulfillment.png` exists (147 KB) ✓
- `diagram-types/README.md` contains `activity_order_fulfillment.png` ✓
- Activity row has no `_(planned)_` annotation ✓
- Commits f109c72 and 6b4a620 exist in git log ✓
