# Pattern: Fan-out

> Used by types: tech-architecture

One upstream source dispatches to N downstream consumers. Event bus, scheduler, orchestrator, pub/sub.

## When to use

Event bus → consumers, orchestrator → tasks, API gateway → microservices, scheduler → jobs.

## Geometry

- Source: Icon Block at `(x_s, y_s)`. Its right edge sits at `x_s + 180`.
- Destinations: N Icon Blocks at `x_d = x_s + 360`, stacked vertically with `120px` y-step.
- Vertically center the source against the stack: `y_s = y_d_first + (N - 1) * 60`.
- **Shared rail:** all fan-out arrows route through the same vertical x-coordinate at `x_rail = x_s + 270` (halfway between source and destinations). This is what makes the bundle read as one structure.

```
                     ┌──▶ [ D1 ]   y = 100
[ Source ] ──┐      ─┤
              └──▶  ─┤──▶ [ D2 ]   y = 220
                     └──▶ [ D3 ]   y = 340
```

## Elbow arrow (source → destination i)

Leaves source at `(x_s + 180, y_s + 40)` (right midpoint), horizontal to rail, vertical to destination midpoint, horizontal into `(x_d, y_d_i + 40)`.

```json
{
  "type": "arrow",
  "x": 380, "y": 240,
  "points": [[0, 0], [90, 0], [90, -140], [180, -140]],
  "strokeColor": "#1e3a5f",
  "strokeWidth": 2,
  "roundness": null,
  "elbowed": true,
  "endArrowhead": "arrow"
}
```

The `[90, ±delta]` segment is the destination-specific offset; everything else is shared.

## See in examples

- `../examples/data_pipeline_flow.png` — `Build` fans out into `Worker 1/2/3` with color-coded strokes, then the workers converge into `Test Gate`.

## Notes

- Source is typically Start/Trigger (`#fed7aa` / `#c2410c`); destinations Primary/Neutral.
- For more than ~5 destinations, group them under a labeled container ("Consumers") and draw a single arrow from source to the container; otherwise the arrow bundle dominates the diagram.
- Do not let arrow paths cross destination nodes — increase `x_rail` if necessary.
- **Color-encoded fan-out:** when multiple fan-outs share the same canvas region and arrows would cross, color each fan-out's strokes by origin (one origin = one stroke color). Pick perceptually distinct colors from the palette (e.g., Start `#c2410c` + GitLab `#f97316`). The destinations stay neutral; the *strokes* carry the routing identity.
