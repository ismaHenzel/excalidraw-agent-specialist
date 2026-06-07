# Phase 8: Sequence + Use-Case — Research

**Researched:** 2026-06-07
**Domain:** Excalidraw `.excalidraw` JSON authoring — two new UML primitives: (1) lifeline + activation-bar geometry (sequence diagrams) and (2) actor-as-labelled-box + system-boundary (use-case diagrams), both composed against the frozen v1.0 loop
**Confidence:** HIGH (all conventions already locked in-repo; geometry from Pitfalls.md + SUMMARY.md research flags; verifier source read directly)

---

## Summary

Phase 8 ships the two remaining UML core types. Each introduces its own independent new primitive that does NOT overlap with Phase 7:

- **Sequence** introduces `kb/lifeline-activation.md` — the geometry-heavy primitive that pins per-participant center-x discipline, monotonically increasing message Y values, and activation-bar sizing. The verifier needs two additive structural checks (monotonic-Y guard, center-x alignment) that the project research (PITFALLS.md Pitfall 4, SUMMARY.md) flagged as Phase 8's counterpart to Phase 7's arrowhead-legality check.
- **Use-case** is the most native-friendly UML type in this constrained environment: native `ellipse` elements for use-case ovals, the already-committed actor-as-labelled-box convention (locked in `notation-conventions.md`), and the existing `group-container` primitive for the system boundary. Use-case introduces no new KB primitive — it composes entirely from existing elements.

The phase follows the same shape as Phase 7: a shared primitive is built first, then both type recipes are authored against it, then canonical examples are produced and pass the full loop, and finally resolver rows are wired. The analogy is exact:

| Phase 7 | Phase 8 |
|---------|---------|
| `kb/relationship-endpoint.md` (new primitive) | `kb/lifeline-activation.md` (new primitive) |
| `diagram-types/er.md` (uses primitive) | `diagram-types/sequence.md` (uses primitive) |
| `diagram-types/class.md` (uses primitive) | `diagram-types/use-case.md` (pure composition, no new primitive) |
| Resolver rows wired last (EX-03 gate) | Resolver rows wired last (EX-03 gate) |

**Primary recommendation:** Build `kb/lifeline-activation.md` first (pins the deferred lifeline/activation geometry), author `sequence.md` against it, produce the canonical sequence example through the full loop, then author `use-case.md` composing group-container + notation-conventions (actor=labelled-box), produce the canonical use-case example, and wire both resolver rows only after both examples pass the EX-03 visual gate.

**Phase 8 depends on Phase 7 completing** (Plans 02 + 03 + 04 must be done before any Phase 8 plan executes — `class.md`, `class_order_domain.excalidraw`, and both wired resolver rows must exist). The research findings below assume Phase 7 has delivered its full scope, consistent with the ROADMAP.

---

## Architectural Responsibility Map

This phase has no runtime tiers. The "tiers" are the KB layers and the validate→render→verify pipeline stages.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Lifeline + activation-bar pixel geometry | NEW `kb/lifeline-activation.md` (PRIMITIVE layer) | `notation-conventions.md` (convention) | Per two-layer rule, geometry/JSON skeletons live only in `kb/`; type files reference, never re-derive |
| Sequence type recipe (assembly) | NEW `diagram-types/sequence.md` (TYPE layer) | `kb/lifeline-activation.md` + `notation-conventions.md` | TYPE layer composes primitives by `@`-reference |
| Actor convention (committed) | `diagram-types/notation-conventions.md` (already locked) | — | DTKB-04 committed actor=labelled-box; no re-derive needed |
| System-boundary group container | `kb/group-container.md` (already exists) | — | Reused verbatim; `Used by types:` back-ref must be added |
| Use-case ovals | Native `ellipse` elements (no primitive needed) | — | Native shape; geometry is straightforward and type-local |
| Use-case type recipe (assembly) | NEW `diagram-types/use-case.md` (TYPE layer) | `kb/group-container.md` + `notation-conventions.md` | TYPE layer composes existing primitives by `@`-reference |
| Monotonic-Y + center-x structural guard | `scripts/verifier/verifier_structural.py` (Phase-1 verifier) | KB discipline + visual review | Currently UNGUARDED for sequence geometry — same gap as Phase 7's arrowhead check |
| Resolver wiring | `diagram-types/README.md` (single authoritative table) | — | Wire ONLY after both canonical examples pass EX-03 gate (Pitfall 6) |

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| UML-01 | `diagram-types/sequence.md` recipe exists; agent authors a sequence diagram (lifelines, activation bars, ordered solid messages, dashed returns) that passes the full loop | Locked actor convention (labelled-box) in `notation-conventions.md`. Lifeline/activation geometry deferred to this phase per PITFALLS.md Pitfall 4 and SUMMARY.md research flag. Message=`arrow`+solid; return=`arrow`+dashed; locked arrowhead tokens apply. Success Criteria 1 adds center-x and monotonic-Y requirements that need structural verifier assertions. |
| UML-03 | `diagram-types/use-case.md` recipe exists; agent authors a use-case diagram (actors, ovals, system boundary via group-container) that passes the full loop | Actor=labelled-box locked in `notation-conventions.md` (DTKB-04). System boundary = `group-container` primitive (already exists). Use-case ovals = native `ellipse`. Association = `arrow`+solid (legal token). Include/extend relationships = `arrow`+dashed with text label (FEATURES.md / SUMMARY.md convention for `<<include>>`/`<<extend>>`). |
</phase_requirements>

