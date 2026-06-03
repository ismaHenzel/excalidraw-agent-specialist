# Project Research Summary

**Project:** Excalidraw Claude — Milestone v1.1: Diagram Families & UML Expansion
**Domain:** Excalidraw v2 JSON schema authoring — UML (sequence/class/use-case/activity) + Data Modeling (star/snowflake/ER/data-vault) KB layer
**Researched:** 2026-06-03
**Confidence:** HIGH

## Executive Summary

Milestone v1.1 adds a new `diagram-types/` knowledge-base layer and eight new diagram types (four UML, four data-modeling) to the existing constrained Excalidraw authoring pipeline. The system is a two-tier KB: the existing `kb/` directory supplies reusable geometric primitives (fan-out, tree-hierarchy, decision-branch, etc.); the new `diagram-types/` directory supplies per-type recipes that compose those primitives and encode notation workarounds. No new host dependencies, npm packages, or render-pipeline changes are required — everything stays inside the frozen `@excalidraw/excalidraw@0.17.3` bundle. The integration is additive: one new KB directory, new canonical example pairs, a richer two-tier family picker in the `/excalidraw` command, and a few mandate additions to the specialist agent.

The dominant technical constraint is the arrowhead set: `0.17.3` exposes exactly `arrow | bar | dot | triangle | null` — no crow's-foot, no open diamond, no hollow triangle. Every UML/ER relationship type that references a non-native endpoint must be expressed via composed `line`/`ellipse`/`diamond` glyphs grouped with the connector, or via textual multiplicity labels. This is the single most dangerous misunderstanding for KB authors: writing an illegal arrowhead token produces a silent render default, not an error, so the semantic payload of an entire diagram vanishes without warning. All five affected diagram types (class, ER, use-case dependency arrows, sequence returns, and activity) have documented workarounds in STACK.md that must be embedded verbatim in their `diagram-types/` files.

The one CRITICAL open decision that must be resolved before authoring begins: the existing `star_schema.excalidraw` ground-truth file does NOT follow the recipe the new families are supposed to enforce. It uses zero `groupIds`, zero `containerId`, unbound arrows, and soft-cornered boxes — directly contradicting the grouped/bound/sharp recipe STACK.md mandates for all new compartmented-box types. The team must decide whether to re-author `star_schema.excalidraw` to match the new recipe (establishing true consistency) or grandfather it as a legacy example and start the new recipe with fresh files. This decision gates the start of canonical-example authoring for the entire milestone.

---

## Key Findings

### Recommended Stack

The "stack" for this milestone is the Excalidraw v2 schema vocabulary, not software dependencies. All required element types (`rectangle`, `line`, `arrow`, `ellipse`, `diamond`, `text`, `image`) are confirmed present in `0.17.3` and already exercised by the five shipped example files. The critical properties are `roundness: null` (sharp boxes for all formal notation), `roughness: 0`, `fontFamily: 3` (Cascadia monospace, required for column-aligned compartment rows), `elbowed: true` on all connectors, `groupIds` on every multi-element notation unit, and the legally renderable arrowhead set.

**Core schema primitives and their roles:**
- `rectangle` (sharp, `roundness:null`) — entity/class/activity boxes, participant headers, activation bars, swimlane bands
- `line` — compartment dividers, lifelines (`strokeStyle:"dashed"`), crow's-foot endpoint glyphs (composed workaround)
- `arrow` (`elbowed:true`, `roundness:null`) — all connectors; `strokeStyle:"dashed"` for UML dependency/return
- `ellipse` — use-case ovals, sequence start dots, activity start/end nodes
- `diamond` — activity decision/merge nodes; small (~14px) aggregation/composition glyph (composed workaround)
- `text` (`fontFamily:3`) — all labels; PK/FK as text prefixes (`"PK  id"`), stereotypes via `«»` guillemets
- `groupIds` — mandatory on every multi-element box unit (class box = 8-15 elements)

**Hard arrowhead constraint and workarounds (the load-bearing constraint):**

