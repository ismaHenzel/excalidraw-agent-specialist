---
phase: 05-tech-architecture-activity
reviewed: 2026-06-05T00:00:00Z
depth: standard
files_reviewed: 9
files_reviewed_list:
  - .claude/agents/excalidraw/kb/decision-branch.md
  - .claude/agents/excalidraw/kb/decision-marker.md
  - .claude/agents/excalidraw/kb/feedback-loop.md
  - .claude/agents/excalidraw/kb/task-list.md
  - .claude/agents/excalidraw/kb/linear-pipeline.md
  - .claude/agents/excalidraw/kb/group-container.md
  - .claude/agents/excalidraw/diagram-types/activity.md
  - .claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw
  - .claude/agents/excalidraw/diagram-types/README.md
findings:
  critical: 3
  warning: 6
  info: 2
  total: 11
status: issues_found
---

# Phase 05: Code Review Report

**Reviewed:** 2026-06-05T00:00:00Z
**Depth:** standard
**Files Reviewed:** 9
**Status:** issues_found

## Summary

This phase wired the `activity` diagram type by authoring `diagram-types/activity.md`, six `kb/` primitives with `> Used by types: activity` back-refs, and a canonical example `examples_excalidraw/activity_order_fulfillment.excalidraw`. The structural plumbing (resolver table row, back-refs, verifier pass) is sound. However the canonical example contains three correctness defects that cause it to violate the very KB rules it is supposed to demonstrate, plus five style violations that produce a misleading teaching artifact. Two of those KB rules are also internally contradictory.

The verifier (`verifier_structural.py`) passes clean against the example — all issues found here are above the verifier's check surface and require human or recipe-level enforcement.

---

## Critical Issues

### CR-01: Feedback loop routes through the main flow, not around it — violates feedback-loop.md clearance rule

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (element `arrow_reorder_loop`, line ~779)

**Issue:** `feedback-loop.md` states: *"The loop must route around the main flow, never cross it"* and *"Stay at least 80px clear of any existing element."* The `arrow_reorder_loop` element routes its return (horizontal) leg at `y=270`. The `receive_order` rectangle's bottom edge is at `y=230` (top `180` + height `50`). The clearance between the loop's horizontal leg and the nearest element is only `270 - 230 = 40px` — half the required minimum. Furthermore, the loop's horizontal segment (`x=160..390, y=270`) runs inside the bounding column of the main flow rather than around it. The canonical example is supposed to be the ground truth for how agents produce activity diagrams; a rule violation here will be imitated.

**Fix:** Reroute `arrow_reorder_loop` to go left of `x=80` (outside the leftmost element), then upward, then re-enter `check_stock` from the left edge. This guarantees > 80px clearance and routes around — not through — the flow column. Example corrected points starting from the left edge of `reorder` (x=80, y=435):

```json
{
  "id": "arrow_reorder_loop",
  "type": "arrow",
  "x": 80, "y": 435,
  "points": [
    [0, 0],
    [-60, 0],
    [-60, -120],
    [220, -120],
    [220, -120]
  ]
}
```
Adjust the re-entry final point so the last absolute coordinate lands on `check_stock`'s left border at `(300, 315)`.

---

### CR-02: Canonical example violates 20-grid rule pervasively — rule is stated as hard requirement in activity.md

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (multiple elements)

**Issue:** `activity.md` states: *"Keep coordinates on the 20-grid"* (hard convention). The verifier does not check grid alignment, so this escapes automated detection. Systematic audit shows the following off-grid values (a coordinate is on-grid if divisible by 20):

| Element | Off-grid fields |
|---|---|
| `start_node` | y=70 |
| `receive_order` | h=50 |
| `label_receive` | x=315, y=197, w=150 |
| `check_stock` | y=290, h=50 |
| `label_check` | x=315, y=307, w=150 |
| `decision_stock` | x=310 |
| `label_decision` | x=335, y=442, w=110 |
| `reorder` | y=410, h=50 |
| `label_reorder` | x=95, y=427, w=130 |
| `charge_payment` | h=50 |
| `label_charge` | x=575, y=397, w=150 |
| `ship_order` | y=490, h=50 |
| `label_ship` | x=575, y=507, w=150 |
| `label_yes` | x=478, y=435, w=30 |
| `label_no` | x=246, y=435, w=30 |
| `label_reorder_loop` | y=268 |
| (all 8 arrows) | x, y, w, h off-grid |