---

## Standard Stack

**This milestone has no software-dependency "stack"** (confirmed by `.planning/research/STACK.md` and all prior phases). The "stack" is the Excalidraw v2 schema vocabulary as exposed by the pinned `@excalidraw/excalidraw@0.17.3`. No packages are installed in this phase.

### Core schema vocabulary used by Sequence + Use-Case

| Element type | Purpose this phase | Key locked properties |
|--------------|--------------------|-----------------------|
| `rectangle` | Participant head box (sequence); actor labelled box (use-case); activation bar (sequence) | `roundness: null`, `roughness: 0` for formal notation; participant heads may use mild fill |
| `line` | Lifelines (dashed, vertical, extending from participant head) | `strokeStyle: "dashed"`, `roundness: null`, vertical segment `points=[[0,0],[0,height]]` |
| `arrow` | Message arrows (sequence); association + include/extend (use-case) | `elbowed: true`, `roundness: null`, `endArrowhead` ∈ `{arrow,bar,dot,triangle,null}` only |
| `ellipse` | Use-case ovals (the primary use-case shape) | `roundness: null` not required (ellipses are naturally round); `roughness: 0` |
| `text` | All labels (participant names, message labels, actor names, use-case text, multiplicity) | `fontFamily: 3` (Cascadia monospace), `fontSize: 16` for formal labels |
| `rectangle` (activation bar) | Thin narrow rectangle overlaid on lifeline, centered on lifeline x | `width: 12` (or `16`), `height` = span from first to last message touching this activation; centered on lifeline center-x |

**Version verification:** No registry install this phase. `@excalidraw/excalidraw@0.17.3` is the already-pinned version; the five legal arrowhead tokens are confirmed in-repo by `notation-conventions.md` and `STACK.md`. [VERIFIED: in-repo notation-conventions.md + .planning/research/STACK.md]

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Actor = labelled rectangle + text (`«actor» Name`) | Composed stick-figure (head ellipse + body lines) | **EXPLICITLY NOT USED** — locked by DTKB-04 (`notation-conventions.md`); labelled-box is the committed default; stick-figure geometry is fragile under monospace constraint and has no glyph primitive in the codebase |
| Dashed `line` for lifelines | Dashed `arrow` for lifelines | `line` is correct; arrows carry arrowheads and endpoint-anchor checks that lifelines do not need |
| `<<include>>`/`<<extend>>` as a dedicated arrowhead token | Text label (`«include»`) on a dashed `arrow` | No dedicated token exists; committed workaround is dashed `arrow` + text label — exactly the `dependency` encoding already locked in `notation-conventions.md` |

---

## Package Legitimacy Audit

**Not applicable.** This phase installs no external packages. It authors `.excalidraw` JSON, Markdown KB files, and an optional Python addition to the verifier. No npm/PyPI/crates dependency is added, so the Package Legitimacy Gate is skipped (documented per protocol — same as Phase 7).

---

## Architecture Patterns

### System Architecture Diagram (the authoring + verify flow)

```
User request ("draw a sequence diagram of login flow")
        │
        ▼
/excalidraw  ──► family pick (UML) ──► type sub-pick (sequence | use-case)
        │
        ▼
diagram-types/README.md  (single resolver table)
        │  resolves type → recipe file + kb sub-patterns + example PNG
        ▼
excalidraw_specialist  reads  diagram-types/<type>.md  FIRST  (INT-01)
        │      └─►  @kb/lifeline-activation.md  (NEW — sequence only)
        │      └─►  @kb/group-container.md  (use-case system boundary)
        │      └─►  @diagram-types/notation-conventions.md  (legal-encoding table)
        ▼
authors  <name>.excalidraw  JSON
        │
        ▼
scripts/render/validate_and_render.sh
   ├─ Phase 1: excalidraw_validator.py      ◄── arrowhead-legality check ADDED (Phase 7)
   ├─ Phase 2: render_docker.sh → PNG
   └─ Phase 3: instruction to read PNG
        │
        ▼
excalidraw_verifier  (structural: verifier_structural.py  +  visual multimodal review)
   ├─ structural: emoji, overflow, unanchored-arrow, roughness, fontFamily, elbow…
   │     ◄── ⚠ does NOT check monotonic message Y or activation center-x (Phase 8 gap)
   └─ visual: "are messages in the right order? are lifelines visible?"
        │
        ▼
   passed:false ──► specialist auto-fixes (≤3 iterations) ──► re-render ──► re-verify
   passed:true  ──► (human-verify gate / EX-03) ──► wire resolver row
```

### Recommended File Structure (additive)

```
.claude/agents/excalidraw/
├── kb/
│   └── lifeline-activation.md      # NEW primitive: lifeline + activation-bar geometry
├── diagram-types/
│   ├── sequence.md                  # NEW type recipe (UML-01)
│   ├── use-case.md                  # NEW type recipe (UML-03)
│   ├── README.md                    # EDIT: wire sequence + use-case resolver rows
│   ├── notation-conventions.md      # REFERENCE only (actor convention already locked)
│   └── group-container.md           # REFERENCE only (for use-case system boundary)
├── examples_excalidraw/
│   ├── sequence_<subject>.excalidraw  # NEW canonical source
│   └── use_case_<subject>.excalidraw  # NEW canonical source
└── examples/
    ├── sequence_<subject>.png         # NEW rendered (sibling, passes loop)
    └── use_case_<subject>.png         # NEW rendered (sibling, passes loop)
```