| Notation needed | Legal encoding |
|---|---|
| Association / message direction | `endArrowhead:"arrow"`, solid |
| Dependency / return message | `endArrowhead:"arrow"`, `strokeStyle:"dashed"` |
| Generalization (inheritance) | `endArrowhead:"triangle"` — FILLED (house convention; not hollow) |
| Realization | `endArrowhead:"triangle"` + `strokeStyle:"dashed"` |
| Aggregation / composition (diamond end) | Small `diamond` element (~14px) grouped at connector end; white fill = aggregation, solid = composition |
| ER crow's-foot "many" | Three short grouped `line` strokes OR textual `0..*`/`1..*` label |
| ER "one" bar | `endArrowhead:"bar"` |
| ER "zero/optional" circle | `endArrowhead:"dot"` or small `ellipse` glyph |

**The reusable compartmented-box construction (shared across ALL formal-notation types):**
One `rectangle` (sharp, `roundness:null`) + horizontal `line` dividers (spanning full box width) + one bound/centered `text` for the title + N free-floating left-aligned monospace `text` rows for attributes/columns. All elements in one `groupIds` group. This single recipe covers UML class boxes, ER entity boxes, star/snowflake/data-vault table boxes — it is the architectural primitive of the milestone. Never use a multi-line `text` with `\n` rows; it defeats dividers and breaks the verifier's width-fit check.

### Expected Features

**Must have (table stakes for a "diagram families" milestone):**
- Tech Architecture — reframes existing macro patterns; zero new notation; the warm-up type
- Star schema — canonical analytics model; ground-truth PNG already ships; seeds the table-box recipe
- ER diagram — universal relational data model; introduces crow's-foot glyph
- Sequence diagram — most-drawn UML type in practice; introduces lifeline + activation-bar primitive
- Class diagram — foundational UML; introduces relationship-endpoint glyphs shared with ER

**Should have (differentiators, ship if phase budget allows):**
- Activity diagram — highest reuse of existing Flow/Process primitives; near-free to add; rounds out UML core 4
- Use-case diagram — simplest UML; only new glyphs are actor (labelled box recommended) and system-boundary oval
- Snowflake schema — normalized star; builds directly on star + tree-hierarchy; cheap follow-on

**Defer to v1.2 or later:**
- Data Vault — most complex data-modeling type; niche audience; conceptually layers on ER + star; safe to slip

**v2+ only:**
- Remaining UML 14-type set (state, component, deployment, timing, etc.) — add reactively on demand

### Architecture Approach

The integration is a clean two-layer composition model. The existing `kb/` primitives are unchanged except for adding one-line `Used by types:` back-references. The new `diagram-types/` directory (sibling of `kb/`, not nested inside it) holds one Markdown recipe file per diagram type; each file states purpose, must-have notation, workarounds, and a `@../kb/<pattern>.md` composition list — never copy-pasting geometry from the primitive files. A new `diagram-types/README.md` is the single resolver table mapping family to type to {type file, kb sub-patterns[], example PNG}; both the `/excalidraw` command and the specialist agent read this one table, keeping the mapping in one place.

**Major components:**
1. `/excalidraw` command (EDIT) — rewritten Q1/sub-pick with two-tier family picker; step 2 reads `diagram-types/README.md` to resolve the asset bundle; step 3 dispatch unchanged in mechanism, richer in content
2. `diagram-types/` directory (NEW) — TYPE layer; one recipe file per type; `README.md` resolver table
3. `excalidraw_specialist.md` (EDIT) — adds `diagram-types/` asset path and "read type file FIRST" mandate; render-verify loop unchanged
4. `kb/*.md` (LIGHT EDIT) — back-ref lines only; no geometry changes
5. `examples/` + `examples_excalidraw/` (NEW PAIRS) — one canonical `.excalidraw` + PNG per new type (7-8 pairs; star reuses existing)
6. `excalidraw_verifier.md` — UNCHANGED
7. Render pipeline / scripts — UNCHANGED

