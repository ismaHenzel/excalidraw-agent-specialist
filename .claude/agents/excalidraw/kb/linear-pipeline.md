# Pattern: Linear Pipeline

> Used by types: tech-architecture, activity, snowflake-schema

Sequential left-to-right flow of N steps connected by single-segment elbow arrows.

## When to use

ETL pipelines, request flows, ordered protocols, build/deploy stages — anything where the read direction is "do A, then B, then C."

## Geometry

- Each node: standard Icon Block (`180 × 80`).
- Horizontal gap between nodes: `80px` ⇒ node `x` step is `260` (180 + 80).
- All nodes share the same `y` (e.g., `y = 240`).
- Arrows are straight horizontal connectors from `(x_n + 180, y_n + 40)` to `(x_{n+1}, y_n + 40)`.

```
[ A ] ──▶ [ B ] ──▶ [ C ] ──▶ [ D ]
 x=200    x=460    x=720    x=980
```

## Arrow between two nodes

```json
{
  "type": "arrow",
  "x": 380, "y": 280,
  "width": 80, "height": 0,
  "points": [[0, 0], [80, 0]],
  "strokeColor": "#1e3a5f",
  "strokeWidth": 2,
  "roundness": null,
  "elbowed": true,
  "endArrowhead": "arrow"
}
```

## Notes

- Mark the first node as **Start/Trigger** (`#fed7aa` / `#c2410c`) and the last as **End/Success** (`#a7f3d0` / `#047857`) to make the read direction unambiguous.
- For >5 steps, wrap into two rows. The wrap connector is an L-shaped elbow with 3 points: right out of the last node on row 1, down by `(row_height + 80)`, then left into the first node of row 2. Reverse direction on row 2 or keep left-to-right and add a return rail — pick one and stay consistent.
- Optional stage labels go *above* each node at `y = node_y - 28` in Body/Detail color (`#64748b`).
