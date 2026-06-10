# Phase 7: ER + Class - Pattern Map

**Mapped:** 2026-06-07
**Files analyzed:** 7 (3 new KB/recipe markdown, 1 README edit, 2 new example pairs, 1 optional validator edit)
**Analogs found:** 7 / 7 (all have a close in-repo analog — this is a mature, convention-locked KB)

> **Phase nature:** This is a KB-authoring + example-authoring phase, NOT a runtime-code phase. "Files" are Markdown recipes, `.excalidraw` JSON, and (optionally) one Python validator addition. Every new artifact has a directly-shipped analog from Phases 4–6. The dominant instruction to the planner: **copy the locked construction verbatim; do not re-derive geometry.**

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.claude/agents/excalidraw/kb/relationship-endpoint.md` | primitive (KB pattern) | transform (geometry skeleton) | `kb/tree-hierarchy.md` | role-match (sibling primitive; geometry + JSON-skeleton + back-ref structure identical) |
| `.claude/agents/excalidraw/diagram-types/er.md` | type recipe | transform (composition by reference) | `diagram-types/snowflake-schema.md` | exact (compartmented type recipe composing primitives by `@`-ref) |
| `.claude/agents/excalidraw/diagram-types/class.md` | type recipe | transform (composition by reference) | `diagram-types/snowflake-schema.md` | exact (same compartmented-box base + extra divider + relationship glyphs) |
| `.claude/agents/excalidraw/diagram-types/README.md` | config (resolver table) | CRUD (add rows) | itself — existing `er`/`class` `_(planned)_` rows + "Adding a diagram type" procedure | exact (edit-in-place; rows already reserved) |
| `.claude/agents/excalidraw/examples_excalidraw/er_<subject>.excalidraw` | example (JSON ground truth) | file-I/O (authored JSON) | `examples_excalidraw/snowflake_schema.excalidraw` | exact (compartmented boxes + bound elbow arrows) |
| `.claude/agents/excalidraw/examples_excalidraw/class_<subject>.excalidraw` | example (JSON ground truth) | file-I/O (authored JSON) | `examples_excalidraw/snowflake_schema.excalidraw` | exact (same base + 3 compartments + composed glyphs) |
| `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py` | validator (loop Phase-1) | request-response (deny-list check) | itself — existing metadata/label deny-list loops (lines 17–53) | role-match (additive check; DECISION-GATED, see Open Question 1 / A3) |

## Pattern Assignments

### `kb/relationship-endpoint.md` (NEW primitive, geometry skeleton)

**Analog:** `.claude/agents/excalidraw/kb/tree-hierarchy.md`

This is the one genuinely new primitive. Mirror `tree-hierarchy.md`'s section layout exactly: back-ref header line, *When to use*, *Geometry* (pin the deferred pixel numbers here), *JSON skeleton*, *See in examples*, *Notes*.

**Back-ref header pattern** (`tree-hierarchy.md` line 3) — MUST be present so the two-layer link stays bidirectional:
```markdown
> Used by types: snowflake-schema
```
New file's line: `> Used by types: er, class` (both consume this primitive; this is the literal "done exactly once" link).

**Geometry-section pattern** (`tree-hierarchy.md` lines 12–16) — terse, exact pixel offsets, no prose math in the type files:
```markdown
## Geometry
- Parent at `(x_p, y_p)`. Children at `(x_p + 60, y_child_i)`.
- Vertical y-step between siblings: `40px` (compact) or `48px` (comfortable).
- Connector arrow from parent: leaves at the parent's bottom-center `(x_p + 12, y_p + 28)` ...
```
The new file pins the DEFERRED glyph geometry (per `notation-conventions.md` lines 55–58 + RESEARCH "Claude's Discretion"): diamond `width:14, height:14`; ellipse glyph size; multiplicity-label offset from endpoint; the rule that the glyph is overlaid on the OWNER end and added to the connector's `groupIds` (Pitfall 2 / Pattern 3).

**JSON-skeleton pattern** (`tree-hierarchy.md` lines 31–67) — provide a copy-paste skeleton block. For relationship-endpoint, the skeletons come verbatim from RESEARCH "Code Examples" (lines 235–284): bar/dot ER ends, white-vs-solid diamond, filled-triangle generalization, dashed realization.

**See-in-examples pattern** (`tree-hierarchy.md` lines 74–77) — point at the two NEW canonical PNGs once they pass the loop.

---

### `diagram-types/er.md` (NEW type recipe)

**Analog:** `.claude/agents/excalidraw/diagram-types/snowflake-schema.md` (the closest shipped compartmented type recipe)

**Layer-header pattern** (`snowflake-schema.md` line 3) — every type file opens with this exact one-liner:
```markdown
> Layer: TYPE recipe. Composes primitives from [`../kb/`](../kb/README.md) and the shared [`compartmented-box.md`](./compartmented-box.md) construction; does not re-derive their geometry. Indexed in [`README.md`](./README.md).
```

**"Reuse verbatim — do not re-derive" pattern** (`snowflake-schema.md` lines 25–30) — copy this exact framing so the recipe inherits, never re-derives, the locked offsets:
```markdown
Snowflake **reuses the star schema's compartmented-box geometry VERBATIM** — do not
re-derive any box offset numbers. All parametric offsets (header height 40, row pitch 20,
left-pad 12, fontSize 16, box-width rule `len*0.6*16`) are locked in
[`@./compartmented-box.md`](./compartmented-box.md) ...
```
ER's wording: entity boxes are the compartmented-box construction (2 compartments: title + attribute rows), offsets per `@./compartmented-box.md`. PK/FK rows are monospace text-prefix rows (`PK  id`, `FK  region_id`) — RESEARCH Code Example lines 223–233. Cardinality per `@./notation-conventions.md` (one=`bar`, zero=`dot`/ellipse, many=textual `0..*`/`1..*`). Glyph geometry per the new `@../kb/relationship-endpoint.md`.

**Binding-rules block** (`snowflake-schema.md` lines 65–72) — copy verbatim; the legal arrowhead set callout is already in the analog:
```markdown
- `endArrowhead: "arrow"` only on all connectors ... No `crowsfoot`/`diamond`/`hollow`
  tokens — they render silently as bare lines.
