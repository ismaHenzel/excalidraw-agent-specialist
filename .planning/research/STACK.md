# Stack Research

**Domain:** Excalidraw v2 JSON drawing primitives for NEW diagram families (UML core-4 + data-modeling) in the existing Docker/Playwright render pipeline
**Researched:** 2026-06-03
**Confidence:** HIGH (element types/properties verified against the published `@excalidraw/excalidraw@0.17.3` `.d.ts` and cross-checked against the 5 shipped `examples_excalidraw/*.excalidraw` sources)

> **Scope note.** This is NOT a software-dependency stack. There are no new host deps, no
> new npm/pip packages, no render-pipeline changes. The "stack" here is the **Excalidraw v2
> schema vocabulary** — the element types, properties, and notation workarounds the
> `diagram-types` KB will need to draw UML (sequence/class/use-case/activity) and data models
> (star/snowflake/data-vault/ER) correctly. Everything below stays inside the frozen
> `0.17.3` bundle the pipeline already loads. **Do not add new dependencies.**

---

## Recommended Stack

### Core Technologies

These are the Excalidraw v2 element `type` values — the complete drawing vocabulary. All
verified present in the `0.17.3` element-type union and all already exercised by the shipped
examples (so the render pipeline is known to draw them).

| Element `type` | Verified | Purpose for new families | Why it fits Architect's Precision |
|------------|---------|---------|-----------------|
| `rectangle` | 0.17.3 + all examples | Entity boxes (ER/star/snowflake/vault), class boxes, activity action nodes, swimlane bands, sequence activation bars, UML object boxes | With `roundness: null` + `roughness: 0` it renders as a crisp sharp-cornered box — the literal building block of every formal-notation diagram |
| `line` | 0.17.3 union | Class-compartment dividers, sequence lifeline dashes, swimlane separators, table header rules, crow's-foot endpoint glyphs (workaround) | A `line` (no arrowheads) is the only primitive for non-connector strokes; supports `strokeStyle: "dashed"` for lifelines |
| `arrow` | 0.17.3 + all examples | All connectors: associations, dependencies, messages, FK relationships, generalization. `elbowed: true` orthogonal routing | Sharp elbow arrows are the house connector; `roundness: null` + orthogonal `points` give the orthogonal "wiring diagram" look |
| `ellipse` | 0.17.3 + examples (`process_decision`, `architecture_overview`) | Use-case ovals, sequence "found message" start dots, actor head (workaround), data-vault hub markers | Native oval = the literal UML use-case shape; no workaround needed there |
| `diamond` | 0.17.3 + `process_decision.excalidraw` | Activity-diagram decision/merge nodes; (UML aggregation/composition diamonds are NOT arrowheads — see workarounds) | Native diamond already used by `decision-branch` pattern — reuse it for activity decisions |
| `text` | 0.17.3 + all examples | All labels: class names, attributes, PK/FK rows, multiplicity (`1..*`), message labels, stereotypes (`«interface»`), guards (`[condition]`) | `fontFamily: 3` (Cascadia/monospace) keeps tabular PK/FK rows column-aligned |
| `image` | 0.17.3 + all examples | Brand/tech icons inside Tech-Architecture nodes (reuse existing `icon-block`) | Existing icon strategy; unchanged for new families |

### Supporting Libraries

Not libraries — the **critical element PROPERTIES** the new families depend on. All confirmed
in the `0.17.3` `.d.ts` and in the shipped example JSON.

