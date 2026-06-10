# Phase 5: Tech Architecture + Activity - Research

**Researched:** 2026-06-04
**Domain:** Knowledge-base authoring (Markdown recipe files) + canonical example authoring (`.excalidraw` JSON) within the frozen v1.0 render→verify→fix loop
**Confidence:** HIGH

## Summary

This phase is **pure documentation + example authoring**, not software. There are no external packages, no code changes to the loop/validator/verifier (all frozen per v1.0 and the v1.1 "additive only" decision), and no new notation to invent. The two types it ships — Tech Architecture (ARCH-01) and Activity (UML-04) — were deliberately sequenced first in v1.1 *because* they reuse existing `kb/` primitives wholesale, validating the TYPE-layer→PRIMITIVE-layer composition workflow before any glyph research is spent.

A major finding from inspecting the live repo: **`diagram-types/tech-architecture.md` already exists and is fully authored and wired** (it was the Phase-4 smoke-test type — README resolver row 1 is the only "fully authored" row). For ARCH-01, Phase 5's real work is *confirmation/back-reference completion*, not authoring from scratch: the tech-architecture recipe must "name the group-container / icon-block / multi-zoom-overview / fan-out / convergence / linear-pipeline sub-patterns" (it already does, success-criterion 1) and the composed `kb/*.md` primitives must gain `> Used by types:` back-references (success-criterion 4 — currently only `linear-pipeline.md` and `group-container.md` carry one, both pointing at tech-architecture; the other four primitives lack them).

The substantive new work is **`diagram-types/activity.md` plus its canonical example pair** (`examples_excalidraw/activity_*.excalidraw` + rendered `examples/*.png`), which must pass the full validate→render→verify loop (UML-04, EX-01, EX-03). Activity composes only primitives that already exist (`linear-pipeline`, `decision-branch`, `decision-marker`, `feedback-loop`, `group-container`, `task-list`) — the README resolver table already lists the planned composition for the activity row. The one genuinely new layout concern is **swimlanes** (optional, per the success criterion), which has no dedicated primitive; the recipe must express swimlanes as a `group-container` composition (parallel labelled lane containers), not invent geometry.

**Primary recommendation:** Treat ARCH-01 as a verification/back-ref-completion task and UML-04 as the authoring task. Author `activity.md` composing existing primitives only; build the Activity example as start/end **ellipses** + action **rectangles** + decision **diamonds**, every arrow's last point landing within 8px of a shape border (the hard `arrow_endpoint_unanchored` error), every text element carrying explicit `width`/`height` (the hard `text_missing_dimensions` error). Express swimlanes via parallel `group-container` lanes. Do not touch any script, the validator, the verifier, or the `/excalidraw` command — they are generic and frozen.

## Architectural Responsibility Map

This is a single-tier knowledge plugin (a Claude Code subagent + command + KB files), so "tiers" map to the plugin's internal layers rather than client/server/DB.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Type purpose + "how to draw it" prose | TYPE layer (`diagram-types/<type>.md`) | — | A type recipe answers "what is this for and how do I assemble it from primitives" (DTKB-02) |
| Geometry / JSON skeletons (diamond, ellipse, arrow coords) | PRIMITIVE layer (`kb/<pattern>.md`) | — | Type files compose by `@`-reference and never re-derive geometry (DTKB-03 anti-drift) |
| Family→type→bundle dispatch | `/excalidraw` command + resolver table | `diagram-types/README.md` | Single authoritative resolver table (TAX-03); command is already generic, reads the table |
| Authoring / fixing the `.excalidraw` | `excalidraw_specialist` subagent | type recipe + composed kb files | Specialist reads `diagram-types/<type>.md` FIRST (INT-01, already wired) |
| Structural + visual pass/fail | `excalidraw_verifier` subagent + `verifier_structural.py` | — | FROZEN v1.0 contract; the example must satisfy it, never modify it |
| Technical pre-render validation | `excalidraw_validator.py` | `validate_and_render.sh` | FROZEN; checks metadata, no `label` prop on shapes, text contrast |

