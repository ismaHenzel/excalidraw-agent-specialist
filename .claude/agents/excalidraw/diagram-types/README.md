# Diagram Types (the TYPE layer)

This directory is the **TYPE layer** of the two-layer Excalidraw KB. It is a **sibling of `../kb/`**, not nested inside it — a diagram *type* is a **composition of** primitives, not "a kind of" primitive.

## Two-layer KB

| Layer | Directory | Granularity | Answers |
|---|---|---|---|
| **TYPE layer** (this dir) | `diagram-types/` | one file per *diagram type* (`tech-architecture.md`, `star-schema.md`, …) | *What is this diagram for, and how do I assemble it from primitives?* |
| **PRIMITIVE layer** | [`../kb/`](../kb/README.md) | one file per *layout sub-pattern* (`fan-out.md`, `tree-hierarchy.md`, …) | *What is the geometry + JSON skeleton of this reusable shape?* |

A type file **composes primitives by `@`-reference** (`@../kb/<pattern>.md`) and **never re-derives geometry** — coordinate math and JSON skeletons live only in `../kb/`. The two layers cross-reference each other so they cannot silently drift: type files link *down* to the primitives they compose; each composed primitive carries a `> Used by types:` back-ref, and `../kb/README.md` documents this relationship and links back here.

## Resolver table

This is the **single authoritative** family → type map shared by the `/excalidraw` command and the specialist. Do not duplicate it elsewhere — both read this one table to resolve a chosen type into its recipe file, composed `kb/` sub-patterns, and canonical example PNG.

| Family | Type | Type file | Composes (kb sub-patterns) | Example PNG |
|--------|------|-----------|----------------------------|-------------|
| Tech Architecture | tech-architecture | `tech-architecture.md` | group-container, icon-block, multi-zoom-overview, fan-out, convergence, linear-pipeline | `../examples/architecture_overview.png` (reuse) |
| Data Modeling | star-schema | `star-schema.md` | fan-out, convergence, evidence-card, group-container | `../examples/star_schema_v2.png` |
| Data Modeling | snowflake-schema | `snowflake-schema.md` | star's set + tree-hierarchy + linear-pipeline | `../examples/snowflake_schema.png` |
| Data Modeling | er | `er.md` | compartmented-box, relationship-endpoint, notation-conventions | `../examples/er_retail_orders.png` |
| Data Modeling | data-vault | `data-vault.md` _(planned — Phase 9)_ | group-container, fan-out, tree-hierarchy, convergence, evidence-card | _(planned)_ |
| UML | sequence | `sequence.md` | lifeline-activation, notation-conventions | `../examples/sequence_login_flow.png` |
| UML | class | `class.md` | compartmented-box, relationship-endpoint, notation-conventions | `../examples/class_order_domain.png` |
| UML | use-case | `use-case.md` | group-container, notation-conventions | `../examples/use_case_checkout.png` |
| UML | activity | `activity.md` | linear-pipeline, decision-branch, decision-marker, feedback-loop, group-container, task-list | `../examples/activity_order_fulfillment.png` |

> **Wired rows:** **tech-architecture** (Phase-4 smoke-test type), **activity** (wired as of Phase 5 — canonical example `activity_order_fulfillment.excalidraw` passes the full validate→render→verify loop), **star-schema** (wired as of Phase 6 — canonical example `star_schema_v2.excalidraw` passes the full loop; resolver points at the new compliant `star_schema_v2.png`, the legacy `example_star_schema.png` is de-indexed), **snowflake-schema** (wired as of Phase 6 Plan 02 — canonical example `snowflake_schema.excalidraw` passes the full loop; resolver points at `snowflake_schema.png`), **er** (wired as of Phase 7 Plan 02 — canonical example `er_retail_orders.excalidraw` passes the full validate→render→verify loop; EX-03 visual gate approved 2026-06-07; resolver points at `er_retail_orders.png`), **class** (wired as of Phase 7 Plan 03 — canonical example `class_order_domain.excalidraw` passes the full validate→render→verify loop; EX-03 visual gate approved 2026-06-07; resolver points at `class_order_domain.png`), **sequence** (wired as of Phase 8 — canonical example `sequence_login_flow.excalidraw` passes the full validate→render→verify loop; EX-03 visual gate approved 2026-06-07; resolver points at `sequence_login_flow.png`), and **use-case** (wired as of Phase 8 — canonical example `use_case_checkout.excalidraw` passes the full validate→render→verify loop; EX-03 visual gate approved 2026-06-08; resolver points at `use_case_checkout.png`). Rows marked _(planned)_ are placeholders for later phases — their recipe file and/or canonical example are not yet authored, so they MUST NOT be claimed as wired until the phase that ships them.

## Legacy example resolution

**Subject:** the pre-v1.1 legacy data-model example — `examples_excalidraw/star_schema.excalidraw` and its rendered PNG `examples/example_star_schema.png`.

**Disposition: GRANDFATHERED (EX-02, Option B).** The legacy `star_schema.excalidraw` is **grandfathered** as a pre-v1.1 legacy example. Its geometry is **not mutated** in Phase 4.

**Verified non-compliance** (inspected source, 158 elements): every `groupIds` array is empty (0 grouped box units), 0 `containerId`, 0 `boundElements` (all 113 monospace texts are free-floating, manually positioned), arrows have `startBinding`/`endBinding` of `null` (unbound, not glued to borders) and `roundness: {type: 2}`, and the outer container uses `roundness: {type: 3}` (soft, not the sharp `roundness: null` the new recipe mandates for formal boxes and connectors).

**Reason for grandfathering:**
- The **compliant** star-schema example — authored to the grouped / bound / sharp-roundness compartmented-box recipe — is **deferred to Phase 6** (the phase that establishes the data-modeling table-box recipe). Re-authoring it now is out of Phase 4's critical path.
- Star is **not** the Phase-4 smoke-test type; **tech-architecture** is. Phase 4 only needs to prove the type→primitive composition plumbing against one existing type.

**Explicit warning:** the legacy `star_schema.excalidraw` is **NOT a safe template** for the new grouped/bound/sharp recipe. Do not imitate its free-floating, unbound, soft-cornered style when authoring new compartmented-box examples.

**Phase 6 resolution (DM-01):** the compliant canonical star example is now authored — `examples_excalidraw/star_schema_v2.excalidraw` + `examples/star_schema_v2.png` — and the resolver row points at it. The legacy `star_schema.excalidraw` / `example_star_schema.png` remain on disk as historical artifacts but are **de-indexed** as the star canonical (per RESEARCH Open Question 1 resolution).

## Adding a diagram type

Mirrors the `../kb/README.md` "Adding a new pattern" procedure:

1. Create `diagram-types/<type>.md` with sections: *Purpose*, *How to draw it*, *Composes (primitive layer)* (`@../kb/<pattern>.md` links — never re-derive geometry), and *Ground truth* (`@../examples/<type>.png`).
2. Add the canonical example **pair** — `examples_excalidraw/<type>.excalidraw` source + rendered `examples/<type>.png` — and confirm it passes the full validate → render → verify loop before indexing.
3. Add **exactly ONE** row to the resolver table above, under the correct family, naming the type file, the composed `kb/` sub-patterns, and the example PNG.
4. Add a `> Used by types: <type>` back-ref line to each composed `../kb/<pattern>.md` so the two-layer link stays bidirectional.
