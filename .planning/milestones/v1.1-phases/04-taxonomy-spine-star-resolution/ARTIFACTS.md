# Phase 4 — Artifacts this phase produces

Authoritative list of every NEW file and every new doc section/anchor created in Phase 4 (Taxonomy Spine & Star Resolution). Consumed by /gsd-execute-phase and by downstream phases (5-9) that index types into the resolver table.

## New files

| Path | Created by | Purpose |
|------|------------|---------|
| `.claude/agents/excalidraw/diagram-types/` (directory) | 04-01 | The TYPE layer, a SIBLING of `kb/` (not nested) |
| `.claude/agents/excalidraw/diagram-types/README.md` | 04-01 | Authoritative family→type resolver table + "Legacy example resolution" record (EX-02) |
| `.claude/agents/excalidraw/diagram-types/tech-architecture.md` | 04-01 | Smoke-test type recipe composing existing `kb/` primitives |
| `.claude/agents/excalidraw/diagram-types/notation-conventions.md` | 04-02 | Committed arrowhead-workaround conventions (DTKB-04) |
| `.claude/agents/excalidraw/diagram-types/compartmented-box.md` | 04-02 | Reusable compartmented-box construction (INT-02) |

## Modified files (additive only)

| Path | Modified by | Edit |
|------|-------------|------|
| `.claude/agents/excalidraw/kb/README.md` | 04-01 | "## Layers" two-layer note linking to `../diagram-types/README.md` (DTKB-03) |
| `.claude/agents/excalidraw/kb/group-container.md` | 04-01 | `> Used by types: tech-architecture` back-ref |
| `.claude/agents/excalidraw/kb/icon-block.md` | 04-01 | `> Used by types: tech-architecture` back-ref |
| `.claude/agents/excalidraw/kb/multi-zoom-overview.md` | 04-01 | `> Used by types: tech-architecture` back-ref |
| `.claude/agents/excalidraw/kb/fan-out.md` | 04-01 | `> Used by types: tech-architecture` back-ref |
| `.claude/agents/excalidraw/kb/convergence.md` | 04-01 | `> Used by types: tech-architecture` back-ref |
| `.claude/agents/excalidraw/kb/linear-pipeline.md` | 04-01 | `> Used by types: tech-architecture` back-ref |
| `.claude/agents/excalidraw/examples_excalidraw/star_schema.excalidraw` | 04-01 | EX-02: grandfathered by default (geometry untouched), or re-authored to grouped/bound/sharp under Option A |
| `.claude/commands/excalidraw.md` | 04-03 | Sections 1-3 rewritten to the two-tier picker + resolver (TAX-01/02/03); sections 4-6 + Rules byte-identical (FROZEN) |
| `.claude/agents/excalidraw/excalidraw_specialist.md` | 04-03 | `<asset_paths>` diagram-types/ bullet + `<operational_mandates>` #1 "read type recipe first" (INT-01); loop/contract unchanged |

## New doc sections / anchors

| Anchor | File | Created by |
|--------|------|------------|
| `## Legacy example resolution` | `diagram-types/README.md` | 04-01 (placeholder) → 04-01 Task 3 (EX-02 record) |
| Resolver table (`\| Family \| Type \| Type file \| Composes (kb sub-patterns) \| Example PNG \|`) | `diagram-types/README.md` | 04-01 |
| "Adding a diagram type" procedure | `diagram-types/README.md` | 04-01 |
| `## Layers` | `kb/README.md` | 04-01 |

## Explicitly NOT touched (FROZEN v1.0)

`scripts/` (incl. `validate_and_render.sh`, `excalidraw_validator.py`), `excalidraw_verifier.md`, the render pipeline, and sections 4-6 + "## Rules" of `.claude/commands/excalidraw.md` (sha256 of the `### 4.`-to-EOF region pinned to `c1604b18abcf442774a7a097646901691dcddaa18af637237f0d21409eb6bcba`).

## Multi-source coverage audit

| Source item | Type | Covered by | Status |
|-------------|------|-----------|--------|
| Phase 4 goal: two-tier picker + resolver + conventions + specialist wiring + star resolution, proven against one type | GOAL | 04-01, 04-02, 04-03 | COVERED |
| TAX-01 four families | REQ | 04-03 Task 1 | COVERED |
| TAX-02 type sub-pick + numbered-menu fallback | REQ | 04-03 Task 1 | COVERED |
| TAX-03 resolver-table dispatch | REQ | 04-03 Task 1+3 | COVERED |
| DTKB-01 diagram-types/ sibling + resolver README | REQ | 04-01 Task 1 | COVERED |
| DTKB-02 per-type recipe (purpose/how/composes, references primitives) | REQ | 04-01 Task 2 | COVERED |
| DTKB-03 two-layer cross-references | REQ | 04-01 Task 1 | COVERED |
| DTKB-04 committed notation workarounds | REQ | 04-02 Task 1 | COVERED |
| INT-01 specialist reads type recipe first | REQ | 04-03 Task 2 | COVERED |
| INT-02 reusable compartmented-box construction | REQ | 04-02 Task 2 | COVERED |
| EX-02 resolve legacy star_schema.excalidraw | REQ | 04-01 Task 3 | COVERED |
| Arrowhead constraint (arrow\|bar\|dot\|triangle\|null) workarounds | RESEARCH | 04-02 Task 1 | COVERED |
| Compartmented-box recipe + multi-line prohibition | RESEARCH | 04-02 Task 2 | COVERED |
| diagram-types/ sibling-not-nested; single resolver (no drift) | RESEARCH/ARCH | 04-01 Task 1 | COVERED |
| star_schema non-compliance (0 groupIds, soft roundness, unbound) | RESEARCH/PITFALLS | 04-01 Task 3 | COVERED |
| Smoke-test scaffolding against one existing type | RESEARCH/ARCH | 04-03 Task 3 | COVERED |
| Loop/validator/verifier FROZEN (additive only) | CONTEXT (STATE decisions) | All plans (threat models + freeze sha) | COVERED |
| Two-tier picker; diagram-types sibling of kb | CONTEXT (STATE decisions) | 04-03 / 04-01 | COVERED |
| Not a git repo (no commits) | CONTEXT | N/A — planner writes files only | COVERED |

Exclusions (not gaps): DM-*, UML-*, ARCH-01, EX-01, EX-03 are scoped to Phases 5-9; v2 items (UMLX-01, HARD-*) and Out-of-Scope items per REQUIREMENTS.md.