**Key implication:** ARCH-01 success-criterion 1 ("references the `kb/` primitives, not re-deriving geometry") and the two-layer cross-ref (criterion 4) are *enforced by which layer owns what*. Any coordinate math written into `activity.md` is a layer violation — it belongs in the composed `kb/` files.

## Standard Stack

**No external packages are installed or added in this phase.** This is Markdown + `.excalidraw` JSON authoring against an existing, frozen toolchain. The toolchain that *renders and checks* the example already exists:

### Existing toolchain (frozen — do not modify)
| Component | Location | Purpose | Status |
|-----------|----------|---------|--------|
| `validate_and_render.sh` | `scripts/render/` | Orchestrates validate → docker render → "now read the PNG" | FROZEN |
| `excalidraw_validator.py` | `scripts/render/` | Pre-render technical checks (metadata, no `label` prop, text contrast warnings) | FROZEN |
| `render_docker.sh` + Dockerfile | `scripts/render/` | Renders `.excalidraw` → sibling `.png` via `@excalidraw/excalidraw@0.17.3` | FROZEN |
| `verifier_structural.py` | `scripts/verifier/` | 9 structural checks (see Common Pitfalls) | FROZEN |
| `excalidraw_verifier.md` | agent root | 5 visual checks on the PNG + merge → `passed` + sibling report JSON | FROZEN |
| `/excalidraw` command | `.claude/commands/excalidraw.md` | Two-tier family/type picker → resolver-table dispatch → loop | FROZEN (generic — needs no per-type edit) |

### Files this phase creates or edits
| File | Action | Requirement |
|------|--------|-------------|
| `diagram-types/activity.md` | CREATE | UML-04 |
| `examples_excalidraw/<activity-name>.excalidraw` | CREATE (new example source) | EX-01 |
| `examples/<activity-name>.png` | CREATE (rendered, copied per kb/README refresh procedure) | EX-01, EX-03 |
| `diagram-types/README.md` | EDIT — promote the `activity` row from _(planned)_ to wired; add example PNG | DTKB-01, TAX-03 |
| `diagram-types/tech-architecture.md` | VERIFY (likely no change — already names all 6 sub-patterns) | ARCH-01 |
| `kb/decision-branch.md`, `kb/decision-marker.md`, `kb/feedback-loop.md`, `kb/task-list.md`, `kb/multi-zoom-overview.md`, `kb/fan-out.md`, `kb/convergence.md`, `kb/icon-block.md` | EDIT — add/complete `> Used by types:` back-refs | DTKB-03, ARCH-01 criterion 4, UML-04 criterion 4 |

**Installation:** None. No `npm install` / `pip install` / package additions.

## Package Legitimacy Audit

**Not applicable.** This phase installs no external packages. The only runtime dependency (`@excalidraw/excalidraw@0.17.3`, loaded via the Docker render image from `esm.sh`) was vendored/wired in v1.0 and is frozen; vendoring it locally is explicitly deferred to v2 (HARD-01). No new registry packages are introduced, so there is nothing to slopcheck.

## Architecture Patterns

### System data flow (how an Activity request becomes a verified PNG)

```
User runs /excalidraw
   │
   ▼
[Q1 family pick] ──"UML / SW-Engineering"──▶ [Q2 type sub-pick] ──"Activity"──▶ resolved type = activity
   │
   ▼
Orchestrator READS diagram-types/README.md resolver table
   │  finds activity row → recipe file + composed kb list + example PNG
   ▼
Spawn excalidraw_specialist (author mode)
   │  reads diagram-types/activity.md FIRST (INT-01)
   │  then reads composed kb/*.md (decision-branch, linear-pipeline, …) for geometry
   │  composes elements → writes .excalidraw → runs validate_and_render.sh → sibling .png
   ▼
Orchestrator spawns excalidraw_verifier(.excalidraw path)
   │  verifier_structural.py (9 checks) + 5 visual PNG checks → merge → passed?
   ▼
passed:true ──▶ SUCCESS                passed:false (N<3) ──▶ specialist fix mode ──▶ loop
                                       passed:false (N==3) ──▶ HONEST FAILURE
```

