# Pattern: Convergence

> Used by types: tech-architecture, star-schema, data-vault

N upstream sources merge into one downstream sink. The mirror of fan-out.

## When to use

Multiple data sources → warehouse, multiple producers → queue, multiple validators → final gate, multiple inputs → join step.

## Geometry

- Sources: N Icon Blocks at `x_s`, stacked vertically with `120px` y-step.
- Sink: one Icon Block at `x_k = x_s + 360`, vertically centered on the source stack: `y_k = y_s_first + (N - 1) * 60`.
- **Shared rail** at `x_rail = x_s + 270`. All sources' arrows route to this rail before turning into the sink.

```
[ S1 ] ──┐
[ S2 ] ──┼──▶ [ Sink ]
[ S3 ] ──┘
```

## Elbow arrow (source i → sink)

Leaves source at `(x_s + 180, y_s_i + 40)`, horizontal to rail, vertical to sink midpoint, horizontal into `(x_k, y_k + 40)`.

```json
{
  "type": "arrow",
  "x": 380, "y": 100,
  "points": [[0, 0], [90, 0], [90, 140], [180, 140]],
  "strokeColor": "#1e3a5f",
  "strokeWidth": 2,
  "roundness": null,
  "elbowed": true,
  "endArrowhead": "arrow"
}
```

## See in examples

- `../diagram-types/data_pipeline_flow.png` — the three parallel Workers converge into the single `Test Gate` sink.

## Notes

- Sink is often End/Success (`#a7f3d0` / `#047857`) when it represents a terminal success state. Use Decision yellow if convergence implies a merge/gate.
- For >4 sources, group them under a labeled container ("Sources") and draw a single arrow into the sink; otherwise the rail crowds up.
- If sources represent heterogeneous categories, color each source's stroke with its brand color and keep fills neutral — the strokes encode origin without adding labels.
