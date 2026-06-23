# Pattern: Tree / Hierarchy

> Used by types: snowflake-schema, data-vault

Vertical parent → children rendering for folder structures, repo layouts, namespace trees, catalog schemas. Children indent right and connect to the parent with right-angle elbow arrows.

## When to use

Repository folder structure, Unity Catalog schema, namespace breakdown, file taxonomy — any "this contains these" relationship where the order doesn't imply time.

## Geometry

- Each node: icon (`24 × 24`) + label text directly to its right.
- Parent at `(x_p, y_p)`. Children at `(x_p + 60, y_child_i)`.
- Vertical y-step between siblings: `40px` (compact) or `48px` (comfortable).
- Connector arrow from parent: leaves at the parent's bottom-center `(x_p + 12, y_p + 28)`, drops to `y_child_i + 12`, turns right into the child's left edge `(x_p + 60, y_child_i + 12)`.

```
📁 orchestrators
  ├── 📁 sap
  │     ├── 📄 6 hours
  │     └── 📄 daily
  ├── 📁 sit
  │     └── 📄 daily
  └── 📁 general
        └── 📄 daily
```

## JSON skeleton (parent + one child + connector)

```json
[
  {
    "type": "image",
    "x": 100, "y": 100, "width": 24, "height": 24,
    "fileId": "<folder-icon>"
  },
  {
    "type": "text",
    "x": 132, "y": 106,
    "text": "orchestrators",
    "fontSize": 16, "fontFamily": 3,
    "strokeColor": "#1e40af"
  },
  {
    "type": "image",
    "x": 160, "y": 148, "width": 24, "height": 24,
    "fileId": "<folder-icon>"
  },
  {
    "type": "text",
    "x": 192, "y": 154,
    "text": "sap",
    "fontSize": 16, "fontFamily": 3,
    "strokeColor": "#1e40af"
  },
  {
    "type": "arrow",
    "x": 112, "y": 128,
    "points": [[0, 0], [0, 32], [48, 32]],
    "strokeColor": "#1e3a5f",
    "strokeWidth": 1.5,
    "roundness": null,
    "elbowed": true,
    "endArrowhead": "arrow"
  }
]
```

## Multi-level

For grandchildren, repeat the same rule: each level adds `60px` to the x-coordinate. Connector from a child to a grandchild drops from the child's bottom and turns into the grandchild's left edge — same geometry, shifted one level.

## See in examples

- `../diagram-types/tech-architecture/architecture_overview.png` — the Repository panel renders `lakehouse-dbt/` as a 3-level folder tree inside its container, with thin elbow tree connectors.

## Notes

- Use `folder_icon.png` (yellow) for directories and a file-type-specific icon (e.g., `yaml`) for leaves.
- Trees do not use the standard Icon Block container — the icon + label is enough. A container would make the tree feel "boxed in" and lose the indent semantic.
- Keep arrows thin (`strokeWidth: 1.5`) for trees; they're structural, not flow. Heavier strokes are reserved for actual data/control flow elsewhere in the diagram.
- For >12 leaves, collapse with a "…" placeholder text node — readability beats completeness.
