# Architecture Research

**Domain:** Integrating new diagram FAMILIES + a `diagram-types/` KB layer into the existing `/excalidraw` command + specialist + layout-pattern KB
**Researched:** 2026-06-03
**Confidence:** HIGH (existing files read directly; integration is additive and bounded; peer STACK.md/FEATURES.md supply the per-type specs and dependencies)

> **Scope.** This file answers *how the v1.1 additions plug into the v1.0 architecture* — not what to draw (FEATURES.md) and not which primitives to use (STACK.md). It gives the roadmapper concrete integration points (files to add, files to edit), the new-vs-modified split, the family→type→assets→specialist data flow, and a dependency-honoring build order. **The render→verify→fix loop is untouched.** Every change is additive: one new KB directory, new example pairs, a richer Q1/Q2 in one command file, and a few paragraphs added to one agent file.

---

## Standard Architecture

### System Overview — the two-tier KB and where v1.1 hooks in

```
┌──────────────────────────────────────────────────────────────────────┐
│  /excalidraw command (orchestrator, main conversation)                │
│  ── Q1 family → sub-pick type → Q2 structure ──► resolves a TYPE      │
│     then dispatches the specialist with a RESOLVED ASSET BUNDLE        │
└───────────────┬───────────────────────────────────────┬──────────────┘
                │ Agent(author)                           │ Agent(fix)
                ▼                                          ▲
┌──────────────────────────────────┐         ┌────────────────────────────┐
│ excalidraw_specialist.md          │         │ excalidraw_verifier.md      │
│ reads the bundle it was handed:   │         │ (UNCHANGED — read-only)     │
│  • diagram-types/<type>.md  (NEW) │         └────────────────────────────┘
│  • kb/<sub-pattern>.md  (existing)│  render→verify→fix loop UNCHANGED
│  • examples/<type>.png  (new/old) │
└───────────────┬───────────────────┘
                │ reads on demand
   ┌────────────┴───────────────────────────────────────────────┐
   ▼                          ▼                          ▼        ▼
┌──────────────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────────┐
│ diagram-types/   │  │   kb/*.md    │  │ icons/   │  │ examples/    │
│  *.md   (NEW —   │→@│ LAYOUT       │  │ logos    │  │ PNG ground   │
│  TYPE recipes)   │  │ PRIMITIVES   │  │          │  │ truth        │
│  composes ↓ refs │  │ (existing 13)│  │          │  │ (+ new pairs)│
└────────┬─────────┘  └──────────────┘  └──────────┘  └──────────────┘
         │  diagram-types/README.md = family→type index (NEW)
         └─ each type file @-references the primitive kb/ files it composes
```

**Two-layer KB model (the load-bearing design decision):**

| Layer | Directory | Granularity | Answers | Status |
|-------|-----------|-------------|---------|--------|
| **TYPE layer** (new) | `.claude/agents/excalidraw/diagram-types/` | one file per *diagram type* (`sequence.md`, `class.md`, `star-schema.md`, `er.md`…) | *What is this diagram for, and how do I assemble it from primitives?* | **NEW** |
| **PRIMITIVE layer** (existing) | `.claude/agents/excalidraw/kb/` | one file per *layout sub-pattern* (`fan-out.md`, `tree-hierarchy.md`…) | *What is the geometry + JSON skeleton of this reusable shape?* | **EXISTING — unchanged content, +cross-refs**|

The TYPE layer is a thin **recipe/composition** layer. It never re-derives geometry; it `@`-references the primitive `kb/` files (exactly as the v1.0 specialist already references them) and adds only: purpose, must-have notation, the new-primitive notation workarounds from STACK.md, and the family/type taxonomy.

### Component Responsibilities

