# Pattern: Decision Branch

> Used by types: activity

Diamond-style gate with two (or more) labeled outcomes.

## When to use

Conditional routing, validation gates, A/B selection, error vs. success branching, retry vs. fail.

## Geometry

- Decision diamond: `160 × 100`, fill `#fef3c7`, stroke `#b45309` (Decision palette).
- Outcomes: two Icon Blocks at `x_d + 260`, one above and one below the diamond centerline at `y_offset = ±80` from the diamond's vertical center.
- Arrow labels: small text ("Yes"/"No" or condition string) placed at the midpoint of each arrow.

```
                  ┌──▶ [ Yes path ]
[ Decision ◇ ] ──┤
                  └──▶ [ No path ]
```

## JSON skeleton (diamond)

```json
{
  "type": "diamond",
  "x": 400, "y": 240, "width": 160, "height": 100,
  "backgroundColor": "#fef3c7",
  "strokeColor": "#b45309",
  "roughness": 0,
  "roundness": { "type": 3 }
}
```

If `diamond` is not in the target Excalidraw schema, substitute a `rectangle` with `angle: 0.785398` (45° in radians).

## Elbow arrow with label

The arrow leaves the diamond's right vertex at `(x_d + 160, y_d + 50)`, routes right, turns up or down, then enters the outcome's left midpoint.

```json
{
  "type": "arrow",
  "x": 560, "y": 290,
  "points": [[0, 0], [60, 0], [60, -50], [120, -50]],
  "strokeColor": "#1e3a5f",
  "strokeWidth": 2,
  "roundness": null,
  "elbowed": true,
  "endArrowhead": "arrow"
}
```

Label, placed near the horizontal leg:
```json
{
  "type": "text",
  "x": 580, "y": 270,
  "text": "Yes",
  "fontSize": 14, "fontFamily": 3,
  "strokeColor": "#64748b"
}
```

## See in examples

- For inline binary pass/fail gates (CI/CD style), prefer `decision-marker.md` and see `../diagram-types/tech-architecture/data_pipeline_flow.png` — the diamond is *not* the right tool there. Reserve this pattern for ≥2 *labeled* condition branches, as in `../diagram-types/tech-architecture/process_decision.png` (the `Rollout mode?` diamond with `score >= 0.9` / `canary ok` / `score < 0.7`).

## Notes

- For >2 outcomes (switch/case), stack outcome blocks evenly with shared rail at `x_d + 220` (same approach as fan-out).
- Color the "happy path" outcome with End/Success and the failure path with Warning/Reset (`#fee2e2` / `#dc2626`) to make the read direction obvious.
