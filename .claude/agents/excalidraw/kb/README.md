# Excalidraw Knowledge Base

Everything the Excalidraw Visual Architect agent reads on demand lives under this `kb/` folder. It is organized in two layers plus the canonical example assets, all in one place.

## How to navigate

```
kb/
├── README.md          ← you are here — the map
├── patterns/          ← PRIMITIVE layer: reusable layout sub-patterns (geometry + JSON skeletons)
│   ├── README.md          ← primitive index (macro / flow / decision / structure)
│   ├── fan-out.md, convergence.md, tree-hierarchy.md, …
│   └── (15 pattern files)
└── diagram-types/     ← TYPE layer: one recipe per diagram type, WITH its example assets
    ├── README.md          ← type index + authoritative resolver table
    ├── tech-architecture.md, star-schema.md, sequence.md, …  (recipe files)
    ├── <name>.png             ← canonical reference render (visual ground truth)
    └── <name>.excalidraw      ← editable source for that render, side by side
```

**Two layers, one rule:** a diagram *type* is a **composition of** primitives, not "a kind of" primitive.

| Layer | Folder | Granularity | Answers |
|---|---|---|---|
| **TYPE** | [`diagram-types/`](diagram-types/README.md) | one file per *diagram type* (`tech-architecture.md`, `star-schema.md`, …) | *What is this diagram for, and how do I assemble it from primitives?* |
| **PRIMITIVE** | [`patterns/`](patterns/README.md) | one file per *layout sub-pattern* (`fan-out.md`, `tree-hierarchy.md`, …) | *What is the geometry + JSON skeleton of this reusable shape?* |

A type file **composes primitives by `@`-reference** (`@../patterns/<pattern>.md`) and **never re-derives geometry** — coordinate math and JSON skeletons live only in `patterns/`. Type files link *down* to the primitives they compose; each composed primitive carries a `> Used by types:` back-ref. The two indexes cannot silently drift.

## Where the example images live

Every canonical example PNG sits **inside its diagram type's subfolder under `diagram-types/`, next to the recipe that owns it**, together with its editable `.excalidraw` source (same basename) — e.g. `diagram-types/sequence/sequence_login_flow.png`. *The diagram type and its image live together.*

- To **see** what a type should look like: open `diagram-types/<type>/<name>.png`.
- To **edit** a reference: open `diagram-types/<type>/<name>.excalidraw`, change it, re-render — the PNG beside it is the output.
- To find **which image demonstrates which pattern**: see the reference example index in [`patterns/README.md`](patterns/README.md); to find **which image belongs to which type**: see the resolver table in [`diagram-types/README.md`](diagram-types/README.md).

## Reading order for authoring a diagram

1. Resolve the diagram **type** → read [`diagram-types/README.md`](diagram-types/README.md), find the resolver-table row.
2. Read the type recipe `diagram-types/<type>/<type>.md` **first** — it names which primitives to compose and which `.png` is ground truth.
3. Read each composed primitive `patterns/<pattern>.md` for its geometry + JSON skeleton.
4. Read the canonical `diagram-types/<type>/<name>.png` as the visual target.

## Conventions (all patterns and types)

- All coordinates are multiples of 20 (grid alignment).
- All elements use `roughness: 0`; text uses `fontFamily: 3` (monospace).
- Full color palette, text hierarchy, and brand colors live in the agent prompt — not duplicated in the KB.
- All example connectors are sharp elbow arrows (`elbowed: true`, `roundness: null`, orthogonal points).