The Activity *example* (EX-01/EX-03) is authored by running exactly this loop once and confirming `passed: true`, then copying the source into `examples_excalidraw/` and the PNG into `examples/` per the `kb/README.md` refresh procedure.

### Recommended file layout (already established — follow it)
```
.claude/agents/excalidraw/
├── diagram-types/          # TYPE layer (sibling of kb/)
│   ├── README.md           # authoritative resolver table — edit the activity row
│   ├── tech-architecture.md# ALREADY EXISTS (Phase-4 smoke type) — verify only
│   └── activity.md         # CREATE
├── kb/                     # PRIMITIVE layer — add "Used by types:" back-refs
│   ├── decision-branch.md  # diamond gate (Activity decision)
│   ├── decision-marker.md  # inline ✗/✓ (Activity binary gate alt)
│   ├── linear-pipeline.md  # sequential action chain
│   ├── feedback-loop.md    # loop back to earlier action
│   ├── task-list.md        # vertical action stack
│   └── group-container.md  # swimlane lanes + scope
├── examples/               # rendered PNG ground truth
└── examples_excalidraw/    # .excalidraw source for each example
```

### Pattern 1: Activity diagram as a composition of existing primitives
**What:** A UML activity diagram = start node → action nodes → decision gates → (optional swimlanes) → end node, with possible loops back.
**When to use:** The user picks UML / Activity, or asks to diagram a process/workflow's step-by-step behaviour.
**Mapping to existing primitives (no new geometry):**

| Activity element | Reuse primitive | Excalidraw shape |
|------------------|-----------------|------------------|
| Start node (initial) | (atomic) filled `ellipse` | `ellipse`, solid fill |
| End node (final) | (atomic) `ellipse` (often double/filled ring) | `ellipse` |
| Action / activity node | `linear-pipeline` (sequential) or `task-list` (vertical w/ side I/O) | `rectangle` |
| Decision / merge gate | `decision-branch.md` (labelled diamond) | `diamond` |
| Binary pass/fail gate | `decision-marker.md` (inline ✗/✓ circles) | `ellipse` ×2 + glyph text |
| Loop back to earlier action | `feedback-loop.md` | elbow `arrow` routing outside flow |
| Swimlane / partition | `group-container.md` (parallel labelled lanes) | `rectangle` containers |

**Note on `diamond`:** `decision-branch.md` hedges "if diamond is not in the target schema, substitute a rectangle rotated 45°." That hedge is now **resolved** — `diamond` IS a first-class type in this toolchain. `verifier_structural.py` lines 110 and 240 treat `("rectangle","ellipse","diamond")` as valid anchor shapes, and `excalidraw_validator.py` line 33 lists `diamond`. `[VERIFIED: codebase grep of scripts/verifier/verifier_structural.py and scripts/render/excalidraw_validator.py]` Use a real `diamond` for decision gates — arrows can anchor to its border (the `_on_diamond_border` check exists).

### Pattern 2: Swimlanes via parallel group-containers (no new primitive)
**What:** Swimlanes are *optional* in the success criterion. Express them as N adjacent `group-container` rectangles (one per actor/role/partition), each branded/titled top-left, with action nodes placed inside the lane that owns them. Cross-lane transitions are arrows crossing the shared lane border (the same "piercing" idiom `task-list.md` documents for side I/O).
**When to use:** Only when the user's request names responsible parties/roles. Otherwise omit — the criterion says "optional swimlanes."
**Why no new primitive:** Per DTKB-02/DTKB-03 the TYPE file composes existing primitives and never re-derives geometry. A swimlane is geometrically just `group-container` repeated horizontally or vertically. Authoring a `swimlane.md` primitive would be scope creep into Phase 5; the recipe should *name group-container as the swimlane mechanism* in prose.