### Pattern 1: Lifeline-activation primitive — the geometry anchor for sequence diagrams

**What:** Pin participant center-x values, lifeline height, activation-bar width/placement, and message Y pitch ONCE in `kb/lifeline-activation.md`. `sequence.md` `@`-references it. This is exactly how `er.md` and `class.md` reference `kb/relationship-endpoint.md` — Phase 8's geometry work is done exactly once, in the primitive.

**When to use:** Every sequence diagram element that relates to time-ordering or participant alignment.

**Key geometry decisions to pin in the primitive (deferred to this phase by SUMMARY.md):**

| Property | Recommended value | Rationale |
|----------|------------------|-----------|
| Participant head box width | 120px | Typical name length ≤ 10 chars; `10 * 0.6 * 16 = 96px` + margin → 120px on 20-grid |
| Participant head box height | 40px | Matches compartmented-box header height convention |
| Lifeline center-x pitch | 180px (adjacent participants) | Leaves ~60px corridor on each side of participant head for message routing |
| Activation bar width | 12px | Visible at typical diagram zoom; narrower than participant head; centered on lifeline x |
| Activation bar x | `lifeline_center_x - 6` (half of 12px) | Ensures bar center == lifeline center exactly |
| Message Y pitch | 40px per message (minimum) | Provides visual separation; `2x` the row pitch of compartmented boxes |
| Lifeline `line` element | dashed, from `participant_head_bottom_y` to `diagram_bottom_y` | `strokeStyle: "dashed"`, `points=[[0,0],[0,lifeline_height]]` |

**Why these numbers matter:** PITFALLS.md Pitfall 4 is explicit — lifeline center-x and activation bar center-x MUST match, and message Ys MUST be monotonically non-decreasing. Any deviation produces an unreadable sequence. Pinning the numbers in the primitive front-loads correctness so the first render is close; the 3-iteration loop is for polish.

[ASSUMED] — The recommended pixel values above are derived from the project's established 20-grid convention and the compartmented-box precedent; they have not been verified by executing a render. The authoring agent confirms or adjusts through the loop.

### Pattern 2: Use-case native composition (no new primitive needed)

**What:** Use-case uses entirely native Excalidraw elements that already have KB support:
- Use-case ovals = `ellipse` (native, no special primitive)
- Actors = labelled rectangle + text (`«actor» ActorName`) per locked `notation-conventions.md`
- System boundary = `group-container` primitive (already exists in `kb/group-container.md`)
- Association = `arrow` + solid (already in `notation-conventions.md`)
- Include/Extend = `arrow` + dashed + text label (`«include»`/`«extend»`)

**When to use:** All use-case diagrams. The simplest UML type to draw in this system.

**Example pattern — use-case oval:**
```jsonc
// Source: native ellipse element, SUMMARY.md element list
{ "type":"ellipse","x":300,"y":200,"width":160,"height":60,
  "roughness":0,"strokeStyle":"solid","backgroundColor":"transparent",
  "strokeColor":"#1e1e1e",
  "groupIds":[] }
// Label inside or below the oval:
{ "type":"text","text":"Login","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":340,"y":220 }
```

**Example pattern — actor (labelled box per notation-conventions.md):**
```jsonc
// Actor = rectangle + text label with «actor» stereotype — NOT a stick figure
{ "type":"rectangle","x":100,"y":200,"width":100,"height":40,
  "roughness":0,"roundness":null,"backgroundColor":"transparent",
  "strokeColor":"#1e1e1e","groupIds":["actor_user"] }
{ "type":"text","text":"«actor»","fontFamily":3,"fontSize":14,
  "strokeColor":"#1e1e1e","x":130,"y":205,"groupIds":["actor_user"] }
{ "type":"text","text":"User","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":130,"y":220,"groupIds":["actor_user"] }
```

[ASSUMED] — Exact sizing (actor box 100x40, actor label placement) is derived from the compartmented-box left-pad precedent; confirm through the loop.

### Pattern 3: Sequence message encoding (two types)

**What:** Two kinds of arrows in sequence diagrams, both using existing legal tokens:
1. **Synchronous call / message**: solid `arrow` with `endArrowhead: "arrow"` — exactly `Association` from `notation-conventions.md`
2. **Return / response**: dashed `arrow` with `endArrowhead: "arrow"` + `strokeStyle: "dashed"` — exactly `Dependency` from `notation-conventions.md`

Neither type is new. The only new constraint is **message order**: message Y values must be strictly increasing (top = first message, bottom = last).

```jsonc
// Synchronous message (solid arrow)
// Source: notation-conventions.md Association row
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"<lifeline_rect_id_of_sender>","gap":4},
  "endBinding":{"elementId":"<activation_bar_rect_id_of_receiver>","gap":4},
  "x":220,"y":160,"points":[[0,0],[120,0]] }

// Return message (dashed arrow)
// Source: notation-conventions.md Dependency row
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"dashed",
  "startBinding":{"elementId":"<activation_bar_rect_id_of_callee>","gap":4},
  "endBinding":{"elementId":"<lifeline_rect_id_or_activation_of_caller>","gap":4},
  "x":340,"y":200,"points":[[0,0],[-120,0]] }
```

