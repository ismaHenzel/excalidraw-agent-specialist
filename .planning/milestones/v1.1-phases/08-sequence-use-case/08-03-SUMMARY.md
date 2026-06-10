---
phase: 08-sequence-use-case
plan: "03"
subsystem: diagram-types + canonical-example
tags: [uml, use-case, group-container, notation-conventions, ex-03]
dependency_graph:
  requires:
    - kb/group-container.md (system boundary primitive)
    - diagram-types/notation-conventions.md (actor=labelled-box convention DTKB-04)
  provides:
    - diagram-types/use-case.md (UML-03 TYPE recipe)
    - examples_excalidraw/use_case_checkout.excalidraw (canonical JSON ground truth)
    - examples/use_case_checkout.png (rendered canonical PNG — passes structural loop)
  affects:
    - diagram-types/README.md (resolver row wiring — deferred to 08-04 after EX-03 approval)
tech_stack:
  added: []
  patterns:
    - Pure-composition TYPE recipe (mirrors activity.md — no new primitive)
    - KB two-layer @-reference discipline (TYPE composes from kb/ + notation-conventions)
    - EX-03 gate discipline (resolver row wired only after full loop + human visual approval)
key_files:
  created:
    - .claude/agents/excalidraw/diagram-types/use-case.md
    - .claude/agents/excalidraw/examples_excalidraw/use_case_checkout.excalidraw
    - .claude/agents/excalidraw/examples/use_case_checkout.png
  modified: []
decisions:
  - "Actors use labelled-box convention per DTKB-04 (rectangle + «actor» text) — NOT stick-figure, NOT emoji"
  - "System boundary uses group-container roundness:{type:3} — the one intentional rounded rectangle"
  - "Include relationship encoded as dashed arrow + «include» text label (Dependency row convention)"
  - "Association arrows use endArrowhead:null, startArrowhead:null (undirected plain lines)"
  - "Ellipses have no roundness override (naturally elliptical — roundness:null is wrong for ellipses)"
  - "Resolver row wiring deferred to 08-04 (EX-03 gate not yet cleared)"
metrics:
  duration: "< 30 min"
  completed: "2026-06-08"
  tasks_completed: 1
  files_modified: 3
---

# Phase 08 Plan 03: Use-Case Recipe + Canonical Example Summary

Authored the use-case TYPE-layer recipe (`diagram-types/use-case.md`) — a pure-composition type that composes `group-container` (system boundary) and `notation-conventions` (actor=labelled-box, legal arrowhead tokens, Association + Dependency encodings) by `@`-reference, introducing no new primitive. Produced the canonical Checkout System use-case example (`use_case_checkout.excalidraw` + `use_case_checkout.png`) that passes the full validate→render→verify loop with structural issues == [].

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Author use-case.md recipe + canonical example pair (full loop) | 3ae3f60 | use-case.md, use_case_checkout.excalidraw, use_case_checkout.png |
| — | Add sibling rendered PNG | 8c27df4 | examples_excalidraw/use_case_checkout.png |

## Task 2: EX-03 Visual Gate — PENDING

Task 2 is a `checkpoint:human-verify` gate. The structural loop is green; EX-03 visual approval is awaiting the operator. The resolver row wiring is blocked on this approval (see 08-04).

## Artifact Details

### diagram-types/use-case.md (new)

- Layer header: `> Layer: TYPE recipe. Composes primitives from ../kb/; does not re-derive their geometry. Indexed in README.md.`
- Sections: Purpose, How to draw it (bullet-per-element-type), Composes (primitive layer), Ground truth
- How to draw it covers: Actor=labelled box (rectangle+«actor» text, NOT stick-figure, NOT emoji), use-case oval (native ellipse, no roundness override), system boundary (group-container roundness:{type:3}), Association (null/null arrowheads, solid), Include/extend (dashed+arrow arrowhead+«include» text)
- Composes: group-container.md + notation-conventions.md
- Ground truth: points to examples/use_case_checkout.png

### use_case_checkout.excalidraw (new)