### Anti-Patterns to Avoid
- **Re-deriving coordinate math in `activity.md`.** Geometry lives only in `kb/`. The type file links down with `@../kb/<pattern>.md` and describes *which* primitive and *why*, never `x:/y:` numbers. (Mirrors how `tech-architecture.md` is written — zero coordinates in it.)
- **Inventing a `swimlane.md` primitive or new arrowhead glyphs.** Out of scope; Activity is a "zero-new-notation" type by roadmap design.
- **A single multi-line `text` block for action lists.** Compartmented/row constructs must use per-row text (INT-02). For action nodes, one `text` per node, each with explicit dimensions.
- **Editing the validator/verifier/command to "make the example pass."** The v1.0 loop is frozen; the example must satisfy the existing checks, not the reverse.
- **Claiming the activity resolver row is "wired" before the example pair passes the loop.** README explicitly forbids this for _(planned)_ rows.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Decision gate geometry | New diamond math in `activity.md` | `@../kb/decision-branch.md` | Diamond size/fill/outcome offsets already specified; `diamond` border is verifier-anchorable |
| Sequential action chain | New step-spacing math | `@../kb/linear-pipeline.md` | 180×80 nodes, 260 x-step, elbow arrows already specified |
| Loop-back routing | New elbow path | `@../kb/feedback-loop.md` | "route around, never cross" + 5-point elbow skeleton specified |
| Binary pass/fail | New ✗/✓ rendering | `@../kb/decision-marker.md` | Glyph circles + colors + Unicode U+2717/U+2713 specified |
| Swimlanes | A `swimlane.md` primitive | `@../kb/group-container.md` ×N | A lane is just a titled container repeated; geometry already exists |
| Rendering + checking the example | A new render/verify script | `validate_and_render.sh` + the two subagents | The entire loop already exists and is frozen |

**Key insight:** This phase's entire reason for existing is to prove that *no hand-rolling is necessary* — that a new type ships purely by composing existing primitives. If authoring Activity requires inventing geometry, that is a signal the composition is wrong, not that a new primitive is needed.

## Runtime State Inventory

> Phase 5 is greenfield authoring (new Markdown + new example files) plus back-ref edits to existing Markdown. There is no rename/refactor of a stored string. This section is included only to confirm nothing runtime-stateful is touched.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — no datastore keys, collections, or IDs change. The KB is flat files. | None |
| Live service config | None — no external service holds Activity state. The Docker render image is invoked fresh per render. | None |
| OS-registered state | None — no scheduled tasks, daemons, or registered processes reference these files. | None |
| Secrets/env vars | `EXCALIDRAW_ASSETS_DIR` is read by the verifier for icon fallback resolution; unchanged by this phase. No new secrets. | None |
| Build artifacts | None — no compiled package; `scripts/render/.venv` and `uv.lock` are unchanged. | None |

**The canonical question (after all files updated, what still holds an old string?):** Nothing — Phase 5 adds files and back-refs; it renames nothing. Verified by reading the resolver table, command, specialist, and scripts: the command/loop are *generic* and dispatch by reading the resolver table at runtime, so adding the `activity` row is sufficient — no per-type code path exists to update.

## Common Pitfalls

These are the **structural verifier checks** (`verifier_structural.py`) the Activity example MUST satisfy. Severity matters: an `error` makes `passed: false`; a `warning` does not block. `[VERIFIED: codebase grep of verifier_structural.py]`