| Component | Responsibility | Implementation |
|-----------|----------------|----------------|
| `/excalidraw` Q1 (family) | Pick one of 4 families | AskUserQuestion, 4 options (exactly fits the cap) |
| `/excalidraw` sub-pick (type) | Resolve family→specific type | Plain-text follow-up when family has >4 types (UML has 4, DM has 4 = at the cap) |
| `/excalidraw` resolver | Map resolved type → `{diagram-types/<type>.md, kb sub-patterns[], example PNG}` bundle | A lookup table embedded in the command prose |
| `diagram-types/<type>.md` (NEW) | Per-type recipe: purpose, must-haves, notation workarounds, `@kb/*` composition list, `@examples/*.png` | Markdown, mirrors `kb/` file shape |
| `diagram-types/README.md` (NEW) | Family→type index + the resolver table (single source of truth the command and specialist share) | Markdown index |
| `kb/*.md` (existing) | Primitive geometry/JSON skeletons | Unchanged; gains "Used by types:" back-refs |
| `excalidraw_specialist.md` (edit) | Read the type file FIRST, then its composed primitives | +1 asset path, +1 mandate, edits to Pattern-First mandate |
| `excalidraw_verifier.md` | Verify render correctness | **UNCHANGED** |
| Render pipeline / scripts | Validate + render PNG | **UNCHANGED** (STACK.md: no new primitives, no new deps) |

---

## Recommended Project Structure

```
.claude/agents/excalidraw/
├── excalidraw_specialist.md          # EDIT: +asset path, +type-first mandate
├── excalidraw_verifier.md            # UNCHANGED
├── kb/                               # PRIMITIVE layer — EXISTING
│   ├── README.md                     # EDIT: add a "primitives vs types" note + link to ../diagram-types/
│   ├── fan-out.md … (13 files)       # EDIT (light): add "Used by types:" back-ref line
│   └── …
├── diagram-types/                    # NEW — the TYPE layer
│   ├── README.md                     # NEW: family→type index + resolver table
│   ├── tech-architecture.md          # NEW (Tech Arch family — 1 type)
│   ├── sequence.md                   # NEW (UML)
│   ├── class.md                      # NEW (UML)
│   ├── use-case.md                   # NEW (UML)
│   ├── activity.md                   # NEW (UML)
│   ├── star-schema.md                # NEW (Data Modeling)
│   ├── snowflake-schema.md           # NEW (Data Modeling)
│   ├── er.md                         # NEW (Data Modeling)
│   └── data-vault.md                 # NEW (Data Modeling — last/deferred)
├── examples/                         # EXISTING — add new canonical PNGs
│   ├── example_star_schema.png       # EXISTING (reuse for star-schema.md)
│   ├── example_sequence.png          # NEW (1 per new type)
│   ├── example_class.png             # NEW
│   └── …                             # one PNG per new type
└── examples_excalidraw/              # EXISTING — add source .excalidraw per new PNG
    └── <type>.excalidraw             # NEW sources for the above PNGs
```

### Structure Rationale

- **`diagram-types/` is a sibling of `kb/`, not nested inside it.** They are different *layers*, not parent/child. Nesting would imply a type is "a kind of pattern"; it is a *composition of* patterns. Sibling dirs keep the two read-paths independent and let the specialist's existing relative-path convention extend trivially (one new `<asset_paths>` bullet).
- **`diagram-types/README.md` is the single index** the command's resolver and the specialist both consult — same role `kb/README.md` plays for primitives. Avoids duplicating the family→type→assets mapping in two files (command + agent) where it would drift.
- **New example pairs go in the existing `examples/` + `examples_excalidraw/`** following the documented "add a reference example" workflow already in `kb/README.md` — no new convention.
- **The primitive `kb/` files keep their geometry/JSON skeletons** and gain only a one-line "Used by types:" back-reference, making the cross-layer link bidirectional and discoverable from either side.

---

## Architectural Patterns

### Pattern 1: TYPE file `@`-references PRIMITIVE files (downward composition)

**What:** Each `diagram-types/<type>.md` lists the `kb/` sub-patterns it composes and links them, instead of restating geometry. This is exactly how the v1.0 specialist already treats `kb/` ("a diagram is a composition of named patterns").

**When to use:** Every type file. The FEATURES.md "Composes sub-patterns" line for each type IS this list.

**Cross-reference shape (the explicit two-layer link the roadmapper asked for):**

```markdown
# diagram-types/star-schema.md
## Composes (primitive layer)
- `@../kb/fan-out.md` — dimensions radiating from the central fact
- `@../kb/convergence.md` — FK relationships converging on the fact
- `@../kb/evidence-card.md` — each table box (titled, row-listed)
- `@../kb/group-container.md` — optional fact/dimension grouping
## Ground truth
- `@../examples/example_star_schema.png`
```