**Key constraint:** Message arrow Y values in the JSON must represent a monotonically non-decreasing sequence (first message at lowest Y, last at highest Y). [VERIFIED: PITFALLS.md Pitfall 4]

### Pattern 4: Resolver rows wired LAST (EX-03 gate)

**What:** `diagram-types/README.md` resolver rows for `sequence` and `use-case` are wired only AFTER each example passes the full validate→render→verify loop with EX-03 human visual approval.

**When to use:** After each canonical example pair is authored AND passes the full loop. Never before.

**Why this matters:** Pitfall 6 — indexing broken ground truth means the specialist imitates the broken example in every future diagram of that type forever. Sequence is especially sensitive because geometry errors are silent until the PNG is rendered.

### Anti-Patterns to Avoid

- **Self-message (actor to itself) with zero-width route:** Self-messages need a small rectangular loop — a horizontal arm to the right, vertical drop, horizontal arm back. Never two collinear points at the same x (zero-width segment). [ASSUMED] — standard UML self-message layout; confirm sizing through the loop.
- **Activation bar NOT centered on lifeline:** If `bar.x != lifeline_x - bar.width/2`, the visual shows the bar floating beside the line — fails verifier visual check and looks wrong. Pin using the formula.
- **Message Y values out of order:** If message 3 has a lower Y than message 2, the diagram reads in the wrong sequence — the single most dangerous sequence-diagram defect. Monotonic Y is the ordering mechanism.
- **Use-case oval with `roundness: null`:** Ellipses are inherently elliptical; `roundness: null` is for sharp rectangles. Omit roundness from ellipses or leave at default.
- **`include`/`extend` using a solid arrow:** Must be dashed (`strokeStyle: "dashed"`) to be visually distinct from plain association — mirror the `Dependency` encoding.
- **Emoji or stick-figure for actors:** The committed convention is labelled-box. Stick-figure requires composed geometry not documented in any KB primitive. Emoji renders as tofu. [VERIFIED: notation-conventions.md]

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Lifeline + activation geometry | Per-diagram lifeline center-x / bar offsets in `sequence.md` | ONE `kb/lifeline-activation.md` primitive `@`-referenced by `sequence.md` | Two-layer rule; "deferred to this phase" note in SUMMARY.md; mirrors how `er.md`/`class.md` reference `kb/relationship-endpoint.md` |
| Actor representation | Ad-hoc per-diagram stick-figure or emoji | Actor=labelled-box locked in `notation-conventions.md` (DTKB-04) | Convention is committed; mixing representations looks like a bug |
| System boundary | New "swimlane" or bespoke frame | `group-container` primitive (`kb/group-container.md`) already exists | Exact match: group-container is a bordered rounded rectangle that carries context for everything inside it |
| Include/extend arrows | New arrowhead token | `arrow` + `strokeStyle:"dashed"` + text label `«include»`/`«extend»` | No dedicated token exists; committed workaround already in `notation-conventions.md` (Dependency row) |
| Compartmented box for participant heads | New box geometry | The standard compartmented-box offsets (header 40, left-pad 12) — but NO compartment dividers are needed for participant heads; just the rectangle + title text | Participant heads are simpler than class boxes — they do not need row dividers |

**Key insight:** Sequence's hard work is geometry discipline (center-x pinning, monotonic Y), not new element types. Use-case has essentially zero hard work — it is pure native element composition against already-locked conventions. The investment for this phase is concentrated in the lifeline-activation primitive and the optional verifier assertions.

---

## Runtime State Inventory

> Omitted — this is a greenfield KB-authoring phase (no rename, refactor, or migration). No runtime state is affected.

---

## Common Pitfalls

### Pitfall 1: Activation bar NOT centered on its lifeline (the silent geometry error)

**What goes wrong:** The activation bar rectangle is placed at `x = lifeline_x` instead of `x = lifeline_x - bar.width/2`. At typical diagram widths the 6px offset is visible — the bar appears to the right of the lifeline. Worse, if the lifeline is narrow, the bar may overlap or leave a gap.

**Why it happens:** The lifeline `line` element's x position is its left edge; it is easy to place the activation bar starting at that same x rather than centering.

