# Phase 8: Sequence + Use-Case — Pattern Map

**Mapped:** 2026-06-07
**Files analyzed:** 7 (1 new KB primitive, 2 new type recipes, 1 README edit, 2 new example pairs, 1 optional verifier edit)
**Analogs found:** 7 / 7

> **Phase nature:** KB-authoring + example-authoring phase. No runtime code. Every new artifact mirrors a directly-shipped Phase 5–7 analog. The dominant instruction to the planner: **copy the locked construction verbatim; do not re-derive geometry.**

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `.claude/agents/excalidraw/kb/lifeline-activation.md` | primitive (KB pattern) | transform (geometry skeleton) | `kb/relationship-endpoint.md` | exact (sibling primitive authored in Phase 7; same section layout, back-ref header, geometry pinning, JSON skeleton structure) |
| `.claude/agents/excalidraw/diagram-types/sequence.md` | type recipe | transform (composition by reference) | `diagram-types/snowflake-schema.md` | exact (layer-header, verbatim-reuse framing, Composes section, Ground-truth section) |
| `.claude/agents/excalidraw/diagram-types/use-case.md` | type recipe | transform (composition by reference) | `diagram-types/activity.md` | exact (pure-composition type; no new primitive; Composes section lists existing kb/ primitives) |
| `.claude/agents/excalidraw/diagram-types/README.md` | config (resolver table) | CRUD (add rows) | itself — _(planned)_ rows at lines 25, 27 | exact (edit-in-place; placeholder rows already reserved) |
| `.claude/agents/excalidraw/examples_excalidraw/sequence_<subject>.excalidraw` | example (JSON ground truth) | file-I/O (authored JSON) | `examples_excalidraw/snowflake_schema.excalidraw` | role-match (bound elbow arrows, rectangle/line elements, monospace text; sequence adds lifeline `line` + activation `rectangle` elements) |
| `.claude/agents/excalidraw/examples_excalidraw/use_case_<subject>.excalidraw` | example (JSON ground truth) | file-I/O (authored JSON) | `examples_excalidraw/snowflake_schema.excalidraw` | role-match (bound elbow arrows, rectangle elements, monospace text; use-case adds `ellipse` ovals and group-container boundary) |
| `.claude/agents/excalidraw/scripts/verifier/verifier_structural.py` | structural verifier | request-response (structural assertion) | itself — existing check list (emoji, overflow, unanchored-arrow, roughness, fontFamily, elbow, points-too-few) | role-match (optional additive center-x check; DECISION-GATED, see Open Question 1) |

---

## Pattern Assignments

### `kb/lifeline-activation.md` (NEW primitive, geometry skeleton)

**Analog:** `.claude/agents/excalidraw/kb/relationship-endpoint.md`

Mirror `relationship-endpoint.md`'s section layout exactly. That file is the freshest, most directly analogous primitive and was authored specifically to be the Phase 8 template per RESEARCH.md Sources.

**Back-ref header pattern** (`relationship-endpoint.md` line 3):
```markdown
> Used by types: er, class
```
New file's line: `> Used by types: sequence`

**Opening prose pattern** (`relationship-endpoint.md` lines 5–12) — brief purpose statement + cross-reference to convention and box files without re-deriving them:
```markdown
Shared primitive for all composed relationship-endpoint glyphs used in ER diagrams and
UML class diagrams: ...
The convention table itself is locked in
`@../diagram-types/notation-conventions.md` (DTKB-04). The box offsets ... are locked in
`@../diagram-types/compartmented-box.md` (INT-02). Do NOT re-derive either here.
```
New file adapts: purpose = lifeline + activation-bar geometry for sequence diagrams; forward-reference to `@../diagram-types/notation-conventions.md` for message-encoding tokens (Association=arrow+solid, Dependency=arrow+dashed); forward-reference to `@../diagram-types/compartmented-box.md` for participant head box header height (40px).

**"When to use" pattern** (`relationship-endpoint.md` lines 16–21) — one-sentence scope:
```markdown
## When to use

Use this primitive whenever an ER entity or UML class relationship requires an endpoint
marker ...
```
New file: "Use this primitive for every element in a sequence diagram that relates to participant positioning, lifeline placement, activation-bar sizing, or message Y ordering."