- Every arrow's start and end points must land within 8px of a **rectangle** border. Bind
  via `startBinding`/`endBinding` to the box rectangle ids.
```

**"Composes (primitive layer)" section** (`snowflake-schema.md` lines 74–86) — bulleted `@`-ref list:
```markdown
## Composes (primitive layer)
- [`@./compartmented-box.md`](./compartmented-box.md) — finalized offsets used verbatim ...
- [`@../kb/relationship-endpoint.md`](../kb/relationship-endpoint.md) — glyph geometry ...
- [`@./notation-conventions.md`](./notation-conventions.md) — legal-encoding table ...
```

**"Ground truth" section** (`snowflake-schema.md` lines 87–94) — point at `../examples/er_<subject>.png` with a description of what to imitate.

**Filename note (A4 / Open Question 3):** resolver reserves `er.md`; REQUIREMENTS prose says `er-diagram.md`. Planner: pick `er.md` (matches resolver row + Success Criteria) and correct REQUIREMENTS, or vice-versa — make them consistent before authoring.

---

### `diagram-types/class.md` (NEW type recipe)

**Analog:** `.claude/agents/excalidraw/diagram-types/snowflake-schema.md` (same layer-header / verbatim-reuse / Composes / Ground-truth skeleton as `er.md` above)

Class differs from ER only in: **three compartments** (title + attributes + methods → one extra full-width `line` divider at `box.y + 40 + 20*k`, per `compartmented-box.md` line 79 "Between-row dividers"), **stereotypes** via `«»` guillemets (RESEARCH Code Example lines 256–258; safe under `fontFamily:3` per A1), and the **relationship glyph set** (generalization=filled `triangle`, realization=`triangle`+dashed, aggregation=white `diamond`, composition=solid `diamond`, association=`arrow`, dependency=`arrow`+dashed) — all from `@./notation-conventions.md` + `@../kb/relationship-endpoint.md`.

**Composition-glyph-over-anchored-connector pattern (Pattern 3 / Pitfall 2):** the recipe MUST state that the connector `arrow` binds to the box RECTANGLE (keeps `check_arrow_endpoint_unanchored` green) while the ~14px diamond is a SEPARATE element overlaid on the owner end and added to the connector's `groupIds`. See the empty-`groupIds` arrow in the snowflake example (below) — for class, the glyph and arrow share one non-empty group id.

---

### `diagram-types/README.md` (EDIT — wire resolver rows)

**Analog:** itself. Rows already exist as placeholders (lines 23, 26):
```markdown
| Data Modeling | er | `er.md` _(planned — Phase 7)_ | evidence-card, group-container, tree-hierarchy | _(planned)_ |
| UML | class | `class.md` _(planned — Phase 7)_ | tree-hierarchy, group-container, evidence-card (+ relationship-glyph) | _(planned)_ |
```

**Procedure to follow** (`README.md` lines 48–55 "Adding a diagram type") — already specifies the exact 4 steps. Update the two rows: replace `_(planned — Phase 7)_` with the real `kb/` sub-pattern list (must include `relationship-endpoint`), set the Example PNG cell to the real PNG path, and add each to the "Wired rows" note paragraph (line 30). **Pitfall 6 / EX-01/EX-03:** wire ONLY after the canonical example passes the full loop — never before.

---

### `examples_excalidraw/er_<subject>.excalidraw` and `class_<subject>.excalidraw` (NEW JSON ground truth)

**Analog:** `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw` (52 elements: 7 rectangle, 7 line, 32 text, 6 arrow — the proven compartmented + bound-elbow structure)

**Top-level file shape** (analog): keys `type, version, source, elements, appState, files`. Copy this envelope.

**Compartmented box = one group of {rectangle + line divider(s) + bound title text + free-floating row texts}.** Copy these exact element shapes from the analog:

Rectangle frame (sharp, grouped, title bound):
```jsonc
{ "type":"rectangle","x":600,"y":360,"width":200,"height":180,"roughness":0,
  "strokeStyle":"solid","backgroundColor":"transparent","fillStyle":"solid",
  "groupIds":["grp_fact_sales"],
  "boundElements":[{"type":"text","id":"fact_sales_box_title"}] }
