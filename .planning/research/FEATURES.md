# Feature Research

**Domain:** Diagram-type knowledge layer for an Excalidraw authoring subagent (UML, Data Modeling, Tech Architecture families)
**Researched:** 2026-06-03
**Confidence:** HIGH (UML/data-modeling conventions are stable, well-documented standards; mapping to existing kb sub-patterns is a design judgement at MEDIUM)

## Scope Note

"Features" here = the diagram TYPES the new `diagram-types/` KB layer must cover. Each type below is a candidate KB entry. The downstream consumer (KB author + roadmapper) needs, per type:
purpose · must-have structural elements · how-to-draw sketch · which existing `kb/` sub-patterns compose inside it · complexity · dependencies.

The existing 13 `kb/` patterns are the **primitive layer**. Each diagram type is a **recipe** that composes 2-5 of those primitives. The mapping below is the load-bearing output: it tells the KB author exactly which primitive files each type file should `@`-reference instead of re-deriving geometry.

The agent already ships `examples/example_star_schema.png` — star schema is the cheapest type to author (ground truth exists).

---

## Feature Landscape

### Table Stakes (Must Ship — a "diagram families" milestone is incomplete without these)

| Type (Family) | Why Expected | Complexity | Notes |
|---------------|--------------|------------|-------|
| **Tech Architecture** (Tech Arch) | The plugin's bread-and-butter; `architecture_overview.png` already exists as ground truth. The default thing people draw. | LOW | Mostly a reframe of existing macro patterns. No new notation. |
| **ER diagram** (Data Modeling) | The universal "how do my tables relate" diagram; most-requested data model; gateway to all other DM types. | MEDIUM | Crow's-foot notation needs custom connector endpoints Excalidraw doesn't ship natively (drawn with small line glyphs). |
| **Star schema** (Data Modeling) | Canonical analytics model; example PNG already exists. | LOW | Pure fan-out of dimensions around one fact table. Ground truth in hand. |
| **Sequence diagram** (UML) | The most-drawn UML type in practice; what engineers reach for to explain a flow. | MEDIUM | Lifelines + activation bars + ordered messages; vertical-time discipline is the hard part. |
| **Class diagram** (UML) | The foundational UML diagram; defines the structure everything else references. | MEDIUM-HIGH | Three-compartment boxes + 5 relationship arrow styles (the arrowheads are the fiddly part). |

### Differentiators (Ship If Phase Budget Allows — valued, not assumed)

| Type (Family) | Value Proposition | Complexity | Notes |
|---------------|-------------------|------------|-------|
| **Activity diagram** (UML) | Workflow/business-process visualization; overlaps heavily with the existing Flow/Process family, so cheap to add. | LOW-MEDIUM | Largely a relabel of existing decision-branch + linear-pipeline + swimlanes. Highest reuse of existing primitives. |
| **Use-case diagram** (UML) | Quick stakeholder-facing overview of "who does what with the system." | LOW | Simplest UML type: actors (stick figures) + ovals + a boundary box. New glyphs (stick figure, oval) but trivial layout. |
| **Snowflake schema** (Data Modeling) | Normalized star; shows dimension hierarchies. | MEDIUM | Builds directly on star schema — star + tree-hierarchy on the dimension arms. Don't author before star. |

### Anti-Features (Don't Build / Defer)

| Type | Why Tempting | Why Problematic | Alternative |
|------|--------------|-----------------|-------------|
| **Full UML 14-type set** (state, component, deployment, timing, etc.) | "Complete UML support" sounds thorough | Long tail of rarely-drawn types; each needs its own notation research; dilutes the milestone. PROJECT.md explicitly defers them. | Ship the core 4 (sequence/class/use-case/activity). Add others reactively. |
| **Data vault** (Data Modeling) | Completes the data-warehouse story | Most complex DM type; hub/link/satellite semantics + raw/business-vault layering; niche audience. Builds on ER + star concepts. | Defer to v1.2 or author last, after ER + star + snowflake validate the DM authoring approach. |
| **Auto-layout / graph-routing engine** for class/ER relationships | Would place boxes "optimally" | Out of scope; the agent places by composing fixed-geometry primitives, not by running a layout solver. | Keep composing primitives with grid-snapped coordinates as today. |
| **Live notation validator** (e.g. "is this valid UML?") | Sounds rigorous | The verifier checks render correctness, not semantic UML conformance. Scope creep into the verifier. | KB files document conventions; the human/agent judges semantics. |