### Pitfall 1: Unanchored arrow endpoints (ERROR — hard gate)
**What goes wrong:** `check_arrow_endpoint_unanchored` requires each arrow's *last* point to land within `ENDPOINT_TOLERANCE_PX = 8` of the border of a `rectangle`/`ellipse`/`diamond`. Activity has many arrows (action→decision, decision→branches, loop-backs). Any arrow whose head floats free fails.
**Why it happens:** Composing arrows from primitive skeletons at a translated origin without re-checking the head lands on the target shape's border.
**How to avoid:** For every arrow, compute `(x + last_point_dx, y + last_point_dy)` and confirm it sits on a target diamond/ellipse/rectangle border. Decision diamonds and start/end ellipses are valid anchors (border math implemented for all three).
**Warning signs:** Verifier issue `arrow_endpoint_unanchored` with the exact float coords of the dangling head.

### Pitfall 2: Text elements missing width/height (ERROR — hard gate)
**What goes wrong:** `check_text_missing_dimensions` errors on any `text` lacking `width` AND `height`. Such text renders in the PNG (export measures on the fly) but collapses to an invisible zero-size box when opened in the Excalidraw editor.
**How to avoid:** Every action label, decision label, lane title, and arrow label needs explicit `width = len(longest line) * fontSize * 0.6` and `height = lines * fontSize * lineHeight`, plus `lineHeight`, `textAlign`, `verticalAlign`, `originalText`.
**Warning signs:** Issue `text_missing_dimensions` naming the text element id.

### Pitfall 3: Static text overflow (ERROR — hard gate)
**What goes wrong:** `check_text_overflow_static` estimates monospace width (`len(text) * 0.6 * fontSize`) and errors if a non-`containerId` text inside a shape exceeds the shape width.
**How to avoid:** Size action rectangles to fit their labels (or shorten labels). Long action verbs ("Validate submitted application form") need wide nodes.
**Warning signs:** Issue `text_overflow_static` with the px estimate vs. container width and a concrete widen-to-N suggestion.

### Pitfall 4: Image path unresolvable (ERROR — hard gate, only if icons used)
**What goes wrong:** `check_image_path_unresolvable` errors if an `image` element's `file_path` resolves to nothing (checked relative to the `.excalidraw` dir, then `EXCALIDRAW_ASSETS_DIR`).
**How to avoid:** Activity nodes are usually plain shapes — icons are optional. If a lane uses a brand icon, point `file_path` at an existing `icons/*.png` (78 icons present).

### Pitfall 5: Non-sharp / under-pointed arrows (WARNING — does not block, but house style)
**What goes wrong:** `check_arrow_not_elbow` warns when an arrow lacks `elbowed: true` or has `roundness {type:2}`; `check_arrow_points_too_few` warns at <3 points. Also `check_roughness_nonzero` (expect 0) and `check_fontfamily_nonmonospace` (expect 3).
**How to avoid:** Author all connectors as sharp elbow arrows (`elbowed: true`, `roundness: null`, ≥3 orthogonal points); all text `fontFamily: 3`; all elements `roughness: 0`. These match every primitive skeleton already.
**Note:** These are warnings, so they will NOT fail the loop — but the canonical example should be exemplary, so satisfy them anyway.

### Pitfall 6: Visual checks on the rendered PNG (all ERROR)
**What goes wrong:** The verifier subagent applies 5 visual checks to the PNG: `text_overflow_visual`, `arrow_disconnected_visual`, `missing_glyph_box`, `layout_collision`, and one more — all `severity: error`. **`layout_collision`** is the key swimlane risk: overlapping lane containers, an action box straddling two lanes, or a loop-back arrow crossing a label all fail.
**How to avoid:** Keep swimlanes non-overlapping with clear gutters; route feedback loops *outside* the flow bounding box (per `feedback-loop.md`); keep ≥20px-grid spacing.
**Warning signs:** Issues `layout_collision` / `text_overflow_visual` / `arrow_disconnected_visual` in the report.

