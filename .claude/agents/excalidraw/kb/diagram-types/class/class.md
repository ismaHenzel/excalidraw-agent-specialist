# Diagram Type: UML Class

> Layer: TYPE recipe. Composes primitives from [`../../patterns/`](../../patterns/README.md) and the shared [`compartmented-box.md`](../compartmented-box.md) construction; does not re-derive their geometry. Indexed in [`README.md`](../README.md).

## Purpose

A **UML Class Diagram** models the static structure of a system by showing its **classes**
(each with a name, attributes, and operations), the structural **relationships** among them
(association, dependency, generalization, realization, aggregation, composition), and
optional **stereotypes** that annotate special roles (`«interface»`, `«abstract»`,
`«service»`, etc.).

Use a class diagram when a request is about: object-oriented design, domain modeling,
class hierarchies and inheritance, interfaces and implementations, ownership relationships
(whole-part aggregation or tight-coupling composition), or any structural blueprint where
classes and their relationships are the primary concern.

## How to draw it

Class boxes **reuse the compartmented-box construction VERBATIM** — do not re-derive any
box offset numbers. All parametric offsets (header height 40, row pitch 20, left-pad 12,
fontSize 16, box-width rule `len*0.6*16`) are locked in
[`@../compartmented-box.md`](../compartmented-box.md). Only the class-specific extensions
are added on top, as described below.

### Step 1 — Build each class box (three compartments)

Each class box is the **compartmented-box construction** with **THREE compartments**:

1. **Title compartment** (40px header, same as star/snowflake/ER) — the class name, with
   an optional stereotype text in guillemets above or below it.
2. **Attributes compartment** — attribute rows (`- name: Type`, etc.).
3. **Methods compartment** — operation rows (`+ method(): ReturnType`, etc.).

The three-compartment extension adds **exactly ONE extra full-width `line` divider** at
`box.y + 40 + 20*k` where `k` is the number of attribute rows — i.e. the second divider
sits on the row boundary immediately after the last attribute row, per
`@../compartmented-box.md` "Between-row dividers". The first divider (header divider) is at
`box.y + 40`, unchanged from all other compartmented types.

All offsets are inherited verbatim from `@../compartmented-box.md` (INT-02):

| Offset | Locked value |
|--------|--------------|
| Header height | 40px (`header divider Y = box.y + 40`) |
| Row pitch | 20px (each attribute or method row is +20px) |
| Left-pad | 12px (every row text: `x = box.x + 12`) |
| fontSize | 16 (`fontFamily: 3` monospace) |
| Second divider Y | `box.y + 40 + 20*k` (k = number of attribute rows) |

Box width must satisfy `box.width >= max_over_rows(len(row.text) * 0.6 * 16)` rounded UP
to the next 20-grid value so `text_overflow_static` passes. Box height =
`40 (header) + k_attrs*20 + k_methods*20 + 10` bottom-pad, rounded up to the 20-grid.

All elements of a box (the rectangle frame, both line dividers, the title text, and every
row text) share ONE `groupIds` id.

### Step 2 — Attribute and method rows

Every attribute row and every method row is a **separate `text` element** — one `text` per
row, `fontFamily: 3`, `fontSize: 16`. **Never pack multiple rows into a single multi-line
text element using `\n`** (Pitfall — violates the HARD prohibition in
`@../compartmented-box.md`).

Visibility markers use **ASCII**: `+` (public), `-` (private), `#` (protected). **Never
use lock/key emoji or any Unicode emoji character as a visibility prefix** — raw Unicode
emoji render as missing-glyph boxes under `fontFamily: 3` (Pitfall 5, structural verifier
rejects them).

### Step 3 — Stereotypes via guillemets

Stereotypes are authored with `«»` guillemets (e.g. `«interface»`, `«abstract»`,
`«service»`) as a monospace `text` element in the title compartment, above or inline with
the class name. These are NOT emoji and are confirmed safe under `fontFamily: 3`
(Assumption A1). If `«»` guillemets render as tofu/missing-glyph boxes in a specific
environment, fall back to ASCII `<<interface>>` and document the fallback.

### Step 4 — Relationship glyph set

The full UML class relationship set comes **exclusively** from `@../notation-conventions.md`
(the legal-encoding table, DTKB-04) and `@../../patterns/relationship-endpoint.md` (the exact
diamond/triangle glyph geometry and grouping mechanics). Do not invent new tokens.

