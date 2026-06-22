# Diagram Type: Snowflake Schema

> Layer: TYPE recipe. Composes primitives from [`../patterns/`](../patterns/README.md) and the shared [`compartmented-box.md`](./compartmented-box.md) construction; does not re-derive their geometry. Indexed in [`README.md`](./README.md). Builds on [`star-schema.md`](./star-schema.md).

## Purpose

A **Snowflake Schema** is a normalized variant of the star schema: it is a star where one
or more dimension tables are **decomposed into a hierarchy of normalized sub-tables**. For
example, `dim_product` might split into `dim_product → dim_category → dim_department`,
each sub-table holding only the attributes at that level of granularity.

Use snowflake instead of star when dimension attributes themselves have a meaningful
**parent → child** structure worth separating into distinct tables (e.g. product belongs
to a category, which belongs to a department). This eliminates redundancy in the dimension
tables at the cost of additional joins. The diagram makes the normalization hierarchy
explicit by showing the sub-table chain as an indented tree branching off the original
dimension box.

Reach for this type when a request is about: a normalized OLAP warehouse model, a
"dimension decomposed into lookup chains" schema, or any star schema whose dimension
attributes have a natural multi-level parent→child hierarchy worth expressing visually.

## How to draw it

Snowflake **reuses the star schema's compartmented-box geometry VERBATIM** — do not
re-derive any box offset numbers. All parametric offsets (header height 40, row pitch 20,
left-pad 12, fontSize 16, box-width rule `len*0.6*16`) are locked in
[`@./compartmented-box.md`](./compartmented-box.md) and inherited from
[`@./star-schema.md`](./star-schema.md). Only the **normalized dimension extension** is
added on top via [`@../patterns/tree-hierarchy.md`](../patterns/tree-hierarchy.md).

### Step 1 — Build the star base (unchanged from star-schema)

Assemble the fact box and the kept dimension boxes exactly as documented in
[`@./star-schema.md`](./star-schema.md):

- Each table (fact and every dimension) is a **compartmented box** per
  [`@./compartmented-box.md`](./compartmented-box.md): sharp rectangle (`roundness: null`,
  `roughness: 0`), full-width `line` header divider (`x == box.x`,
  `points = [[0,0],[width,0]]`), one title text bound via `containerId`, and N
  free-floating per-row monospace texts (`fontFamily: 3`, `fontSize: 16`). One `groupIds`
  id per box. No multi-line text elements.
- Place the fact box centrally; fan non-normalized dimensions around it with bound elbow
  arrows per the fan-out primitive (`endArrowhead: "arrow"`, anchored to the box rectangle
  borders — never to row texts or line dividers).

### Step 2 — Normalize one or more dimensions into a sub-table chain

Select the dimension(s) to normalize (e.g. `dim_product`) and replace each with a
**tree-hierarchy of smaller compartmented boxes** per
[`@../patterns/tree-hierarchy.md`](../patterns/tree-hierarchy.md):

- **Sub-table boxes** use the **same compartmented-box recipe** as the parent dimension —
  the same sharp rectangle, same line header divider, same left-pad 12, same fontSize 16.
  They are smaller because they hold fewer rows (only the attributes at that normalization
  level), but their box style is identical. Do NOT use a different-looking box for
  sub-tables.
- **Indent** each child sub-table **+60px x** and **~40px y-step** relative to its parent,
  exactly as `kb/tree-hierarchy.md` specifies.
- **Connect** parent → child sub-tables with **thin elbow arrows** (`strokeWidth: 1.5`,
  `elbowed: true`, `roundness: null`, `endArrowhead: "arrow"`), anchored to the sub-box
  **RECTANGLE borders** (never to texts or line dividers). These are plain association
  arrows, not crow's-foot — the legal arrowhead set is `arrow|bar|dot|triangle|null`.

### Binding rules (same as star — LOCKED)

- `endArrowhead: "arrow"` only on all connectors (fact→dim fan-out and dim→sub-table tree
  elbows). No `crowsfoot`/`diamond`/`hollow` tokens — they render silently as bare lines.
- Every arrow's start and end points must land within 8px of a **rectangle** border. Bind
  via `startBinding`/`endBinding` to the box rectangle ids.
- All boxes (fact, dimensions, sub-tables): `roundness: null`, `roughness: 0`, one shared
  `groupIds` per box.

## Composes (primitive layer)

- [`@./star-schema.md`](./star-schema.md) — the star base: fact box + kept dimensions +
  fan-out connectors. Snowflake is this composed set, extended.
- [`@./compartmented-box.md`](./compartmented-box.md) — the finalized parametric offsets
  (header 40, row pitch 20, left-pad 12, fontSize 16) used verbatim by every box —
  fact, dimension, and normalized sub-tables alike.
- [`@../patterns/tree-hierarchy.md`](../patterns/tree-hierarchy.md) — the normalized dimension
  sub-table layout: children indent +60px x, ~40px y-step, thin (`strokeWidth: 1.5`)
  elbow connectors anchored to sub-box RECTANGLE borders.
- [`@../patterns/linear-pipeline.md`](../patterns/linear-pipeline.md) — optional sequential read
  path across the normalization chain.

## Ground truth

- [`./snowflake_schema.png`](./snowflake_schema.png) — the canonical
  Snowflake Schema reference: a Sales star with `dim_product` normalized into a
  `dim_product → dim_category → dim_department` tree-hierarchy of three smaller
  compartmented boxes. Every box (fact, kept dimensions, and sub-tables) uses the same
  locked compartmented-box recipe; sub-tables are connected by thin elbow arrows indented
  per `tree-hierarchy`. Imitate its normalization layout and consistent box geometry.
