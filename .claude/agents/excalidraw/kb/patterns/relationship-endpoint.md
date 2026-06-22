# Pattern: Relationship Endpoint Glyphs

> Used by types: er, class

Shared primitive for all composed relationship-endpoint glyphs used in ER diagrams and
UML class diagrams: diamond (aggregation/composition), ellipse (ER optional endpoint),
triangle (generalization/realization), bar/dot (ER cardinality), and textual multiplicity
labels. Authors of `er.md` and `class.md` `@`-reference this file for geometry and
JSON skeletons rather than re-deriving them.

The convention table itself is locked in
`@../diagram-types/notation-conventions.md` (DTKB-04). The box offsets (compartment
header height, row pitch, left-pad) are locked in `@../diagram-types/compartmented-box.md`
(INT-02). Do NOT re-derive either here.

## When to use

Use this primitive whenever an ER entity or UML class relationship requires an endpoint
marker — any cardinality notation, an aggregation/composition diamond, a
generalization/realization triangle, or a dependency/association arrowhead. This covers
every arrow drawn in both diagram types.

## Legal arrowhead tokens

Excalidraw 0.17.3 exposes **exactly five** arrowhead values. Any other token renders
**silently as a bare line** — no error, no warning (Pitfall 1 in RESEARCH.md):

    arrow | bar | dot | triangle | null

Tokens that are ILLEGAL and must NEVER appear in authored JSON:

    crowsfoot  diamond  hollow  open  (and any other invented name)

The Phase-1 validator (`excalidraw_validator.py`) rejects any `startArrowhead` or
`endArrowhead` outside the legal set, exiting with code 1. Do not attempt to use
illegal tokens as workarounds — use the composed-glyph recipes below instead.

## Geometry

### Diamond glyph (aggregation / composition)

- **Element type:** `diamond`
- **Width:** 14px, **Height:** 14px
- **Placement:** Overlaid at the OWNER end of the connector, centered on the connector
  line at the point where it meets the box border.
- **Offset:** x and y adjusted so the diamond center sits at the connector's owner-end
  endpoint. Keep to the 20-grid where the owner box corner allows; the 14px glyph may
  fall off-grid (acceptable — the box anchor is on-grid).
- **Aggregation fill:** `backgroundColor: "#ffffff"`, `fillStyle: "solid"` (white, open diamond).
- **Composition fill:** `backgroundColor: "#1e1e1e"`, `fillStyle: "solid"` (dark solid diamond).
- `roundness: null` on the glyph element.

### Ellipse glyph (ER "zero / optional" alternative endpoint)

- **Element type:** `ellipse`
- **Width:** 10px, **Height:** 10px (small, sits at the endpoint)
- **Placement:** At the "optional" end of the ER connector, centered on the line.
- Use only when the `dot` arrowhead (`endArrowhead: "dot"`) is insufficient for
  visual clarity. In most cases `dot` is preferred (no extra element).

### Textual multiplicity label (ER "many")

- **Element type:** `text`
- **Text values:** `0..*`, `1..*`, `1`, `0..1`
- **Font:** `fontFamily: 3` (Cascadia monospace), `fontSize: 16`
- **Placement offset:** Place along the connector line, OUTSIDE every box bounding box.
  Typically 20-40px from the endpoint, on the 20-grid.
- **Critical:** Do NOT place inside any box bbox — `text_overflow_static` will treat
  the label as an overflowing row (Pitfall 3 in RESEARCH.md). Keep labels in clear
  connector-corridor space.
- **strokeColor:** `"#1e1e1e"` (high-contrast, passes verifier check).

### Anchoring rule (Pattern 3 — glyph grouped on an anchored connector)

The connector `arrow` MUST bind/anchor to the **rectangle** box border (via
`startBinding`/`endBinding`). The composed glyph (diamond/ellipse) is a SEPARATE element
placed over the owner end and joined to the connector's `groupIds` so it travels with the
connector. This ensures `check_arrow_endpoint_unanchored` passes — the arrow endpoint
lands on the box rectangle, not on the tiny glyph.

```
box rectangle  <--[arrow endpoint anchored here]---[diamond overlaid, same groupId]
```

If you terminate the connector at the diamond instead of the box, the structural verifier
will raise `arrow_endpoint_unanchored` error because the glyph is offset from the box
border by more than the 8px tolerance.

## JSON skeleton

### ER "one" end

```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"bar","startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<entity_a_id>","gap":4},
  "endBinding":{"elementId":"<entity_b_id>","gap":4},
  "groupIds":["<rel_id>"] }
```

### ER "zero / optional" end (dot arrowhead — preferred)

```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"dot","startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<entity_a_id>","gap":4},
  "endBinding":{"elementId":"<entity_b_id>","gap":4},
  "groupIds":["<rel_id>"] }
```

