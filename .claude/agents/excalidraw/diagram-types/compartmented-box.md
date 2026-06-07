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

## Finalized parametric offsets (locked — reused by every compartmented type)

The exact parametric offsets below are **FINALIZED** — they are no longer deferred.
They were proven against the frozen `validate_and_render.sh` + `excalidraw_verifier`
loop by the first compartmented type to ship (star-schema). Every later compartmented
type — snowflake, ER, class, data-vault — references these numbers **verbatim** and does
NOT re-derive them. A change here propagates to every type.

| Offset | Locked value | Meaning |
|--------|--------------|---------|
| **Header height** | **40px** | The header (title) compartment is 40px tall. The header divider sits at `box.y + 40`. |
| **Row pitch** | **20px** | Vertical spacing between successive row texts (the row pitch, and divider Y step). On the 20-grid. |
| **Left-pad** | **12px** | Every title text and every row text uses left x = `box.x + 12`. A per-element inset; the only value not on the 20-grid. |
| **fontSize** | **16** | All title and row texts use `fontSize: 16` with `fontFamily: 3` (monospace). |

**Derived placement formulas (use these exactly):**

- **Header divider Y** = `box.y + 40` (header height). `x == box.x`, `points = [[0,0],[width,0]]`.
- **Title text** at `x = box.x + 12`, `y = box.y + 10` (vertically inset inside the 40px header).
- **First row text** at `x = box.x + 12`, `y = box.y + 50` (10px below the header divider).
- **Row i (1-based)** at `y = box.y + 40 + 10 + (i-1) * 20` — i.e. first row 50, then +20 per row.
- **Between-row dividers** (optional, for grouped sections) land on `box.y + 40 + 20*k` — a
  20-grid Y that sits ON a row boundary and never bisects a row.
- **Box width rule (PASSES `text_overflow_static`):**
  `box.width >= max_over_rows(len(row.text) * 0.6 * fontSize)`, rounded **UP** to the next
  20-grid value. At `fontSize:16` that is `9.6px` per character; size the box to the LONGEST
  row, then round up. (The verifier estimates text width as `len(text)*0.6*fontSize` and
  flags an `error` if it exceeds the enclosing rectangle's width — author TO this formula.)
- **Box height** = `40 (header) + rows*20 + 10` bottom-pad, rounded up to the 20-grid.

These offsets are FINALIZED (no longer deferred). The alignment rules above (common left x,
full-width dividers `x==box.x` and `points[-1][0]==box.width`, 20-grid) and the HARD
prohibition on multi-line single text remain in force and are NOT weakened by this section.
