# Compartmented Box — Reusable Construction (INT-02)

This file documents, ONCE, the single reusable construction that every compartmented
diagram type composes: UML class boxes, ER entity boxes, and star / snowflake /
data-vault table boxes. Later type files REFERENCE this construction rather than
re-deriving it, so the recipe stays consistent and a fix here propagates everywhere.

## The construction (four element kinds, one group)

A compartmented box is assembled from these elements, and ALL of them live in a single
`groupIds` group so the box translates and places as one unit:

1. **One sharp rectangle** — the box outline. `roundness: null` (sharp corners; never a
   soft/rounded box for formal notation). This is the container frame.
2. **Horizontal line dividers** — one `line` element per compartment boundary, each
   spanning the FULL box width (header divider, attribute/method divider, etc.).
3. **One title text** — a single bound/centered `text` for the box name, centered in the
   header compartment.
4. **N separate free-floating row texts** — one `text` element PER attribute/column/row,
   left-aligned, in monospace (`fontFamily: 3`) so columns line up. Each row is its own
   element; there is exactly one row string per text element.

The `strokeStyle` on dividers and frame stays solid unless a type recipe says otherwise.

## HARD prohibition: no multi-line single text blocks

**Multi-line single `text` blocks — a single `text` element whose string contains `\n`
to pack several rows — are DISALLOWED for compartments. This is a binding rule, never
an exception for formal boxes.** Packing rows into one multi-line text:

- defeats divider placement — there is no per-row boundary to draw a `line` between, and
- breaks the verifier's per-element width-fit check, which measures one width per
  element; a multi-line block's true width is its widest row, so a long row silently
  overflows the box (Pitfall 2).

Each row is ALWAYS its own separate `text` element. A multi-line text is only ever
acceptable for a throwaway free note block, never for a compartmented box.

## Alignment rules (Pitfall 3)

- **Rows share a common left x.** Every row `text` uses the same left x = `box.x + pad`;
  their x values must all match (no column drift).
- **Dividers span the full width.** Each divider `line`'s x-range MUST equal the box's
  x-range — from `box.x` to `box.x + width` exactly. A divider that stops short of the
  border, or overruns it, is a defect.
- **20-grid coordinates.** All coordinates are multiples of 20 (the house grid rule).
- **Row pitch is a multiple of 20.** Vertical spacing between rows, and the header
  height, are multiples of 20 so divider Y values land on grid and never bisect a row.

## Grouping is mandatory

The box MUST be GROUPED via `groupIds` (frame + dividers + title + every row text share
one group id) so it can be placed, translated, and nudged as a unit without the dividers
desyncing from the rows. The legacy `star_schema.excalidraw` is NOT a safe template for
this construction: it uses **0 `groupIds`**, free-floating unbound text, and soft
`roundness`, directly contradicting this recipe. Do not copy its structure.

## Scope of this file

This file fixes the CONSTRUCTION and the alignment RULES. The exact PARAMETRIC OFFSETS —
header height, the specific row-pitch number, divider Y formulas, left-pad value — are
finalized in Phase 6 (the first compartmented type to ship). Later type files reference
those finalized offsets and this construction rather than re-deriving the geometry.
