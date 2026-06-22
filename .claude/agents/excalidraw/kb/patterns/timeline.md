# Pattern: Timeline

Events arranged along a horizontal time axis.

## When to use

Release schedules, incident postmortems, project milestones, lifecycle stages, sequence-with-time-context flows.

## Geometry

- Horizontal axis: thin rectangle (`height: 4`, length = total duration in pixels), fill `#64748b`, at `y = y_axis`.
- Event markers: ellipse `16 × 16`, centered on the axis at `(x_event - 8, y_axis - 6)`.
- Event labels: text above and below the axis, alternating to avoid overlap, at `y_axis - 32` and `y_axis + 16`.
- Optional time gridlines: thin vertical rectangles every N px in `#e2e8f0` behind the axis.

```
   T0       T1       T2       T3
   ●━━━━━━━━●━━━━━━━━●━━━━━━━━●
 Start    Build    Deploy    Done
```

## Axis JSON

```json
{
  "type": "rectangle",
  "x": 100, "y": 300, "width": 800, "height": 4,
  "backgroundColor": "#64748b",
  "strokeColor": "#64748b",
  "roughness": 0
}
```

## Event marker

```json
{
  "type": "ellipse",
  "x": 200, "y": 294, "width": 16, "height": 16,
  "backgroundColor": "#3b82f6",
  "strokeColor": "#1e3a5f",
  "roughness": 0
}
```

## Event label (alternating)

```json
{
  "type": "text",
  "x": 180, "y": 268,
  "text": "Build",
  "fontSize": 14, "fontFamily": 3,
  "strokeColor": "#1e40af"
}
```

## Notes

- Stick to 4–8 events per axis. For more, switch to a swim-lane or Gantt-style layout.
- Use End/Success green for the terminal event marker (`backgroundColor: "#a7f3d0"`, `strokeColor: "#047857"`).
- For incident timelines, color the marker by severity: Error (`#fecaca` / `#b91c1c`) for the failure point, Warning (`#fee2e2` / `#dc2626`) for escalations, Success for recovery.
- Keep label spacing ≥ 80px horizontal to avoid collisions; if events are denser, tilt labels to vertical or use leader lines.
