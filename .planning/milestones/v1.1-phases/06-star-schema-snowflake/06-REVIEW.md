---
phase: 06-star-schema-snowflake
reviewed: 2026-06-07T00:00:00Z
depth: standard
files_reviewed: 12
files_reviewed_list:
  - .claude/agents/excalidraw/diagram-types/compartmented-box.md
  - .claude/agents/excalidraw/diagram-types/README.md
  - .claude/agents/excalidraw/diagram-types/snowflake-schema.md
  - .claude/agents/excalidraw/diagram-types/star-schema.md
  - .claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw
  - .claude/agents/excalidraw/examples_excalidraw/star_schema_v2.excalidraw
  - .claude/agents/excalidraw/kb/convergence.md
  - .claude/agents/excalidraw/kb/evidence-card.md
  - .claude/agents/excalidraw/kb/fan-out.md
  - .claude/agents/excalidraw/kb/group-container.md
  - .claude/agents/excalidraw/kb/linear-pipeline.md
  - .claude/agents/excalidraw/kb/tree-hierarchy.md
findings:
  critical: 2
  warning: 4
  info: 2
  total: 8
status: issues_found
---

# Phase 06: Code Review Report

**Reviewed:** 2026-06-07T00:00:00Z
**Depth:** standard
**Files Reviewed:** 12
**Status:** issues_found

## Summary

Reviewed all twelve files in scope: four recipe/type Markdown files (compartmented-box.md, README.md, snowflake-schema.md, star-schema.md), two canonical Excalidraw JSON examples (snowflake_schema.excalidraw, star_schema_v2.excalidraw), and six KB primitive files (convergence.md, evidence-card.md, fan-out.md, group-container.md, linear-pipeline.md, tree-hierarchy.md).

The `star_schema_v2.excalidraw` example is structurally sound: all box heights match the locked formula, header dividers land at `box.y + 40`, row texts land at correct pitches, `groupIds` are populated, all connectors use `elbowed: true` / `roundness: null` / `endArrowhead: "arrow"`, and `startBinding`/`endBinding` reference correct element ids. No overflow, no multi-line text blocks, no undeclared element types.

Two critical defects were found in `snowflake_schema.excalidraw` and `snowflake-schema.md`:

1. The `tree_cat_to_dept` connector in `snowflake_schema.excalidraw` has a diagonal final segment, violating the elbowed-arrow requirement.
2. The `snowflake-schema.md` recipe text instructs authors to place each child sub-table with a "~40px y-step," but the canonical ground truth example places all three normalized boxes on the identical y-row (y=160), contradicting the recipe.

Four warnings cover back-reference incompleteness for transitively composed KB primitives, a collinear redundant midpoint in a tree arrow, a dim_date column name inconsistency between examples, and a missing `compartmented-box` row in the resolver table.

No hardcoded secrets, no executable code paths, no adversarial content in label text, no `eval()` or `innerHTML` patterns, and no prohibited multi-line text blocks were found across any file.

## Critical Issues

### CR-01: Diagonal final segment in `tree_cat_to_dept` arrow violates elbowed-arrow rule

**File:** `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw:2111`

**Issue:** The `tree_cat_to_dept` arrow (connecting `dim_category_box` to `dim_dept_box`) declares `"elbowed": true` and `"roundness": null`, which mandates right-angle-only segments. However its `points` array is:

```json
[[0, 0], [30, 0], [60, -10]]
```

The final segment `[30,0] → [60,-10]` has a non-zero y-delta of -10, making it a 10px diagonal rather than a horizontal line. The arrow also has `"height": 10` confirming this. A true elbow arrow must have every segment either purely horizontal or purely vertical; a diagonal segment is geometrically invalid under `elbowed: true`. When rendered, the Excalidraw engine may force a right-angle routing that ignores the specified points, or render the diagonal, producing a result that does not match the ground truth PNG. The binding rule in `snowflake-schema.md` ("thin elbow arrows, elbowed: true, roundness: null") is broken by this element.

**Fix:** Make the final segment horizontal (y-delta = 0). Correct the points so all three segments are axis-aligned. Because `dim_category_box.right = 1500` and `dim_dept_box.left = 1560`, a flat horizontal connector suffices:

```json
{
  "id": "tree_cat_to_dept",
  "type": "arrow",
  "x": 1500,
  "y": 210.0,
  "width": 60,
  "height": 0,
  "points": [[0, 0], [30, 0], [60, 0]],
  "strokeWidth": 1.5,
  "elbowed": true,
  "roundness": null,
  "endArrowhead": "arrow"
}
```