**Trade-off:** The type file must stay in sync if a primitive is renamed — mitigated by the bidirectional back-ref and the single `diagram-types/README.md` index.

### Pattern 2: PRIMITIVE file back-references TYPE files (upward discoverability)

**What:** Each touched `kb/*.md` gains one line: `> Used by types: star-schema, snowflake, er` (in the file and/or the index). Makes the new layer discoverable from the existing one.

**When to use:** Only on primitives a type composes (per the FEATURES.md mapping). `decision-branch.md` → activity; `tree-hierarchy.md` → class, snowflake, er, data-vault; etc.

**Trade-off:** Light churn across ~10 existing files, but no geometry changes — purely additive metadata.

### Pattern 3: Command-side resolver table (family/type → asset bundle)

**What:** The `/excalidraw` command, after resolving the type, looks up a small table to know exactly which `diagram-types/<type>.md`, which `kb/<sub-pattern>.md` list, and which `examples/<type>.png` to name in the specialist dispatch. The authoritative copy of this table lives in `diagram-types/README.md`; the command references it ("read `diagram-types/README.md`, find the row for the chosen type, pass its KB files + example").

**When to use:** Step 2/3 of the command protocol, replacing today's ad-hoc "read kb/README.md + relevant PNG".

**Trade-off:** The command now reads `diagram-types/README.md` first (one extra read) — negligible cost, and it keeps the mapping in ONE place.

### Pattern 4: Two-tier picker within the 4-option AskUserQuestion cap

**What:** Q1 = family (exactly 4 → fits the cap). Then a **type sub-pick**:
- **Families with ≤4 types** (UML=4, Data Modeling=4): a SECOND `AskUserQuestion` with the family's types as the ≤4 options. Clean, structured.
- **Families with 1 type** (Tech Architecture): no sub-pick — the family *is* the type; skip straight to Q2.
- **Families that ever exceed 4 types** (future-proofing, and the PROJECT.md "plain-text sub-pick" requirement): a **plain-text follow-up** listing the types as a numbered menu; the user replies with a number/name. This is the escape hatch the 4-option cap forces and is already the established pattern for the command's "describe the structure" branch.

**Current counts (from FEATURES.md):** every shipping family has ≤4 types, so the two-`AskUserQuestion` path covers v1.1 entirely; the plain-text path is the documented fallback for when a family grows past 4 (e.g. full UML set in v2).

**Why not one flat list:** 4 families × up to 4 types = up to 16 leaves, far over the 4-option cap. Two tiers is mandatory, not stylistic.

---

## Data Flow

### Family/type selection → specialist dispatch (the concrete pipeline the roadmapper asked for)

```
User runs /excalidraw
   ↓
Q1 (AskUserQuestion, 4 opts): Tech Architecture | Data Modeling | UML / SW Eng | Flow / Process
   ↓  (resolve family → type)
 ├─ Tech Architecture → (1 type) → type = tech-architecture        [no sub-pick]
 ├─ Data Modeling     → AskUserQuestion: star | snowflake | data-vault | ER
 ├─ UML / SW Eng      → AskUserQuestion: sequence | class | use-case | activity
 └─ Flow / Process    → (existing kinds, or a type sub-pick if mapped)
   ↓  resolved TYPE
Read diagram-types/README.md → look up the type's row →
   { type_file: diagram-types/<type>.md,
     sub_patterns: [kb/<a>.md, kb/<b>.md, …],   ← from FEATURES.md "composes" mapping
     example: examples/<type>.png }
   ↓
Q2 (structure approach) — UNCHANGED (Propose / Describe / Just generate)
   ↓  (if Propose: read the type file + example, present 2–3 compositions naming kb sub-patterns)
   ↓
Agent(excalidraw_specialist, author mode) prompt now ALSO includes:
   • the resolved TYPE name + the absolute diagram-types/<type>.md to read FIRST
   • the explicit kb/<sub-pattern>.md list (as today)
   • the example PNG (as today)
   ↓
render → verify → fix loop  ── UNCHANGED ──►  success / honest-failure
```