**How to avoid:** Use the formula `activation_bar_x = lifeline_center_x - ACTIVATION_BAR_WIDTH/2` locked in `kb/lifeline-activation.md`. Document `lifeline_center_x` explicitly as the anchor (not the lifeline line element's left x).

**Warning signs:** Rendered PNG shows activation bar not perfectly bisected by the dashed lifeline; structural verifier (if the center-x check is added) reports mismatch.

### Pitfall 2: Message Y values not monotonically increasing (the sequence-order error)

**What goes wrong:** The author writes message arrows in the order they are easiest to calculate (perhaps grouping by participant) rather than in order of increasing Y. The rendered diagram appears to show messages out of temporal order — a critical semantic error.

**Why it happens:** Without a structural check, the order is invisible until the PNG is read. The author may believe Y=100 for message 2 and Y=80 for message 3 is fine because both "look right" on screen.

**How to avoid:** Always write message arrows with strictly non-decreasing Y values. The `kb/lifeline-activation.md` primitive documents a message Y pitch (minimum 40px between messages) and an example of how to lay out a 4-message exchange. Recommend adding a structural verifier check (see Wave 0 gap below).

**Warning signs:** A return arrow appears ABOVE its triggering call arrow in the rendered PNG; structural verifier (if added) reports out-of-order Y.

### Pitfall 3: Self-message collapses to zero width or overlaps activation bar

**What goes wrong:** An actor messaging itself (e.g., a service calling an internal method) is drawn as a connector from the lifeline back to the same lifeline. If the author uses two points at the same x, the route has zero width and renders as a dot or invisible. If the loop route overlaps the activation bar, the diagram reads as two separate messages.

**Why it happens:** Sequence diagram self-messages require a specific detour geometry — rightward arm, downward segment, return arm — which has no automatic routing in Excalidraw (elbowed arrows route to the nearest border, not to a detour).

**How to avoid:** For self-messages, use a 3-point elbow route: from the activation bar's right edge, go `+40px` right, then down `+40px`, then back to the same bar's right edge at a lower Y. The `kb/lifeline-activation.md` primitive should document this self-message geometry explicitly. [ASSUMED] — exact self-message route sizes to be confirmed through the loop.

**Warning signs:** Verifier visual review reports "self-message is not visible" or "self-message and activation bar overlap."

### Pitfall 4: Use-case association drawn with wrong arrowhead direction

**What goes wrong:** An association between actor and use-case should be a plain line (`endArrowhead: null`, `startArrowhead: null`) or a directed association (`endArrowhead: "arrow"`). The author may draw both ends with arrowheads, or use the wrong direction.

**Why it happens:** Use-case associations are often described as "lines" with no directionality, but in Excalidraw there is no "no-arrowhead" line type for `arrow` elements except `null`.

**How to avoid:** Actor–use-case associations use `endArrowhead: null`, `startArrowhead: null` for bidirectional (standard UML) OR `endArrowhead: "arrow"` for directed. `include`/`extend` relationships use `endArrowhead: "arrow"` + `strokeStyle: "dashed"`. All are legal tokens.

**Warning signs:** Arrow rendered with two heads; directionality looks reversed from intent.

### Pitfall 5: Canonical example indexed before it passes the loop (Pitfall 6 from Phase 7)

**What goes wrong:** A resolver row for `sequence`/`use-case` is wired while the example still fails verify — broken ground truth that the specialist imitates forever.

**How to avoid:** EX-01/EX-03 are exit criteria — example must pass full validate→render→verify (structural automated + EX-03 visual human approval) BEFORE the resolver row is wired. Phase 7 enforced this; Phase 8 must too.

**Warning signs:** Resolver row marked wired with no verifier pass on record.

### Pitfall 6: Message endpoint NOT anchored to an activatable shape

**What goes wrong:** Message arrow endpoints are placed as free coordinates instead of binding to the activation bar rectangle or participant head rectangle. The structural verifier's `check_arrow_endpoint_unanchored` raises an `error` because the endpoint is not within 8px of a rectangle/ellipse/diamond border.

**Why it happens:** Lifelines are `line` elements, not `rectangle` elements. Binding to a `line` element does not satisfy the anchor check (only `rectangle`, `ellipse`, `diamond` borders count). The author may naturally try to bind message endpoints to the lifeline line.

**How to avoid:** Message arrows bind to the **activation bar `rectangle`** (or the participant head `rectangle` if no activation bar is present at that point). The activation bar is the bindable shape on a lifeline, not the lifeline line itself. [VERIFIED: `scripts/verifier/verifier_structural.py` `check_arrow_endpoint_unanchored` — reads `_on_rectangle_border`, `_on_ellipse_border`, `_on_diamond_border` only; line elements are not accepted as anchor targets]

**Warning signs:** `arrow_endpoint_unanchored` error in the structural report; message arrow floats near but not attached to the lifeline.

---

## Code Examples

> Sources: in-repo locked conventions (`notation-conventions.md`), verifier source code (read directly), and the project research files (`PITFALLS.md` Pitfall 4, `SUMMARY.md` geometry notes). Coordinates are illustrative; the authoring agent computes exact values from the primitive.

### Sequence participant head

```jsonc
// Source: derived from compartmented-box.md header (40px), 20-grid convention
// Participant head: a plain rectangle (no compartment dividers needed)
{ "type":"rectangle","x":200,"y":60,"width":120,"height":40,
  "roughness":0,"roundness":null,"strokeStyle":"solid",
  "backgroundColor":"#e0f2fe","strokeColor":"#1e1e1e",
  "groupIds":["participant_user"],
  "id":"ptcpt_user_head" }
{ "type":"text","text":"User","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":220,"y":70,"width":80,"height":20,
  "groupIds":["participant_user"] }
```

### Sequence lifeline

```jsonc
// Source: PITFALLS.md Pitfall 4, SUMMARY.md
// Lifeline: dashed vertical line from bottom of participant head to bottom of diagram
// lifeline_center_x = participant_head.x + participant_head.width / 2 = 200+60 = 260
{ "type":"line","x":260,"y":100,"width":0,"height":400,
  "points":[[0,0],[0,400]],
  "roughness":0,"strokeStyle":"dashed","strokeColor":"#1e1e1e",
  "roundness":null,
  "groupIds":["participant_user"] }
```

### Sequence activation bar

```jsonc
// Source: PITFALLS.md Pitfall 4
// Activation bar centered on lifeline: x = lifeline_center_x - ACTIVATION_BAR_WIDTH/2
// ACTIVATION_BAR_WIDTH = 12px (recommended — verify through loop)
// lifeline_center_x = 260; activation_bar_x = 260 - 6 = 254
{ "type":"rectangle","x":254,"y":140,"width":12,"height":80,
  "roughness":0,"roundness":null,"strokeStyle":"solid",
  "backgroundColor":"#ffffff","strokeColor":"#1e1e1e",
  "groupIds":["participant_user_activation_1"],
  "id":"activation_user_1" }
```

### Sequence solid message (call)

```jsonc
// Source: notation-conventions.md — Association row (arrow + solid)
// Message arrow binds to activation bar rectangles (NOT to the lifeline line)
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"solid",
  "strokeColor":"#1e1e1e",
  "startBinding":{"elementId":"activation_user_1","gap":4},
  "endBinding":{"elementId":"activation_server_1","gap":4},
  "x":266,"y":160,"points":[[0,0],[130,0]],
  "groupIds":[] }
{ "type":"text","text":"login(username, pwd)","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":280,"y":145,"width":200,"height":20 }
```

### Sequence dashed return

```jsonc
// Source: notation-conventions.md — Dependency row (arrow + dashed)
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"dashed",
  "strokeColor":"#1e1e1e",
  "startBinding":{"elementId":"activation_server_1","gap":4},
  "endBinding":{"elementId":"activation_user_1","gap":4},
  "x":396,"y":200,"points":[[0,0],[-130,0]],
  "groupIds":[] }
{ "type":"text","text":"token","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":320,"y":185,"width":60,"height":20 }
```

### Use-case oval

```jsonc
// Source: SUMMARY.md element list — native ellipse element
{ "type":"ellipse","x":300,"y":200,"width":160,"height":60,
  "roughness":0,"strokeStyle":"solid","backgroundColor":"transparent",
  "strokeColor":"#1e1e1e","groupIds":["uc_login"],"id":"uc_login_oval" }
{ "type":"text","text":"Login","fontFamily":3,"fontSize":16,
  "strokeColor":"#1e1e1e","x":355,"y":222,"width":60,"height":20,
  "groupIds":["uc_login"] }
```

### Use-case actor (labelled box — committed convention)

```jsonc
// Source: notation-conventions.md — Actor row (committed: labelled box, NOT stick-figure)
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

### Use-case association (actor to oval)

```jsonc
// Source: notation-conventions.md — Association row (arrow + solid, or null/null for undirected)
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":null,"startArrowhead":null,"strokeStyle":"solid",
  "startBinding":{"elementId":"actor_customer_box","gap":4},
  "endBinding":{"elementId":"uc_login_oval","gap":4},
  "groupIds":[] }