| Relationship | Committed encoding |
|---|---|
| **Association** | `endArrowhead: "arrow"`, `strokeStyle: "solid"` |
| **Dependency** | `endArrowhead: "arrow"`, `strokeStyle: "dashed"` |
| **Generalization** (inheritance) | `endArrowhead: "triangle"`, `strokeStyle: "solid"` — FILLED (house convention: Excalidraw has no hollow-triangle token; surface to user: "inheritance shown as a filled triangle") |
| **Realization** (implements) | `endArrowhead: "triangle"`, `strokeStyle: "dashed"` |
| **Aggregation** | A ~14px `diamond` element at the OWNER end, `backgroundColor: "#ffffff"`, `fillStyle: "solid"` (white, hollow-looking diamond) — see Step 5 |
| **Composition** | A ~14px `diamond` element at the OWNER end, `backgroundColor: "#1e1e1e"`, `fillStyle: "solid"` (solid dark diamond) — see Step 5 |

Legal arrowhead tokens are **only**: `arrow | bar | dot | triangle | null`. The tokens
`crowsfoot`, `diamond`, `hollow`, and `open` are **illegal** — they render silently as
plain bare lines (Pitfall 1). Encode aggregation/composition via the composed diamond
described in Step 5, never via an `"diamond"` arrowhead token.

### Step 5 — Composition-glyph-over-anchored-connector rule (Pattern 3 / Pitfall 2)

For aggregation and composition, the connector and the diamond glyph are **two separate
elements** sharing the same `groupIds` id:

1. **Connector arrow** — `type: "arrow"`, `elbowed: true`, `roundness: null`. Its
   `startBinding` and `endBinding` point to the **box RECTANGLE ids** (gap 4), NOT to
   the diamond element. This keeps the arrow endpoint anchored to the box border so
   `check_arrow_endpoint_unanchored` passes green.

2. **Diamond glyph** — `type: "diamond"`, `width: 14`, `height: 14`, `roundness: null`,
   `roughness: 0`. Placed overlaid at the OWNER end of the connector (centered on the
   connector line where it meets the owner box border). The glyph shares the connector's
   `groupIds` id so it travels with the connector when the diagram is repositioned.

**Do NOT** terminate the connector at the diamond glyph. If the arrow endpoint is placed
on the tiny 14px diamond rather than on the box rectangle border, the structural verifier
raises an `arrow_endpoint_unanchored` error because the glyph is offset from the box
border by more than the 8px tolerance.

```
box rectangle  <--[arrow endpoint anchored here]---[diamond overlaid, same groupId]
```

### Step 6 — Connector binding rules (ALL connectors)

- Every connector: `elbowed: true`, `roundness: null`, orthogonal points.
- `startBinding` / `endBinding` bind to **box RECTANGLE ids** (never to row texts or
  line dividers). Use `gap: 4`.
- Legal arrowhead tokens: `arrow | bar | dot | triangle | null` only. See Step 4.

## Composes (primitive layer)

- [`@../compartmented-box.md`](../compartmented-box.md) — the finalized parametric offsets
  (header 40, row pitch 20, left-pad 12, fontSize 16) and the HARD no-multi-line-text
  rule; the extra full-width line divider at `box.y + 40 + 20*k` is the "Between-row
  dividers" case documented there. Do NOT re-derive these offsets.
- [`@../../patterns/relationship-endpoint.md`](../../patterns/relationship-endpoint.md) — the diamond/triangle/dashed
  glyph geometry (diamond: 14x14px, white `#ffffff` for aggregation, solid `#1e1e1e` for
  composition; triangle arrowhead conventions; grouping mechanics for Pattern 3). Do NOT
  re-derive glyph pixel values.
- [`@../notation-conventions.md`](../notation-conventions.md) — the one binding legal-encoding
  table for every notation (which token, which glyph, which dashed/solid stroke), the five
  legal arrowhead tokens, and the guillemet stereotype convention. Do NOT re-derive or
  override these conventions.

## Ground truth

- [`./class_order_domain.png`](./class_order_domain.png) — the canonical
  UML Class Diagram reference: an order-management domain showing `Order`, `OrderLine`,
  `Customer`, and a `«Payable»` interface (or `PaymentMethod` abstraction). Each class box
  has three compartments (title + attributes + methods) with ASCII visibility markers and
  monospace rows. Relationships include a filled-triangle generalization, a dashed-triangle
  realization, a solid-diamond composition, a white-diamond aggregation, and a plain
  association arrow. Imitate its compartment layout, glyph anchoring, and relationship
  variety.
