# Pattern: Decision Marker (Inline ✗ / ✓)

> Used by types: activity

An **inline binary outcome** rendered as a red ✗ circle and a green ✓ circle directly on the flow, instead of a diamond. Use when the decision is binary, the failure consequence matters more than the condition wording, and the diagram needs visual punch over precision.

## When to use

CI/CD gates (pass/fail). Validation results. Health checks. Anywhere "did it work or not?" is the question.

## Compare to `decision-branch.md`

| `decision-branch.md` (diamond) | `decision-marker.md` (inline circles) |
|---|---|
| Wordy condition matters | Pass/fail is the whole story |
| 2+ outcomes, each labeled | Exactly 2 outcomes, semantic-only |
| Diamond owns the decision | Outcomes own the decision |
| Use in process flows | Use in gates, validation, CI |

## Geometry

- Two circles (ellipses) `40 × 40`, side by side with `40px` gap, vertically centered below the gating component.
- Red ✗ circle: fill `#dc2626`, stroke `#dc2626`, contains a white "✗" character text element (`fontSize: 24`, color `#ffffff`).
- Green ✓ circle: fill `#10b981`, stroke `#047857`, contains a white "✓" character.
- The arrow from the gating component **forks** into both markers — one arrow into each circle.
- From each marker, the consequent path continues: ✗ typically loops back upstream (`feedback-loop.md`), ✓ continues to the next stage.

```
       [ Validation ]
          │
       ┌──┴──┐
       ▼     ▼
      (✗)   (✓)
       │     │
   restart   deploy
```

## JSON skeleton

```json
[
  {
    "type": "ellipse",
    "x": 400, "y": 300, "width": 40, "height": 40,
    "backgroundColor": "#dc2626",
    "strokeColor": "#dc2626",
    "roughness": 0
  },
  {
    "type": "text",
    "x": 412, "y": 308,
    "text": "✗",
    "fontSize": 24, "fontFamily": 3,
    "strokeColor": "#ffffff"
  },
  {
    "type": "ellipse",
    "x": 480, "y": 300, "width": 40, "height": 40,
    "backgroundColor": "#10b981",
    "strokeColor": "#047857",
    "roughness": 0
  },
  {
    "type": "text",
    "x": 492, "y": 308,
    "text": "✓",
    "fontSize": 24, "fontFamily": 3,
    "strokeColor": "#ffffff"
  }
]
```

## See in examples

- `examples/data_pipeline_flow.png` — the canonical use. `Test Gate` forks into ✗ / ✓; ✗ feeds the `retry from Commit` feedback loop; ✓ continues into `Deploy`.
- `examples/process_decision.png` — the Integration Suite gates into ✗ / ✓ via a small junction; ✗ restarts the runbook, ✓ proceeds to Package.

## Notes

- The `✗` and `✓` glyphs must be Unicode (U+2717, U+2713). Excalidraw renders them in monospace fine.
- Skip text labels on the circles themselves — the glyph is the label. Put any wording on the downstream arrow.
- Do not use this pattern for >2 outcomes. Use `decision-branch.md` diamond there.