---

### CR-02: Recipe text contradicts ground truth example on y-step for normalized sub-tables

**File:** `.claude/agents/excalidraw/diagram-types/snowflake-schema.md:58-59`

**Issue:** `snowflake-schema.md` Step 2 states:

> Indent each child sub-table **+60px x** and **~40px y-step** relative to its parent, exactly as `kb/tree-hierarchy.md` specifies.

The `kb/tree-hierarchy.md` confirms a 40-48px y-step between siblings. However the canonical ground truth example `snowflake_schema.excalidraw` places all three normalized boxes (`dim_product_box`, `dim_category_box`, `dim_dept_box`) at **identical y=160** — a y-step of zero. Any future author following the recipe text will produce a vertically staggered chain that does not match the rendered ground truth PNG (`snowflake_schema.png`), and any author imitating the example JSON will ignore the written rule. This is a direct contradiction between the spec and the ground truth — the two authoritative sources disagree.

The recipe text is either wrong (the real design is a horizontal chain, not a vertically descending one), or the example JSON is wrong (it should stagger y by 40px per level). One must be treated as authoritative and the other corrected.

**Fix (option A — recipe was wrong, example is correct):** Change the recipe text in `snowflake-schema.md` to state that normalized sub-tables are laid out as a horizontal chain (same y, x-step = box_width + 60px gap) rather than a vertical indent:

```markdown
- **Indent** each child sub-table by adding `box_width + 60px` to its x-coordinate (same y as
  the parent dimension), forming a horizontal chain. This adapts the tree-hierarchy x-indent rule
  to full compartmented boxes: the 60px gap between box edges is the visible separation.
```

**Fix (option B — example was wrong, recipe is correct):** Apply the 40px y-step in the excalidraw JSON, placing `dim_category_box` at y=200 and `dim_dept_box` at y=240, then re-render the canonical PNG.

Pick one option and apply it consistently. The recipe and example must agree.

---

## Warnings

### WR-01: Four KB files missing `snowflake-schema` in `Used by types:` back-references

**Files:**
- `.claude/agents/excalidraw/kb/fan-out.md:3`
- `.claude/agents/excalidraw/kb/convergence.md:3`
- `.claude/agents/excalidraw/kb/evidence-card.md:3`
- `.claude/agents/excalidraw/kb/group-container.md:3`

**Issue:** The `README.md` policy states: "each composed primitive carries a `> Used by types:` back-ref so the two-layer link stays bidirectional." `snowflake-schema.md` explicitly composes `star-schema.md` (line 4: "Builds on `star-schema.md`"), and `star-schema.md` directly composes `fan-out.md`, `convergence.md`, `evidence-card.md`, and `group-container.md`. Whether back-refs should be transitive is unspecified in the README, but the net effect is that the four KB files above have no pointer to `snowflake-schema` despite it using those primitives (through the star base). This makes it impossible to find all uses of those primitives by following back-refs alone.

For comparison, `linear-pipeline.md` and `tree-hierarchy.md` correctly list `snowflake-schema` in their back-refs even though their use is also indirect via the "composes" chain.

**Fix:** Add `snowflake-schema` to the `> Used by types:` line in each of the four files:

```markdown
> Used by types: tech-architecture, star-schema, snowflake-schema
```

(for `fan-out.md`, `convergence.md`, `group-container.md`; same pattern for `evidence-card.md` which currently omits `snowflake-schema` entirely).

---

### WR-02: `tree_prod_to_cat` has collinear intermediate point — redundant midpoint in elbow arrow

**File:** `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw:2051`

**Issue:** The `tree_prod_to_cat` arrow has points `[[0,0],[30,0],[60,0]]`. All three points are on the same horizontal line (y=0 in local coordinates). The midpoint `[30,0]` is collinear with both endpoints, adding no geometric information. An elbow arrow with three collinear points is effectively a straight two-point arrow with an unnecessary waypoint. Some Excalidraw versions may treat the intermediate point as a forced bend location, causing unexpected re-routing when the diagram is resized or exported. The canonical skeleton for a straight tree connector should use exactly two points: `[[0,0],[60,0]]`.

**Fix:**
```json
"points": [[0, 0], [60, 0]]
```

---

### WR-03: `dim_date` column name differs between star and snowflake examples — ambiguous ground truth

**Files:**
- `.claude/agents/excalidraw/examples_excalidraw/star_schema_v2.excalidraw:532` — `"text": "full_date"`
- `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw:503` — `"text": "date"`