| Property | Verified value space | Purpose | When to use |
|---------|---------|---------|-------------|
| `strokeStyle` | `"solid" \| "dashed" \| "dotted"` (0.17.3 `.d.ts`) | Solid = association/message/FK; **dashed = UML dependency / return message / lifeline**; dotted rarely | Dashed `arrow` is THE way to express a UML dependency vs a solid association. Lifelines are dashed `line`s |
| `endArrowhead` / `startArrowhead` | `"arrow" \| "bar" \| "dot" \| "triangle" \| null` (0.17.3 `.d.ts`) | Connector semantics. `triangle` = filled generalization/realization head; `arrow` = open/message; `null` = plain association line | See the arrowhead-mapping table below — this is the single most constrained part of the schema |
| `elbowed` | `true` | Orthogonal routing for all formal connectors | Always `true` for these families (matches Architect's Precision); pair with `roundness: null` |
| `roundness` | `null` (sharp) or `{type:1\|2\|3}` | `null` = sharp corners on rect/box/arrow | **Always `null`** for entity/class/activity boxes and connectors. (Note: `icon-block.md` uses `{type:3}` for soft tech nodes — formal-notation boxes should override to `null` for sharp compartments) |
| `boundElements` | `[{type:"text",id}]` / `[{type:"arrow",id}]` | Binds a label to a container (text centered) and registers arrow attachment | Use for single centered labels (class name, use-case text). **Do NOT use for multi-row compartments** — see pitfall below |
| `containerId` (on text) | id of host shape | Marks a `text` as bound/centered inside a container | Only for the single centered case; left-aligned attribute rows are free-floating text instead |
| `startBinding` / `endBinding` | `{elementId, focus, gap}` | Makes an arrow re-anchor to a shape border | Use so FK/association arrows stay glued to entity borders when nudged |
| `groupIds` | `[string]` | Groups the many sub-elements of one notation unit (box + dividers + all row texts) into one logical object | Essential: a class box is ~8–15 elements; group them so the diagram-type KB can place/translate the unit rigidly |
| `fontFamily` | `3` (Cascadia/monospace, per 0.17.3 `FONT_FAMILY`) | Monospace for column-aligned tabular rows | Always `3` (Architect's Precision) — also makes the verifier's monospace width-fit check valid |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Existing `excalidraw_validator.py` | Static JSON lint (metadata, no `label` field, contrast) | Unchanged. New families must still pass it — note its "no `label` field on shapes" rule: use `boundElements`+`text` element, never a `label` key |
| Existing `scripts/validate_and_render.sh` (Docker + Playwright + Chromium + `@excalidraw/excalidraw@0.17.3`) | Render to PNG | Unchanged. Anything below renders in this exact bundle — do not introduce primitives outside `0.17.3` |
| Existing `excalidraw_verifier` subagent | Structural + visual check | Multi-row compartments make the monospace width-fit check more important; flag in roadmap |

## Installation

```bash
# NONE. No new dependencies — host, npm, pip, or otherwise.
# The new families are authored in the same .excalidraw JSON schema (type:"excalidraw", version:2)
# the pipeline already renders with @excalidraw/excalidraw@0.17.3.
```

---

## Notation → Primitive Mapping (the load-bearing part)

### Arrowhead mapping (the hard constraint)

`0.17.3` arrowheads are EXACTLY: `arrow`, `bar`, `dot`, `triangle`, or `null`. **There is no
crow's-foot, no hollow/open triangle, no open diamond, no filled diamond.** Confirmed in the
published `0.17.3` `element/types.d.ts`. All shipped examples only ever use `endArrowhead:"arrow"`.

| Notation needed | Native? | Express with |
|---|---|---|
| UML message / association direction | YES | `endArrowhead: "arrow"`, `strokeStyle: "solid"` |
| UML **dependency** (`«use»`) | YES (via style) | `endArrowhead: "arrow"`, `strokeStyle: "dashed"` |
| UML sequence **return** message | YES (via style) | `endArrowhead: "arrow"`, `strokeStyle: "dashed"` |
| UML **generalization / realization** (inheritance) | PARTIAL | `endArrowhead: "triangle"` — closest match. `triangle` renders FILLED, not the hollow UML triangle. Accept filled triangle as the house convention; realization additionally uses `strokeStyle:"dashed"` |
| UML **aggregation / composition** (diamond end) | NO | No diamond arrowhead exists. **Workaround:** draw a small `diamond` element (~14×14) at the connector's owner end, white fill (aggregation) or solid fill (composition), as a separate grouped glyph |
| Crow's-foot **"many"** (ER) | NO | **Workaround:** draw three short `line` strokes fanning at the entity end (the crow's foot), grouped with the connector. Or `endArrowhead:"arrow"` as a degraded fallback |
| Crow's-foot **"one"** (ER bar) | YES-ish | `endArrowhead: "bar"` is a single perpendicular tick = the "one"/mandatory bar |
| Crow's-foot **"zero/optional"** circle | PARTIAL | `endArrowhead: "dot"` ≈ the optional circle; or a small unfilled `ellipse` glyph for accuracy |
| Sequence **lifeline** | YES | dashed `line` (vertical, `strokeStyle:"dashed"`), NOT an arrow |
| Sequence **activation bar** | YES | thin `rectangle` (~10px wide) over the lifeline |

**Recommended ER cardinality strategy:** prefer the **`bar` (one) + `dot`/`ellipse` (zero) +
3-line crow's-foot glyph (many)** combination for true crow's-foot; OR fall back to **textual
multiplicity labels** (`1`, `0..*`, `1..*`) as `text` elements at line ends — this is the
data-vault/star-schema-friendly approach and is what the existing `star_schema.excalidraw`
effectively relies on (it uses plain `endArrowhead:"arrow"` connectors + no crow's-foot).

### UML element construction

| Notation | Build from |
|---|---|
| **Class box (3 compartments)** | 1 `rectangle` (outer, `roundness:null`) + 2 horizontal `line` dividers + 1 bound/centered `text` (class name, bold via separate styling) + N free-floating left-aligned `text` rows (attributes, methods). Group all with one `groupIds`. **Do NOT use one multi-line `text` for rows** — you lose per-row alignment and the divider lines |
| **Stereotype** `«interface»` | `text` element above class name (use guillemets `«»`, which are non-emoji glyphs that render under `fontFamily:3`) |
| **Actor (stick figure)** | NO native stick-figure. **Workaround:** compose from `ellipse` (head) + `line`s (body/arms/legs), grouped; OR (simpler, recommended) a small `rectangle`/`ellipse` labelled "Actor" with the role name. Pick ONE convention for the canonical example and document it |
| **Use-case** | native `ellipse` + centered bound `text` |
| **System boundary** | `rectangle` (`roundness:null`) enclosing use-case ellipses + a title `text` (reuse `group-container` pattern) |
| **Sequence participant header** | `rectangle` + bound `text` at top of each lifeline |
| **Activity action node** | `rectangle` with `roundness:{type:3}` (rounded — UML actions are stadium/rounded); OR sharp `rectangle` for house consistency |
| **Activity start/end node** | filled `ellipse` (start = solid dot; end = ellipse-in-ellipse via two stacked `ellipse`s) |
| **Activity decision/merge** | native `diamond` (reuse `decision-branch.md`) |
| **Swimlane** | tall `rectangle` bands side-by-side (or stacked), header `text` per lane, `line` separators |

### Data-model element construction

| Notation | Build from |
|---|---|
| **Entity / fact / dimension box** | `rectangle` header + `line` divider + free-floating monospace `text` rows. Exactly the class-box recipe |
| **PK / FK row markers** | `text` prefix in the row string: `"PK  id"`, `"FK  customer_id"` (monospace keeps the columns aligned). No native key glyph exists |
| **Star schema** | central fact `rectangle`, dimension `rectangle`s around it, `arrow` connectors (`endArrowhead:"arrow"` or `bar`). Reuse the **fan-out / convergence** layout patterns. Matches shipped `star_schema.excalidraw` (16 rectangles, 5 elbow arrows, 113 monospace texts) |
| **Snowflake** | star + normalized sub-dimension boxes hanging off dimensions; reuse **tree-hierarchy** for the normalization chains |
| **Data Vault hub/link/satellite** | distinguish by COLOR + shape role, not by special primitive: **hub** = one fill (e.g. blue), **link** = another (e.g. grey, often rendered as a connecting box between hubs), **satellite** = a third (e.g. yellow). All are the same `rectangle`+row recipe; the semantics live in the palette + the diagram-type KB |
| **ER cardinality** | per the arrowhead table above (bar/dot/crow's-foot-glyph or textual `1..*` labels) |

---

## Alternatives Considered

| Recommended | Alternative | When to use alternative |
|-------------|-------------|-------------------------|
| Multi-element compartments (rect + `line` dividers + per-row `text`) | Single multi-line `text` with `\n` rows | Never for formal class/entity boxes — you lose dividers and column alignment. Acceptable only for a quick note block |
| Textual multiplicity labels (`1..*`) OR bar/dot/3-line crow's-foot | `endArrowhead:"arrow"` everywhere (ignore cardinality) | Only as a degraded fallback when the diagram is conceptual and cardinality isn't the point |
| `triangle` (filled) for generalization | Custom hollow-triangle glyph from `line`s | If hollow accuracy matters for a canonical reference example; otherwise filled `triangle` is simpler and consistent |
| Composed stick-figure actor (ellipse+lines) | Labelled box "Actor: <role>" | Box is more legible at small scale and far cheaper to author; use stick-figure only if the canonical example demands textbook fidelity |
| Native `diamond` for aggregation glyph | `rectangle` rotated 45° (`angle: 0.785398`) | Only if a future schema drops `diamond` (it does NOT in 0.17.3 — `diamond` is in the union) |

## What NOT to Use

| Avoid | Why | Use instead |
|-------|-----|-------------|
| A `label` key on a shape | Static validator explicitly bans `label` on shapes; not a v2 field | `boundElements:[{type:"text",id}]` + a real `text` element |
| Raw Unicode emoji in `text` (e.g. key 🔑, person 🧍) | Render as missing-glyph boxes under `fontFamily:3`; verifier rejects them | Text prefixes (`PK`/`FK`), guillemets `«»`, or `image` elements from `icons/` |
| Inventing crow's-foot / open-diamond / hollow-triangle `endArrowhead` values | Not in the `0.17.3` enum (`arrow\|bar\|dot\|triangle` only) — they silently render as default/none | The composed-glyph or textual-label workarounds above |
| New host deps, npm packages, a newer Excalidraw bundle, Mermaid/PlantUML | Out of scope; pipeline is frozen on `0.17.3`; project is Excalidraw-specific | Express everything in `0.17.3` primitives |
| `roundness:{type:3}` on entity/class compartment boxes | Soft corners read as "tech node", not "formal table"; muddies the notation | `roundness:null` (sharp) for all formal-notation boxes |
| One giant ungrouped pile of elements per notation unit | Impossible to translate/place a class box as a unit; verifier/layout churn | `groupIds` on every box+dividers+rows+endpoint-glyph cluster |

## Stack Patterns by Variant

**If drawing UML class / data-model ER (compartmented boxes):**
- Recipe = `rectangle` (sharp) + horizontal `line` dividers + monospace left-aligned `text` rows, all grouped.
- Because column-aligned monospace rows + dividers are the only way to get real compartments; no native "table" primitive exists.

**If drawing UML sequence:**
- Lifelines = dashed `line`s; activations = thin `rectangle`s; messages = `arrow` (solid forward, dashed `strokeStyle` for returns); participant heads = `rectangle`+bound `text`.
- Reuse `timeline`-style horizontal discipline but vertical.

**If drawing UML use-case:**
- Use-cases = native `ellipse`+bound `text`; system boundary = `group-container`; actors = labelled box or composed stick-figure (pick one).
- Most native-friendly UML family — fewest workarounds.

**If drawing UML activity:**
- Reuse `decision-branch` (`diamond`), `linear-pipeline`, and `feedback-loop` directly; add start dot (`ellipse`), end (stacked `ellipse`s), swimlanes (`rectangle` bands + `line`s).

**If drawing data-vault:**
- Same compartment recipe; semantics carried by palette (hub/link/satellite colors), not new primitives. Document the 3-color mapping in the diagram-type KB.

## Version Compatibility

| Schema field | Confirmed in | Notes |
|-----------|-----------------|-------|
| File envelope `{type:"excalidraw", version:2, source}` | `star_schema.excalidraw` + all examples | All new family examples use the same envelope |
| Arrowheads `arrow\|bar\|dot\|triangle\|null` | `@excalidraw/excalidraw@0.17.3` `element/types.d.ts` | HARD limit — no crow's-foot/diamond/hollow head |
| `strokeStyle: solid\|dashed\|dotted` | `0.17.3` `.d.ts` | dashed = dependency/return/lifeline |
| `roundness: {LEGACY:1, PROPORTIONAL_RADIUS:2, ADAPTIVE_RADIUS:3}` or `null` | `0.17.3` `constants.d.ts` | examples use `{type:2}` on arrows, `null`/`{type:3}` on shapes |
| `fontFamily: 3` = Cascadia (monospace) | `0.17.3` `FONT_FAMILY` + project convention | Required by Architect's Precision; enables verifier width-fit check |
| Element union incl. `rectangle,diamond,ellipse,line,arrow,text,image` | `0.17.3` `.d.ts` + examples | All needed primitives confirmed renderable |

## Sources

- `@excalidraw/excalidraw@0.17.3` `element/types.d.ts` (unpkg) — Arrowhead union (`arrow|bar|dot|triangle`), strokeStyle (`solid|dashed|dotted`), element type union — **HIGH** (published artifact for the exact pinned version)
- `@excalidraw/excalidraw@0.17.3` `constants.d.ts` (unpkg) — `ROUNDNESS` (1/2/3) and `FONT_FAMILY` (incl. Cascadia) — **HIGH**
- Shipped sources `.claude/agents/excalidraw/examples_excalidraw/{star_schema,data_pipeline_flow,architecture_overview,process_decision,repo_tree_hierarchy}.excalidraw` — confirmed real property keys per element type, confirmed `diamond`/`ellipse`/`line` are drawable by the pipeline, confirmed examples only use `endArrowhead:"arrow"` (so crow's-foot etc. are genuinely absent today) — **HIGH** (the actual render targets)
- `.claude/agents/excalidraw/kb/{icon-block,decision-branch,README}.md` — existing primitive conventions (`roughness:0`, `fontFamily:3`, sharp elbow arrows, grid-of-20) the new families must inherit — **HIGH**

---
*Stack research for: Excalidraw v2 drawing primitives for UML + data-modeling diagram families*
*Researched: 2026-06-03*