---

## Per-Type Spec (the core deliverable)

Each block is concrete enough for a KB author to write the `diagram-types/<type>.md` file directly.

### TECH ARCHITECTURE (Tech Arch family) — TABLE STAKES, LOW

- **Purpose:** Show the technologies, services, and cloud/infra components of a system and how they connect — "what talks to what, and inside which boundary."
- **Must-have elements:** Named component nodes (each = brand icon + label); logical/environment boundaries; directed connectors showing data/control flow; optional zoom panels for multi-facet systems.
- **How to draw:** Place components as icon-blocks. Wrap related components in titled boundary boxes (Dev/Prod, a cloud, a service mesh). Connect with elbow arrows. For a system overview, tile multiple boundary boxes as zoom panels.
- **Composes sub-patterns:** `group-container` (boundaries — the backbone), `icon-block` (every node), `multi-zoom-overview` (system-level facets), `fan-out`/`convergence` (one service to many / many to one), `linear-pipeline` (request paths). Optional `evidence-card` (cost/throughput callouts).
- **Good vs beginner:** *Good* = every node inside a named boundary, connectors are orthogonal elbows landing on borders, consistent icon sizing. *Beginner* = floating unlabeled boxes, crossing diagonal arrows, no grouping, mixed icon scales.
- **Dependencies:** None — pure reuse of existing macro patterns; author first as the "warm-up" entry.

### UML — SEQUENCE (UML family) — TABLE STAKES, MEDIUM