**"Legal arrowhead tokens" section** (`relationship-endpoint.md` lines 23–36) — keep the deny-list callout verbatim; sequence uses `arrow` (solid message) and `arrow`+dashed (return) — both already legal:
```markdown
## Legal arrowhead tokens

Excalidraw 0.17.3 exposes **exactly five** arrowhead values. Any other token renders
**silently as a bare line** — no error, no warning:

    arrow | bar | dot | triangle | null

Tokens that are ILLEGAL and must NEVER appear in authored JSON:

    crowsfoot  diamond  hollow  open  (and any other invented name)
```

**Geometry section pattern** (`relationship-endpoint.md` lines 38–88) — terse subsections, exact pixel offsets. New file pins the deferred values from RESEARCH.md Standard Stack table and Pitfall 4:

```markdown
## Geometry

### Participant head box
- Width: 120px · Height: 40px (matches compartmented-box header height)
- `roughness: 0`, `roundness: null`, `strokeStyle: "solid"`
- groupIds: one id per participant (head box + lifeline + activation bars share the same group)

### Lifeline
- A `line` element (NOT an `arrow` — lifelines carry no arrowhead)
- `strokeStyle: "dashed"`, `roughness: 0`, `roundness: null`
- Position: x = participant_head.x + participant_head.width / 2  ← this is lifeline_center_x
- Points: [[0,0],[0,lifeline_height]]  (vertical segment, width == 0)
- Starts at participant_head.y + participant_head.height (bottom of head box)

### Activation bar
- A `rectangle` element, width: 12px, height: span of the activation
- x = lifeline_center_x - 6   ← CRITICAL: center must equal lifeline_center_x
- y = y of first message touching this activation
- `roughness: 0`, `roundness: null`, `backgroundColor: "#ffffff"`, `strokeStyle: "solid"`
- This is the BINDABLE shape for message arrows (NOT the lifeline line element)

### Message Y pitch
- Minimum 40px between consecutive message Y values
- Message Y values MUST be monotonically non-decreasing (top = first, bottom = last)

### Participant x pitch
- 180px between adjacent participant lifeline_center_x values
```

**JSON skeleton pattern** (`relationship-endpoint.md` lines 90–221) — one skeleton per shape type. For lifeline-activation, provide participant head, lifeline line, activation bar, solid message, and dashed return skeletons (verbatim from RESEARCH.md Code Examples).

**"See in examples" pattern** (`relationship-endpoint.md` lines 195–201):
```markdown
## See in examples

- `../examples/er_<subject>.png` — canonical ER example ...
- `../examples/class_<subject>.png` — canonical class example ...
```
New file: point at `../examples/sequence_<subject>.png` once it passes the loop (fill real filename in the Wave 2 plan).

**Notes section** (`relationship-endpoint.md` lines 202–221) — bullet list of hard rules. New file must include:
- Message arrows bind to activation bar `rectangle` (or participant head `rectangle`) — NEVER to the lifeline `line` element (structural verifier `check_arrow_endpoint_unanchored` accepts only rectangle/ellipse/diamond borders)
- The lifeline `line` element's x is its LEFT edge; `lifeline_center_x = line.x` (since width is 0 and the line's x already IS the center)
- Self-message route: 3-point elbow from activation bar right edge (+40px x, +40px y, back to bar right edge at lower y) — never two collinear points at the same x

---

### `diagram-types/sequence.md` (NEW type recipe)

**Analog:** `.claude/agents/excalidraw/diagram-types/snowflake-schema.md`

**Layer-header pattern** (`snowflake-schema.md` line 3) — MUST open every type file:
```markdown
> Layer: TYPE recipe. Composes primitives from [`../kb/`](../kb/README.md) and the shared [`compartmented-box.md`](./compartmented-box.md) construction; does not re-derive their geometry. Indexed in [`README.md`](./README.md).
```
Adapt: sequence composes `@../kb/lifeline-activation.md` + `@./notation-conventions.md`; no compartmented-box dividers are needed for participant heads.

**"Reuse verbatim — do not re-derive" framing** (`snowflake-schema.md` lines 25–30):
```markdown
Snowflake **reuses the star schema's compartmented-box geometry VERBATIM** — do not
re-derive any box offset numbers. All parametric offsets ... are locked in
[`@./compartmented-box.md`](./compartmented-box.md) ...
```
Adapt: sequence **reuses `kb/lifeline-activation.md` VERBATIM** — do not re-derive participant spacing, activation bar width, or message Y pitch. All geometry is pinned there.