```

### Use-case include/extend

```jsonc
// Source: notation-conventions.md — Dependency row (arrow + dashed) + stereotype text label
{ "type":"arrow","elbowed":true,"roundness":null,"roughness":0,
  "endArrowhead":"arrow","startArrowhead":null,"strokeStyle":"dashed",
  "startBinding":{"elementId":"uc_login_oval","gap":4},
  "endBinding":{"elementId":"uc_verify_pwd_oval","gap":4},
  "groupIds":["rel_include_1"] }
{ "type":"text","text":"«include»","fontFamily":3,"fontSize":14,
  "strokeColor":"#1e1e1e","x":350,"y":170,"width":80,"height":20 }
```

---

## State of the Art

Not applicable in the usual sense — this is a closed, pinned authoring environment. The relevant "state" changes are internal project milestones:

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Sequence/use-case lifeline/actor geometry "deferred to Phase 8" | This phase pins it in a primitive file (sequence) or composition recipe (use-case) | Phase 8 (now) | PITFALLS.md Pitfall 4 and SUMMARY.md research-flag items are satisfied |
| No monotonic-Y / center-x verifier assertion | (Recommended) structural checks added | Phase 8 if adopted | Silent geometry mis-order → loud Phase-structural error |
| Actor convention undecided (stick-figure vs labelled-box) | Labelled-box locked | Phase 4 (DTKB-04) | No decision to make — apply it |
| `include`/`extend` encoding undecided | Dashed `arrow` + text label | Phase 4 (DTKB-04) via Dependency row | No decision to make — apply it |

**Deprecated/outdated:**
- Stick-figure actor: explicitly NOT used per `notation-conventions.md`. Do not introduce.
- Crow's-foot or diamond arrowhead tokens: already blocked by the Phase 7 arrowhead-legality validator check.

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Recommended activation-bar width (12px), participant-head width (120px), message Y pitch (40px), and lifeline pitch (180px) are appropriate for a readable diagram at typical zoom | Standard Stack / Code Examples / Architecture Patterns | LOW — these are first-pass values derived from the 20-grid convention and compartmented-box precedent; the loop empirically confirms or adjusts. If wrong, adjust in the primitive and re-render. |
| A2 | Self-message geometry (rightward arm `+40px`, downward `+40px`, return arm) is visually distinguishable and passes the anchor check | Common Pitfalls Pitfall 3 | LOW — self-messages are optional for the canonical example; omitting them from the canonical example sidesteps this pitfall. If needed, the specialist iterates until visual review passes. |
| A3 | The optional monotonic-Y and center-x structural verifier additions count as permitted "additive" hardening (same precedent as Phase 7's arrowhead check), not a frozen-validator violation | Validation Architecture Wave 0 | MEDIUM — if treated as frozen, neither check ships and SC-1 of sequence ("activation bars centered on lifeline x") has no automated guard. Planner must decide explicitly. |
| A4 | `«actor»` and `«include»` guillemet text renders safely under `fontFamily: 3` (same as `«interface»` in class diagrams) | Code Examples | LOW — confirmed in-repo for guillemets by STACK.md + Phase 7 class recipe; same rendering path |
| A5 | The Phase 8 planner should treat Phase 7 Plans 02 + 03 + 04 as completed prerequisites | Phase sequence | MEDIUM — as of 2026-06-07, only Plans 01 and 02 of Phase 7 have completed summaries; Plan 03 (`class_order_domain.excalidraw`) and Plan 04 (resolver wiring) are outstanding. Phase 8 plans must be blocked on Phase 7 Plan 04 completion. The planner must include an explicit dependency check at the start of Wave 1. |

---

## Open Questions

1. **Add the monotonic-Y and center-x verifier checks, or rely on KB + visual review?**
   - What we know: `verifier_structural.py` does not currently check message-Y ordering or activation bar center-x alignment (verified by reading the source — only `check_arrow_endpoint_unanchored`, `check_arrow_not_elbow`, `check_raw_emoji_in_text`, `check_text_overflow_static`, `check_roughness_nonzero`, `check_fontfamily_nonmonospace`, `check_arrow_points_too_few` exist). PITFALLS.md Pitfall 4 explicitly names these as assertions to add in the Sequence phase. Phase 7 established the precedent that additive hardening of the verifier/validator is acceptable.
   - What's unclear: Whether the cost of these checks is justified given sequence's relatively small canonical example. The monotonic-Y check in particular requires identifying which elements are message arrows and computing their Y order — more complex than the arrowhead deny-list.
   - Recommendation: **Add the center-x check** (simpler: verify each activation-bar rectangle center-x equals the nearest lifeline line element's x). **Defer monotonic-Y** to be enforced by KB discipline + verifier visual review (the check is complex and the visual review catches it). Surface this decision explicitly in the plan.

2. **What subject domain to use for the canonical sequence example?**
   - What we know: Prior canonical examples used domain-relevant subjects (retail orders for ER, order domain for class, order fulfilment for activity). A login flow or checkout flow are natural sequence diagram subjects.
   - Recommendation: Use a login/authentication sequence — "User sends login request to AuthService, which validates credentials against UserDB and returns a token." Approximately 3 participants, 4-6 messages including a dashed return. Keeps element count modest (avoids 3-iteration cap pressure).

3. **What subject domain to use for the canonical use-case example?**
   - What we know: Use-case examples are typically system-scoped scenarios with 2-4 actors and 4-8 use cases.
   - Recommendation: Use an e-commerce checkout system — "Customer actor, Admin actor, system boundary 'Checkout System', use cases: Browse Products, Add to Cart, Place Order, Process Payment (included from Place Order), View Reports (admin only)." 2 actors, 5 use cases, 1 include, covers all canonical elements.

---

## Environment Availability

This phase is authoring (JSON + Markdown) plus running the existing frozen loop. The only external dependency is the render path, proven in Phases 5–7.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` (validator + structural verifier) | validate + structural checks | Assumed ✓ (used through Phases 1–7) | — | none needed |
| Docker / `render_docker.sh` | Phase-2 PNG render | Assumed ✓ (er_retail_orders rendered 2026-06-07) | — | `render_excalidraw.py` direct path exists |
| `@excalidraw/excalidraw@0.17.3` via esm.sh CDN | render engine | Assumed ✓ (frozen render path) | 0.17.3 | none (HARD-01 vendoring deferred to v2) |