This is not a cosmetic preference: the `gridSize: 20` setting in `appState` means the Excalidraw editor will snap elements to this grid. Elements authored off-grid will visually jump when a user opens and edits the canonical example, destroying the teaching value.

**Fix:** Snap all coordinates to multiples of 20. For example: `start_node.y=80`, `receive_order.h=60`, `check_stock.y=300`, `decision_stock.x=320`, etc. Recalculate all dependent arrow points accordingly.

---

### CR-03: Intra-KB contradiction — diamond `roundness` specification conflicts between `decision-branch.md` and `activity.md`/canonical example

**File:** `.claude/agents/excalidraw/kb/decision-branch.md` (line 32) vs `.claude/agents/excalidraw/diagram-types/activity.md` (line 17) and the canonical example

**Issue:** `decision-branch.md` JSON skeleton specifies `"roundness": { "type": 3 }` on the diamond element. However `activity.md` states diamonds must be *"first-class, verifier-anchorable"* shapes used *directly*, and the canonical example (`decision_stock`) uses `"roundness": null`. Type `3` roundness on a diamond produces visually rounded corners; `null` keeps it sharp. An agent assembling an activity diagram from the two-layer KB will encounter contradictory instructions and may produce incorrect output. Since `activity.md` is the consumer and the canonical example is the ground truth, `decision-branch.md` is the authoritative source of the bug.

**Fix:** Change `decision-branch.md` line 32 from:
```json
"roundness": { "type": 3 }
```
to:
```json
"roundness": null
```
Add a note: *"Diamond shapes in Activity diagrams use `roundness: null` — the `type:3` form is reserved for containers (`group-container.md`)."*

---

## Warnings

### WR-01: Decision-branch arrow labels use wrong color and font size in canonical example

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (elements `label_yes` line ~492, `label_no` line ~528)

**Issue:** `decision-branch.md` specifies branch-label text elements should use `strokeColor: "#64748b"` and `fontSize: 14`. The canonical example uses `strokeColor: "#1e1e1e"` (black) and `fontSize: 12` for both `label_yes` and `label_no`. Any agent or human imitating this example will produce non-conforming diagrams.

**Fix:**
```json
{ "strokeColor": "#64748b", "fontSize": 14 }
```
Apply to both `label_yes` and `label_no` elements.

---

### WR-02: Feedback loop label placed off the return leg — violates feedback-loop.md placement rule

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (element `label_reorder_loop`, line ~566)

**Issue:** `feedback-loop.md` specifies: *"Mid-arrow text on the longest (return) leg, above the segment."* The horizontal (return) leg of `arrow_reorder_loop` runs from absolute `(160, 270)` to `(390, 270)`. The label `label_reorder_loop` is positioned at `x=100, y=268` — `x=100` is 60px to the left of the segment's start (`x=160`), placing the label entirely outside the leg it annotates. The `y=268` (above the segment) is correct; only `x` is wrong.

**Fix:** Move `label_reorder_loop.x` to a value in the range `[160, 280]` to place it above the horizontal leg. Given a mid-point at `x=(160+390)/2=275`:
```json
{ "x": 220, "y": 254 }
```

---

### WR-03: Feedback loop label uses wrong color

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (element `label_reorder_loop`, line ~566)

**Issue:** `feedback-loop.md` specifies `strokeColor: "#64748b"` for the loop label. The canonical example uses `"strokeColor": "#1e1e1e"`. Same class of error as WR-01 — agents imitating the example will produce wrong color.

**Fix:**
```json
{ "strokeColor": "#64748b" }
```

---

### WR-04: Five straight arrows encoded as three-point collinear paths — misrepresents elbow semantics

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (elements `arrow_start_receive`, `arrow_receive_check`, `arrow_check_decision`, `arrow_charge_ship`, `arrow_ship_end`)

**Issue:** These five arrows all have points of the form `[[0,0],[0,N/2],[0,N]]` — three collinear points on the same vertical line. With `elbowed: true`, Excalidraw routes elbowed arrows only when there is a directional change between consecutive segments. Three collinear points produce a straight line with a redundant midpoint, not an elbow. This misleads agents into thinking a three-point structure is required for any arrow (including straight ones), and may cause unexpected rendering in future Excalidraw versions that enforce orthogonality on elbowed paths. `check_arrow_points_too_few` requires `>= 3` points — the intent is for three points to form a real 90-degree elbow, not a collinear triplet.