**Step-by-step "How to draw it" structure** (`snowflake-schema.md` lines 33–71) — numbered steps, each citing a primitive by `@`-ref. Sequence steps:
1. Place participant head boxes per `@../kb/lifeline-activation.md` geometry (120px wide, 40px high, 180px pitch)
2. Draw dashed vertical lifeline `line` from each head's bottom center per `@../kb/lifeline-activation.md`
3. Draw activation bar `rectangle` for each active participant per `@../kb/lifeline-activation.md` (x = lifeline_center_x - 6)
4. Draw message arrows (solid `arrow` for calls, dashed `arrow` for returns) per `@./notation-conventions.md` (Association + Dependency rows); bind to activation bars NOT lifeline lines; enforce monotonic Y
5. Add message text labels with `fontFamily: 3`, `fontSize: 16`

**Binding rules block** (`snowflake-schema.md` lines 65–72) — copy and adapt for sequence:
```markdown
- `endArrowhead: "arrow"` on all message arrows. Returns use `strokeStyle: "dashed"`.
  No `crowsfoot`/`diamond`/`hollow` tokens.
- Every arrow's start and end points must land within 8px of a **rectangle** border.
  Bind via `startBinding`/`endBinding` to activation bar rectangle ids (or participant
  head rectangle ids when no activation bar is active at that point).
- NEVER bind message arrows to `line` elements (lifelines are line elements; they are
  NOT bindable targets for `check_arrow_endpoint_unanchored`).
```

**"Composes (primitive layer)" section** (`snowflake-schema.md` lines 74–86):
```markdown
## Composes (primitive layer)
- [`@../kb/lifeline-activation.md`](../kb/lifeline-activation.md) — all geometry ...
- [`@./notation-conventions.md`](./notation-conventions.md) — legal-encoding table ...
- [`@./compartmented-box.md`](./compartmented-box.md) — participant head box header
  height (40px) used verbatim; no compartment dividers needed.
```

**"Ground truth" section** (`snowflake-schema.md` lines 87–94) — point at `../examples/sequence_<subject>.png`.

---

### `diagram-types/use-case.md` (NEW type recipe)

**Analog:** `.claude/agents/excalidraw/diagram-types/activity.md`

Use-case is a pure-composition type (no new primitive) — `activity.md` is the best structural match because it is also a pure-composition type that lists existing `kb/` primitives without introducing new geometry.

**Layer-header pattern** (`activity.md` line 3) — identical boilerplate:
```markdown
> Layer: TYPE recipe. Composes primitives from [`../kb/`](../kb/README.md); does not re-derive their geometry. Indexed in [`README.md`](./README.md).
```

**"How to draw it" bullet list pattern** (`activity.md` lines 13–24) — bullet-per-element-type, each citing the KB source. Use-case bullets:
- Actor = `rectangle` (100px wide, 60px high) + two `text` elements (`«actor»` stereotype and actor name) per `@./notation-conventions.md` DTKB-04 (labelled-box convention; NOT stick-figure, NOT emoji)
- Use-case oval = native `ellipse` (`roughness: 0`, no `roundness` override needed, `backgroundColor: "transparent"`) with a sibling `text` label; group both under one `groupIds` id
- System boundary = `@../kb/group-container.md` rectangle (the one existing system-boundary primitive); the `group-container`'s `roundness: { type: 3 }` is its natural form — this is the one place where rounded-rectangle is correct
- Association (actor to oval) = `arrow` with `endArrowhead: null`, `startArrowhead: null`, `strokeStyle: "solid"`, bound to actor `rectangle` and oval `ellipse`
- Include/extend = `arrow` with `endArrowhead: "arrow"`, `strokeStyle: "dashed"` + sibling `text` label (`«include»` or `«extend»`) per `@./notation-conventions.md` Dependency row

**"Composes (primitive layer)" section** (`activity.md` lines 26–33):
```markdown
## Composes (primitive layer)
- [`@../kb/group-container.md`](../kb/group-container.md) — system boundary (bordered
  rounded rectangle that scopes all use cases inside it).
- [`@./notation-conventions.md`](./notation-conventions.md) — actor=labelled-box
  convention (DTKB-04); legal arrowhead tokens; Association + Dependency encodings.
```

**"Ground truth" section** (`activity.md` lines 35–37) — point at `../examples/use_case_<subject>.png`.

---

### `diagram-types/README.md` (EDIT — wire resolver rows)

**Analog:** itself — existing _(planned)_ rows at lines 25 and 27:
```markdown
| UML | sequence | `sequence.md` _(planned — Phase 8)_ | timeline, task-list, icon-block (+ lifeline/activation primitive) | _(planned)_ |
| UML | use-case | `use-case.md` _(planned — Phase 8)_ | group-container, fan-out, icon-block (+ stick-figure/oval) | _(planned)_ |
```