### Pitfall 7: `label` property on a shape (ERROR — validator, pre-render)
**What goes wrong:** `excalidraw_validator.py` errors if a `rectangle`/`ellipse`/`diamond` carries a `label` property. Labels must be standalone `text` elements.
**How to avoid:** Never inline a label on a shape; always emit a sibling `text` element.

## Code Examples

The verified geometry skeletons already live in the composed `kb/` files — the recipe must reference them, not duplicate them. The most load-bearing fact for the *example author*:

### Decision gate (real diamond, verifier-anchorable)
```json
// Source: kb/decision-branch.md (geometry) + verified diamond support in verifier_structural.py
{ "type": "diamond", "x": 400, "y": 240, "width": 160, "height": 100,
  "backgroundColor": "#fef3c7", "strokeColor": "#b45309",
  "roughness": 0, "roundness": { "type": 3 } }
```
Arrow into/out of it must land within 8px of the diamond's edge (top/right/bottom/left vertex segments) — `_on_diamond_border` implements the exact tolerance.

### Start/End node (filled ellipse — atomic, valid anchor)
```json
// UML initial/final node; ellipse is a verifier-recognized anchor shape
{ "type": "ellipse", "x": 100, "y": 100, "width": 40, "height": 40,
  "backgroundColor": "#1e1e1e", "strokeColor": "#1e1e1e", "roughness": 0 }
```

