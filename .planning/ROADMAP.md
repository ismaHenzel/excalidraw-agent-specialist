# Roadmap: Excalidraw Specialist — Self-Verifying Diagram Authoring

## Overview

This roadmap spans two milestones on the same Excalidraw subagent plugin.

**Milestone v1.0 (Phases 1–3, COMPLETE)** closed the render-and-verify gap: a standalone verifier subagent, a mandatory render→verify→fix loop in the specialist, and end-to-end validation of self-healing and honest-failure behavior.

**Milestone v1.1 (Phases 4–9)** reorganizes the plugin around four recognizable real-world diagram families and adds a `diagram-types/` knowledge layer so the agent draws UML, data models, and tech architectures correctly — *without disturbing the v1.0 loop, validator, or verifier behavior*. The work is additive: one new KB directory (TYPE layer), a two-tier family/type picker, per-type recipe files that compose the existing `kb/` primitives, and one canonical example pair per shipped type. The journey front-loads the integration spine and zero-new-notation types to prove the plumbing before the hard glyph work, then sequences the harder types so each shared primitive is built exactly once.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3, …): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order. v1.1 continues the integer sequence from v1.0's last phase (3), so v1.1 begins at Phase 4 — numbering is NOT reset per milestone.

### Milestone v1.0 — Self-Verifying Loop (COMPLETE)

- [x] **Phase 1: Verifier Subagent** - Standalone verifier subagent with structural + visual checks and structured pass/fail output
- [x] **Phase 2: Closed-Loop Specialist Integration** - Main specialist always renders, hands off to verifier, auto-fixes up to 3 iterations, enforces emoji policy at generation, manages sibling artefacts
- [x] **Phase 3: End-to-End Closed-Loop Validation** - Exercise the full loop on representative defect diagrams to confirm self-healing and honest-failure behavior

### Milestone v1.1 — Diagram Families & UML Expansion

- [ ] **Phase 4: Taxonomy Spine & Star Resolution** - Two-tier family/type picker, `diagram-types/` KB layer + resolver table + notation-workaround conventions, specialist wiring, compartmented-box primitive, and resolution of the legacy `star_schema.excalidraw` — all proven against one existing type
- [x] **Phase 5: Tech Architecture + Activity** - The two zero/low-new-notation types, proving the type→primitive composition workflow on pure reuse (completed 2026-06-05)
- [x] **Phase 6: Star Schema → Snowflake** - The data-modeling table-box recipe established on star, then extended to its normalized variant (completed 2026-06-07)
- [ ] **Phase 7: ER + Class** - The shared relationship-endpoint-glyph convention built once, then both compartmented-relationship types authored against it
- [ ] **Phase 8: Sequence + Use-Case** - Sequence's geometry-heavy lifeline/activation primitive and the most-native-friendly use-case type
- [ ] **Phase 9: Data Vault** - The long-pole data-modeling type, layering hub/link/satellite semantics onto the proven recipe

## Phase Details

### Phase 1: Verifier Subagent

**Goal**: A standalone `excalidraw_verifier` subagent exists that takes a `.excalidraw` file + sibling PNG, runs both a structural pre-check and a multimodal visual review, and returns a structured pass/fail report — and it can be exercised in isolation against known-good and known-bad fixtures.
**Depends on**: Nothing (first phase)
**Requirements**: VRFY-01, VRFY-02, CONT-01 (structural pre-check half)
**Success Criteria** (what must be TRUE):

  1. The file `.claude/agents/excalidraw/excalidraw_verifier.md` exists with valid YAML frontmatter (`name: excalidraw_verifier`, tools include Read, Grep, Glob) and can be invoked as a Claude Code subagent
  2. Invoking the verifier on a known-good diagram (no overflow, valid arrows, present icons, no raw emoji) returns `{ passed: true, issues: [] }` as a parseable structured object
  3. Invoking the verifier on a diagram containing a raw Unicode emoji codepoint in a `text` element with `fontFamily: 3` returns `{ passed: false, issues: [...] }` with at least one issue whose `check` identifies the emoji and whose `element_id` points at the offending text element — without consuming vision tokens (structural pre-check catches it)
  4. Invoking the verifier on a diagram whose rendered PNG visibly shows text overflowing its container returns `{ passed: false, issues: [...] }` with an issue whose `check` is text-overflow-related and includes a `suggested_fix` string
  5. Each issue object in the report carries the five keys `check`, `element_id`, `severity`, `detail`, `suggested_fix` — verifiable by parsing the verifier's last assistant message as the documented schema

