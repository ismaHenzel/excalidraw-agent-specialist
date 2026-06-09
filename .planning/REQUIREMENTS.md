# Requirements: Excalidraw Specialist — Diagram Families & UML Expansion (v1.1)

**Defined:** 2026-06-03
**Core Value:** The agent draws recognizable, real-world diagram families (tech architecture, data models, UML) correctly — guided by a per-diagram-type knowledge layer — while preserving the self-verifying render→verify→fix loop shipped in v1.0.

> **Numbering note:** v1.0 requirements (VRFY-*, LOOP-*, CONT-*) are all shipped; they are
> recorded in PROJECT.md's "Validated" section. This file is scoped to v1.1's NEW
> requirements. New category prefixes (TAX, DTKB, INT, DM, UML, ARCH, EX) start at 01.

## v1.1 Requirements

Requirements for this milestone — reorganizing the plugin around diagram families and adding a
diagram-type knowledge layer plus UML and data-modeling types.

### Taxonomy & Picker (TAX)

- [ ] **TAX-01**: The `/excalidraw` command's intent step presents four diagram **families** — Tech Architecture, Data Modeling, UML / SW-Engineering, Flow / Process — as the top-level choice (replacing today's four vague "kinds")
- [ ] **TAX-02**: When the chosen family has more than one type, the command asks a second **type** sub-pick (sequence/class/use-case/activity for UML; star/snowflake/data-vault/ER for Data Modeling); single-type families skip the sub-pick. The two-tier flow respects `AskUserQuestion`'s 4-option cap, with a documented plain-text numbered-menu fallback for any family that grows past 4 types
- [ ] **TAX-03**: The resolved family+type drives dispatch: it selects the matching `diagram-types/<type>.md` recipe, the relevant layout sub-pattern `kb/*.md` files, and the canonical example PNG that get passed to the specialist — via a single authoritative resolver table

### Diagram-Type KB Layer (DTKB)

- [ ] **DTKB-01**: A new KB layer `diagram-types/` exists as a sibling of `kb/`, with a `diagram-types/README.md` index containing the authoritative resolver table (type → recipe file · composed sub-patterns · example PNG)
- [ ] **DTKB-02**: Each diagram-type file states the type's **purpose** (what it's for / when to use it), **how to draw it** (required structural elements + conventions), and the list of existing layout sub-patterns it **composes** — referencing the primitive `kb/*.md` files rather than re-deriving their geometry
- [ ] **DTKB-03**: The two KB layers cross-reference each other: type files link down to the primitives they compose; the primitive `kb/README.md` documents the two-layer relationship so the layers cannot silently drift
- [ ] **DTKB-04**: The diagram-type KB documents the notation **workarounds** forced by the fixed Excalidraw arrowhead set (`arrow|bar|dot|triangle|null` only) — composed-glyph or textual-label conventions for crow's-foot cardinality, UML aggregation/composition diamonds, and generalization triangles — and commits to a single convention for each ambiguous notation (e.g. textual multiplicity vs. crow's-foot glyph; stick-figure vs. labelled-box actor)

### Specialist & Loop Integration (INT)

- [ ] **INT-01**: `excalidraw_specialist.md` is revised so that, given a resolved family+type, it reads the `diagram-types/<type>.md` recipe **first** and consults the composed sub-patterns it names — without changing the existing render→verify→fix loop, validator, or verifier behavior
- [ ] **INT-02**: The reusable **compartmented-box** construction (sharp rectangle + horizontal `line` dividers + per-row monospace `text` bound by `groupIds`) is documented once and reused by UML class and all data-model entity types — multi-line single `text` blocks are explicitly disallowed for compartments so dividers and the verifier's width-fit check stay valid

### Data Modeling Types (DM)

- [x] **DM-01**: A `diagram-types/star-schema.md` recipe exists and the agent can author a star-schema diagram (central fact + dimension entity boxes, fan-out composition) that passes the full loop
- [x] **DM-02**: A `diagram-types/er.md` recipe exists and the agent can author an ER diagram (entity boxes with PK/FK rows, committed cardinality notation) that passes the full loop
- [x] **DM-03**: A `diagram-types/snowflake-schema.md` recipe exists (building on star-schema with normalized dimension tree-hierarchy) and the agent can author a snowflake diagram that passes the full loop
- [ ] **DM-04**: A `diagram-types/data-vault.md` recipe exists (hub / link / satellite, distinguished by the semantic palette) and the agent can author a data-vault diagram that passes the full loop

### UML Types (UML)

- [x] **UML-01**: A `diagram-types/sequence.md` recipe exists and the agent can author a UML sequence diagram (lifelines, activation bars, ordered solid messages, dashed returns) that passes the full loop
- [x] **UML-02**: A `diagram-types/class.md` recipe exists and the agent can author a UML class diagram (compartmented boxes, association/aggregation/composition/generalization via the committed glyph workarounds) that passes the full loop
- [x] **UML-03**: A `diagram-types/use-case.md` recipe exists and the agent can author a UML use-case diagram (actors, ovals, system boundary via group-container) that passes the full loop
- [x] **UML-04**: A `diagram-types/activity.md` recipe exists and the agent can author a UML activity diagram (start/end nodes, actions, decision-branch gates, optional swimlanes) that passes the full loop

