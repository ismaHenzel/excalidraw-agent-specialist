# Diagram Type: Data Vault

> Layer: TYPE recipe. Composes primitives from [`@./compartmented-box.md`](./compartmented-box.md), [`@../patterns/fan-out.md`](../patterns/fan-out.md), [`@../patterns/tree-hierarchy.md`](../patterns/tree-hierarchy.md), [`@../patterns/convergence.md`](../patterns/convergence.md), [`@../patterns/group-container.md`](../patterns/group-container.md), and [`@./notation-conventions.md`](./notation-conventions.md); does not re-derive their geometry. Indexed in [`README.md`](./README.md).

## Reuse verbatim — do not re-derive

Hub, link, and satellite boxes are the **SAME** compartmented box that star/snowflake/ER/class
already use. Reuse [`@./compartmented-box.md`](./compartmented-box.md) offsets
**VERBATIM**:

| Offset | Locked value |
|--------|-------------|
| Header height | **40px** |
| Row pitch | **20px** |
| Left-pad | **12px** |
| fontSize | **16** (`fontFamily: 3` monospace) |
| Box width rule | `max_over_rows(len*0.6*16)` rounded UP to the 20-grid |

The **only** differences between the three table classes are `backgroundColor` (the role
fill from the 3-role palette) and the mandatory role-label text — **NOT the geometry**.
Do not re-derive box offsets, divider positions, or row placement. A change in
`compartmented-box.md` propagates to all three classes here.

## Purpose

A **Data Vault** model is a pattern for building enterprise-scale historical raw vaults:
it stores every business key, relationship, and descriptive attribute separately so that
history is preserved in full and new sources integrate without destructive changes.

Three table classes form the model:

- **Hub** — the business-key table. One hub per business concept (Customer, Product, Order).
  Holds exactly the hash key, the natural business key(s), a load-date, and a record source.
  Hubs never join directly — they connect through links.
- **Link** — the relationship table. Captures an association between two or more hubs (e.g.
  an Order line links Customer + Product + Order). Contains the link hash key, a foreign hash
  key for each referenced hub, a load-date, and a record source.
- **Satellite** — the descriptive / history table. Attached to a hub or link; holds attributes
  that change over time (e.g. customer address, product price). Multiple satellites can attach
  to the same hub/link, each tracking a different attribute group or source.

Scope: **raw-vault slice only** — hub / link / satellite. Business Vault tables, PIT bridges,
and other Data Vault 2.0 constructs are out of scope for this recipe.

Reach for this type when: a request involves auditable, historized enterprise data (data
warehouse raw vault), multiple source systems feeding the same business keys, or a model that
must survive source-system changes without schema rewrites.

## How to draw it

### Step 1 — Hub boxes (the spine)

Each hub is a compartmented box per [`@./compartmented-box.md`](./compartmented-box.md):
sharp rectangle (`roundness: null`, `roughness: 0`), full-width `line` header divider
(`x == box.x`, `points = [[0,0],[width,0]]`), one title text, and per-row monospace texts
(`fontFamily: 3`, `fontSize: 16`), all sharing one `groupIds`.

**Hub role:**
- `backgroundColor: "#93c5fd"` (Tertiary blue), `strokeColor: "#1e3a5f"`
- Mandatory role label: **`«hub»`** placed in/above the header (see the 3-role palette section)
- Standard rows: `HUB_<BIZ>_HK PK`, the natural business key column(s), `LOAD_DTS`,
  `RECORD_SRC`

Width rule: `HUB_CUSTOMER_HK PK` ≈ 20 chars → `20 * 9.6 = 192` → box width ≥ 200.
Place hubs in a horizontal row (the "spine" of the vault).

### Step 2 — Link boxes

Link boxes use the **same compartmented-box construction** as hubs — sharp rectangle, same
header/row offsets, same `groupIds` discipline — but with the link role fill.

**Link role:**
- `backgroundColor: "#fed7aa"` (Start/Trigger amber), `strokeColor: "#c2410c"`
- Mandatory role label: **`«link»`** in/above the header
- Standard rows: `LINK_<REL>_HK PK`, two or more `HUB_*_HK` foreign hash keys,
  `LOAD_DTS`, `RECORD_SRC`

Place link boxes between the hubs they relate. Width driven by the longest row string.

### Step 3 — Satellite boxes

Satellite boxes use the **same compartmented-box construction**, attached to their parent
hub or link, with the satellite role fill.