**Procedure to follow** (README lines 48–55 "Adding a diagram type") — same 4-step procedure used for all prior phases.

**Exact edits required:**
1. Replace `sequence` row — type file: `sequence.md`, Composes: `lifeline-activation, notation-conventions`, Example PNG: `../examples/sequence_<subject>.png`
2. Replace `use-case` row — type file: `use-case.md`, Composes: `group-container, notation-conventions`, Example PNG: `../examples/use_case_<subject>.png`
3. Add both to the "Wired rows" note paragraph (line 30)
4. Add `> Used by types:` back-refs — `kb/lifeline-activation.md` adds `, sequence`; `kb/group-container.md` adds `, use-case` to its existing `> Used by types: tech-architecture, activity, star-schema` line (line 3)

**CRITICAL (Pitfall 5 / EX-03 gate):** wire ONLY after each canonical example passes `validate_and_render.sh` + structural verifier green + EX-03 human visual approval. Sequence and use-case resolver rows are independent — wire each when its own example passes, not together.

---

### `examples_excalidraw/sequence_<subject>.excalidraw` (NEW JSON ground truth)

**Analog:** `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw`

**Top-level file envelope** — same keys as all existing examples: `type, version, source, elements, appState, files`.

**Element inventory for a 3-participant login sequence (recommended subject):**
- 3 participant head `rectangle` elements (120×40, `roughness: 0`, `roundness: null`, mild fill)
- 3 `text` elements for participant names (`fontFamily: 3`, `fontSize: 16`)
- 3 lifeline `line` elements (dashed, vertical, `points: [[0,0],[0,height]]`)
- 2–3 activation bar `rectangle` elements (12px wide, `roughness: 0`, `roundness: null`, white fill)
- 4–6 message `arrow` elements (solid or dashed, `elbowed: true`, `roundness: null`, bound to activation bars or participant heads)
- 4–6 message label `text` elements

**Participant head rectangle** (from RESEARCH.md Code Examples):
```jsonc
{ "type":"rectangle","x":200,"y":60,"width":120,"height":40,
  "roughness":0,"roundness":null,"strokeStyle":"solid",
  "backgroundColor":"#e0f2fe","strokeColor":"#1e1e1e",
  "groupIds":["participant_user"],"id":"ptcpt_user_head" }
```

**Lifeline line** (from RESEARCH.md Code Examples):
```jsonc
{ "type":"line","x":260,"y":100,"width":0,"height":400,
  "points":[[0,0],[0,400]],
  "roughness":0,"strokeStyle":"dashed","strokeColor":"#1e1e1e",
  "roundness":null,"groupIds":["participant_user"] }
```
Note: line.x = lifeline_center_x (= ptcpt.x + ptcpt.width/2 = 200+60 = 260); width is 0.

**Activation bar rectangle** (from RESEARCH.md Code Examples):
```jsonc
{ "type":"rectangle","x":254,"y":140,"width":12,"height":80,
  "roughness":0,"roundness":null,"strokeStyle":"solid",
  "backgroundColor":"#ffffff","strokeColor":"#1e1e1e",
  "groupIds":["participant_user_activation_1"],"id":"activation_user_1" }
```
Note: x = 260 - 6 = 254 (lifeline_center_x - ACTIVATION_BAR_WIDTH/2).

**Solid message arrow** (bound to activation bar rectangles):
```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"solid",
  "strokeColor":"#1e1e1e",
  "startBinding":{"elementId":"activation_user_1","gap":4},
  "endBinding":{"elementId":"activation_server_1","gap":4},
  "x":266,"y":160,"points":[[0,0],[130,0]],"groupIds":[] }
```

**Dashed return arrow**:
```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"dashed",
  "strokeColor":"#1e1e1e",
  "startBinding":{"elementId":"activation_server_1","gap":4},
  "endBinding":{"elementId":"activation_user_1","gap":4},
  "x":396,"y":200,"points":[[0,0],[-130,0]],"groupIds":[] }
```

**DO NOT imitate** `star_schema.excalidraw` (grandfathered, non-compliant). Imitate `snowflake_schema.excalidraw` for envelope/connector structure; add the lifeline/activation shapes from `kb/lifeline-activation.md`.

---

### `examples_excalidraw/use_case_<subject>.excalidraw` (NEW JSON ground truth)

