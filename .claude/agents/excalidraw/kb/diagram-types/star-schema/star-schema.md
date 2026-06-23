# Diagram Type: Star Schema

> Layer: TYPE recipe. Composes primitives from [`../../patterns/`](../../patterns/README.md) and the shared [`compartmented-box.md`](../compartmented-box.md) construction; does not re-derive their geometry. Indexed in [`README.md`](../README.md).

## Purpose

A **Star Schema** is the canonical dimensional data model: one central **fact table**
surrounded by, and fanned out to, several **dimension tables**. The fact table holds the
foreign keys (one per dimension) plus the numeric measures; each dimension table holds the
descriptive attributes that give those facts context. Drawn out, the fact box sits in the
middle and the dimension boxes radiate around it like the points of a star — hence the name.

Reach for this type when a request is about: a dimensional / OLAP warehouse model, a
"fact-and-dimensions" reporting schema, a BI star, or any "central measurements table joined
to lookup tables" design. Use the normalized **snowflake-schema** variant instead when a
dimension must be decomposed into a sub-hierarchy of normalized tables.

## How to draw it

Assemble the diagram from the composed primitives below — do not improvise coordinate math
here; defer all box geometry to [`compartmented-box.md`](../compartmented-box.md) and all
connector geometry to [`@../../patterns/fan-out.md`](../../patterns/fan-out.md).

- **Build every table as a compartmented box.** Each fact and dimension table is a
  *compartmented box* per [`@../compartmented-box.md`](../compartmented-box.md):
  a SHARP rectangle (`roundness: null`, `roughness: 0`), a **full-width horizontal `line`
  header divider** (`x == box.x`, `points = [[0,0],[width,0]]` so `points[-1][0] == box.width`
  exactly), one title text bound to the box, and **N free-floating per-row monospace texts**
  (`fontFamily: 3`, `fontSize: 16`) — one `text` element per column, never a multi-line block.
  Apply the **finalized offsets verbatim**: header height 40, row pitch 20, left-pad 12
  (every row x = `box.x + 12`), and `box.width >= max_over_rows(len(row.text) * 0.6 * 16)`
  rounded up to the 20-grid. Every element of a box shares ONE `groupIds` id.
- **Place the fact box centrally, dimensions fanned around it.** The central fact box lists
  the dimension foreign keys (e.g. `date_key   FK`) and the measures (e.g. `quantity`,
  `unit_price`); the dimension boxes radiate around it.
- **Wire fact → dimension with the fan-out primitive.** Use the
  [`@../../patterns/fan-out.md`](../../patterns/fan-out.md) dispatch geometry for the fact-to-dimension
  connectors — one source (the fact) to N destinations (the dimensions). Connectors are
  bound elbow arrows (`elbowed: true`, `roundness: null`, `>=3` points). Never re-derive the
  arrow coordinate math here.

## Binding rules (LOCKED)

- **Arrowhead.** Connectors use `endArrowhead: "arrow"` only (a plain association; DTKB-04).
  Never use `crowsfoot`/`diamond`/`hollow` — those tokens render silently as a bare line.
- **Anchor to the box RECTANGLE border.** Every arrow's start/end point must land within 8px
  of a **rectangle** border, and arrows should bind via `startBinding`/`endBinding` to the box
  rectangle ids. **Never** anchor an arrow to a row `text` or to a `line` divider — those are
  not in the verifier's anchorable shape set, so an arrow ending there reads as unanchored.
- **Sharp + grouped.** Boxes use `roundness: null` (sharp corners, never `{type:3}`), and
  every element of a single box (rectangle, header divider, title, all rows) shares one
  `groupIds` id so the box places and moves as a unit.

## Composes (primitive layer)

- [`@../compartmented-box.md`](../compartmented-box.md) — the shared table-box construction +
  the finalized parametric offsets every fact/dimension box uses.
- [`@../../patterns/fan-out.md`](../../patterns/fan-out.md) — one source (fact) dispatching to N destinations
  (dimension tables); the fact-to-dimension connector geometry.
- [`@../../patterns/convergence.md`](../../patterns/convergence.md) — the mirror of fan-out, for reading the
  schema in the "dimensions feed the fact" direction.
- [`@../../patterns/evidence-card.md`](../../patterns/evidence-card.md) — an optional real-data card (a row
  count, a sample measure) attached beside the model to make it argue, not just display.
- [`@../../patterns/group-container.md`](../../patterns/group-container.md) — an optional bordered scope around
  the whole schema (e.g. "Sales mart").

## Ground truth

- [`./star_schema_v2.png`](./star_schema_v2.png) — the canonical compliant
  Star Schema reference: a central `fact_sales` box fanned out to `dim_date`, `dim_product`,
  `dim_customer`, and `dim_store`, each a grouped sharp box with a full-width `line` header
  divider and per-row monospace text. Imitate its grouped/bound/sharp compartmented-box
  composition — NOT the grandfathered legacy `star_schema.excalidraw` (ungrouped, soft,
  unbound), which is explicitly not a safe template.
