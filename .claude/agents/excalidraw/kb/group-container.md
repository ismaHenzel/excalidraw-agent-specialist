# Pattern: Group Container

> Used by types: tech-architecture, activity, star-schema, use-case

A bordered rounded rectangle that **carries context** for everything inside it: an environment, a technology boundary, a team's surface area. The single most important macro-pattern in the architect's style — almost every other pattern lives inside one of these.

## When to use

Whenever a set of elements share a context that needs naming: an environment (Dev / Prod), a technology (Databricks / GitLab repo), a logical scope (Pipeline / Orchestrator structure). Containers turn a cloud of nodes into "this happens *inside* X."

## Geometry

- Rounded rectangle, stroke 2px, `strokeColor: "#1e3a5f"` (or brand color), no fill (or very pale fill if you need separation from a parent container).
- Padding: keep 24px on all sides between the inner content's bounding box and the container border.
- Title row at the top-left, **inset 20px from the left edge** and **vertically at y_container + 20**:
  - Brand icon `24 × 24` at `(x + 20, y + 20)`.
  - Title text at `(x + 56, y + 24)`, `fontSize: 20`, `fontFamily: 3`, Title color `#1e40af`.

```
┌─ [icon] Title ──────────────────────────────────┐
│                                                 │
│   (contents — other patterns nest here)         │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Nesting

- Working depth is **2–3 levels**: e.g., *Environment* → *Technology* → *Pipeline*.
- Each level should be visually distinguishable; the common trick is to **drop the title bar** on the innermost level and just use a thin border, since the parent already supplies the context.
- A container without a title is a "grouping rectangle" — fine as the innermost level, never as a top-level element.

## JSON skeleton

```json
[
  {
    "type": "rectangle",
    "x": 100, "y": 100, "width": 720, "height": 360,
    "backgroundColor": "transparent",
    "strokeColor": "#1e3a5f",
    "strokeWidth": 2,
    "roughness": 0,
    "roundness": { "type": 3 }
  },
  {
    "type": "image",
    "x": 120, "y": 120, "width": 24, "height": 24,
    "fileId": "<gitlab-icon-id>"
  },
  {
    "type": "text",
    "x": 156, "y": 124,
    "text": "Dev Branch CI/CD",
    "fontSize": 20, "fontFamily": 3,
    "strokeColor": "#1e40af"
  }
]
```

## See in examples

- `examples/architecture_overview.png` — the outer `Architecture Draw` scope plus three sibling panel containers (Catalog · Repository · Pipeline), each branded at the top-left.
- `examples/repo_tree_hierarchy.png` — a single GitLab-branded `data-platform-monorepo` container wrapping the whole tree.
- `examples/data_pipeline_flow.png` — a GitLab-branded `CI/CD Data Pipeline` container around the flow.

## Notes

- A title without an icon is allowed but reads as weaker — prefer the icon+title pair when a technology owns the scope.
- Use the brand stroke color when the container *is* the technology (Databricks orange `#c2410c`); otherwise use neutral `#1e3a5f`.
- Resist the urge to box everything. The methodology rule (<30% containers) still applies — a container with one child is almost always a mistake.
