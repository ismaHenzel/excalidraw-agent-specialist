# Excalidraw Layout Patterns (the PRIMITIVE layer)

Compact pattern references for the Excalidraw Visual Architect agent. Each pattern file is small enough to read on demand. The canonical reference PNGs that show these patterns in real diagrams live one level over in [`../diagram-types/`](../diagram-types/README.md), beside the diagram-type recipe that owns each image.

## Layers

This directory is the **PRIMITIVE layer** — one file per reusable layout sub-pattern (geometry + JSON skeletons). Per-type recipes live in the sibling [`../diagram-types/`](../diagram-types/README.md), the **TYPE layer**: one file per diagram type (tech-architecture, star-schema, sequence, …). A type file *composes* these primitives by `@`-reference and never re-derives their geometry. The two layers cross-reference each other so they cannot silently drift — composed primitives below carry `> Used by types:` back-refs, and the [diagram-types resolver table](../diagram-types/README.md) is the single family→type map. For the whole-KB map start at the [kb hub README](../README.md).

## Index

### Macro (composition / scope)
| Pattern | File | When |
|---|---|---|
| Group Container | `group-container.md` | Bordered scope with brand icon + title — environments, technologies, logical groupings |
| Multi-Zoom Overview | `multi-zoom-overview.md` | System overviews showing multiple facets (catalog · repo · pipeline) in one canvas |

### Flow (control / data)
| Pattern | File | When |
|---|---|---|
| Linear Pipeline | `linear-pipeline.md` | Sequential steps, left-to-right |
| Fan-out | `fan-out.md` | One source dispatches to N destinations |
| Convergence | `convergence.md` | N sources merge into one destination |
| Task List | `task-list.md` | Vertical stack of tasks with side I/O (read DB, call API) |
| Feedback Loop | `feedback-loop.md` | Arrow returning to an earlier stage (retry, restart) |
| Timeline | `timeline.md` | Events along a horizontal time axis |

### Decision
| Pattern | File | When |
|---|---|---|
| Decision Branch | `decision-branch.md` | Diamond gate with labeled outcomes (≥2 conditions) |
| Decision Marker | `decision-marker.md` | Inline ✗/✓ circles for binary pass/fail gates |

### Structure (atomic / reference)
| Pattern | File | When |
|---|---|---|
| Icon Block | `icon-block.md` | The atomic node: tech logo + label inside a container |
| Tree / Hierarchy | `tree-hierarchy.md` | Folder trees, catalog schemas, namespace breakdowns |
| Evidence Card | `evidence-card.md` | Real-data cards (cost, metrics, output samples) |
| Relationship Endpoint | `relationship-endpoint.md` | ER / UML connector endpoints (cardinality bars, diamonds, arrowheads) |
| Lifeline / Activation | `lifeline-activation.md` | Sequence-diagram lifelines and activation bars |

## Reference example index

The reference PNGs now live **beside the diagram-type recipe that owns each one**, in `../diagram-types/`. Each pattern file's *See in examples* section links the specific PNG(s) that demonstrate it.

| Image | Patterns demonstrated |
|---|---|
| `../diagram-types/architecture_overview.png` | `multi-zoom-overview`, `group-container`, `icon-block`, `tree-hierarchy`, `evidence-card`, persona worked-example |
| `../diagram-types/data_pipeline_flow.png` | `linear-pipeline`, `fan-out`, `convergence`, `feedback-loop`, `decision-marker`, `group-container` |
| `../diagram-types/process_decision.png` | `decision-branch`, `decision-marker`, `task-list`, `timeline`, `feedback-loop`, side I/O |
| `../diagram-types/repo_tree_hierarchy.png` | `tree-hierarchy`, `group-container`, `icon-block` |
| `../diagram-types/example_star_schema.png` | legacy user-authored data-model example (dimensional / star schema); **de-indexed** as the star canonical — see `../diagram-types/star_schema_v2.png` |

> Each reference image's editable `.excalidraw` source sits next to it in `../diagram-types/` (same basename). Edit the source there, re-render it, and the PNG beside it refreshes the reference. All connectors in these examples are sharp elbow arrows (`elbowed: true`, `roundness: null`, orthogonal points).

## Conventions used across all patterns

- All coordinates are multiples of 20 (grid alignment).
- All elements use `roughness: 0` and text uses `fontFamily: 3` (monospace).
- Full color palette, text hierarchy, and brand colors live in the agent prompt — not duplicated here.
- Coordinates in each pattern are illustrative starting values; translate them rigidly as a group when placing the pattern at a different origin.

## Adding a new pattern

1. Create `kb/patterns/<pattern-name>.md` with sections: *When*, *Geometry*, *JSON skeleton*, *Notes*. Include a *See in examples* section pointing to any `../diagram-types/<name>.png` that demonstrates it.
2. Add a row to the index above (in the right category).
3. If a diagram type composes the new pattern, add a `> Used by types: <type>` back-ref so the two-layer link stays bidirectional.