### Resolver table (lives in `diagram-types/README.md`; shared by command + specialist)

| Family | Type | Type file | Composes (kb sub-patterns) | Example PNG |
|--------|------|-----------|----------------------------|-------------|
| Tech Architecture | tech-architecture | `tech-architecture.md` | group-container, icon-block, multi-zoom-overview, fan-out, convergence, linear-pipeline | `architecture_overview.png` (reuse) |
| Data Modeling | star-schema | `star-schema.md` | fan-out, convergence, evidence-card, group-container | `example_star_schema.png` (reuse) |
| Data Modeling | snowflake-schema | `snowflake-schema.md` | star's set + tree-hierarchy + linear-pipeline | NEW |
| Data Modeling | er | `er.md` | evidence-card, group-container, tree-hierarchy | NEW |
| Data Modeling | data-vault | `data-vault.md` | group-container, fan-out, tree-hierarchy, convergence, evidence-card | NEW (last/deferred) |
| UML | sequence | `sequence.md` | timeline, task-list, icon-block (+ new lifeline/activation primitive) | NEW |
| UML | class | `class.md` | tree-hierarchy, group-container, evidence-card (+ new relationship-glyph) | NEW |
| UML | use-case | `use-case.md` | group-container, fan-out, icon-block (+ new stick-figure/oval) | NEW |
| UML | activity | `activity.md` | linear-pipeline, decision-branch, decision-marker, feedback-loop, group-container, task-list | NEW |

This single table is the data-flow contract: family selection indexes a row; the row names exactly the type file, the kb files, and the example PNG passed to the specialist.

---

## Required Edits — New vs Modified (explicit for the roadmapper)

### NEW files

| File | Content source |
|------|----------------|
| `.claude/agents/excalidraw/diagram-types/README.md` | The family→type index + resolver table above |
| `.claude/agents/excalidraw/diagram-types/tech-architecture.md` | FEATURES.md Tech Architecture spec |
| `…/diagram-types/{sequence,class,use-case,activity}.md` | FEATURES.md UML specs + STACK.md notation workarounds |
| `…/diagram-types/{star-schema,snowflake-schema,er,data-vault}.md` | FEATURES.md DM specs + STACK.md workarounds |
| `examples/<type>.png` + `examples_excalidraw/<type>.excalidraw` | One canonical pair per NEW type (7–8 pairs; star reuses existing) |
| *(optional)* `kb/<new-primitive>.md` | STACK.md flags 3 candidate new primitives: lifeline+activation-bar (sequence), relationship-endpoint glyph (class+ER), stick-figure/oval (use-case). Decide: add as `kb/` primitives (preferred — reused across types) vs inline in type files. |

### MODIFIED files

| File | Edit | Size |
|------|------|------|
| `.claude/commands/excalidraw.md` | Rewrite Q1 to the 4 families; add the type sub-pick (AskUserQuestion ≤4 / plain-text >4); add "read `diagram-types/README.md`, resolve the row" to step 2; pass `diagram-types/<type>.md` in the dispatch (step 3, the `kb/<pattern>.md` list bullet). §4–§6 loop UNCHANGED. | Moderate — §1–§3 only |
| `.claude/agents/excalidraw/excalidraw_specialist.md` | (a) `<asset_paths>`: add a `Diagram-Type KB` bullet for `diagram-types/`, stating "read the type recipe FIRST, then its composed `kb/` primitives." (b) `<operational_mandates>` #1 (Pattern First): prepend "If the orchestrator names a `diagram-types/<type>.md`, read it first — it tells you which `kb/` primitives to compose and any notation workarounds." (c) optionally `<drawing_methodology>` note on UML/DM notation per STACK.md. | Small — additive |
| `.claude/agents/excalidraw/kb/README.md` | Add a short "Layers" note: primitives here, types in `../diagram-types/`; link out. | Tiny |
| `.claude/agents/excalidraw/kb/*.md` (composed ones) | One "Used by types:" back-ref line each. | Tiny ×~10 |

### UNCHANGED (do not touch)