**Satellite role:**
- `backgroundColor: "#fef3c7"` (Decision pale-yellow), `strokeColor: "#b45309"`
- Mandatory role label: **`«sat»`** in/above the header
- Standard rows: parent `HUB_*_HK FK` or `LINK_*_HK FK`, `LOAD_DTS PK` (history key),
  `HASH_DIFF`, descriptive attribute column(s), `RECORD_SRC`

Multiple satellites may attach to one hub/link — each tracking a distinct attribute group
or source system.

### Step 4 — Hub→link spine connectors

Connect hubs to links using plain elbow arrows. Two patterns from the composed primitives:

- **Fan-out** (`@../patterns/fan-out.md`): a hub fanning out to multiple links it participates in.
  Route through a shared vertical rail between hub and links; all arrows from the same hub
  share the rail x-coordinate.
- **Convergence** (`@../patterns/convergence.md`): two or more hubs converging into one link
  (the link holds foreign hash keys for each participating hub). Route through a shared rail.

All spine connectors: `endArrowhead: "arrow"`, `strokeWidth: 2`, `strokeColor: "#1e3a5f"`,
`elbowed: true`, `roundness: null`, `roughness: 0`, ≥3 orthogonal points. Bind via
`startBinding`/`endBinding` to the box **RECTANGLE** ids only — NEVER to row texts or
`line` dividers (those are not in the anchorable shape set and will trip
`arrow_endpoint_unanchored`).

### Step 5 — Satellite attachment connectors

Attach each satellite to its parent hub or link using thin elbow arrows from
[`@../patterns/tree-hierarchy.md`](../patterns/tree-hierarchy.md):

- `strokeWidth: 1.5` (thin — structural, not flow), `endArrowhead: "arrow"`
- `elbowed: true`, `roundness: null`, `roughness: 0`, ≥3 orthogonal points
- Bind to the parent and satellite **RECTANGLE** ids only

Place satellites indented to the side of their parent (indent +60px x or below, per
layout density), connected by the thin elbow.

## 3-role palette + role label + legend

This section contains the **SC-2 rules**: hub/link/satellite must be distinguishable in
grayscale — NEVER by color alone.

### Role fills (3-role palette)

Drawn from the documented Semantic Color Palette with the widest WCAG luminance spread
available (0.53 → 0.73 → 0.89):

| Role | Fill | Stroke | Luminance | Role label |
|------|------|--------|-----------|------------|
| **Hub** | `#93c5fd` (Tertiary blue) | `#1e3a5f` | 0.53 (darkest) | `«hub»` |
| **Link** | `#fed7aa` (Start/Trigger amber) | `#c2410c` | 0.73 (mid) | `«link»` |
| **Satellite** | `#fef3c7` (Decision pale-yellow) | `#b45309` | 0.89 (lightest) | `«sat»` |

### HARD RULES — SC-2 (grayscale safety)

1. **MANDATORY text role label on EVERY box.** Every hub carries `«hub»`, every link
   carries `«link»`, every satellite carries `«sat»`. Place the label as a separate
   `text` element (`fontFamily: 3`, `fontSize: 14`) in/above the box header, inside the
   same `groupIds` as the box. ASCII fallback `[HUB]`/`[LINK]`/`[SAT]` is acceptable if
   guillemets ever render as tofu, but guillemets are confirmed safe under `fontFamily: 3`
   (Cascadia, Phase 7 A1).

   **The label — NOT the color — is the SC-2 carrier. Color-alone distinction is
   DISALLOWED.** A diagram where the three roles are only distinguishable by fill color
   fails the SC-2 grayscale-safety requirement. The fill is decorative reinforcement only.

2. **MANDATORY in-canvas legend.** Include a small legend (a `@../patterns/group-container.md`
   bordered box or a 3-row swatch+label strip) that decodes role↔color so a grayscale
   reader recovers the mapping. Minimum: a 3-row strip with a colored swatch rectangle
   and a text label per role (`Hub / Link / Satellite`).

   Example legend structure (from `@../patterns/group-container.md`): a bordered rectangle
   containing three swatch rectangles (each with the role fill + `roundness: null`) and
   three text labels placed to their right, all sharing one `groupIds`.

3. **EX-03 visual gate must explicitly confirm grayscale-distinguishability.** There is
   NO automated color check in the loop. The visual review step MUST include a grayscale
   check: "are hub / link / satellite still readable as distinct roles when color is
   stripped?" — the label + luminance spread are the only mechanisms.