**Fix:** Use two-point straight arrows for vertical runs with no turn:
```json
"points": [[0, 0], [0, 50]]
```
Reserve the three-point form for actual elbows where the middle point defines a turn.

---

### WR-05: Feedback loop exit direction violates feedback-loop.md convention

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (element `arrow_reorder_loop`, line ~779)

**Issue:** `feedback-loop.md` states: *"Exit leg — vertical or horizontal segment from the failure point, moving away from the main flow (typically downward or leftward)."* `arrow_reorder_loop` starts at `(160, 410)` which is the top-center of the `reorder` rectangle (top edge at `y=410`), and its first segment moves upward (`y` decreases). An exit from the top of a node moving upward contradicts the "downward or leftward" guidance; it also exits in the same direction as the incoming forward flow, making the loop visually indistinguishable from forward progress at first glance.

**Fix:** Exit from the bottom edge of `reorder` (`y=460`) moving downward, then route left and upward outside the main flow column to re-enter `check_stock` from the left side. This matches the ASCII diagram in `feedback-loop.md`.

---

### WR-06: `linear-pipeline.md` is missing a "See in examples" section

**File:** `.claude/agents/excalidraw/kb/linear-pipeline.md` (entire file)

**Issue:** Every other pattern file in the reviewed set (`decision-branch.md`, `decision-marker.md`, `feedback-loop.md`, `task-list.md`, `group-container.md`) contains a "See in examples" section that anchors the abstract geometry to a concrete visual reference. `linear-pipeline.md` has no such section. The new canonical activity example (`activity_order_fulfillment.excalidraw`) demonstrates a linear pipeline chain (start → receive → check → [branch]), but is not referenced. The `activity_order_fulfillment.png` render is also now available. This gap makes `linear-pipeline.md` the only primitive file that requires agents to work from geometry alone with no visual anchor.

**Fix:** Add the following section to `linear-pipeline.md`:
```markdown
## See in examples

- `examples/activity_order_fulfillment.png` — the vertical action chain (Receive Order → Check Stock → decision diamond) demonstrates sequential node spacing and uniform arrow style.
- `examples/data_pipeline_flow.png` — horizontal left-to-right pipeline with Start/Trigger → End/Success color conventions.
```

---

## Info

### IN-01: Activity-specific kb files do not reference the new canonical example in their "See in examples" sections

**File:** `.claude/agents/excalidraw/kb/decision-branch.md` (line 66), `kb/decision-marker.md` (line 75), `kb/feedback-loop.md` (line 64), `kb/task-list.md` (line 55)

**Issue:** The `See in examples` sections in the four activity-specific KB files reference only the pre-existing `data_pipeline_flow.png` and `process_decision.png` examples. The new `activity_order_fulfillment.png` (now the canonical activity ground truth) is not referenced in any of these files. When an agent assembles an activity diagram using these primitives, it will not be directed to the canonical activity example.

**Fix:** Append a bullet to the `See in examples` section of each affected file:
```markdown
- `examples/activity_order_fulfillment.png` — canonical UML Activity reference for this pattern.
```

---

### IN-02: `decision_stock` x-offset from diamond deviates from `decision-branch.md` prescribed geometry

**File:** `.claude/agents/excalidraw/examples_excalidraw/activity_order_fulfillment.excalidraw` (element `charge_payment`, line ~331)

**Issue:** `decision-branch.md` specifies outcome blocks at `x_d + 260`. The `decision_stock` diamond is at `x=310`; `charge_payment` is at `x=560`, giving an offset of `250px` instead of the specified `260px`. The deviation is 10px and will not cause visual failure, but the canonical example should match the spec it demonstrates, especially given the 20-grid rewrite needed for CR-02 will move coordinates anyway.

**Fix:** When re-snapping to the 20-grid (CR-02 fix), place `charge_payment.x = decision_stock.x + 260`. If `decision_stock.x=320` (on-grid), then `charge_payment.x=580`.

---

_Reviewed: 2026-06-05T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