```
Full-width header divider (`x == box.x`, `points=[[0,0],[width,0]]`, same group):
```jsonc
{ "type":"line","x":600,"y":400,"width":200,"height":0,"points":[[0,0],[200,0]],
  "roughness":0,"strokeStyle":"solid","groupIds":["grp_fact_sales"] }
```
Title text (bound via `containerId`, monospace):
```jsonc
{ "type":"text","x":612,"y":370,"width":100,"height":20,"fontFamily":3,"fontSize":16,
  "text":"fact_sales","groupIds":["grp_fact_sales"],"containerId":"fact_sales_box" }
```
Bound elbow connector (binds to box rectangle ids; `elbowed:true`, `roundness:null` implied by sharp-points):
```jsonc
{ "type":"arrow","x":600,"y":450,"elbowed":true,"endArrowhead":"arrow",
  "points":[[0,0],[-100,0],[-100,-210],[-200,-210]],
  "startBinding":{"elementId":"fact_sales_box","focus":0,"gap":4,"fixedPoint":[0.5001,0.5001],"mode":"orbit"},
  "endBinding":{"elementId":"dim_date_box","focus":0,"gap":4,"fixedPoint":[0.5001,0.5001],"mode":"orbit"},
  "groupIds":[] }
```
**ER-specific:** row texts use `PK  ...`/`FK  ...` prefixes; "one" connectors set `endArrowhead:"bar"`; "many" adds a free `text:"0..*"` placed OUTSIDE every box bbox (Pitfall 3). **Class-specific:** add a second `line` divider at `box.y + 40 + 20*k`; add `«stereotype»` text; for aggregation/composition give the connector a real `groupIds` id and add a `{ "type":"diamond","width":14,"height":14,"backgroundColor":"#ffffff"|"#1e1e1e","fillStyle":"solid","groupIds":[<same id>] }` overlay at the owner end.

> **Do NOT imitate** `examples_excalidraw/star_schema.excalidraw` (0 groupIds, unbound arrows, soft roundness — grandfathered, explicitly NOT a safe template; README lines 34–44). Imitate `snowflake_schema.excalidraw` and `star_schema_v2.excalidraw` only.

---

### `scripts/render/excalidraw_validator.py` (OPTIONAL EDIT — arrowhead-enum deny-list) — DECISION-GATED

**Analog:** itself — the existing deny-list loops (lines 30–37) over `elements`:
```python
for el in elements:
    if el.get("type") in ["rectangle", "ellipse", "diamond"] and "label" in el:
        shapes_with_labels.append(el.get("id", "unknown"))
if shapes_with_labels:
    errors.append(f"Found 'label' property in shapes: ...")