**Missing dependencies with no fallback:** None identified — the render+verify toolchain is the same one that shipped star, snowflake, activity, and ER in Phases 5–7.

---

## Validation Architecture

> `nyquist_validation: true` in config — section included. Note: this project's "tests" are the validate→render→verify loop scripts, not a unit-test framework.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Custom loop: `scripts/render/validate_and_render.sh` (validator + render) + `excalidraw_verifier` subagent (`scripts/verifier/verifier_structural.py` + multimodal visual review). No pytest/jest. |
| Config file | none — scripts invoked directly |
| Quick run command | `python3 .claude/agents/excalidraw/scripts/verifier/verifier_structural.py <file.excalidraw>` (structural only, sub-second) |
| Full suite command | `bash .claude/agents/excalidraw/scripts/render/validate_and_render.sh <file.excalidraw>` then read the PNG + invoke `excalidraw_verifier` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | Check Exists? |
|--------|----------|-----------|-------------------|---------------|
| UML-01 | Sequence example: legal arrowheads, elbowed connectors, endpoints anchored | structural | `verifier_structural.py` (arrow_endpoint_unanchored, arrow_not_elbow, arrowhead deny-list) | ✅ existing |
| UML-01 | Sequence example: activation bars centered on lifeline x | structural | (none today) | ❌ Wave 0 gap — add if adopted (Open Question 1) |
| UML-01 | Sequence example: message Y values monotonically non-decreasing | structural | (none today) | ❌ Wave 0 gap — recommended DEFERRED to visual review (Open Question 1) |
| UML-01 | Participant names, message labels monospace, no overflow | structural | `verifier_structural.py` (text_overflow_static, fontfamily_nonmonospace) | ✅ existing |
| UML-03 | Use-case example: legal arrowheads, actor boxes present, ovals present | structural + visual | `validate_and_render.sh use_case_<subject>.excalidraw` + verifier | ✅ structural (existing checks sufficient); visual confirms oval + actor layout |
| UML-03 | Use-case example: `include`/`extend` dashed arrows carry text labels | visual | visual multimodal review | ✓ (manual — visual review covers) |
| SC-3 | Canonical example pairs exist and pass the full loop for both sequence and use-case | structural + EX-03 | `validate_and_render.sh` + verifier visual pass | ❌ Wave 0 — no examples yet; created in Wave 2 plans |