**Two-tier family picker design within the 4-option cap:**
Q1 `AskUserQuestion` presents exactly 4 families (Tech Architecture / Data Modeling / UML-SW Eng / Flow-Process) — hitting the cap precisely. For families with multiple types (UML=4, Data Modeling=4), a second `AskUserQuestion` lists that family's types (again <=4, so within cap). For Tech Architecture (1 type), the family IS the type — skip the sub-pick. For any future family growing past 4 types, a plain-text numbered menu is the documented escape hatch. A flat single-question list of all 9-16 types is impossible at the 4-option cap and explicitly prohibited.

### Critical Pitfalls

1. **Illegal arrowhead tokens render silently as plain lines** — An author writes `endArrowhead:"crowsfoot"` or `"diamond"`; `0.17.3` ignores the unknown value and renders no head at all, erasing the semantic payload of the entire diagram. Fix: embed STACK.md's notation-to-primitive mapping table in every affected `diagram-types/` file; add a validator check rejecting any arrowhead value not in `{arrow,bar,dot,triangle,null}`.

2. **Multi-line `text` defeats compartment layout and width-fit verification** — Packing a class/entity box into one `text` element with `\n`-separated rows loses dividers, column alignment, and causes the verifier's structural width-fit check to miss overflows (it measures one width per element, not the widest row). Fix: always use separate `text` elements per row; harden the verifier to split `\n` and measure the widest row.

3. **Misaligned compartment dividers and drifting row columns** — Manual geometry accumulates off-by-pixel errors: dividers that don't span the full box width, rows whose left x drifts, non-grid Y positions. Fix: define the box as a parametric recipe with fixed offsets in `diagram-types/` (header height H, row pitch R as multiples of 20, divider from `box.x` to `box.x+width` exactly).

4. **Sequence-diagram lifelines and activation bars misalign with messages** — Lifelines, activation bars, and message arrows must share an exact center x per participant; message Y values must monotonically increase top-to-bottom. Any deviation makes the scenario read in the wrong sequence. Fix: pin each participant to a fixed center x (multiple of 20); add structural verifier assertions for monotonic Y and center-x alignment.

5. **Canonical examples eyeballed instead of verify-loop gated** — An example that passes visual inspection but was never run through `validate_and_render.sh` + `excalidraw_verifier` becomes broken ground truth the specialist imitates in every future diagram of that type. Fix: "canonical example PASSES the full verify loop" is an exit criterion for every phase, not a separate phase.

---

## Implications for Roadmap

### CRITICAL OPEN DECISION (must resolve before Phase 0)

**The existing `star_schema.excalidraw` does NOT follow the grouped/bound/sharp recipe the new families require.** Inspection confirms: 0 `groupIds`, 0 `containerId`/`boundElements` usage, arrows with `startBinding:null`/`endBinding:null` and `roundness:{type:2}`, outer container with `roundness:{type:3}` (soft). The STACK.md recipe mandates `groupIds` on every box unit, bound titles, unbound attribute rows, and `roundness:null` (sharp) on all formal boxes and connectors.

**Decision required:** (A) Re-author `star_schema.excalidraw` to comply with the new recipe before using it as ground truth for star schema, OR (B) grandfather it as a legacy file, label it as pre-v1.1 style, and author a new compliant `star_schema_v2.excalidraw` as the canonical example going forward. Option A gives one consistent recipe across all types; Option B ships faster but creates two visual dialects. **This decision gates canonical-example authoring for the entire milestone.**

---

### Phase 0: Scaffolding — Integration Spine

**Rationale:** Prove the data-flow wiring (family picker to type resolver to specialist dispatch) before writing any diagram content. Everything else slots into this spine. Failures here break all subsequent phases.
**Delivers:** `diagram-types/` directory + empty `README.md` resolver table; rewritten `/excalidraw` Q1/sub-pick/resolver (sections 1-3 only); `excalidraw_specialist.md` asset-path + "type-file first" mandate addition; smoke-test with one existing type to validate end-to-end flow.
**Addresses:** Anti-pattern of duplicating resolver tables; two-tier picker architecture; 4-option cap compliance.
**Avoids:** Integration gotcha where type selection loads wrong or generic assets; the picker wiring never fires.
**Research flag:** Standard patterns — additive edits to known files, no domain research needed. Skip `--research-phase`.