### ER "many" (textual multiplicity — NO arrowhead glyph)

```jsonc
// Connector: endArrowhead null (no glyph — the label carries the semantic)
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":null,"startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<entity_a_id>","gap":4},
  "endBinding":{"elementId":"<entity_b_id>","gap":4},
  "groupIds":["<rel_id>"] }

// Textual multiplicity label — OUTSIDE all box bboxes:
{ "type":"text","text":"0..*","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":<on-grid-x>,"y":<on-grid-y> }
```

### UML aggregation (white-fill diamond at owner end)

```jsonc
// Connector anchors to the PART box (not to the diamond):
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":null,"startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<class_part_id>","gap":4},
  "endBinding":{"elementId":"<class_whole_id>","gap":4},
  "groupIds":["<rel_id>"] }

// Diamond overlaid at the WHOLE (owner) end, same group:
{ "type":"diamond","width":14,"height":14,"roundness":null,"roughness":0,
  "backgroundColor":"#ffffff","fillStyle":"solid",
  "strokeColor":"#1e1e1e",
  "x":<owner_end_x - 7>,"y":<owner_end_y - 7>,
  "groupIds":["<rel_id>"] }
```

### UML composition (solid-fill diamond at owner end)

```jsonc
// Same connector as aggregation — change only the diamond fill:
{ "type":"diamond","width":14,"height":14,"roundness":null,"roughness":0,
  "backgroundColor":"#1e1e1e","fillStyle":"solid",
  "strokeColor":"#1e1e1e",
  "x":<owner_end_x - 7>,"y":<owner_end_y - 7>,
  "groupIds":["<rel_id>"] }
```

### UML generalization (inheritance — filled triangle, solid stroke)

```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"triangle","startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<subclass_id>","gap":4},
  "endBinding":{"elementId":"<superclass_id>","gap":4} }
// Note: "triangle" is FILLED (house convention — Excalidraw has no hollow-triangle token).
// Surface this to the user when relevant: "inheritance shown as a filled triangle."
```

### UML realization (implements — filled triangle, dashed stroke)

```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"triangle","startArrowhead":null,"strokeStyle":"dashed",
  "startBinding":{"elementId":"<class_id>","gap":4},
  "endBinding":{"elementId":"<interface_id>","gap":4} }
```

### UML association (plain arrow, solid stroke)

```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<src_id>","gap":4},
  "endBinding":{"elementId":"<dst_id>","gap":4} }
```

### UML dependency (arrow, dashed stroke)

```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"dashed",
  "startBinding":{"elementId":"<client_id>","gap":4},
  "endBinding":{"elementId":"<supplier_id>","gap":4} }
```

## See in examples

- `../diagram-types/er_retail_orders.png` — canonical ER example: a retail domain with `customer`, `order`, and `product` entity boxes connected by bound elbow connectors encoding explicit ER cardinality endpoints (`bar` for "one", `dot`/textual label for "optional"/"many").
- `../diagram-types/class_order_domain.png` — canonical UML Class Diagram example: an order-management domain showing `Order`, `OrderLine`, `Customer`, `PremiumCustomer`, `Discount`, and a `«Payable»` interface; exercises the full aggregation/composition white and solid diamond glyphs, generalization and realization filled-triangle arrowheads, and plain association arrow.

Both pass the full validate→render→verify loop (structural automated + EX-03 visual
human approval); resolver rows for `er` and `class` are wired in
`diagram-types/README.md` as of Phase 7.

## Notes

- **Do NOT re-derive compartmented-box offsets here.** Header height (40px), row pitch
  (20px), left-pad (12px), and the box-width formula are finalized in
  `@../diagram-types/compartmented-box.md` (INT-02). Reference that file — do not copy
  and re-state those numbers inside a type file.
- **Do NOT re-derive the convention table.** The one binding convention per notation
  (which token, which glyph) is locked in `@../diagram-types/notation-conventions.md`
  (DTKB-04). Type files embed or reference that table verbatim.
- The `elbowed: true`, `roundness: null` rule applies to ALL connectors in both types.
  Non-elbow connectors trigger `arrow_not_elbow` warnings in the structural verifier.
- Multiplicity labels use `fontFamily: 3` to match box row text and avoid mixed-font
  rendering artifacts. Keep them short (4-5 chars) and off-grid only if the 20-grid
  alignment would land them inside a box bbox.
- PK/FK row prefixes in ER entity boxes use monospace text elements with the prefix
  pattern `PK  <col>` / `FK  <col>` — never key emoji (Pitfall 5, structural verifier
  rejects raw emoji under `fontFamily: 3`).
- Stereotypes in class diagrams use guillemets (`«interface»`, `«abstract»`) — these
  are confirmed renderable under `fontFamily: 3` and are NOT emoji (confirmed in STACK.md).