- `excalidraw_verifier.md`, all of `scripts/`, `excalidraw_validator.py`, the render pipeline, the MCP integration, and `/excalidraw` §4–§6 (the verify→fix loop). STACK.md confirms **zero new dependencies and zero new primitives outside `0.17.3`**, so the renderer/validator need no changes.

---

## Suggested Build Order (honors STACK.md + FEATURES.md dependencies)

The order below front-loads zero-new-notation work to validate the *integration plumbing* before tackling the hard glyph work, and respects every dependency surfaced in FEATURES.md (star before snowflake; shared endpoint-glyph primitive before class+ER co-located; data vault last).

**Phase 0 — Scaffolding (the integration spine; no diagram content yet).**
Create `diagram-types/` + `diagram-types/README.md` (empty resolver table), wire the `/excalidraw` Q1/sub-pick/resolver, and add the `excalidraw_specialist.md` asset path + mandate. Validate the data flow end-to-end with ONE existing type. *Do this first — everything else slots into it.*

**Phase A — Tech Architecture + Activity (zero/low new notation; pure reuse).**
- `tech-architecture.md` reuses existing macro patterns + `architecture_overview.png` (no new example). Fastest possible confidence that the type→primitive composition works.
- `activity.md` reuses decision-branch/linear-pipeline/feedback-loop/task-list wholesale (FEATURES.md: highest reuse, cheapest UML). Only new bit = fork/join bars.
- *Rationale:* no new primitives → proves the plumbing before any glyph research.

**Phase B — Star → Snowflake (DM table-box; star de-risked by existing PNG).**
- `star-schema.md` first — ground-truth PNG already ships; seeds the table-box recipe.
- `snowflake-schema.md` second — **literally star + `tree-hierarchy`; must come after star** (FEATURES.md hard dependency).
- *Rationale:* table-box recipe established once, reused.