**Plans**: TBD

### Phase 2: Closed-Loop Specialist Integration

**Goal**: The existing `excalidraw_specialist.md` is revised so that every diagram delivery path mandatorily renders via `scripts/validate_and_render.sh`, hands the resulting PNG + JSON to `excalidraw_verifier`, parses the structured report, auto-fixes on failure up to 3 iterations, manages sibling-only artefacts, and refuses to emit raw emoji codepoints at generation time.
**Depends on**: Phase 1
**Requirements**: LOOP-01, LOOP-02, LOOP-03, CONT-01 (generation-side half)
**Success Criteria** (what must be TRUE):

  1. When the specialist is invoked to create any diagram, a sibling `.png` exists next to the `.excalidraw` file before the agent claims completion — there is no code path in the agent prompt that lets it deliver a `.excalidraw` without a corresponding rendered PNG
  2. When the verifier returns `passed: false`, the specialist mutates the source JSON based on the `suggested_fix` hints, re-runs `validate_and_render.sh`, and re-invokes the verifier — repeating up to 3 total verify attempts
  3. On a verifier `passed: false` after the 3rd attempt, the specialist's final message to the user contains: (a) the path to the failed PNG, (b) the full structured issue list, (c) the path to the source `.excalidraw` — and does not claim success
  4. When the user requests an emoji in a diagram, the specialist generates an `image` element pointing to a matching `icons/*.png` rather than a `text` element containing the raw Unicode codepoint — verifiable by inspecting the generated JSON
  5. After any iteration of the loop, only one PNG and at most one verifier-report sibling exist next to the `.excalidraw` file — earlier-iteration PNGs are overwritten, not accumulated