### Phase 1: Tech Architecture + Activity — Zero New Notation

**Rationale:** Front-loads the two lowest-cost types to validate the type-file to primitive-composition workflow before any glyph research is needed. Tech Architecture reuses `architecture_overview.png` (no new example to render). Activity reuses decision-branch, linear-pipeline, feedback-loop, task-list wholesale — cheapest UML type.
**Delivers:** `tech-architecture.md` + `activity.md`; new `activity.excalidraw` + PNG (one new example pair); back-refs added to ~6 `kb/*.md` files; canonical examples pass full verify loop.
**Addresses:** Tech Architecture (table stakes); Activity diagram (differentiator, near-free).
**Avoids:** Starting with hard glyph work before the composition plumbing is proven; wasting glyph research effort if the type-file format needs iteration.
**Research flag:** Standard patterns — pure composition of existing primitives. Skip `--research-phase`.

### Phase 2: Star Schema then Snowflake — DM Table-Box Recipe

**Rationale:** Star before snowflake is a hard dependency (snowflake = star + tree-hierarchy; FEATURES.md explicit). Star has a ground-truth PNG (modulo the open re-author decision). This phase establishes the reusable compartmented-box recipe (rect + line dividers + monospace row texts + groupIds) that ALL subsequent data-model and class types reuse. Pitfall 3 (misaligned compartments) must be solved here — the parametric box recipe is the fix.
**Delivers:** `star-schema.md` + `snowflake-schema.md`; new (or re-authored) `star_schema.excalidraw` + PNG; `snowflake_schema.excalidraw` + PNG; parametric compartmented-box recipe documented in KB; Pitfall 3 verifier assertion (divider x-range == box x-range, rows share left x).
**Addresses:** Star schema (table stakes); Snowflake schema (differentiator).
**Avoids:** Authoring snowflake before star; using the non-compliant existing star example as ground truth without a decision.
**Research flag:** Standard patterns for star. Snowflake may need light planning research on normalization-hierarchy layout if tree-hierarchy geometry doesn't translate directly.

### Phase 3: ER + Class — Shared Endpoint-Glyph Primitive