**Analog:** `.claude/agents/excalidraw/examples_excalidraw/snowflake_schema.excalidraw`

**Recommended subject:** e-commerce Checkout System — 2 actors (Customer, Admin), 5 use cases (Browse Products, Add to Cart, Place Order, Process Payment, View Reports), 1 `<<include>>` (Place Order includes Process Payment), 1 system boundary group-container.

**Actor (labelled box — committed convention)** (from RESEARCH.md Code Examples):
```jsonc
{ "type":"rectangle","x":100,"y":200,"width":100,"height":60,
  "roughness":0,"roundness":null,"backgroundColor":"transparent",
  "strokeColor":"#1e1e1e","groupIds":["actor_customer"],"id":"actor_customer_box" }
{ "type":"text","text":"«actor»","fontFamily":3,"fontSize":14,
  "strokeColor":"#1e1e1e","x":130,"y":205,"width":60,"height":20,
  "groupIds":["actor_customer"] }
{ "type":"text","text":"Customer","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":112,"y":225,"width":80,"height":20,
  "groupIds":["actor_customer"] }
```

**Use-case oval** (from RESEARCH.md Code Examples):
```jsonc
{ "type":"ellipse","x":300,"y":200,"width":160,"height":60,
  "roughness":0,"strokeStyle":"solid","backgroundColor":"transparent",
  "strokeColor":"#1e1e1e","groupIds":["uc_login"],"id":"uc_login_oval" }
{ "type":"text","text":"Login","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":355,"y":222,"width":60,"height":20,
  "groupIds":["uc_login"] }
```

**System boundary** — use `group-container.md` JSON skeleton rectangle (`roundness: { type: 3 }` IS correct here — this is the one place where rounded is intentional):
```jsonc
{ "type":"rectangle","x":240,"y":100,"width":500,"height":400,
  "backgroundColor":"transparent","strokeColor":"#1e3a5f",
  "strokeWidth":2,"roughness":0,"roundness":{"type":3} }
```

**Association arrow** (undirected — both arrowheads null):
```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":null,"startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"actor_customer_box","gap":4},
  "endBinding":{"elementId":"uc_login_oval","gap":4},"groupIds":[] }
```

**Include/extend arrow** (dashed + text label):
```jsonc
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"dashed",
  "startBinding":{"elementId":"uc_place_order_oval","gap":4},
  "endBinding":{"elementId":"uc_process_payment_oval","gap":4},
  "groupIds":["rel_include_1"] }
{ "type":"text","text":"«include»","fontFamily":3,"fontSize":14,
  "strokeColor":"#1e1e1e","x":350,"y":170,"width":80,"height":20 }
```

---

### `scripts/verifier/verifier_structural.py` (OPTIONAL EDIT — center-x check) — DECISION-GATED

**Analog:** itself — the existing check list confirmed by RESEARCH.md: `check_arrow_endpoint_unanchored`, `check_arrow_not_elbow`, `check_raw_emoji_in_text`, `check_text_overflow_static`, `check_roughness_nonzero`, `check_fontfamily_nonmonospace`, `check_arrow_points_too_few`.

**If the center-x check is adopted (Open Question 1 — recommended YES):**

The new check mirrors the shape of existing checks (each is a standalone function returning a list of issues). Pattern from the existing label-deny-list loops in `excalidraw_validator.py` lines 30–37:
```python
for el in elements:
    if el.get("type") in ["rectangle", "ellipse", "diamond"] and "label" in el:
        shapes_with_labels.append(el.get("id", "unknown"))
if shapes_with_labels:
    errors.append(f"Found 'label' property in shapes: ...")
```

New check structure (conceptual — exact line numbers assigned during authoring):
```python
def check_sequence_activation_center_x(elements):
    issues = []
    line_elements = [e for e in elements if e.get("type") == "line"
                     and e.get("strokeStyle") == "dashed"
                     and e.get("width", 0) == 0]
    activation_bars = [e for e in elements if e.get("type") == "rectangle"
                       and 10 <= e.get("width", 0) <= 16]
    for bar in activation_bars:
        bar_center_x = bar["x"] + bar["width"] / 2
        nearby_lines = [l for l in line_elements
                        if abs(l["x"] - bar_center_x) < 8]
        if nearby_lines:
            for line in nearby_lines:
                if abs(line["x"] - bar_center_x) > 1:
                    issues.append({
                        "check": "activation_bar_center_x_mismatch",
                        "element_id": bar.get("id", "unknown"),
                        "severity": "error",
                        "detail": f"Activation bar center x {bar_center_x} != "
                                  f"nearest lifeline x {line['x']}",
                        "suggested_fix": f"Set bar x to {line['x'] - bar['width']/2}"
                    })
    return issues
```