### Why color-alone is disallowed

Nothing in `verifier_structural.py` (10 checks: emoji, overflow, missing-dims,
unanchored-arrow, image-path, roughness, fontfamily, points-too-few, not-elbow,
sequence-center-x) checks color, contrast, or palette. The frozen validator checks
metadata + label fields only. There is no automated SC-2 guard. **The text role label
and the legend are the ONLY deterministic guarantees that the diagram does not collapse
to ambiguity when color is removed.**

## Binding rules (connector encoding)

All connectors in a Data Vault diagram — spine arrows (hub→link) and satellite attachment
arrows — use the **plain-association** encoding from
[`@./notation-conventions.md`](./notation-conventions.md):

- `endArrowhead: "arrow"` **only** on all connectors. Data Vault relationships are not
  cardinality-decorated in this scope (no crow's-foot, no diamond, no hollow arrowhead).
- **FORBIDDEN tokens** (render silently as bare lines, no error): `crowsfoot`, `diamond`,
  `hollow`, `open`. Do not invent or use any token outside the legal five
  (`arrow | bar | dot | triangle | null`).
- `elbowed: true`, `roundness: null`, `roughness: 0`, ≥3 orthogonal points on every
  connector.
- **Anchor to RECTANGLE ids ONLY.** Every `startBinding.elementId` and
  `endBinding.elementId` must reference a box rectangle id — NEVER a row `text` id or a
  `line` divider id. Row texts and dividers are not in the anchorable shape set and will
  trip `arrow_endpoint_unanchored`.
- Gap 4 in bindings: `{ "elementId": "<rect_id>", "focus": 0, "gap": 4 }`.

Box construction rules (same as snowflake/ER/class):
- `roundness: null` on all boxes and dividers (sharp corners; no soft/rounded boxes).
- One shared `groupIds` per box: frame rectangle + header divider + role-label text + title
  text + every row text all share the same group id. Moving the box moves all its elements.

## Composes (primitive layer)

- [`@./compartmented-box.md`](./compartmented-box.md) — the single reusable
  box construction: finalized offsets (header 40px, row pitch 20px, left-pad 12px,
  fontSize 16, fontFamily 3, width rule `len*0.6*16` rounded to 20-grid); HARD prohibition
  on multi-line single text; alignment rules (full-width dividers, common left x, 20-grid
  coordinates). Reused verbatim by hub, link, and satellite boxes.
- [`@../patterns/fan-out.md`](../patterns/fan-out.md) — hub→link spine geometry: one hub radiating
  arrow elbows to multiple links through a shared vertical rail.
- [`@../patterns/tree-hierarchy.md`](../patterns/tree-hierarchy.md) — satellite attachment: thin
  (`strokeWidth: 1.5`) elbow connectors, +60px x indent, anchored to RECTANGLE borders.
- [`@../patterns/convergence.md`](../patterns/convergence.md) — ≥2 hubs converging into one link:
  shared rail geometry, all hubs' arrows routing to the rail before turning into the link.
- [`@../patterns/group-container.md`](../patterns/group-container.md) — the in-canvas legend box: a
  bordered named scope housing the 3-row swatch+label strip that decodes role↔color for
  grayscale readers.
- [`@./notation-conventions.md`](./notation-conventions.md) — legal arrowhead encoding
  (`arrow | bar | dot | triangle | null`); plain-association committed encoding for data
  vault connectors (`endArrowhead: "arrow"`); silent-failure rule for illegal tokens.

## Ground truth

- [`./data_vault_sales.png`](./data_vault_sales.png) — the canonical
  Data Vault reference: a Sales raw-vault slice with hub boxes (`«hub»`, `#93c5fd`),
  link boxes (`«link»`, `#fed7aa`), and satellite boxes (`«sat»`, `#fef3c7`); hub→link
  spine connectors via fan-out and convergence geometry; satellite attachments via thin
  tree-hierarchy elbow connectors; and an in-canvas legend. Every box uses the locked
  compartmented-box recipe with finalized offsets; every connector uses `endArrowhead:
  "arrow"` anchored to RECTANGLE ids. Authored in `09-02-PLAN.md`; indexed in
  `diagram-types/README.md` after EX-03 visual gate passes (`09-03-PLAN.md`).