- **Purpose:** Show how participants (objects/actors) interact over time for one scenario, and the order of those interactions. (Creately: "show how objects interact… and the order those interactions occur.")
- **Must-have elements:** **Participant heads** (named boxes) across the top; **lifelines** (dashed vertical line dropping from each head); **activation bars** (thin rectangles on a lifeline = object is busy); **messages** as horizontal arrows — solid line + filled arrowhead for synchronous calls, dashed line + open arrowhead for returns, half-open arrowhead for async; **self-messages** (arrow looping back to the same lifeline). Temporal order is strictly top-to-bottom.
- **How to draw:** Lay participant boxes in a horizontal row at the top (use icon-block per head). Drop a dashed lifeline from each box center. Draw the first message as a horizontal arrow left→right between two lifelines; start an activation bar on the receiver. Stack each subsequent message lower on the Y axis (time flows down). Add return arrows (dashed) for every synchronous call.
- **Composes sub-patterns:** `timeline` (the top-to-bottom time axis is a vertical timeline — strongest analog), `task-list` (the vertical stack of ordered interactions with side participants mirrors task-list's vertical+side-I/O geometry), `icon-block` (participant heads). New primitives needed: dashed lifeline + activation-bar rectangle (candidate new `kb/` primitive).
- **Good vs beginner:** *Good* = strict vertical time ordering, return arrows present for sync calls, activation bars start/end at the right messages, ≤6 participants. *Beginner* = missing return messages, messages out of time order, no activation bars, one mega-diagram covering many scenarios (should split). (These are the explicit mistakes the sources flag.)
- **Dependencies:** Introduces lifeline + activation-bar primitive; sequence is the first UML type to author so this primitive lands here.

### UML — CLASS (UML family) — TABLE STAKES, MEDIUM-HIGH

- **Purpose:** Foundational structural diagram: classes, their attributes and operations, and the relationships between them.
- **Must-have elements:** **Three-compartment box** per class — name (top), attributes (middle), operations/methods (bottom); visibility markers (`+ - #`); **multiplicity** adornments on association ends (`1`, `0..*`, `1..*`); and the **five relationship arrow styles**: association (plain line), aggregation (hollow diamond at the whole), composition (filled diamond at the whole), inheritance/generalization (hollow triangle pointing at parent), dependency (dashed arrow, open head).
- **How to draw:** Each class is a stacked rectangle group: title row + horizontal divider + attribute lines + divider + method lines. Place related classes near each other; connect with the relationship line whose endpoint glyph encodes the relationship. Inheritance arrows point UP to the parent. Add multiplicity text near each association end.
- **Composes sub-patterns:** `tree-hierarchy` (inheritance trees are exactly parent→children hierarchies — reuse its vertical parent/child geometry), `group-container` (package/module grouping of classes), `evidence-card` (the 3-compartment class box is structurally an evidence-card variant — stacked labeled rows in a bordered box). New primitives: the relationship-endpoint glyphs (diamonds/triangles) are the genuinely new drawing work.
- **Good vs beginner:** *Good* = compartments consistently sized, correct diamond/triangle endpoints, multiplicities labeled, no crossing relationship lines. *Beginner* = wrong arrowhead (using a plain arrow where composition is meant), missing compartments, attributes and methods mixed, no multiplicity.
- **Dependencies:** Reuses tree-hierarchy for the inheritance case; introduces relationship-glyph primitive shared with ER. Author after sequence.

### UML — USE-CASE (UML family) — DIFFERENTIATOR, LOW

- **Purpose:** Graphical overview of actors, the system's functions (use cases), and how they interact — stakeholder-facing scope picture.
- **Must-have elements:** **Actors** (stick figures, outside the boundary); **use cases** (ovals/ellipses, inside); **system boundary** (rectangle enclosing all use cases); **association lines** actor↔use-case; **`<<include>>`** (dashed arrow, mandatory sub-use-case) and **`<<extend>>`** (dashed arrow, optional behavior) relationships.
- **How to draw:** Draw the boundary rectangle. Place use-case ovals inside it. Put actor stick figures to the left/right outside the box. Connect each actor to the use cases it triggers with plain lines. Add dashed `<<include>>`/`<<extend>>` arrows between use cases where needed.
- **Composes sub-patterns:** `group-container` (the system boundary box is exactly a titled container), `fan-out` (one actor associating to many use cases = fan-out geometry), `icon-block` (actor + label). New primitives: stick-figure glyph + oval node (both simple).
- **Good vs beginner:** *Good* = actors outside the boundary, all use cases inside, verb-phrase use-case names, sparing include/extend. *Beginner* = actors inside the box, use cases that are really steps (belongs in activity/sequence), overusing include/extend, no boundary.
- **Dependencies:** None structural beyond new glyphs; simplest UML type — good candidate to author after sequence/class to build momentum.

### UML — ACTIVITY (UML family) — DIFFERENTIATOR, LOW-MEDIUM (highest reuse)

- **Purpose:** Represent a workflow / business or operational process as a flow of activities, including branches and parallelism.
- **Must-have elements:** **Initial node** (filled circle); **activity nodes** (rounded rectangles); **control flow** arrows; **decision/merge** (diamonds); **fork/join** (thick synchronization bars — one-in/many-out for fork, many-in/one-out for join, for parallel flows); **final node** (filled circle in ring); optional **swimlanes** (vertical lanes = responsible actor/object).
- **How to draw:** Start with the initial-node circle. Chain activities with arrows (left-to-right or top-to-bottom). At branches insert a decision diamond with guard-labeled outgoing arrows. For parallel work, insert a fork bar splitting to N flows, rejoin with a join bar. End at the final node. Optionally partition the whole flow into vertical swimlanes.
- **Composes sub-patterns:** `linear-pipeline` (the activity chain), `decision-branch` (decision/merge diamonds — direct reuse), `decision-marker` (inline pass/fail), `feedback-loop` (loops back to a prior activity), `group-container` (swimlanes are labeled containers), `task-list` (vertical activity stacks). Almost entirely existing primitives.
- **Good vs beginner:** *Good* = single initial node, guarded decision branches, fork always matched by a join, clear swimlane ownership. *Beginner* = unmatched fork/join (parallel flows that never sync), unguarded decisions, mixing activity nodes with sequence-style messages.
- **Dependencies:** Highest reuse of existing Flow/Process primitives; minimal new notation (fork/join bars). Cheapest UML type after use-case.

### DATA MODELING — STAR SCHEMA (DM family) — TABLE STAKES, LOW

- **Purpose:** Dimensional analytics model — one central fact table surrounded by denormalized dimension tables for fast BI queries.
- **Must-have elements:** **One central fact table** (measures + foreign keys to dimensions); **N dimension tables** radiating around it; **relationship lines** fact↔each dimension (one fact row references many dimension keys). Table boxes list columns; PK/FK marked.
- **How to draw:** Place the fact table center. Arrange dimension tables in a ring/grid around it (the classic "star"). Connect each dimension to the fact with a relationship line. Each table is a titled box with a column list.
- **Composes sub-patterns:** `fan-out`/`convergence` (the fact-at-center, dimensions-around radial layout = fan-out geometry), `icon-block`/`evidence-card` (each table box is a titled, row-listed container), `group-container` (optional fact/dimension grouping).
- **Good vs beginner:** *Good* = fact clearly central and visually distinct, dimensions evenly placed, FK relationships drawn, ≤8 dimensions. *Beginner* = no visual fact/dimension distinction, normalized (snowflaked) dimensions in a "star," crossing relationship lines.
- **Dependencies:** None — `example_star_schema.png` exists as ground truth. Author first in the DM family; it seeds the table-box primitive snowflake and data-vault reuse.

### DATA MODELING — SNOWFLAKE SCHEMA (DM family) — DIFFERENTIATOR, MEDIUM

- **Purpose:** A normalized star schema — dimension tables are split into sub-dimension hierarchies to remove redundancy.
- **Must-have elements:** Same as star (central fact + dimensions) **plus** normalized dimension branches: each dimension may connect to further sub-dimension tables forming hierarchies (the "snowflake" arms).
- **How to draw:** Start from the star layout. For each dimension that normalizes, attach child sub-dimension tables outward in a small tree, connected by relationship lines. The silhouette becomes branched rather than radial.
- **Composes sub-patterns:** Everything star uses, **plus** `tree-hierarchy` (the normalized dimension arms are parent→child tables — direct reuse) and `linear-pipeline`/chained relationships for the normalization depth.
- **Good vs beginner:** *Good* = clear which dimensions are normalized and why, hierarchy direction consistent, fact still visually central. *Beginner* = over-normalizing every dimension (no analytic benefit), losing the central-fact focus.
- **Dependencies:** **Builds on star schema** — do not author before star. = star + tree-hierarchy.

### DATA MODELING — ER DIAGRAM (DM family) — TABLE STAKES, MEDIUM

- **Purpose:** Show entities (tables), their attributes, and the relationships/cardinalities between them — the universal relational data model.
- **Must-have elements:** **Entity boxes** with attribute lists; **primary key** (bold/underlined) and **foreign key** (italic) markers; **relationship lines** with **crow's-foot cardinality** endpoints — bar = one, crow's foot = many, open circle = zero/optional (e.g. bar+crow's-foot = "one or more," circle+bar = "zero or one"). FK lives on the "many" side.
- **How to draw:** Each entity is a titled box listing its columns with PK/FK styling. Draw relationship lines between related entities; terminate each end with the crow's-foot/bar/circle glyph encoding min+max cardinality. Place strongly-related entities adjacent to minimize line crossings.
- **Composes sub-patterns:** `icon-block`/`evidence-card` (entity = titled, row-listed box), `group-container` (subject-area grouping), `tree-hierarchy` (one-to-many parent/child layout). New primitive: crow's-foot endpoint glyphs (shared concept with class-diagram relationship glyphs — coordinate the two).
- **Good vs beginner:** *Good* = crow's-foot ends show both min and max cardinality, PK/FK visually distinct, few crossing lines, FK on the many side. *Beginner* = plain arrows instead of crow's-foot, cardinality omitted, no PK/FK marking, spaghetti relationship lines.
- **Dependencies:** Introduces the crow's-foot glyph primitive (relate to class-diagram glyph work). Independent of star/snowflake; author alongside star.

### DATA MODELING — DATA VAULT (DM family) — DEFER / NICE-TO-HAVE, HIGH

- **Purpose:** Insert-only, audit-friendly warehouse modeling pattern for agile, scalable historization — separates business keys, relationships, and descriptive history.
- **Must-have elements:** **Hubs** (unique business keys only, no descriptive attrs); **Links** (relationships/transactions between hubs); **Satellites** (descriptive, time-varying attributes — SCD2 history) hanging off hubs and links. Color/shape convention distinguishes the three.
- **How to draw:** Place hub boxes as the spine. Connect hubs through link boxes (a link sits between the hubs it relates). Attach satellite boxes to their parent hub/link with connectors. Use consistent shape/color coding per table class (hub/link/satellite).
- **Composes sub-patterns:** `group-container` (hub-and-spoke clusters), `fan-out` (a hub fanning out to its satellites), `tree-hierarchy` (hub→satellite attachment), `convergence` (links pulling multiple hubs together), `icon-block`/`evidence-card` (table boxes).
- **Good vs beginner:** *Good* = clean hub/link/satellite separation, consistent color coding, satellites only attached to hubs/links. *Beginner* = mixing descriptive attributes into hubs, links carrying attributes (belongs in satellites), confusing it with a star schema.
- **Dependencies:** **Most complex DM type.** Conceptually layers on ER (entities/relationships) and star (table boxes/fan-out). Author LAST in the family, or defer to v1.2. PROJECT.md keeps it in-scope but the roadmapper should treat it as the long-pole entry.

---

## Feature Dependencies

```
Tech Architecture        (standalone — pure reuse of existing macro patterns)

UML core 4:
  Sequence  ──introduces──> [lifeline + activation-bar primitive]
  Class     ──introduces──> [relationship-glyph primitive: diamond/triangle]
                └──shares glyph concept with──> ER (crow's-foot)
  Use-case  ──introduces──> [stick-figure + oval primitives]   (independent, simplest)
  Activity  ──reuses──> existing Flow/Process primitives only   (cheapest UML)

Data Modeling:
  Star schema  ──seeds──> [table-box primitive]   (ground-truth PNG already exists)
       └──required by──> Snowflake (= star + tree-hierarchy)
  ER           ──introduces──> [crow's-foot glyph]   (independent of star)
  Data Vault   ──builds on concepts from──> ER + Star   (most complex; defer/last)
```

### Dependency Notes

- **Snowflake requires Star:** snowflake is literally a normalized star; author star first and reuse its table-box geometry + fan-out.
- **Class & ER share a glyph-drawing problem:** both need non-native endpoint decorations (diamonds/triangles, crow's feet). Solving one informs the other — sequence them adjacently and consider a shared `kb/` relationship-endpoint primitive.
- **Activity overlaps Flow/Process:** it reuses decision-branch, linear-pipeline, feedback-loop, swimlane-via-container almost wholesale — lowest marginal cost; pairs naturally with the existing Flow family.
- **Data Vault is the long pole:** highest complexity, niche audience, conceptually depends on ER + star. Either author last in the milestone or defer.

---

## MVP Definition

### Launch With (this milestone, core)

- [ ] **Tech Architecture** — warm-up; reframes existing patterns, zero new notation.
- [ ] **Star schema** — ground-truth PNG exists; seeds DM table-box primitive.
- [ ] **ER diagram** — universal data model; introduces crow's-foot glyph.
- [ ] **Sequence diagram** — most-used UML; introduces lifeline/activation primitive.
- [ ] **Class diagram** — foundational UML; introduces relationship glyphs (shares with ER).
- [ ] **Activity diagram** — near-free (reuses Flow primitives); rounds out UML core.
- [ ] **Use-case diagram** — simplest UML; small new glyphs only.

### Add After Validation (v1.x)

- [ ] **Snowflake schema** — once star + tree-hierarchy validated. Cheap follow-on.
- [ ] **Data Vault** — once ER + star authoring approach proven. Long pole; safe to slip.

### Future Consideration (v2+)

- [ ] **Remaining UML types** (state, component, deployment, timing, etc.) — reactive, on demand.

## Feature Prioritization Matrix

| Type | User Value | Authoring Cost | Priority |
|------|------------|----------------|----------|
| Tech Architecture | HIGH | LOW | P1 |
| Star schema | HIGH | LOW | P1 |
| Sequence | HIGH | MEDIUM | P1 |
| ER | HIGH | MEDIUM | P1 |
| Class | HIGH | MEDIUM-HIGH | P1 |
| Activity | MEDIUM | LOW | P1 (cheap) |
| Use-case | MEDIUM | LOW | P2 |
| Snowflake | MEDIUM | MEDIUM | P2 |
| Data Vault | LOW-MEDIUM | HIGH | P3 |

## Roadmap Implications (phase-grouping suggestion for the roadmapper)

- **New-primitive work clusters into 3 buckets:** (1) lifeline + activation bar [sequence], (2) relationship-endpoint glyphs: diamonds/triangles + crow's foot [class + ER — co-locate], (3) stick-figure + oval [use-case]. Group KB entries that share a primitive into the same phase so the primitive is built once.
- **Suggested phase shape:** Phase A = Tech Architecture + Activity (zero/low new notation, pure reuse → fast confidence). Phase B = Star + Snowflake (DM table-box + tree reuse; star's PNG de-risks it). Phase C = ER + Class (shared glyph primitive). Phase D = Sequence + Use-case (their own new primitives). Data Vault = its own tail phase or deferred.
- **Examples to author:** PROJECT.md wants one canonical `.excalidraw` + PNG per new type. Star already has one. That's 7-8 new example pairs at full scope — a meaningful, separable chunk of effort the roadmapper should size explicitly.

## Sources

- Creately — UML diagram types & examples (sequence/class/use-case/activity conventions): https://creately.com/blog/diagrams/uml-diagram-types-examples/
- uml-diagrams.org — sequence diagram graphical notation (lifeline, message, execution spec): https://www.uml-diagrams.org/sequence-diagrams.html
- Sparx Systems — UML 2 sequence/class/use-case/activity tutorials: https://sparxsystems.com/resources/tutorials/uml2/
- Creately — class diagram relationships (association/aggregation/composition/inheritance): https://creately.com/guides/class-diagram-relationships/
- uml-diagrams.org — activity diagram controls (fork, join, decision, merge): https://www.uml-diagrams.org/activity-diagrams-controls.html
- Lucidchart — ER diagram symbols & crow's-foot notation: https://www.lucidchart.com/blog/er-diagram-symbols-and-notation
- sql-designer.com — crow's-foot cardinality explained: https://sql-designer.com/blog/crowfoot-notation
- Exasol — data warehouse models (star, snowflake, data vault): https://www.exasol.com/hub/data-warehouse/models-modeling/
- AltexSoft — Data Vault architecture (hub/link/satellite): https://www.altexsoft.com/blog/data-vault-architecture/
- Existing KB primitives: `.claude/agents/excalidraw/kb/README.md` and pattern files (tree-hierarchy, group-container, fan-out, etc.)

---
*Feature research for: diagram-type KB layer (UML + Data Modeling + Tech Architecture families)*
*Researched: 2026-06-03*
