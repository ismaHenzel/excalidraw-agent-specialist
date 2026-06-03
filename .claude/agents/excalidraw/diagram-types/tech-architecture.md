# Diagram Type: Tech Architecture

> Layer: TYPE recipe. Composes primitives from [`../kb/`](../kb/README.md); does not re-derive their geometry. Indexed in [`README.md`](./README.md).

## Purpose

A **Tech Architecture** diagram shows the technologies, services, and clouds that make up a system, and the relationships between them — how data and control flow across the boundaries of environments, platforms, and teams. Use it when the audience needs to understand *what the moving parts are and how they connect* rather than the step-by-step behaviour of any single process.

Reach for this type when a request is about: a platform or system overview, a deployment landscape, a service map, a "what does our stack look like" walkthrough, or a multi-facet view (catalog · repository · pipeline) of one platform. This is the Phase-4 smoke-test type — it reuses existing macro primitives wholesale and introduces no new notation.

## How to draw it

Assemble the diagram from the composed primitives below — do not improvise coordinate math here; defer all geometry to the primitive files.

- **Scope every logical area in a container.** Each environment, technology boundary, or team surface is a *group container* with a brand icon + title at the top-left. Containers turn a cloud of nodes into "this happens inside X." Keep nesting to 2–3 levels and stay under the <30% container methodology rule.
- **Represent each technology as an icon block.** The atomic node is a brand logo + label inside a small container — never a raw emoji. This keeps the diagram legible at a glance and consistent with the house icon strategy.
- **Lay out the system as a multi-zoom overview** when showing several facets of one platform in a single canvas (e.g. catalog · repository · pipeline panels side by side).
- **Wire relationships with the flow primitives.** Use *fan-out* where one source dispatches to several destinations, *convergence* where several sources merge into one, and *linear-pipeline* for sequential left-to-right stages. All connectors are sharp elbow arrows (`elbowed: true`, `roundness: null`, orthogonal points) per the house convention — the geometry lives in the primitive files.
- **Keep coordinates on the 20-grid** and `roughness: 0`, `fontFamily: 3` (monospace) for all text, exactly as the primitives specify.

## Composes (primitive layer)

- [`@../kb/group-container.md`](../kb/group-container.md) — bordered, branded scope for each environment / technology / logical area.
- [`@../kb/icon-block.md`](../kb/icon-block.md) — the atomic node: a tech logo + label for each service or technology.
- [`@../kb/multi-zoom-overview.md`](../kb/multi-zoom-overview.md) — arranging multiple facets of one platform in a single overview canvas.
- [`@../kb/fan-out.md`](../kb/fan-out.md) — one source dispatching to several downstream technologies.
- [`@../kb/convergence.md`](../kb/convergence.md) — several sources merging into a single destination service.
- [`@../kb/linear-pipeline.md`](../kb/linear-pipeline.md) — sequential left-to-right stages between technologies.

## Ground truth

- [`../examples/architecture_overview.png`](../examples/architecture_overview.png) — the canonical Tech Architecture reference (reused this phase; no new example authored). Imitate its container/icon/overview composition.