**Gate (A3 / Open Question 1 from RESEARCH.md):** RESEARCH recommends adding the center-x check (simpler) and DEFERRING the monotonic-Y check (complex, visual review covers it). Planner MUST surface this decision explicitly. If declined, record that SC-1 ("activation bars centered on lifeline x") has no automated guard and relies on KB discipline + verifier visual review only.

---

## Shared Patterns

### Locked notation encoding (reference, never re-derive)
**Source:** `diagram-types/notation-conventions.md` (DTKB-04)
**Apply to:** `kb/lifeline-activation.md`, `sequence.md`, `use-case.md`, both example JSON files
```
Legal arrowhead tokens ONLY: arrow | bar | dot | triangle | null
Sequence message (call):  arrow + solid  (Association row)
Sequence return:          arrow + dashed (Dependency row)
Use-case association:     null/null + solid
Use-case include/extend:  arrow + dashed (Dependency row) + «include»/«extend» text label
Actor = labelled-box (rectangle + «actor» text) — committed DTKB-04, NOT stick-figure, NOT emoji
```

### KB two-layer cross-reference discipline
**Source:** `diagram-types/README.md` lines 7–12 + `kb/relationship-endpoint.md` line 3 + `kb/tree-hierarchy.md` line 3
**Apply to:** `kb/lifeline-activation.md` (carries `> Used by types: sequence`), `sequence.md`/`use-case.md` (link DOWN via `@../kb/` refs), README resolver (both directions), `kb/group-container.md` (add `, use-case` to its `> Used by types:` back-ref)
```
Type files compose by @-reference; NEVER contain coordinate math.
Geometry lives ONLY in kb/ primitives.
Every composed primitive carries > Used by types: <type-list> so the two layers cannot drift.
```

### Verifier structural guard (what must stay green — read-only for sequence/use-case authoring)
**Source:** `scripts/verifier/verifier_structural.py` — existing checks confirmed by RESEARCH.md:
`check_arrow_endpoint_unanchored` (tolerance 8px, accepts rectangle/ellipse/diamond borders — lifeline `line` elements are NOT accepted), `check_arrow_not_elbow` (all connectors must be `elbowed: true`), `check_raw_emoji_in_text` (no raw emoji under `fontFamily: 3`), `check_text_overflow_static`, `check_fontfamily_nonmonospace`, `check_roughness_nonzero`.

**CONFIRMED GAP (RESEARCH.md Open Question 1):** no monotonic-Y check exists. Center-x check is recommended additive addition (Decision-gated). Monotonic-Y is deferred to KB discipline + visual review.

### EX-03 gate discipline (Phase 7 pattern — carried forward identically)
**Source:** Phase 7 pattern; `diagram-types/README.md` lines 30, 52–55; RESEARCH.md Pattern 4 / Pitfall 5
**Apply to:** both resolver row edits
```
Wire resolver row ONLY after:
  1. validate_and_render.sh exits 0
  2. verifier_structural.py issues == []
  3. EX-03 human visual approval of the rendered PNG
Sequence and use-case rows are independent — wire each when its own example passes.
Never wire a placeholder row speculatively.
```

---

## No Analog Found

None. Every artifact has a directly-shipped Phase 4–7 analog. The only PARTIALLY-novel content is the *deferred pixel values* inside `kb/lifeline-activation.md` (participant head width 120px, lifeline pitch 180px, activation bar width 12px, message Y pitch 40px) — these are first-pass design numbers (MEDIUM confidence, ASSUMED per RESEARCH.md A1) to be confirmed empirically through the loop. The *file structure* that holds them is the `relationship-endpoint.md` primitive template (exact match).

---

## Metadata

**Analog search scope:** `.claude/agents/excalidraw/diagram-types/`, `.claude/agents/excalidraw/kb/`, `.claude/agents/excalidraw/examples_excalidraw/`, `.claude/agents/excalidraw/scripts/verifier/`
**Files scanned (read in full):** `relationship-endpoint.md`, `tree-hierarchy.md`, `group-container.md`, `snowflake-schema.md`, `activity.md`, `diagram-types/README.md` (first 60 lines), Phase 7 PATTERNS.md
**Pattern extraction date:** 2026-06-07
