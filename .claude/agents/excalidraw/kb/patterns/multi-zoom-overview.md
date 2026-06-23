# Pattern: Multi-Zoom Overview

> Used by types: tech-architecture

A **meta-layout** that places multiple sub-diagrams side-by-side inside one canvas, each one showing a different *facet* of the same system: catalog structure, repository layout, conceptual pipeline, practice pipeline. The viewer can scan the whole architecture in one screen and zoom mentally between perspectives.

## When to use

System overview slides, onboarding diagrams, architecture decision records — anywhere you need to show *what the thing is* across multiple dimensions (data / code / runtime / cost). Use sparingly; this is the heaviest macro-pattern.

## Geometry

- Outer "Architecture Draw" container spanning the canvas width.
- Inner panels arranged in a row (or grid for 5+ panels). Each panel is itself a Group Container with its own title.
- Standard panel width: `260`–`560` depending on density; height matches the tallest panel (align tops, not bottoms — Western reading order).
- Panel gap: `40px` horizontal.
- Above the row, a slim **evidence strip** can carry Evidence Cards (cost, metrics) — see `evidence-card.md`.
- Below the row, a separate `Developer Example` container provides a *worked* concrete instance of everything above.

```
┌─ Architecture Draw ───────────────────────────────────────────────────────┐
│  ┌ Catalog ─┐  ┌ Catalog ─┐  ┌ Catalog ─┐  ┌ Repo ───┐  ┌ Pipeline ────┐ │
│  │ dev      │  │ qs       │  │ prod     │  │ src/    │  │ Conceptual + │ │
│  │ ...      │  │ ...      │  │ ...      │  │  data/  │  │ Practice     │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘  └──────────────┘ │
└───────────────────────────────────────────────────────────────────────────┘
┌─ Developer Example ( Linus Torvalds ) ────────────────────────────────────┐
│  ( same layout, scoped to one user's slice )                               │
└────────────────────────────────────────────────────────────────────────────┘
```

## Panel composition

Each panel is one of the other patterns:
- **Catalog listings** → vertical list of items with colored leading bullets (gold, silver, platinum, quarentine).
- **Repository structure** → `tree-hierarchy.md`.
- **Conceptual pipeline** → DAG: feeders → join → final → quality check.
- **Practice pipeline** → real screenshot-like cards showing actual outputs ("Output records: 1996").

## Worked-example section

When the overview is long, add a `Developer Example ( <persona name> )` container *below* the overview, replicating the layout but scoped to one user's path. This is the visual equivalent of "here's the same thing with my specific numbers" — much more memorable than abstract structure alone.

## See in examples

- `../diagram-types/tech-architecture/architecture_overview.png` — canonical multi-zoom: an evidence strip on top, then `Architecture Draw` with three panels (Catalog · Repository · Pipeline), then a `Developer Example ( Ada Lovelace )` worked-example below, with a violet trace following one component across all three facets.

## Notes

- This pattern is **earned**, not default. Use it only for system-level overviews. Single-flow diagrams should stay single-flow.
- All panels share the same fontFamily/roughness/colors — heterogeneity *within* a panel is fine, heterogeneity *between* panels destroys the meta-layout.
- The persona name in the developer example matters more than you'd think. It anchors the diagram in a story.