**Checkout System — element inventory:**
- 1 system-boundary rectangle (`roundness: {"type": 3}`, `strokeColor: "#1e3a5f"`) with title text "Checkout System"
- 2 actor labelled boxes: `actor_customer_box` (Customer) and `actor_admin_box` (Admin), each with `«actor»` stereotype text + actor name text, placed OUTSIDE system boundary
- 5 use-case ellipse ovals inside system boundary: Browse Products, Add to Cart, Place Order, Process Payment, View Reports — each paired with a text label under a groupId
- 4 solid undirected association arrows (endArrowhead:null, startArrowhead:null): Customer→Browse Products, Customer→Add to Cart, Customer→Place Order, Admin→View Reports
- 1 dashed `«include»` arrow (endArrowhead:"arrow", strokeStyle:"dashed"): Place Order → Process Payment, with `«include»` stereotype text label

**Structural verifier result: issues == []** (exit 0, empty issue list)

**Arrowhead legality: PASS** — grep for crowsfoot/hollow/open returns 0

**Raw emoji: PASS** — no raw emoji codepoints in any text element

### use_case_checkout.png (new)

Rendered from the full validate→render→verify loop. Visual assessment:
- Checkout System rounded boundary visible with label at top center
- Customer and Admin labelled boxes clearly outside the boundary, each showing `«actor»` stereotype
- 5 use-case ovals inside the boundary with readable monospace labels
- 4 solid association lines connecting actors to their use cases
- Dashed arrow from Place Order to Process Payment with `«include»` label visible
- All text monospace, no overflow, no emoji tofu boxes

## Structural Verification Record

```
python3 .claude/agents/excalidraw/scripts/verifier/verifier_structural.py \
  .claude/agents/excalidraw/examples_excalidraw/use_case_checkout.excalidraw
→ []
```

**Exit code: 0. Issues: none.**

Auto-fix iterations: 1 (fixed `arrow_points_too_few` on `rel_include_1` — added intermediate point to include arrow for 3-point elbow routing)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed arrow_points_too_few on rel_include_1 (include arrow)**
- **Found during:** Task 1 structural verifier run
- **Issue:** Include arrow (`rel_include_1`) had only 2 points; verifier requires >=3 for elbow routing
- **Fix:** Added intermediate midpoint `[30, 0]` to produce 3-point elbow `[[0,0],[30,0],[60,0]]`
- **Files modified:** `examples_excalidraw/use_case_checkout.excalidraw`
- **Iterations used:** 1 of 3 allowed

## Threat Surface Scan

No new network endpoints, auth paths, file access patterns, or schema changes introduced.

T-08-06 (actor as emoji/stick-figure) mitigated: 2 actor rectangles with `«actor»` text; no raw emoji in any text element; `check_raw_emoji_in_text` verifier check clean.
T-08-07 (illegal arrowhead token) mitigated: grep for crowsfoot/hollow/open returns 0; all arrows use legal tokens (arrow, null only).
T-08-05 (resolver row wired before example passes) mitigated: plan does NOT touch README.md; wiring deferred to 08-04 after EX-03 approval.

## Known Stubs

None. The use-case recipe composes exclusively from existing committed primitives. The canonical example is fully wired with real element data.

## Self-Check: PASSED

- [x] `.claude/agents/excalidraw/diagram-types/use-case.md` exists (contains "Layer: TYPE recipe")
- [x] `.claude/agents/excalidraw/examples_excalidraw/use_case_checkout.excalidraw` exists (contains "ellipse")
- [x] `.claude/agents/excalidraw/examples/use_case_checkout.png` exists (188971 bytes)
- [x] Commit 3ae3f60 exists (`feat(08-03): author use-case.md recipe + canonical use_case_checkout example`)
- [x] Structural verifier issues == [] (confirmed via automated run)
- [x] grep for crowsfoot/hollow/open in excalidraw = 0
- [x] No raw emoji in text elements
- [x] No ellipse element carries roundness:null
- [x] `group-container` referenced in use-case.md
- [x] `notation-conventions` referenced in use-case.md