### Tech Architecture (ARCH)

- [ ] **ARCH-01**: A `diagram-types/tech-architecture.md` recipe exists, reframing the existing architecture/overview material as a Tech Architecture diagram type (technologies, services, clouds and their relationships) composing group-container / icon-block / multi-zoom-overview sub-patterns

### Canonical Examples (EX)

- [ ] **EX-01**: One canonical reference pair (`examples/<type>.png` + `examples_excalidraw/<type>.excalidraw`) exists for each shipped family/type, indexed in `diagram-types/README.md`, and serves as visual ground truth for the specialist
- [ ] **EX-02**: The existing `star_schema.excalidraw` is resolved against the new recipe — either re-authored to the grouped/bound/sharp-roundness convention or explicitly grandfathered with a documented reason — before new examples are authored, so all references are mutually consistent
- [ ] **EX-03**: Every canonical example must pass the full `validate → render → verify` loop; "the type's canonical example passes the loop" is a required exit criterion of the phase that ships that type

## v2 Requirements

Deferred to future milestones.

### Additional UML (UMLX)

- **UMLX-01**: Remaining UML types beyond the core 4 (state machine, component, deployment, object, package, communication, timing, composite-structure, profile, interaction-overview)

### Hardening (carried from v1.0)

- **HARD-01**: Vendor the `@excalidraw/excalidraw@0.17.3` JS bundle into the Docker image (remove CDN dependency on `esm.sh`)
- **HARD-02**: Clean up `icons/` (collapse 8 Databricks variants; remove non-icon PNGs)
- **HARD-03**: Sandbox path resolver in `render_excalidraw.py`
- **HARD-04**: SDK-driven E2E harness that spawns the specialist subagent and validates the loop without an operator

## Out of Scope

Explicitly excluded from this milestone. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Remaining ~10 UML types (state, component, deployment, …) | Core 4 (sequence/class/use-case/activity) ship first; rest deferred to v2 to keep the milestone shippable |
| Native crow's-foot / hollow-triangle / diamond arrowheads | Not in the `0.17.3` arrowhead enum; the milestone uses composed-glyph/textual workarounds, not a renderer change |
| Multi-tool diagram support (Mermaid, draw.io, PlantUML import) | Plugin stays Excalidraw-specific; types are authored as native `.excalidraw`, not transpiled |
| Pixel-diff visual regression of new examples vs. a baseline | Verifier judges per-diagram correctness, not stylistic similarity; consistent with v1.0 scope decision |
| Auto-generating diagrams from source code / schemas (e.g. class diagram from a codebase) | This milestone is about drawing conventions + KB, not reverse-engineering inputs |
| Changing the render→verify→fix loop, validator, or verifier internals | v1.0 loop is frozen; v1.1 is additive — new KB layer + family wiring only |

## Traceability

Updated during roadmap creation (v1.1 phases 4–9).

| Requirement | Phase | Status |
|-------------|-------|--------|
| TAX-01 | Phase 4 | Pending |
| TAX-02 | Phase 4 | Pending |
| TAX-03 | Phase 4 | Pending |
| DTKB-01 | Phase 4 | Pending |
| DTKB-02 | Phase 4 | Pending |
| DTKB-03 | Phase 4 | Pending |
| DTKB-04 | Phase 4 | Pending |
| INT-01 | Phase 4 | Pending |
| INT-02 | Phase 4 | Pending |
| EX-02 | Phase 4 | Pending |
| ARCH-01 | Phase 5 | Pending |
| UML-04 | Phase 5 | Complete |
| DM-01 | Phase 6 | Complete |
| DM-03 | Phase 6 | Complete |
| DM-02 | Phase 7 | Complete |
| UML-02 | Phase 7 | Complete |
| UML-01 | Phase 8 | Complete |
| UML-03 | Phase 8 | Complete |
| DM-04 | Phase 9 | Pending |
| EX-01 | Phases 5–9 | Pending |
| EX-03 | Phases 5–9 | Pending |

> **EX-01 / EX-03 are cross-cutting exit criteria, not a standalone phase.** Each shipped
> type's canonical example pair (EX-01) must pass the full validate→render→verify loop (EX-03)
> as a required exit criterion of the phase that ships that type (Phases 5–9). EX-02 (resolving
> the legacy `star_schema.excalidraw`) is a one-time gate sequenced in Phase 4, before any new
> canonical example is authored.

**Coverage:**

- v1.1 requirements: 21 total
- Mapped to phases: 21 (every requirement maps to at least one phase; EX-01/EX-03 are deliberately cross-cutting across Phases 5–9)
- Unmapped: 0

---
*Requirements defined: 2026-06-03*
*Traceability mapped to phases: 2026-06-03*