**Plans**: `02-01-PLAN.md` — surgical edit to `excalidraw_specialist.md` (adds `<content_policy>` + `<verification_loop>` sections, revises mandates #5 and #7). See `02-01-SUMMARY.md` for the success-criteria → prompt-substring traceability table.

### Phase 3: End-to-End Closed-Loop Validation

**Goal**: The closed loop behaves correctly on representative defect cases — it self-heals fixable defects, surfaces stubborn defects honestly after 3 attempts, and produces clean artefact directories. This phase validates the full milestone before declaring it shipped; no new requirements are introduced.
**Depends on**: Phase 2
**Requirements**: (none — acceptance gate validating VRFY-01, VRFY-02, LOOP-01, LOOP-02, LOOP-03, CONT-01 end-to-end)
**Success Criteria** (what must be TRUE):

  1. Running the specialist on a request that historically produced text-overflow output now delivers a rendered PNG with text fitting its container, achieved within 3 verify-fix iterations
  2. Running the specialist on a request that asks for an emoji glyph (e.g. "add a checkmark next to the success node") delivers a rendered PNG where the glyph is a brand/functional icon from `icons/`, not a missing-glyph box
  3. Running the specialist on a deliberately under-specified or impossible request (one that the verifier will keep failing) results in a final user-facing message that includes the failed PNG path, the structured issues, and the source JSON path — and explicitly does not say "done" or equivalent
  4. After any specialist run, the output directory contains exactly the `.excalidraw` source plus one sibling `.png`, with no `.excalidraw.v1`, `.excalidraw.v2`, or numbered-iteration artefacts

**Plans**: `03-01-PLAN.md` — scenario corpus (`fixtures/e2e/scenarios/`) + artefact-side check script (`scripts/e2e_check.sh`) + operator protocol (`fixtures/e2e/README.md`). Real specialist runs are operator-driven (interactive Claude Code session). See `03-01-SUMMARY.md` for the success-criteria → check-script-assert traceability table.

### Phase 4: Taxonomy Spine & Star Resolution

**Goal**: The integration spine exists and is proven end-to-end against ONE existing diagram type before any new notation is authored. The `/excalidraw` command asks a two-tier family→type pick; a single authoritative resolver table in `diagram-types/README.md` maps the resolved type to its recipe file, composed `kb/` sub-patterns, and example PNG; the specialist reads the type recipe first; the reusable compartmented-box construction and the fixed notation-workaround conventions are documented once; and the legacy `star_schema.excalidraw` is resolved (re-authored or grandfathered) so all references will be mutually consistent before new canonical examples are authored.
**Depends on**: Phase 3 (v1.0 loop must be shipped and frozen)
**Requirements**: TAX-01, TAX-02, TAX-03, DTKB-01, DTKB-02, DTKB-03, DTKB-04, INT-01, INT-02, EX-02
**Success Criteria** (what must be TRUE):

  1. Running `/excalidraw` presents exactly four families — Tech Architecture, Data Modeling, UML / SW-Engineering, Flow / Process — as the top-level `AskUserQuestion`, and a family with multiple types triggers a second type sub-pick within the 4-option cap, with a documented plain-text numbered-menu fallback for any family that grows past four types
  2. A `diagram-types/` directory exists as a sibling of `kb/` with a `diagram-types/README.md` whose single resolver table maps each type to its recipe file, its composed `kb/*.md` sub-patterns, and its canonical example PNG; selecting any wired type in `/excalidraw` dispatches the specialist with exactly that type's recipe + sub-pattern list + example (verified against one existing type as a smoke test)
  3. The diagram-type KB commits to one convention per ambiguous notation forced by the fixed `arrow|bar|dot|triangle|null` arrowhead set (crow's-foot cardinality, aggregation/composition diamonds, generalization triangle, actor representation, multiplicity), and documents the reusable compartmented-box construction (sharp rectangle + horizontal `line` dividers + per-row monospace `text` bound by `groupIds`, with multi-line single `text` blocks explicitly disallowed) once for reuse by all later compartmented types
  4. The two KB layers cross-reference each other: type files link down to the primitives they compose, and the primitive `kb/README.md` documents the two-layer relationship so the layers cannot silently drift
  5. The existing `star_schema.excalidraw` is explicitly resolved — either re-authored to the grouped/bound/sharp convention or grandfathered with a documented reason recorded in `diagram-types/README.md` — and this decision is recorded before any new canonical example is authored**Plans**: 3 plans

**Wave 1**

- [ ] 04-01-PLAN.md — diagram-types/ layer + authoritative resolver table + tech-architecture recipe + two-layer cross-refs + star_schema (EX-02) resolution
- [ ] 04-02-PLAN.md — committed notation-workaround conventions (DTKB-04) + reusable compartmented-box construction (INT-02)

**Wave 2** *(blocked on Wave 1 completion)*

- [~] 04-03-PLAN.md — /excalidraw two-tier family/type picker + resolver wiring (TAX-01/02/03) + specialist reads type recipe first (INT-01) + end-to-end smoke test (sections 4-6 frozen) — Tasks 1-2 complete; Task 3 awaiting human smoke test

**UI hint**: yes

### Phase 5: Tech Architecture + Activity

**Goal**: The two lowest-cost diagram types ship, validating the type-file→primitive-composition workflow on pure reuse of existing `kb/` primitives before any glyph research is invested. Tech Architecture reframes the existing architecture/overview material (reusing `architecture_overview.png`); Activity reuses decision-branch / linear-pipeline / feedback-loop / task-list wholesale.
**Depends on**: Phase 4
**Requirements**: ARCH-01, UML-04
**Success Criteria** (what must be TRUE):

  1. `diagram-types/tech-architecture.md` exists, reframes the architecture/overview material as the Tech Architecture type, and names the group-container / icon-block / multi-zoom-overview / fan-out / convergence / linear-pipeline sub-patterns it composes (referencing the `kb/` primitives, not re-deriving geometry)
  2. `diagram-types/activity.md` exists and authoring an activity-diagram request (start/end nodes, action nodes, decision-branch gates, optional swimlanes) yields a rendered PNG that passes the full validate→render→verify loop
  3. A canonical example pair exists and is indexed in `diagram-types/README.md` for each shipped type (Activity gets a new `.excalidraw` + PNG; Tech Architecture reuses the existing `architecture_overview.png`), each passing the full loop
  4. The composed `kb/*.md` primitives gain "Used by types:" back-references so the two-layer link is discoverable from the primitive side

**Plans**: 3 plans

**Wave 1**

- [x] 05-01-PLAN.md — ARCH-01: confirm tech-architecture recipe + complete kb `Used by types:` back-refs (two-layer cross-ref)
- [x] 05-02-PLAN.md — UML-04: author `diagram-types/activity.md` recipe composing existing primitives

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 05-03-PLAN.md — UML-04/EX-01/EX-03: author canonical Activity example pair, pass the full loop (visual checkpoint), promote resolver row

**UI hint**: yes

### Phase 6: Star Schema → Snowflake

**Goal**: The reusable data-modeling table-box recipe (the compartmented box from Phase 4) is established on star schema, then extended to its normalized snowflake variant. Star is authored first as a hard dependency — snowflake is literally star + a normalized dimension tree-hierarchy. The parametric divider/row alignment that all later compartmented types depend on is solved and verifier-checkable here.
**Depends on**: Phase 4 (compartmented-box primitive, star resolution), Phase 5 (composition workflow proven)
**Requirements**: DM-01, DM-03
**Success Criteria** (what must be TRUE):

  1. `diagram-types/star-schema.md` exists and authoring a star-schema request (central fact + dimension entity boxes, fan-out composition) yields a rendered PNG that passes the full loop, with compartment dividers spanning the full box width and rows sharing a common left x
  2. `diagram-types/snowflake-schema.md` exists (building on star-schema with a normalized dimension tree-hierarchy) and authoring a snowflake request yields a rendered PNG that passes the full loop — and snowflake is authored only after star is passing
  3. A canonical example pair (`.excalidraw` + PNG) exists and is indexed for both star schema and snowflake, each passing the full validate→render→verify loop, consistent with the star resolution from Phase 4
  4. The compartmented entity boxes use separate per-row monospace `text` elements (never a single multi-line `text`) so dividers stay placeable and the verifier's width-fit check stays valid

**Plans**: 2 plans

**Wave 1**

- [x] 06-01-PLAN.md — DM-01: finalize compartmented-box offsets + author `star-schema.md` + compliant `star_schema_v2` example pair (full loop) + resolver row + kb back-refs

**Wave 2** *(blocked on Wave 1 — snowflake authored only after star passes, SC-2)*

- [x] 06-02-PLAN.md — DM-03: author `snowflake-schema.md` (star + normalized dimension tree-hierarchy) + `snowflake_schema` example pair (full loop) + resolver row + tree-hierarchy/linear-pipeline back-refs (completed 2026-06-07; EX-03 gate approved)

**UI hint**: yes

### Phase 7: ER + Class

**Goal**: The single hardest unsolved drawing problem — non-native relationship-endpoint glyphs (crow's-foot cardinality, aggregation/composition diamonds, generalization triangle) — is solved once as a shared convention/primitive, then both compartmented-relationship types are authored against it. ER and class are co-located so the shared endpoint-glyph work is done exactly once, per the committed conventions from Phase 4 (DTKB-04). No illegal arrowhead token ever ships.
**Depends on**: Phase 6 (compartmented table-box recipe), Phase 4 (DTKB-04 glyph conventions)
**Requirements**: DM-02, UML-02
**Success Criteria** (what must be TRUE):

  1. The shared relationship-endpoint-glyph convention is built once and referenced by both type files: every relationship connector uses only legal arrowhead tokens (`arrow|bar|dot|triangle|null`) plus composed `line`/`diamond`/`ellipse` glyphs or textual multiplicity — no illegal arrowhead value appears in any authored JSON
  2. `diagram-types/er.md` exists and authoring an ER request (entity boxes with PK/FK row prefixes, the committed crow's-foot/bar/dot or textual cardinality convention) yields a rendered PNG that passes the full loop, with each relationship's cardinality visually distinguishable from a plain association
  3. `diagram-types/class.md` exists and authoring a class request (three-compartment boxes, association/aggregation/composition/generalization via the committed glyph workarounds, stereotypes via guillemets) yields a rendered PNG that passes the full loop
  4. A canonical example pair (`.excalidraw` + PNG) exists and is indexed for both ER and class, each passing the full validate→render→verify loop

**Plans**: TBD
**UI hint**: yes

### Phase 8: Sequence + Use-Case

**Goal**: The two remaining UML core types ship, each introducing its own independent new primitive. Sequence introduces the geometry-heavy lifeline + activation-bar primitive (fixed center-x per participant, monotonically increasing message Y). Use-case is the most native-friendly UML type (native ovals, labelled-box actors per the committed convention, system-boundary via group-container).
**Depends on**: Phase 7 (relationship/endpoint glyph experience; verifier hardening de-risks geometry-sensitive sequence)
**Requirements**: UML-01, UML-03
**Success Criteria** (what must be TRUE):

  1. `diagram-types/sequence.md` exists and authoring a sequence request (participant heads, dashed lifelines, activation bars, ordered solid messages, dashed returns) yields a rendered PNG that passes the full loop, with each activation bar centered on its lifeline x and message Y values increasing top-to-bottom
  2. `diagram-types/use-case.md` exists and authoring a use-case request (actors via the committed convention, use-case ovals, system boundary via group-container) yields a rendered PNG that passes the full loop
  3. A canonical example pair (`.excalidraw` + PNG) exists and is indexed for both sequence and use-case, each passing the full validate→render→verify loop

**Plans**: TBD
**UI hint**: yes

### Phase 9: Data Vault

**Goal**: The most complex data-modeling type ships last, layering hub/link/satellite semantics onto the proven compartmented-box + fan-out + tree-hierarchy recipes. The three table classes are distinguished by a documented, accessibility-safe palette paired with a text role label (never color alone). Kept in v1.1 scope per explicit user decision.
**Depends on**: Phase 6 (star/snowflake table-box), Phase 7 (ER relationships)
**Requirements**: DM-04
**Success Criteria** (what must be TRUE):

  1. `diagram-types/data-vault.md` exists and authoring a data-vault request (hubs as the spine, links between hubs, satellites attached to hubs/links) yields a rendered PNG that passes the full validate→render→verify loop
  2. The hub/link/satellite distinction uses a documented 3-role palette paired with a text role label so the three classes remain distinguishable in grayscale (no color-only distinction)
  3. A canonical example pair (`.excalidraw` + PNG) exists and is indexed for data vault, passing the full loop

**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Verifier Subagent | 3/3 | Complete | 2026-05-23 |
| 2. Closed-Loop Specialist Integration | 1/1 | Complete | 2026-05-24 |
| 3. End-to-End Closed-Loop Validation | 1/1 | Complete (artefact-side; specialist runs are operator-driven) | 2026-05-24 |
| 4. Taxonomy Spine & Star Resolution | 2/3 (Task 3 checkpoint:human-verify) | Executing — awaiting smoke test | 2026-06-03 (partial) |
| 5. Tech Architecture + Activity | 3/3 | Complete   | 2026-06-05 |
| 6. Star Schema → Snowflake | 2/2 | Complete   | 2026-06-07 |
| 7. ER + Class | 0/? | Not started | - |
| 8. Sequence + Use-Case | 0/? | Not started | - |
| 9. Data Vault | 0/? | Not started | - |