**Rationale:** ER and class share the hardest unsolved problem — non-native relationship endpoint glyphs (crow's-foot, diamond, hollow triangle). Solving it once as a shared `kb/` primitive (e.g. `relationship-endpoint.md`) and then authoring both types against it is strictly more efficient than solving it twice. The shared endpoint-glyph primitive must be built BEFORE the type files are authored. Pitfall 1 (illegal arrowhead tokens) and Pitfall 2 (multi-line text breaking width-fit) are both addressed here; the verifier arrowhead-enum check lands in this phase.
**Delivers:** New `kb/relationship-endpoint.md` (crow's-foot + diamond + filled-triangle glyph recipes); `er.md` + `class.md`; `er.excalidraw` + PNG; `class.excalidraw` + PNG; arrowhead-enum validator check; multi-line width-fit verifier hardening.
**Addresses:** ER diagram (table stakes); Class diagram (table stakes).
**Avoids:** Authoring ER and class in separate phases (glyph work done twice); shipping illegal arrowhead tokens silently.
**Research flag:** Needs `--research-phase` — the crow's-foot composed-glyph geometry (sizing, rotation, grouped-line positioning) and the diamond glyph sizing are novel; no existing `kb/` pattern covers them. The textual-multiplicity fallback strategy also needs a documented house choice.

### Phase 4: Sequence + Use-Case — Independent New Primitives

**Rationale:** Each type introduces its own new primitive with no cross-dependency to each other. Sequence introduces the lifeline + activation-bar primitive (Pitfall 4 — the alignment-heavy one). Use-case introduces the actor convention (labelled box recommended over stick-figure) and system-boundary oval. They can parallelize or run sequentially. They follow Phase 3 because the verifier improvements there (structural pre-checks) reduce iteration cost for the equally geometry-sensitive sequence type.
**Delivers:** New `kb/lifeline-activation.md`; `sequence.md` + `use-case.md`; `sequence.excalidraw` + PNG; `use-case.excalidraw` + PNG; Pitfall 4 verifier assertions (monotonic Y, center-x alignment, message endpoint on lifeline).
**Addresses:** Sequence diagram (table stakes); Use-case diagram (differentiator).
**Avoids:** Sequence's tight geometry constraints blowing the 3-iteration auto-fix cap (parametric KB recipe front-loads correctness).
**Research flag:** Sequence needs `--research-phase` for the lifeline/activation-bar parametric geometry (fixed center-x discipline, message Y pitch, self-message loop sizing). Use-case is standard patterns; skip.

### Phase 5 (or defer to v1.2): Data Vault

**Rationale:** Most complex data-modeling type; conceptually layers on ER (entities/relationships) + star (table boxes/fan-out); niche audience; high authoring cost. Must come after Phase 2 (star/snowflake) and Phase 3 (ER) are validated. FEATURES.md and PROJECT.md both flag it as the safe slip item.
**Delivers:** `data-vault.md`; `data-vault.excalidraw` + PNG; documented hub/link/satellite 3-color palette convention.
**Addresses:** Data Vault (nice-to-have).
**Avoids:** Color-only distinction for hub/link/satellite (accessibility pitfall — pair color with text role label).
**Research flag:** Needs `--research-phase` — hub/link/satellite visual conventions, 3-color palette for accessibility, and raw-vault vs. business-vault layering notation are niche and under-specified relative to the other types.

---

### Phase Ordering Rationale

- **Star before snowflake** (Phase 2 internal order): hard schema dependency; snowflake is defined as star + normalized dimension branches.
- **Shared endpoint-glyph primitive before class + ER** (Phase 3 start): building the glyph once and referencing it from both type files saves work and ensures visual consistency; glyph geometry is the hard part of both types.
- **Data vault last / deferred** (Phase 5): highest complexity, builds on ER + star, niche audience; every other type de-risks it.
- **Scaffolding before content** (Phase 0): the family picker and resolver wiring must exist for any type to be testable end-to-end; proving it with one type before writing new notation prevents integration bugs from hiding behind content bugs.
- **Zero-notation types first** (Phase 1): validates the type-file format and composition model before glyph research is invested.

### Research Flags

Phases needing `--research-phase` during planning:
- **Phase 3 (ER + Class):** crow's-foot composed-glyph geometry (sizing, rotation, multi-line grouping); diamond glyph sizing; house choice between glyph and textual-multiplicity fallback; verifier structural assertions for these new check types.
- **Phase 4 (Sequence):** lifeline + activation-bar parametric geometry; message Y pitch; self-message loop sizing; monotonic-Y verifier assertion implementation.
- **Phase 5 (Data Vault):** hub/link/satellite visual conventions; accessible 3-color palette; raw-vault vs. business-vault layering notation.

Phases with standard patterns (skip `--research-phase`):
- **Phase 0 (Scaffolding):** additive edits to known files; no domain-specific research.
- **Phase 1 (Tech Arch + Activity):** pure composition of existing `kb/` primitives; Activity reuses decision-branch/linear-pipeline wholesale.
- **Phase 2 (Star + Snowflake):** star has ground-truth; snowflake = star + tree-hierarchy (known primitive). The parametric box recipe is new but fully specified in STACK.md.
- **Phase 4 (Use-case):** simplest UML; actor-as-labelled-box convention is already decided; no novel geometry.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Arrowhead enum, element types, and property values verified directly against `0.17.3` `.d.ts` and all 5 shipped example sources. Zero ambiguity on what is and is not legal. |
| Features | HIGH (standards) / MEDIUM (mapping) | UML/data-modeling conventions are stable published standards. The `@kb/*` composition mappings per type are design judgements with HIGH internal consistency but no external validation yet. |
| Architecture | HIGH | All edited files read directly; integration is additive and bounded; two-layer design is clean and consistent with existing patterns. |
| Pitfalls | HIGH (schema) / MEDIUM (integration) | Schema-constraint pitfalls verified against `0.17.3` facts and the actual `star_schema.excalidraw` source (158 elements inspected). Integration/KB-drift pitfalls are design-judgement extrapolations — well-reasoned but not yet empirically tested. |

**Overall confidence:** HIGH for the technical approach; the one MEDIUM-confidence area is the exact parametric geometry of the new primitives (crow's-foot glyph sizing, lifeline pitch), which is why Phase 3 and Phase 4 carry `--research-phase` flags.

### Gaps to Address

- **Open decision: star_schema.excalidraw re-author vs. grandfather.** Must be resolved before Phase 2 begins. If grandfathered, the new example must be clearly distinguished in the index; if re-authored, the re-author should happen in Phase 2 before any new DM examples are modeled on it.
- **Crow's-foot glyph exact geometry.** STACK.md specifies "three short `line` strokes fanning at the entity end" but does not give pixel dimensions, angles, or offsets. Phase 3 research must nail this so all ER examples are consistent.
- **Diamond glyph exact sizing.** STACK.md says ~14px but this is approximate. Phase 3 must document the exact dimensions that read as a glyph (not a box) at typical diagram zoom levels.
- **Actor convention final choice.** STACK.md recommends labelled box over stick-figure but notes "pick ONE convention and document it." Phase 4 must make this a binding KB rule, not a suggestion.
- **Verifier arrowhead-enum check implementation.** The structural validator currently does not reject unknown arrowhead tokens. This check must be added in Phase 3 — the implementation is straightforward but is a code change to `excalidraw_validator.py` that needs explicit roadmap allocation.
- **Hub/link/satellite 3-color palette.** STACK.md says "document the 3-color mapping in the diagram-type KB" but does not specify the colors. Phase 5 must pick accessible, print-safe colors and document them as a binding convention.

---

## Sources

### Primary (HIGH confidence)
- `@excalidraw/excalidraw@0.17.3` `element/types.d.ts` (unpkg) — arrowhead union `arrow|bar|dot|triangle`, strokeStyle, element type union
- `@excalidraw/excalidraw@0.17.3` `constants.d.ts` (unpkg) — `ROUNDNESS` (1/2/3) and `FONT_FAMILY` (incl. Cascadia)
- `.claude/agents/excalidraw/examples_excalidraw/star_schema.excalidraw` — 158 elements inspected; reveals non-compliance with new recipe (0 groupIds, 0 containerId, soft roundness)
- `.claude/agents/excalidraw/examples_excalidraw/{data_pipeline_flow,architecture_overview,process_decision,repo_tree_hierarchy}.excalidraw` — confirms renderable element types and existing arrowhead usage
- `.claude/commands/excalidraw.md` — current Q1/Q2 protocol; edit sites identified
- `.claude/agents/excalidraw/excalidraw_specialist.md` — asset paths, mandates; edit sites identified
- `.claude/agents/excalidraw/kb/README.md` — existing conventions; "Adding a new pattern" workflow
- `.planning/PROJECT.md` — milestone scope, two-tier picker requirement, 4-option cap, loop-untouched constraint
- `.planning/codebase/ARCHITECTURE.md` + `CONCERNS.md` — v1.0 architecture, CDN pin, icon/path security concerns

### Secondary (MEDIUM confidence)
- Creately — UML diagram types/examples (sequence/class/use-case/activity conventions)
- uml-diagrams.org — sequence + activity diagram graphical notation
- Sparx Systems — UML 2 tutorials (sequence/class/use-case/activity)
- Lucidchart — ER diagram symbols and crow's-foot notation
- Exasol / AltexSoft — data warehouse models (star/snowflake/data vault)

---
*Research completed: 2026-06-03*
*Ready for roadmap: yes — pending resolution of the star_schema.excalidraw open decision*