### Every text element needs explicit dimensions (the #1 hard error)
```json
// Source: check_text_missing_dimensions in verifier_structural.py
{ "type": "text", "x": 156, "y": 124, "text": "Validate input",
  "fontSize": 16, "fontFamily": 3,
  "width": 144, "height": 20, "lineHeight": 1.25,
  "textAlign": "left", "verticalAlign": "top",
  "originalText": "Validate input", "strokeColor": "#1e1e1e" }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `decision-branch.md` hedge: "if diamond not in schema, use rotated rectangle" | `diamond` is a first-class, verifier-anchorable type | This toolchain (v1.0) | Use a real `diamond` for Activity gates — no rotation workaround needed |
| Flat single list of diagram "kinds" in `/excalidraw` | Two-tier family→type picker reading the resolver table | Phase 4 (shipped/awaiting smoke verify) | Activity is reached via UML family → Activity sub-pick; command needs no per-type edit |
| Per-type hard-coded dispatch | Single authoritative resolver table in `diagram-types/README.md` | Phase 4 | Shipping Activity = add one resolver row; the loop is generic |

**Deprecated/outdated within this repo:**
- The legacy `examples_excalidraw/star_schema.excalidraw` is **grandfathered, NOT a template** — its unbound/free-floating/soft-cornered style violates the current recipe. Do not imitate it when authoring the Activity example. (Relevant only as a "don't copy this" warning; star is Phase 6.)

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Activity swimlanes should be expressed via `group-container` rather than a new `swimlane.md` primitive | Pattern 2 / Don't Hand-Roll | LOW — if a planner decides a dedicated primitive is warranted, that is a deliberate scope choice; the success criterion only requires "optional swimlanes" to render correctly, achievable either way |
| A2 | `tech-architecture.md` needs no edit for ARCH-01 criterion 1 (it already names all 6 sub-patterns) | Standard Stack / Summary | LOW — verified the file lists group-container, icon-block, multi-zoom-overview, fan-out, convergence, linear-pipeline; a re-read at plan time confirms |
| A3 | UML initial node = filled ellipse, final node = ellipse ring is the convention to adopt | Code Examples | LOW — standard UML; exact fill/ring styling is the recipe author's discretion since no `notation-conventions.md` entry mandates it yet |

## Open Questions

1. **Does the existing `tech-architecture.md` fully satisfy ARCH-01 criterion 1 verbatim, or does the phrase "reframes the architecture/overview material" imply added prose?**
   - What we know: The file already states purpose ("technologies, services, clouds"), names all 6 composed sub-patterns, and reuses `architecture_overview.png` as ground truth.
   - What's unclear: Whether the planner wants additional "reframing" prose beyond what's there.
   - Recommendation: Treat ARCH-01 as a verify-and-complete-backrefs task; only add prose if a gap against the criterion is found on re-read.

2. **Which arrow-anchoring strategy for the Activity example — manual coordinate landing vs. Excalidraw `boundElements`/`startBinding`/`endBinding`?**
   - What we know: `check_arrow_endpoint_unanchored` is satisfied by the last point landing within 8px of a border (pure geometry); it does NOT require `boundElements`. The grandfathered star example used unbound arrows successfully rendered.
   - What's unclear: Whether to also add bindings for editor-edit-ability (a quality-not-correctness concern).
   - Recommendation: Geometry-land the arrowheads to pass the verifier; optionally add bindings for polish. Bindings are not required to pass.

3. **Swimlane orientation (horizontal vs. vertical lanes) for the canonical example.**
   - What we know: Either is valid UML; `group-container` supports both.
   - Recommendation: Pick one in the recipe and the example for consistency; vertical lanes (columns) read most naturally with top-to-bottom action flow. Author's discretion.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 | `excalidraw_validator.py`, `verifier_structural.py` | ✓ | 3.14.4 | — |
| Docker | `render_docker.sh` (renders `.excalidraw`→PNG) | ✓ | running | — |
| `@excalidraw/excalidraw@0.17.3` | render image (via `esm.sh` CDN) | ✓ (in render image) | 0.17.3 | none — vendoring deferred to v2 (HARD-01) |
| icons (`icons/*.png`) | optional Activity lane brand icons | ✓ | 78 icons present | omit icons (Activity nodes need none) |

**Missing dependencies with no fallback:** None.
**Missing dependencies with fallback:** None blocking. (The `esm.sh` CDN dependency is a known v2 hardening item but is operational today.)

## Validation Architecture

> `nyquist_validation` is `true` in config. The "test suite" for this phase is the existing render→verify→fix loop applied to the canonical example — there is no unit-test framework for a documentation/KB phase; the loop *is* the executable check.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | The frozen v1.0 loop: `validate_and_render.sh` → `excalidraw_verifier` → `<basename>.verifier-report.json` |
| Config file | none (shell + python scripts, no test runner) |
| Quick run command | `bash .claude/agents/excalidraw/scripts/render/validate_and_render.sh <path>.excalidraw` then read the PNG |
| Full suite command | Run the example through the full `/excalidraw` orchestration loop and confirm `passed: true` in the sibling report JSON |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| UML-04 | Authoring an activity request yields a PNG passing the full loop | integration (loop) | spawn `/excalidraw` → activity → confirm report `passed:true` | recipe ❌ (Wave 0), example ❌ (Wave 0) |
| ARCH-01 | tech-architecture recipe names the 6 sub-patterns | structural (file inspection) | `grep -c 'kb/' diagram-types/tech-architecture.md` (expect ≥6) | ✅ exists |
| EX-01 | Canonical example pair exists + indexed | structural | confirm `examples_excalidraw/<activity>.excalidraw` + `examples/<activity>.png` + resolver row | ❌ (Wave 0) |
| EX-03 | Example passes validate→render→verify | integration (loop) | verifier report `passed:true` for the example | ❌ (Wave 0) |
| DTKB-03 (criterion 4) | Composed primitives carry `> Used by types:` back-refs | structural | `grep -L 'Used by types' kb/{decision-branch,decision-marker,feedback-loop,task-list}.md` (expect empty) | partial — only 2 of needed files have back-refs today |

### Sampling Rate
- **Per task commit:** run `validate_and_render.sh` on the example and read the PNG (catches static errors fast).
- **Per wave merge:** run the full verifier and confirm `passed: true` in the report JSON.
- **Phase gate:** the Activity example passes the full loop (EX-03) AND both tech-architecture + activity resolver rows are consistent (verified before `/gsd-verify-work`).

### Wave 0 Gaps
- [ ] `diagram-types/activity.md` — covers UML-04 (recipe authoring)
- [ ] `examples_excalidraw/<activity>.excalidraw` + `examples/<activity>.png` — covers EX-01/EX-03
- [ ] Back-ref completion in `kb/decision-branch.md`, `kb/decision-marker.md`, `kb/feedback-loop.md`, `kb/task-list.md` (and confirm fan-out/convergence/icon-block/multi-zoom-overview for tech-architecture) — covers DTKB-03 / criterion 4
- [ ] `diagram-types/README.md` activity row promoted from _(planned)_ to wired with example PNG path
- Framework install: none needed (loop already exists)

## Security Domain

> `security_enforcement` is not set in config; this is a documentation/KB phase authoring Markdown and a static `.excalidraw` JSON file consumed only by a local render/verify toolchain. There is no authentication, session, network input, or cryptography surface.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | — (no auth surface) |
| V3 Session Management | no | — |
| V4 Access Control | no | — |
| V5 Input Validation | minimal | The example JSON is author-controlled, not user-supplied at runtime; `excalidraw_validator.py` already validates structure. `image.file_path` resolution is sandboxed-pending (HARD-03, deferred v2) but only author-authored paths are introduced here. |
| V6 Cryptography | no | — (never hand-rolled; none used) |

### Known Threat Patterns for this stack
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Unresolvable / path-traversal `image.file_path` in example JSON | Tampering | `check_image_path_unresolvable` resolves only existing files under the excalidraw dir / `EXCALIDRAW_ASSETS_DIR`; author points icons at existing `icons/*.png`. Full path sandboxing is HARD-03 (v2). |

**Net:** No new security surface. The phase introduces author-controlled static files only.

## Sources

### Primary (HIGH confidence)
- `.claude/agents/excalidraw/scripts/verifier/verifier_structural.py` — all 9 structural checks, severities, and the diamond/ellipse/rectangle anchor support (read in full)
- `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py` — pre-render validator rules (read in full)
- `.claude/agents/excalidraw/excalidraw_verifier.md` — 5 visual checks + `passed` computation + report schema
- `.claude/agents/excalidraw/diagram-types/README.md` — authoritative resolver table, activity row, "Adding a diagram type" procedure
- `.claude/agents/excalidraw/diagram-types/tech-architecture.md` — confirmed already names all 6 sub-patterns (ARCH-01)
- `.claude/agents/excalidraw/kb/{decision-branch,decision-marker,linear-pipeline,feedback-loop,task-list,group-container}.md` — composed primitive geometry + current back-ref state
- `.claude/commands/excalidraw.md` — two-tier picker, generic resolver-table dispatch, loop ownership
- `.planning/{STATE,ROADMAP,REQUIREMENTS}.md` — phase scope, decisions, requirement IDs

### Secondary (MEDIUM confidence)
- UML activity-diagram conventions (start/end/action/decision/swimlane) — standard UML 2.x training knowledge, mapped onto existing primitives; exact node styling (filled-circle initial node) is conventional, not repo-mandated

### Tertiary (LOW confidence)
- None — all load-bearing claims verified against the live codebase.

## Metadata

**Confidence breakdown:**
- Standard stack (files to create/edit): HIGH — derived directly from the resolver table, requirement IDs, and inspection of which files already exist
- Architecture (composition mapping): HIGH — every Activity element maps to an existing, read primitive
- Pitfalls (verifier contract): HIGH — read the verifier source in full; severities and tolerances are exact
- Swimlane approach: MEDIUM — UML-standard, expressed via existing `group-container`; no dedicated primitive exists (intentional)

**Research date:** 2026-06-04
**Valid until:** 2026-07-04 (stable — KB/toolchain is frozen; no fast-moving external dependency)
</content>
</invoke>