### Sampling Rate

- **Per task commit:** `verifier_structural.py <file>` (sub-second structural gate) + arrowhead-legality check (already in validator from Phase 7).
- **Per example completion:** full `validate_and_render.sh` + visual verifier pass.
- **Phase gate:** both canonical examples pass full loop (structural green + EX-03 visual human approval) before resolver rows are wired.

### Wave 0 Gaps

- [ ] `kb/lifeline-activation.md` — the shared sequence primitive must exist before `sequence.md` can `@`-reference it.
- [ ] **Optional: center-x structural check** — add to `verifier_structural.py`: for each `rectangle` in a sequence diagram whose width is 12–16px (activation bar heuristic), assert its center x (`el.x + el.width/2`) equals the x-midpoint of the nearest `line` element above it. Decision-gated — Open Question 1.
- [ ] No framework install needed — the loop is the existing frozen toolchain.

*(If Open Question 1 center-x check is declined, the "activation bars centered on lifeline x" requirement of Success Criterion 1 has no automated guard and relies on KB discipline + verifier visual review — record that explicitly.)*

---

## Security Domain

> `security_enforcement` not present in config → not applicable for this phase. This is a local diagram-authoring KB project with no auth, network input, data persistence, or untrusted input surface introduced by Phase 8. No ASVS category applies to authoring `.excalidraw` JSON + Markdown. The only latent risk — `render_excalidraw.py` path resolution (HARD-03) — is a pre-existing deferred item.

---

## Sources

### Primary (HIGH confidence — in-repo, read directly this session)

- `.claude/agents/excalidraw/diagram-types/notation-conventions.md` — DTKB-04 locked legal-encoding table including Actor (labelled-box) and Dependency (dashed arrow) — sequences and use-case message/include/extend encodings derive from here
- `.claude/agents/excalidraw/diagram-types/er.md` + `class.md` — direct analogs for `sequence.md` authoring pattern (TYPE layer recipe structure, @-reference pattern, verbatim-reuse framing)
- `.claude/agents/excalidraw/kb/relationship-endpoint.md` — structural analog for `kb/lifeline-activation.md` (section layout: back-ref header, When to use, Geometry, JSON skeleton, See in examples, Notes)
- `.claude/agents/excalidraw/kb/group-container.md` — the use-case system-boundary primitive (confirmed existing, geometry and JSON skeleton already present)
- `.claude/agents/excalidraw/kb/tree-hierarchy.md` + `fan-out.md` — additional primitive file structure patterns
- `.claude/agents/excalidraw/scripts/verifier/verifier_structural.py` — verified: existing check set (emoji, overflow, unanchored-arrow, roughness, fontFamily, points-too-few, not-elbow); NO monotonic-Y or center-x check
- `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py` — arrowhead-legality check already present (added Phase 7 Plan 01); no additional gaps for sequence/use-case
- `.planning/ROADMAP.md` — Phase 8 scope, Success Criteria, "depends on Phase 7"
- `.planning/REQUIREMENTS.md` — UML-01 and UML-03 requirement text
- `.planning/research/PITFALLS.md` — Pitfall 4 (sequence lifeline/activation alignment), Pitfall 5 (emoji)
- `.planning/research/SUMMARY.md` — research flags for Phase 4 (Sequence) and Phase 4 (Use-case); geometry deferred items; Phase 4 Use-case "standard patterns" classification

### Secondary (HIGH confidence — prior phase artifacts)

- `.planning/phases/07-er-class/07-RESEARCH.md` — template for this research doc; validated Phase 7 pattern (shared primitive first, type recipes second, examples third, resolver last)
- `.planning/phases/07-er-class/07-PATTERNS.md` — analog mapping that Phase 8 mirror-images
- `.planning/phases/07-er-class/07-01-PLAN.md` — plan template for the Wave 1 primitive plan
- `.planning/phases/07-er-class/07-04-PLAN.md` — plan template for the Wave 3 resolver-wiring plan

### Tertiary (LOW confidence)

- None. No external web sources were needed — every claim is grounded in committed in-repo artifacts.

---

## Metadata

**Confidence breakdown:**
- Standard stack (schema vocabulary): HIGH — locked tokens verified in-repo; element types confirmed
- Architecture (two-layer composition, primitive-first pattern): HIGH — mirrors Phase 7 exactly
- Pitfalls: HIGH — verifier source read directly; geometry gap (center-x, monotonic-Y) confirmed by reading both check sets
- Lifeline/activation pixel geometry: MEDIUM (ASSUMED) — recommended values derived from 20-grid convention and compartmented-box precedent, not yet render-proven; confirmed empirically through the loop

**Research date:** 2026-06-07
**Valid until:** Stable — pinned, closed authoring environment; valid until locked conventions or frozen loop scripts change.
