# Pattern: Feedback Loop

> Used by types: activity

An arrow that exits a flow midway and **returns to an earlier point**, typically labeled with the trigger condition (Retry, Restart, Reset). The visual rule: the loop must route *around* the main flow, never cross it.

## When to use

Retry on failure, restart-development on validation reject, escalate-back-to-design, any branch that sends control back upstream.

## Geometry

Three legs of elbow arrow:
1. **Exit leg** — vertical or horizontal segment from the failure point, moving *away from* the main flow (typically downward or leftward).
2. **Return leg** — long parallel segment that runs *outside* the main flow's bounding box. Stay at least 80px clear of any existing element.
3. **Re-entry leg** — short segment turning back into the upstream node's left or top edge.

The return leg should be at the same axis-distance from the main flow as the longest container border so the routing reads as deliberate, not improvised.

```
   ┌─────────────────────────────────────┐
   │   [ Start ] ──▶ [ Pipeline ] ──▶ ✗  │
   │      ▲                          │   │
   │      │      Restart             │   │
   │      └──────────────────────────┘   │
   └─────────────────────────────────────┘
```

## Label placement

Mid-arrow text on the longest (return) leg, **above** the segment, in Body/Detail color `#64748b`, `fontSize: 14`, `fontFamily: 3`. The label should answer *"when does this fire?"* in 2–4 words.

## JSON skeleton

```json
[
  {
    "type": "arrow",
    "x": 720, "y": 260,
    "points": [
      [0, 0],
      [0, 160],
      [-600, 160],
      [-600, -40],
      [-580, -40]
    ],
    "strokeColor": "#1e3a5f",
    "strokeWidth": 2,
    "roundness": null,
    "elbowed": true,
    "endArrowhead": "arrow"
  },
  {
    "type": "text",
    "x": 280, "y": 396,
    "text": "Restart Development",
    "fontSize": 14, "fontFamily": 3,
    "strokeColor": "#64748b"
  }
]
```

## See in examples

- `examples/data_pipeline_flow.png` — `on fail → retry from Commit` loops from the ✗ marker around the bottom, outside the forward flow, back into `Commit`.
- `examples/process_decision.png` — `Restart on fail` loops from the ✗ gate outside the container back to the `Lint` task.

## Notes

- Stroke color stays neutral (`#1e3a5f`) — the *label* carries the semantic, not the color.
- If your diagram has 2+ feedback loops, route them at different "radius distances" outside the main flow so they don't overlap. Inner loop = tighter; outer loop = farther out.
- A feedback loop combined with an inline decision marker (`decision-marker.md`) is the canonical "validation gate with retry" composition.