```
The new check mirrors this shape exactly: iterate `elements`, for any `el` with `startArrowhead`/`endArrowhead` not in `{"arrow","bar","dot","triangle",None}`, append to `errors`. It appends to the same `errors` list, so the existing report + exit-code machinery (lines 54–69) needs no change.

**Gate (A3 / Open Question 1):** the v1.0 validator is nominally FROZEN. RESEARCH recommends adding this as permitted ADDITIVE hardening (rejects what was always illegal → converts the silent-render failure into a loud Phase-1 error, satisfying SC-1). Planner MUST surface this decision explicitly. If declined, SC-1 has no automated guard and relies on KB discipline + the verifier's visual review only — record that explicitly.

## Shared Patterns

### Locked compartmented-box geometry (reuse verbatim)
**Source:** `diagram-types/compartmented-box.md` (lines 58–90, INT-02 finalized offsets)
**Apply to:** `er.md`, `class.md`, both example JSON files
```
Header height 40px · Row pitch 20px · Left-pad 12px · fontSize 16 (fontFamily 3)
Header divider Y = box.y + 40 ; Title at (box.x+12, box.y+10) ; Row i at box.y + 40 + 10 + (i-1)*20
Between-row divider (class methods) = box.y + 40 + 20*k
Box width >= max_row(len * 0.6 * 16), rounded UP to 20-grid  (passes text_overflow_static)
Box height = 40 + rows*20 + 10, rounded up to 20-grid
HARD: one text element per row — NEVER a multi-line \n block. All elements share one groupIds.
```

### Locked notation encoding (reference, never re-derive)
**Source:** `diagram-types/notation-conventions.md` (lines 9–41, DTKB-04)
**Apply to:** `er.md`, `class.md`, `kb/relationship-endpoint.md`
```
Legal arrowhead tokens ONLY: arrow | bar | dot | triangle | null
ER one=bar · zero/optional=dot (or ellipse glyph) · many=textual 0..*/1..*
Generalization=triangle(FILLED) · Realization=triangle+dashed
Aggregation=white-fill diamond · Composition=solid-fill diamond · Association=arrow · Dependency=arrow+dashed
Stereotype=«» guillemets (safe under fontFamily:3)
```

### Bound elbow connector (keeps endpoints anchored)
**Source:** `examples_excalidraw/snowflake_schema.excalidraw` (arrow element) + `snowflake-schema.md` lines 65–72
**Apply to:** every connector in both example files
```
elbowed:true · roundness:null · orthogonal points
startBinding/endBinding -> box RECTANGLE id, gap:4   (NOT to row texts or line dividers)
Composed glyph (diamond/ellipse) is OVERLAID + joins the connector's groupIds — the arrow still ends on the box border (Pitfall 2)
```

### Verifier structural guard (what must stay green — frozen, read-only)
**Source:** `scripts/verifier/verifier_structural.py` — relevant checks confirmed present:
`check_arrow_endpoint_unanchored` (line 238, tolerance 8px, accepts rectangle/ellipse/diamond borders), `check_text_overflow_static` (189, via `_find_containing_shape` 103 — Pitfall 3), `check_arrow_not_elbow` (409 — Pitfall 4), `check_raw_emoji_in_text` (121 — Pitfall 5), `check_fontfamily_nonmonospace` (358), `check_roughness_nonzero` (336).
**CONFIRMED GAP:** no arrowhead-legality check exists in either the validator or the verifier (grep verified) — this is the SC-1 Wave-0 gap.

### KB two-layer cross-reference discipline
**Source:** `diagram-types/README.md` lines 7–12 + `kb/tree-hierarchy.md` line 3 back-ref
**Apply to:** `relationship-endpoint.md` (carries `> Used by types: er, class`), `er.md`/`class.md` (link DOWN via `@../kb/relationship-endpoint.md`), README resolver (both directions). Type files compose by `@`-reference and carry NO coordinate math — geometry lives only in `kb/`.

## No Analog Found

None. Every artifact has a directly-shipped Phase 4–6 analog. The only PARTIALLY-novel content is the *deferred pixel values* inside `kb/relationship-endpoint.md` (diamond placement offset, ellipse size, multiplicity-label offset) — these are net-new design numbers (MEDIUM confidence per RESEARCH metadata) to be proven empirically through the loop, but the *file structure* that holds them is the `tree-hierarchy.md` primitive template.

## Metadata

**Analog search scope:** `.claude/agents/excalidraw/diagram-types/`, `.claude/agents/excalidraw/kb/`, `.claude/agents/excalidraw/examples_excalidraw/`, `.claude/agents/excalidraw/scripts/render/`, `.claude/agents/excalidraw/scripts/verifier/`
**Files scanned:** 7 read in full (snowflake-schema.md, compartmented-box.md, notation-conventions.md, README.md, tree-hierarchy.md, group-container.md, excalidraw_validator.py) + snowflake_schema.excalidraw inspected programmatically + verifier_structural.py grepped for check names
**Pattern extraction date:** 2026-06-07