**Phase C — ER + Class (co-located; SHARED endpoint-glyph primitive).**
- Build the shared relationship-endpoint glyph primitive ONCE (STACK.md: crow's-foot for ER, diamond/triangle for class — both are composed-glyph workarounds, no native arrowhead). Author `er.md` and `class.md` together so the glyph is built once and reused. **Shared endpoint-glyph primitive before class+ER content** (per the downstream ask).
- *Rationale:* FEATURES.md: "Class & ER share a glyph-drawing problem; sequence them adjacently and consider a shared `kb/` relationship-endpoint primitive."

**Phase D — Sequence + Use-case (each introduces its own new primitive).**
- `sequence.md` introduces the lifeline + activation-bar primitive (STACK.md: dashed `line` + thin `rectangle`).
- `use-case.md` introduces stick-figure/oval (simplest; STACK.md recommends a labelled box as the cheap convention).
- *Rationale:* independent new primitives; no cross-dependency, so they can parallelize or follow C.

**Phase E (or DEFER) — Data Vault.**
- `data-vault.md` LAST. FEATURES.md: most complex DM type, conceptually layers on ER + star, niche audience. PROJECT.md keeps it in scope but flags it as the long pole. **Safe to slip to v1.2.**

**Examples track (parallel):** one `.excalidraw` + PNG per new type (7–8 pairs; star reuses). Each example pair is authored in the phase that introduces its type, then rendered through the existing pipeline and copied into `examples/` per the documented refresh workflow.

### Dependency-honoring summary (the explicit asks)

- **Star before snowflake** → Phase B order enforced.
- **Shared endpoint-glyph primitive before class+ER** → Phase C builds the glyph first, then authors both types against it.
- **Data vault last / deferred** → Phase E (or out to v1.2).
- **Scaffolding before content** → Phase 0; proves the family→type→bundle→specialist flow with an existing type before any new notation is researched.

---

## Anti-Patterns

### Anti-Pattern 1: Nesting `diagram-types/` inside `kb/`

**What people do:** Put type files under `kb/diagram-types/` as "just more patterns."
**Why it's wrong:** Conflates the composition layer with the primitive layer; breaks the clean "a type composes primitives" mental model and the specialist's two-distinct-read-paths flow.
**Do this instead:** Sibling directories; type files `@`-reference `kb/` primitives across the layer boundary.

### Anti-Pattern 2: Duplicating the resolver table in both the command and the agent

**What people do:** Hard-code the family→type→assets mapping in `/excalidraw` AND restate it in the specialist.
**Why it's wrong:** Two copies drift; a renamed primitive or new type must be edited twice.
**Do this instead:** One authoritative table in `diagram-types/README.md`; both the command and the specialist read it.

### Anti-Pattern 3: A flat single-question type picker

**What people do:** One AskUserQuestion listing all ~9–16 types.
**Why it's wrong:** Exceeds the hard 4-option AskUserQuestion cap; PROJECT.md explicitly mandates two-tier.
**Do this instead:** Q1 family (4) → sub-pick type (AskUserQuestion ≤4, or plain-text menu when a family grows past 4).

### Anti-Pattern 4: Touching the verify→fix loop or the renderer

**What people do:** "While I'm in here" edits to `excalidraw_verifier.md` or the render scripts.
**Why it's wrong:** Out of scope; STACK.md confirms zero new deps/primitives; PROJECT.md says the loop is untouched. Risks regressing shipped v1.0 behavior.
**Do this instead:** Keep all v1.1 work additive: new KB dir, new examples, Q1/Q2 prose, specialist asset-path/mandate additions.

### Anti-Pattern 5: Re-deriving geometry inside type files

**What people do:** Paste coordinate math / JSON skeletons into `diagram-types/*.md`.
**Why it's wrong:** Duplicates `kb/` primitives; the two layers diverge.
**Do this instead:** Type files carry purpose + notation + a `@kb/*` composition list + notation *workarounds* (the genuinely new STACK.md content); geometry stays in `kb/`.

---

## Integration Points

### Cross-layer references (how the two KB layers reference each other — explicit)

| Direction | Mechanism | Example |
|-----------|-----------|---------|
| TYPE → PRIMITIVE (down) | `@../kb/<pattern>.md` links in a "Composes" section of each type file | `class.md` → `@../kb/tree-hierarchy.md` |
| PRIMITIVE → TYPE (up) | `> Used by types:` back-ref line in each composed `kb/` file + the `kb/README.md` layers note | `tree-hierarchy.md` → "Used by types: class, snowflake, er, data-vault" |
| Both indexed | `diagram-types/README.md` resolver table is the single map; `kb/README.md` links to it | (table above) |

### Internal boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `/excalidraw` command ↔ specialist | `Agent` tool dispatch prompt (now includes the resolved type file + kb list + example) | Same dispatch mechanism as v1.0; only the bundle contents grow |
| specialist ↔ `diagram-types/` | `Read` (relative path, same convention as `kb/`) | New `<asset_paths>` bullet; read type file FIRST |
| `diagram-types/` ↔ `kb/` | `@`-reference links resolved by the specialist reading both | The composition contract; no code, just markdown links |
| command ↔ `diagram-types/README.md` | `Read` to resolve the type's asset row | One extra read in step 2 |

---

## Sources

- `.claude/commands/excalidraw.md` — current Q1/Q2 protocol + dispatch + the untouched §4–§6 loop — **HIGH** (read directly)
- `.claude/agents/excalidraw/excalidraw_specialist.md` — `<asset_paths>`, `<operational_mandates>` #1 (Pattern First), `<drawing_methodology>` — the exact edit sites — **HIGH** (read directly)
- `.claude/agents/excalidraw/kb/README.md` — existing index + "Adding a new pattern" workflow the new layer mirrors — **HIGH** (read directly)
- `.planning/research/STACK.md` (peer) — zero new deps/primitives; notation workarounds (lifeline, glyphs, crow's-foot) the type files carry — **HIGH**
- `.planning/research/FEATURES.md` (peer) — per-type "composes sub-patterns" mapping = the resolver table source; dependency graph (star→snowflake, class/ER shared glyph, data-vault last) — **HIGH**
- `.planning/PROJECT.md` (Current Milestone) — two-tier picker, 4-option cap, diagram-types layer, loop-untouched constraints — **HIGH**
- `.planning/codebase/ARCHITECTURE.md` — confirms the v1.0 agent→kb/icons/examples read-path the new layer extends — **HIGH**

---
*Architecture research for: integrating diagram families + `diagram-types/` KB layer into the existing `/excalidraw` plugin*
*Researched: 2026-06-03*
