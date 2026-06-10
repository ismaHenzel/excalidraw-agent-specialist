# Phase 7: ER + Class - Research

**Researched:** 2026-06-07
**Domain:** Excalidraw `.excalidraw` JSON authoring — relationship-endpoint notation glyphs (crow's-foot cardinality, aggregation/composition diamonds, generalization triangle) composed from the legal element set, plus two compartmented-relationship diagram-type recipes (ER, UML class)
**Confidence:** HIGH (all conventions already locked in-repo; codebase verified directly)

## Summary

This phase is **not** a research-into-the-unknown phase. The hard design decisions were already made and committed in Phase 4: `diagram-types/notation-conventions.md` (DTKB-04) locks the single legal encoding for every non-native relationship glyph, and `diagram-types/compartmented-box.md` (INT-02) locks the box geometry with finalized parametric offsets. Phase 6 proved that recipe end-to-end on star and snowflake. Phase 7's job is to (a) author the two type files (`er.md`, `class.md`) so both reference the *same* locked endpoint-glyph convention exactly once, (b) pin down the **deferred pixel geometry** of the composed glyphs (diamond size/placement, ellipse size, textual-multiplicity label placement) that `notation-conventions.md` explicitly punted to "the phase that first ships ER/Class (Phase 7)", and (c) author one canonical example pair per type that passes the full validate→render→verify loop.

The single most important verified finding: **no automated check enforces arrowhead-token legality.** I read both `scripts/render/excalidraw_validator.py` (Phase-1 of the loop) and `scripts/verifier/verifier_structural.py` (the structural verifier) — neither inspects `startArrowhead`/`endArrowhead` against the legal set `{arrow,bar,dot,triangle,null}`. An illegal token (`crowsfoot`, `diamond`, `hollow`) renders **silently as a plain line** in `0.17.3` — no error, no warning — so Success Criterion 1 ("no illegal arrowhead value appears in any authored JSON") currently has **zero automated guard**. The pre-existing research (`.planning/research/PITFALLS.md` Pitfall 1, `SUMMARY.md`) recommends adding a validator rule that rejects any arrowhead value outside the five legal tokens. The planner should decide whether to add that cheap validator check this phase (recommended) or rely solely on KB discipline + visual review.

**Primary recommendation:** Build the shared endpoint-glyph convention as a SINGLE new primitive file (`kb/relationship-endpoint.md`) that pins the deferred glyph pixel geometry, have both `er.md` and `class.md` `@`-reference it (mirroring how snowflake references compartmented-box), reuse the locked compartmented-box offsets verbatim for entity/class boxes, and add the arrowhead-enum validator check so the silent-render failure becomes a loud authoring-time error.

## Architectural Responsibility Map

This phase has no runtime tiers — it is authoring-convention + KB work against the frozen v1.0 loop. The "tiers" here are the KB layers and the validate→render→verify pipeline stages.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Legal endpoint-glyph encoding (convention choice) | `diagram-types/notation-conventions.md` (already locked) | — | DTKB-04 fixed the convention once; type files reference, never re-derive |
| Glyph pixel geometry (diamond/ellipse size, multiplicity label placement) | NEW `kb/relationship-endpoint.md` primitive | `notation-conventions.md` (convention) | `notation-conventions.md` explicitly DEFERRED pixel geometry to this phase; geometry belongs in the PRIMITIVE layer per the two-layer rule |
| Compartmented entity/class box geometry | `diagram-types/compartmented-box.md` (already locked) | — | INT-02 finalized offsets; reused verbatim by every compartmented type |
| ER type recipe (assembly) | NEW `diagram-types/er.md` | compartmented-box + relationship-endpoint | TYPE layer composes primitives by `@`-reference |
| Class type recipe (assembly) | NEW `diagram-types/class.md` | compartmented-box + relationship-endpoint | TYPE layer composes primitives by `@`-reference |
| Arrowhead-token legality enforcement | `scripts/render/excalidraw_validator.py` (Phase-1 of loop) | KB discipline + verifier visual review | Currently UNGUARDED — cheap validator addition converts silent failure to loud error |
| Endpoint anchoring / overflow safety | `scripts/verifier/verifier_structural.py` (frozen) | — | Existing checks interact with composed glyphs — see Pitfalls 2 & 3 below |

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DM-02 | `diagram-types/er-diagram.md` recipe exists; agent authors an ER diagram (entity boxes with PK/FK rows, committed cardinality notation) that passes the full loop | Locked cardinality convention in `notation-conventions.md` (ER "one"=`bar`, "zero/optional"=`dot`/`ellipse`, "many"=textual multiplicity). Compartmented-box offsets locked. PK/FK = monospace text-prefix rows (new convention, see Code Examples). NOTE filename discrepancy: REQUIREMENTS.md/ROADMAP say `er-diagram.md` in one place and the phase Success Criteria + resolver say `er.md` — resolve in planning (resolver table already reserves `er.md`). |
| UML-02 | `diagram-types/class.md` recipe exists; agent authors a UML class diagram (three-compartment boxes, association/aggregation/composition/generalization via committed glyph workarounds, stereotypes via guillemets) that passes the full loop | Locked encodings: generalization=`triangle` (FILLED), realization=`triangle`+`dashed`, aggregation=white-fill `diamond`, composition=solid-fill `diamond`, association=`arrow`, dependency=`arrow`+`dashed`. Three-compartment box = compartmented-box with two dividers. Stereotypes via `«»` guillemets (confirmed safe under `fontFamily:3` per SUMMARY.md/STACK.md). |

<user_constraints>
## User Constraints

**No CONTEXT.md exists for this phase yet** (`has_context: false`). This research is standalone (no `/gsd-discuss-phase` decisions to honor). The binding constraints come from already-committed project artifacts, treated with the same authority as locked decisions:

### Locked Decisions (from committed KB + ROADMAP/STATE)
- **DTKB-04 glyph conventions are LOCKED** (`diagram-types/notation-conventions.md`). Both type files MUST embed or reference this table verbatim — no re-deriving, no alternative convention. Where a choice existed (crow's-foot glyph vs. textual multiplicity; stick-figure vs. labelled-box actor), the committed default was already chosen and the alternative is explicitly NOT used.
  - ER "many" = **textual multiplicity label** (`0..*` / `1..*`). The grouped 3-line crow's-foot glyph is the alternative and is **NOT used**.
  - Generalization = `endArrowhead:"triangle"` **FILLED** (house convention; no hollow token exists).
- **Compartmented-box offsets are FINALIZED** (`diagram-types/compartmented-box.md`): header 40px, row pitch 20px, left-pad 12px, fontSize 16, monospace `fontFamily:3`, box-width rule `len*0.6*16` rounded up to 20-grid. Reused verbatim — not re-derived.
- **v1.0 loop, validator, and verifier are FROZEN** — all v1.1 work is additive. (Exception worth flagging: the *optional* arrowhead-enum validator addition — see Open Question 1 — would touch `excalidraw_validator.py`; decide explicitly whether that counts as permitted additive hardening or stays frozen.)
- **Star is grandfathered (EX-02 Option B)**; legacy `star_schema.excalidraw` is NOT a safe template (0 groupIds, unbound arrows, soft roundness). Do not imitate it.
- **EX-01/EX-03 are per-type EXIT CRITERIA**: each shipped type's canonical example must pass the full validate→render→verify loop (structural automated + visual human approval) before its resolver row is wired.
- **Native crow's-foot / hollow-triangle / diamond arrowheads are OUT OF SCOPE** — workarounds only, no renderer change.
- **ER and class co-located in one phase** so the shared endpoint-glyph work is done exactly once.

### Claude's Discretion
- Whether the shared endpoint-glyph convention lives as a new `kb/` primitive file vs. an embedded section (recommendation below: new `kb/relationship-endpoint.md` primitive — consistent with the two-layer architecture).
- Exact glyph PIXEL geometry (diamond dimensions ~14px, placement offset, ellipse size, multiplicity-label offset from endpoint) — explicitly deferred to this phase by `notation-conventions.md` line 55-58.
- Whether to add the arrowhead-enum validator check (recommended; see Open Question 1).
- Example diagram subject matter (what entities/classes the canonical pair depicts).

### Deferred Ideas (OUT OF SCOPE)
- Native decorated arrowheads (renderer change). | Pixel-diff visual regression vs. baseline. | Auto-generating diagrams from schemas/code. | Sequence lifeline/activation primitive (Phase 8). | Use-case actor/oval (Phase 8). | Data Vault hub/link/satellite (Phase 9). | Remaining ~10 UML types (v2).
</user_constraints>

## Standard Stack

**This milestone has no software-dependency "stack"** (confirmed by `.planning/research/STACK.md`). The "stack" is the Excalidraw v2 schema vocabulary as exposed by the pinned `@excalidraw/excalidraw@0.17.3` (loaded via esm.sh CDN per the frozen render path). No packages are installed in this phase.

### Core schema vocabulary used by ER + Class

| Element type | Purpose this phase | Key locked properties |
|--------------|--------------------|-----------------------|
| `rectangle` | Entity/class box frame; aggregation/composition glyph is NOT a rectangle | `roundness: null`, `roughness: 0` |
| `line` | Compartment dividers (full box width); crow's-foot glyph IF ever used (it is NOT — textual default) | `roundness: null`; divider `x==box.x`, `points=[[0,0],[width,0]]` |
| `arrow` | All relationship connectors | `elbowed: true`, `roundness: null`, `startArrowhead`/`endArrowhead` ∈ `{arrow,bar,dot,triangle,null}` ONLY |
| `diamond` | Aggregation glyph (white fill) / composition glyph (solid fill), ~14px, grouped at owner end | `roundness: null`; `backgroundColor` + `fillStyle` distinguish agg vs comp |
| `ellipse` | ER "zero/optional" endpoint glyph (alternative to `dot` arrowhead) | small glyph at endpoint |
| `text` | All labels; PK/FK row prefixes; stereotypes `«»`; textual multiplicity `0..*`/`1..*` | `fontFamily: 3` (Cascadia monospace), `fontSize: 16` for box rows |

**Version verification:** No registry install this phase. `@excalidraw/excalidraw@0.17.3` is the pinned, already-vendored-via-CDN version; the five legal arrowhead tokens are confirmed in-repo by `notation-conventions.md` and `.planning/research/STACK.md`. [VERIFIED: in-repo notation-conventions.md + STACK.md]

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Textual multiplicity `0..*` for ER "many" | Grouped 3-line crow's-foot glyph | **EXPLICITLY NOT USED** — locked by DTKB-04; mixing the two across diagrams looks like a bug. Do not reopen. |
| New `kb/relationship-endpoint.md` primitive | Inline glyph geometry inside each type file | Inlining duplicates geometry across `er.md` + `class.md` → drift risk; the two-layer rule says geometry lives in `kb/`. Prefer the primitive. |
| Filled `triangle` for generalization | (no hollow token exists) | None — forced house convention; surface to user as "inheritance shown filled (Excalidraw lacks a hollow head)". |

## Package Legitimacy Audit

**Not applicable.** This phase installs no external packages. It authors `.excalidraw` JSON and Markdown KB files only, against the already-pinned `0.17.3` schema. No npm/PyPI/crates dependency is added, so the Package Legitimacy Gate is skipped (documented per protocol).

## Architecture Patterns

### System Architecture Diagram (the authoring + verify flow)

```
User request ("draw an ER diagram of …")
        │
        ▼
/excalidraw  ──► family pick (Data Modeling | UML) ──► type sub-pick (er | class)
        │
        ▼
diagram-types/README.md  (single resolver table)
        │  resolves type → recipe file + kb sub-patterns + example PNG
        ▼
excalidraw_specialist  reads  diagram-types/<type>.md  FIRST  (INT-01)
        │      └─►  @compartmented-box.md   (box offsets, locked)
        │      └─►  @kb/relationship-endpoint.md  (NEW — glyph geometry)
        │      └─►  @notation-conventions.md  (legal-encoding table)
        ▼
authors  <name>.excalidraw  JSON
        │
        ▼
scripts/render/validate_and_render.sh
   ├─ Phase 1: excalidraw_validator.py      ◄── ⚠ does NOT check arrowhead legality
   ├─ Phase 2: render_docker.sh → PNG
   └─ Phase 3: instruction to read PNG
        │
        ▼
excalidraw_verifier  (structural: verifier_structural.py  +  visual multimodal review)
   ├─ structural checks: emoji, overflow, unanchored-arrow, roughness, fontFamily, elbow…
   │     ◄── ⚠ also does NOT check arrowhead legality
   └─ visual: "is each relationship's cardinality distinguishable?"  ◄── the real glyph guard today
        │
        ▼
   passed:false ──► specialist auto-fixes (≤3 iterations) ──► re-render ──► re-verify
   passed:true  ──► (human-verify gate / EX-03) ──► wire resolver row
```

### Recommended File Structure (additive)

```
.claude/agents/excalidraw/
├── kb/
│   └── relationship-endpoint.md      # NEW primitive: glyph pixel geometry + grouping mechanics
├── diagram-types/
│   ├── er.md                         # NEW type recipe (DM-02)
│   ├── class.md                      # NEW type recipe (UML-02)
│   ├── README.md                     # EDIT: wire er + class resolver rows (after loop passes)
│   ├── notation-conventions.md       # REFERENCE only (already locked — do not weaken)
│   └── compartmented-box.md          # REFERENCE only (offsets locked — do not re-derive)
├── examples_excalidraw/
│   ├── er_<subject>.excalidraw        # NEW canonical source
│   └── class_<subject>.excalidraw     # NEW canonical source
└── examples/
    ├── er_<subject>.png               # NEW rendered (sibling, passes loop)
    └── class_<subject>.png            # NEW rendered (sibling, passes loop)
```

### Pattern 1: Shared endpoint-glyph as a single primitive
**What:** Pin the deferred glyph geometry ONCE in `kb/relationship-endpoint.md`; both `er.md` and `class.md` `@`-reference it. This is exactly how `snowflake-schema.md` references `compartmented-box.md` and `star-schema.md` rather than re-deriving offsets.
**When to use:** Any time two type files need identical notation — which is the entire point of co-locating ER + class in one phase ("done exactly once").
**Why:** The two-layer KB rule (`diagram-types/README.md`) says geometry/JSON skeletons live only in `kb/`; type files compose by reference and carry no coordinate math. A `> Used by types: er, class` back-ref on the new primitive keeps the link bidirectional.

### Pattern 2: Compartmented box reused verbatim
**What:** ER entity boxes (2 compartments: title + attribute rows) and UML class boxes (3 compartments: title + attributes + methods) are both the locked compartmented-box construction — same sharp rectangle, full-width `line` dividers, bound title text, N free-floating monospace row texts, one `groupIds` per box.
**When to use:** Every box in both types.
**Example:** see Code Examples below; class diagram simply has one extra divider at `box.y + 40 + 20*k`.

### Pattern 3: Glyph grouped on top of an anchored connector
**What:** The composed `diamond` (aggregation/composition) sits at the owner end of a connector. The connector `arrow` still binds/anchors to the box **rectangle** border (so `check_arrow_endpoint_unanchored` passes); the small diamond is a SEPARATE element placed over the owner-end and added to the connector's `groupIds` so it travels with it.
**When to use:** Aggregation and composition relationships in class diagrams.
**Why this matters:** If you terminate the connector AT the diamond instead of the box, the arrow's last point won't land on a rectangle/ellipse/diamond border within tolerance → `arrow_endpoint_unanchored` error. Keep the connector anchored to the box; overlay the glyph.

### Anti-Patterns to Avoid
- **Inventing arrowhead tokens** (`crowsfoot`, `diamond`, `hollow`, `open`): renders silently as a bare line; relationship semantics vanish. Use only the five legal tokens + composed glyphs / textual labels.
- **Plain `arrow` everywhere**: erases the one/many/aggregation/composition distinction — the entire semantic payload of an ER/class diagram. Each relationship type MUST be visually distinguishable.
- **Multi-line single `text` for a compartment**: DISALLOWED (defeats dividers + breaks per-element width-fit check). One `text` per row.
- **Imitating legacy `star_schema.excalidraw`**: 0 groupIds, unbound arrows, soft roundness — contradicts the recipe.
- **Mixing crow's-foot glyph and textual multiplicity** across the two diagrams: looks like a bug; textual is the single committed default.
- **Placing a textual multiplicity label inside a box's bounding box**: may trip `text_overflow_static`'s `_find_containing_shape` and produce a false overflow error (see Pitfall 3). Place labels clear of any box bbox.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Box compartment geometry | Per-type offset math in `er.md`/`class.md` | `@compartmented-box.md` finalized offsets verbatim | Already proven through the frozen loop on star+snowflake; re-deriving invites drift |
| Notation encoding choice | Ad-hoc per-diagram arrowhead/glyph decisions | `@notation-conventions.md` locked table | DTKB-04 committed one convention each; consistency is the requirement |
| Glyph geometry duplicated in two files | Inline diamond/ellipse coords in both type files | One `kb/relationship-endpoint.md` primitive `@`-referenced by both | Two-layer rule; "done exactly once" is the phase goal |
| Arrow endpoint binding | Manual coordinate snapping | `startBinding`/`endBinding` to box rectangle ids with `gap` (as snowflake does) | Keeps `arrow_endpoint_unanchored` green and arrows glued on box move |

**Key insight:** Almost everything this phase needs is already built and locked. The genuinely *new* work is narrow: (1) pixel geometry for ~3 small composed glyphs, (2) two type recipes that compose existing primitives, (3) two canonical examples, and optionally (4) one cheap validator check. Resist re-opening locked conventions.

## Common Pitfalls

### Pitfall 1: Illegal arrowhead token renders silently as a plain line — and NOTHING automated catches it
**What goes wrong:** Author writes `endArrowhead:"crowsfoot"` or `"diamond"`; `0.17.3` ignores the unknown value and draws no head. The relationship's cardinality/type silently disappears.
**Why it happens:** Every UML/ER reference shows decorated endpoints as canonical; the schema constraint is invisible until render. **Verified:** neither `excalidraw_validator.py` nor `verifier_structural.py` inspects arrowhead values — I read both.
**How to avoid:** (a) Embed/reference the legal-token set in both type files; (b) STRONGLY recommend adding a validator check that rejects any `startArrowhead`/`endArrowhead` not in `{arrow,bar,dot,triangle,null}` (turns silent failure into a loud Phase-1 error — see Open Question 1); (c) the verifier's *visual* review is the only current guard ("are relationships distinguishable?") — keep it as backstop.
**Warning signs:** A connector's intended cardinality looks identical to a plain association; an arrowhead value in the JSON outside the five tokens; verifier visual review says "all relationships look the same."

### Pitfall 2: Composed diamond/ellipse glyph leaves the connector endpoint unanchored
**What goes wrong:** Author terminates the connector arrow at the small composed glyph instead of the box border, so the arrow's last point is not within `ENDPOINT_TOLERANCE_PX` of a rectangle/ellipse/diamond border → `check_arrow_endpoint_unanchored` raises an `error`.
**Why it happens:** It feels natural to "end the line at the diamond." But the diamond is an overlay, not the anchor.
**How to avoid:** Connector binds to the box **rectangle** (via `startBinding`/`endBinding`, as snowflake does); the ~14px diamond is a separate element placed over the owner end and added to the connector's `groupIds`. The arrow endpoint still lands on the box border. (Note: `_on_diamond_border` exists, so terminating on the GLYPH diamond's border *could* satisfy the check — but the glyph is tiny and offset; binding to the box is the robust path.)
**Warning signs:** `arrow_endpoint_unanchored` error in the structural report; glyph floats detached from the connector at render.

### Pitfall 3: Textual multiplicity label trips a false `text_overflow_static`
**What goes wrong:** A `0..*` / `1..*` label placed near an endpoint happens to fall geometrically inside a box's bounding box; `_find_containing_shape` associates it with that box and, if the box is narrow, flags an overflow `error`.
**Why it happens:** The overflow check measures any free `text` against the shape it sits inside, regardless of intent.
**How to avoid:** Place multiplicity labels in the clear space along the connector, outside every box bbox. Keep them short (they are, `0..*` is 4 chars). On the 20-grid.
**Warning signs:** `text_overflow_static` error pointing at a tiny multiplicity label; label visually overlapping a box edge.

### Pitfall 4: Non-elbow connector raises an `arrow_not_elbow` warning
**What goes wrong:** Connector authored without `elbowed:true` or with `roundness:{type:2}` → `check_arrow_not_elbow` emits a warning ("not a sharp 90-degree elbow connector").
**Why it happens:** Default arrow authoring; copying a curved arrow.
**How to avoid:** Every connector: `elbowed:true`, `roundness:null`, orthogonal points (e.g. `[[0,0],[dx,0],[dx,dy]]`). This matches snowflake's locked binding rules. (Severity is `warning`, not `error`, but keep examples clean.)
**Warning signs:** `arrow_not_elbow` warnings in the structural report.

### Pitfall 5: Symbol-dense notation sneaks in raw emoji / non-monospace glyphs
**What goes wrong:** Author uses 🔑 for PK, 🧍 for actor, 🔒 for visibility; under `fontFamily:3` these render as missing-glyph tofu boxes (and the structural emoji check rejects them).
**Why it happens:** UML/ER notation is symbol-heavy; emoji are lazy shorthand.
**How to avoid:** PK/FK = **text prefixes** (`PK  id`, `FK  customer_id`) in monospace, never key emoji. Visibility = ASCII `+ - #`. Stereotypes = `«»` guillemets (confirmed renderable under `fontFamily:3` per STACK.md/SUMMARY.md — these are NOT emoji and are safe). Map any "key/lock/person" request to an `icons/*.png` image element if a literal glyph is truly needed.
**Warning signs:** `check_raw_emoji_in_text` failure; verifier visual review reports tofu boxes.

### Pitfall 6: Canonical example indexed before it passes the loop
**What goes wrong:** A resolver row for `er`/`class` is wired while the example still fails verify → the agent imitates broken ground truth forever.
**How to avoid:** EX-01/EX-03 are exit criteria — example must pass full validate→render→verify (structural automated + visual human approval / EX-03 gate) BEFORE the resolver row is wired. Star/snowflake followed this; do the same.
**Warning signs:** Resolver row marked wired with no verifier pass on record; blank glyph / plain line in the example PNG.

## Code Examples

> Sources below are derived from in-repo locked conventions (`compartmented-box.md`, `notation-conventions.md`) and the verified snowflake example structure (`examples_excalidraw/snowflake_schema.excalidraw`). Coordinates illustrate the formulas; the authoring agent computes exact values.

### ER entity box row with PK/FK text-prefix (monospace, per-row text)
```jsonc
// Each row is its own text element (NEVER a multi-line block).
// Left x = box.x + 12; row i (1-based) y = box.y + 40 + 10 + (i-1)*20.
{ "type":"text","text":"PK  id","fontFamily":3,"fontSize":16,
  "x": 312, "y": 350, "groupIds":["entity_customer_box"] }
{ "type":"text","text":"FK  region_id","fontFamily":3,"fontSize":16,
  "x": 312, "y": 370, "groupIds":["entity_customer_box"] }
// Box width must satisfy: width >= max_row(len*0.6*16), rounded UP to 20-grid.
// "FK  region_id" = 13 chars -> 13*9.6 = 124.8 -> box width >= 140.
```

### ER cardinality — committed legal encodings (NO crowsfoot token)
```jsonc
// "one" end:
{ "type":"arrow","elbowed":true,"roundness":null,
  "endArrowhead":"bar","startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"entity_a_box","gap":4},
  "endBinding":{"elementId":"entity_b_box","gap":4} }
// "zero / optional" end: endArrowhead:"dot"  (or a small composed ellipse glyph)
// "many": NO arrowhead glyph — a textual multiplicity label placed along the
//         connector, OUTSIDE any box bbox:
{ "type":"text","text":"0..*","fontFamily":3,"fontSize":16,"x":520,"y":340 }
```

### UML class three-compartment box (one extra divider vs. ER)
```jsonc
// Header divider at box.y + 40 (locked). Second divider (attrs|methods)
// lands ON a row boundary: box.y + 40 + 20*k. Full width: x==box.x, points=[[0,0],[width,0]].
{ "type":"line","x":300,"y":340,"points":[[0,0],[160,0]],"roundness":null,
  "groupIds":["class_order_box"] }   // header divider (box.y+40)
{ "type":"line","x":300,"y":420,"points":[[0,0],[160,0]],"roundness":null,
  "groupIds":["class_order_box"] }   // attr|method divider (box.y+40+20*4)
// Stereotype via guillemets (safe under fontFamily:3, NOT an emoji):
{ "type":"text","text":"«interface»","fontFamily":3,"fontSize":16,"x":312,"y":310,
  "groupIds":["class_order_box"] }
```

### UML aggregation vs composition — composed diamond glyph, grouped over an anchored connector
```jsonc
// Connector binds to the OWNER box rectangle (keeps arrow endpoint anchored):
{ "type":"arrow","elbowed":true,"roundness":null,"endArrowhead":null,
  "startBinding":{"elementId":"class_part_box","gap":4},
  "endBinding":{"elementId":"class_whole_box","gap":4},
  "groupIds":["rel_whole_part"] }
// Small (~14px) diamond overlaid at the OWNER (whole) end, in the same group:
// Aggregation = WHITE fill:
{ "type":"diamond","width":14,"height":14,"roundness":null,
  "backgroundColor":"#ffffff","fillStyle":"solid","groupIds":["rel_whole_part"] }
// Composition = SOLID (filled) fill: backgroundColor:"#1e1e1e", fillStyle:"solid"
```

### Generalization / realization — triangle (FILLED, house convention)
```jsonc
// Generalization (inheritance): filled triangle, solid stroke.
{ "type":"arrow","elbowed":true,"roundness":null,"endArrowhead":"triangle",
  "strokeStyle":"solid" }
// Realization (implements): filled triangle + dashed stroke.
{ "type":"arrow","elbowed":true,"roundness":null,"endArrowhead":"triangle",
  "strokeStyle":"dashed" }
// Dependency: arrow + dashed.   Association: arrow + solid.
```

## State of the Art

Not applicable in the usual sense — this is a closed, pinned authoring environment, not a moving ecosystem. The only relevant "state" change is internal to the project:

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Glyph pixel geometry "deferred to Phase 7" | This phase pins it in a primitive file | Phase 7 (now) | `notation-conventions.md` lines 55-58 are satisfied; later types (data-vault) inherit it |
| No automated arrowhead-legality guard | (Recommended) validator rejects illegal tokens | Phase 7 if adopted | Silent-render failure → loud Phase-1 error |
| ER "many" undecided (glyph vs textual) | Textual multiplicity locked | Phase 4 (DTKB-04) | No decision to make — apply it |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `«»` guillemets render correctly under `fontFamily:3` (Cascadia Code) | Pitfall 5 / Code Examples | LOW — stated by STACK.md & SUMMARY.md but not re-rendered this session; the canonical class example's render+verify loop will empirically confirm. If they tofu, fall back to ASCII `<<interface>>`. |
| A2 | `_on_diamond_border` would accept a connector terminating on a 14px glyph diamond | Pitfall 2 | LOW — recommended path (bind to box rectangle) sidesteps this entirely; noted only for completeness. |
| A3 | The cheap arrowhead-enum validator addition counts as permitted "additive" hardening, not a violation of the "validator FROZEN" decision | Open Question 1 | MEDIUM — if treated as frozen-violation, the check can't be added and SC-1 relies on KB discipline + visual review only. Planner must decide. |
| A4 | Filename for the ER recipe is `er.md` (resolver) not `er-diagram.md` (REQUIREMENTS.md/ROADMAP prose) | Phase Requirements (DM-02) | LOW — cosmetic; resolver table already reserves `er.md`. Pick one and make REQUIREMENTS/resolver agree. |

## Open Questions

1. **Add the arrowhead-enum validator check, or rely on KB + visual review?**
   - What we know: Neither `excalidraw_validator.py` nor `verifier_structural.py` checks arrowhead legality (verified by reading both). Pre-existing research (PITFALLS Pitfall 1, SUMMARY) recommends adding the check as "cheap, high value." The v1.0 validator/verifier are nominally FROZEN.
   - What's unclear: Whether a small additive deny-list check counts as permitted hardening or a frozen-component change requiring its own decision.
   - Recommendation: **Add it** as a Phase-1 validator rule (reject any `start/endArrowhead` ∉ `{arrow,bar,dot,triangle,null}`). It is purely additive (rejects what was always illegal), directly satisfies SC-1's "no illegal arrowhead value appears in any authored JSON," and converts a silent failure into a loud one. Surface the decision explicitly in the plan / discuss-phase since it touches a frozen file.

2. **One shared primitive file or embedded sections?**
   - What we know: The two-layer rule says geometry lives in `kb/`; snowflake precedent references a primitive rather than inlining.
   - Recommendation: New `kb/relationship-endpoint.md` primitive with `> Used by types: er, class`; both type files `@`-reference it. Keeps "done exactly once" literal and drift-proof.

3. **ER recipe filename: `er.md` vs `er-diagram.md`?** Resolver reserves `er.md`; REQUIREMENTS prose says `er-diagram.md`. Pick `er.md` (matches resolver, matches Success Criteria) and correct REQUIREMENTS, or vice-versa — just make them consistent before authoring.

## Environment Availability

This phase is authoring (JSON + Markdown) plus running the existing frozen loop. The only external dependency is the render path, already proven in Phases 5-6.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` (validator + structural verifier) | validate + structural checks | Assumed ✓ (used through Phases 1-6) | — | none needed |
| Docker / `render_docker.sh` | Phase-2 PNG render | Assumed ✓ (snowflake rendered 2026-06-07) | — | `render_excalidraw.py` direct path exists |
| `@excalidraw/excalidraw@0.17.3` via esm.sh CDN | render engine | Assumed ✓ (frozen render path) | 0.17.3 | none (HARD-01 vendoring deferred to v2) |

**Missing dependencies with no fallback:** None identified — the render+verify toolchain is the same one that shipped star and snowflake in Phase 6, three days ago.

*Note: the render path depends on the esm.sh CDN (HARD-01 deferred). If the CDN is unreachable at execution time, rendering blocks — same risk all prior phases carried.*

## Validation Architecture

> `nyquist_validation: true` in config — section included. Note: this project's "tests" are the validate→render→verify loop scripts, not a unit-test framework.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Custom loop: `scripts/render/validate_and_render.sh` (validator + render) + `excalidraw_verifier` subagent (`scripts/verifier/verifier_structural.py` + multimodal visual review). No pytest/jest. |
| Config file | none — scripts are invoked directly |
| Quick run command | `python3 .claude/agents/excalidraw/scripts/verifier/verifier_structural.py <file.excalidraw>` (structural only, no render, sub-second) |
| Full suite command | `bash .claude/agents/excalidraw/scripts/render/validate_and_render.sh <file.excalidraw>` then read the PNG + invoke `excalidraw_verifier` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | Check Exists? |
|--------|----------|-----------|-------------------|---------------|
| DM-02 | ER example: legal arrowheads, distinguishable cardinality, boxes fit | structural + visual | `validate_and_render.sh er_<subject>.excalidraw` + verifier | ⚠ arrowhead-legality NOT covered (Wave 0 gap) |
| DM-02 | PK/FK rows monospace, per-row text, no overflow | structural | `verifier_structural.py` (text_overflow_static, fontfamily) | ✅ existing |
| UML-02 | Class example: 3 compartments, glyph workarounds, guillemets render | structural + visual | `validate_and_render.sh class_<subject>.excalidraw` + verifier | ✅ structural; ⚠ arrowhead-legality + glyph-distinctness rely on visual |
| UML-02 | Connectors elbowed/sharp, endpoints anchored | structural | `verifier_structural.py` (arrow_not_elbow, arrow_endpoint_unanchored) | ✅ existing |
| SC-1 | No illegal arrowhead token in any authored JSON | structural | (none today) | ❌ Wave 0 — add validator check (Open Question 1) |

### Sampling Rate
- **Per task commit:** `verifier_structural.py <file>` (sub-second structural gate) + the new arrowhead-legality check if added.
- **Per example completion:** full `validate_and_render.sh` + visual verifier pass.
- **Phase gate:** both canonical examples pass full loop (structural green + EX-03 visual human approval) before resolver rows are wired.

### Wave 0 Gaps
- [ ] **Arrowhead-legality check** — add to `excalidraw_validator.py` (or a new structural check): reject any `start/endArrowhead` ∉ `{arrow,bar,dot,triangle,null}`. Covers SC-1. (Decision-gated — Open Question 1.)
- [ ] `kb/relationship-endpoint.md` — the shared glyph primitive must exist before either type file can `@`-reference it.
- [ ] No framework install needed — the loop is the existing frozen toolchain.

*(If Open Question 1 is resolved as "do not touch the frozen validator," SC-1 has no automated test and relies entirely on KB discipline + the verifier's visual review — record that explicitly.)*

## Security Domain

> `security_enforcement` not present in config → treat as not applicable for this phase. This is a local diagram-authoring KB project with no auth, network input, data persistence, or untrusted input surface introduced by Phase 7. No ASVS category applies to authoring `.excalidraw` JSON + Markdown. (The only latent risk — `render_excalidraw.py` path resolution, HARD-03 — is a pre-existing deferred item, not introduced here.)

## Sources

### Primary (HIGH confidence — in-repo, read directly this session)
- `.claude/agents/excalidraw/diagram-types/notation-conventions.md` — DTKB-04 locked legal-encoding table; pixel geometry deferred to this phase (lines 55-58)
- `.claude/agents/excalidraw/diagram-types/compartmented-box.md` — INT-02 finalized parametric offsets (header 40, pitch 20, pad 12, fontSize 16, width rule)
- `.claude/agents/excalidraw/diagram-types/snowflake-schema.md` + `examples_excalidraw/snowflake_schema.excalidraw` — working compartmented + connector precedent (binding, elbow, groupIds)
- `.claude/agents/excalidraw/diagram-types/README.md` — resolver table (reserves `er.md`, `class.md` rows), two-layer rule, add-a-type procedure
- `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py` — verified: checks metadata + `label` only; NO arrowhead-legality check
- `.claude/agents/excalidraw/scripts/verifier/verifier_structural.py` — verified: emoji, overflow, unanchored-arrow, roughness, fontFamily, points-too-few, not-elbow; NO arrowhead-legality check
- `.claude/agents/excalidraw/scripts/render/validate_and_render.sh` — loop entrypoint (validator → render → read PNG)
- `.planning/ROADMAP.md` + `.planning/STATE.md` + `.planning/REQUIREMENTS.md` — phase scope, locked decisions, DM-02/UML-02

### Secondary (HIGH confidence — pre-existing project research)
- `.planning/research/PITFALLS.md` — Pitfall 1 (arrowhead trap), 2 (multi-line text), 5 (emoji/notation), 6 (broken ground truth) + "Don't Hand-Roll" rows
- `.planning/research/SUMMARY.md` + `STACK.md` — arrowhead constraint, `«»` safe under `fontFamily:3`, compartmented-box construction, glyph workaround table

### Tertiary (LOW confidence)
- None. No external web sources were needed — every claim is grounded in committed in-repo artifacts.

## Metadata

**Confidence breakdown:**
- Standard stack (schema vocabulary): HIGH — locked tokens + offsets verified in-repo
- Architecture (two-layer composition): HIGH — mirrors shipped star/snowflake pattern
- Pitfalls: HIGH — validator/verifier source read directly; arrowhead-legality gap confirmed by reading both check sets
- Glyph pixel geometry: MEDIUM — sizes (~14px diamond) come from committed research, exact placement offsets are this phase's deferred design work and will be proven empirically through the loop

**Research date:** 2026-06-07
**Valid until:** Stable — this is a pinned, closed authoring environment; valid until the locked conventions or frozen loop scripts change (no external time decay).