**Issue:** Both examples represent the same `dim_date` dimension table in a Sales data model. In `star_schema_v2.excalidraw` the second row is `full_date`; in `snowflake_schema.excalidraw` the same row is `date`. Since `snowflake-schema.md` states "reuses the star schema's compartmented-box geometry VERBATIM" and the star base is meant to be inherited unchanged, the `dim_date` table in the snowflake example should use the same column set as in the star example. The discrepancy creates two conflicting ground truths for what `dim_date` contains, which authors will notice when reading both examples side-by-side.

**Fix:** Align the snowflake `dim_date` row 2 to match the star example:

```json
"text": "full_date",
"originalText": "full_date"
```

(The element width 80px accommodates `full_date` at 9 chars × 9.6px = 86.4px — this would require bumping width to 100 to pass the overflow check; alternatively use the existing element width of 80 and rename back to `date` in the star example if `date` is the preferred name.)

---

### WR-04: Resolver table omits `compartmented-box` from snowflake-schema's composed set

**File:** `.claude/agents/excalidraw/diagram-types/README.md:22`

**Issue:** The resolver table row for `snowflake-schema` lists its composed KB sub-patterns as "star's set + tree-hierarchy + linear-pipeline". `compartmented-box.md` is not a KB primitive (it lives in `diagram-types/`, not `kb/`) but it is the shared construction that governs all box geometry for both star and snowflake — including the locked offsets (header 40, row pitch 20, left-pad 12, fontSize 16) and the box-width formula that drives the verifier's `text_overflow_static` check. Its absence from the resolver summary means the command and specialist could load a type recipe and miss the offset constraints entirely. The `tech-architecture` row similarly omits it, but that type does not use compartmented boxes; for data-modeling types the omission is more consequential.

**Fix:** Add a note to the snowflake-schema resolver row (and the star-schema row) that `compartmented-box.md` (shared construction) also applies:

```markdown
| Data Modeling | snowflake-schema | `snowflake-schema.md` | star's set + tree-hierarchy + linear-pipeline; shared construction: `compartmented-box.md` | `../examples/snowflake_schema.png` |
```

---

## Info

### IN-01: `dim_dept_box` element id does not match the title text `dim_department`

**File:** `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw:1577`

**Issue:** The rectangle element for the department table has `"id": "dim_dept_box"` and its associated group id is `"grp_dim_dept"`, but its title text reads `"dim_department"`. All other boxes in the file have element ids that directly mirror the table name (e.g., `dim_product_box` / `"dim_product"`, `dim_category_box` / `"dim_category"`). The inconsistency is not a rendering defect, but it makes cross-referencing between element ids and table names harder for authors and scripts that look up boxes by id.

**Fix:** Either rename the element id to `"dim_department_box"` and the group id to `"grp_dim_department"` for consistency, or change the title text to `"dim_dept"` to match the id convention. The latter is simpler since it also reduces the title char count (from 14 to 8), relaxing the width constraint.

---

### IN-02: `snowflake-schema.md` describes y-step from `tree-hierarchy.md` as "exactly as `kb/tree-hierarchy.md` specifies" but tree-hierarchy geometry targets icon+label nodes, not compartmented boxes

**File:** `.claude/agents/excalidraw/diagram-types/snowflake-schema.md:59`

**Issue:** `kb/tree-hierarchy.md` defines its geometry for "icon (24×24) + label text" nodes — small lightweight elements. Its `+60px x` indent and `40px` y-step assume nodes of roughly 24px width, not compartmented boxes that may be 160–260px wide. The instruction to follow tree-hierarchy geometry "exactly" is misleading because the compartmented boxes in a snowflake schema are architecturally different elements than the folder-icon nodes the KB pattern was designed for. The phrase "exactly as `kb/tree-hierarchy.md` specifies" over-promises precision it cannot deliver without adaptation. This connects directly to CR-02: the y-step adaptation needed for compartmented boxes is not captured anywhere in the recipe.

**Fix:** Add a note in `snowflake-schema.md` Step 2 that the tree-hierarchy x-indent must be adapted for full-width compartmented boxes:

```markdown
> **Adaptation note:** `kb/tree-hierarchy.md` targets lightweight icon+label nodes. For
> compartmented boxes, the effective x-step is `box_width + 60px` (not a literal 60px
> node-to-node indent). The y-step rule applies unchanged: stagger each child ~40px below
> its parent, or use a horizontal chain if diagram space is constrained.
```

---

_Reviewed: 2026-06-07T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
