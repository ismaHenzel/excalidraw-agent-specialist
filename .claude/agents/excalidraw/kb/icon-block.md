# Pattern: Icon Block

> Used by types: tech-architecture

**Atomic unit** for representing a technology or named system component. Every node in higher-level patterns (pipeline, fan-out, etc.) is an Icon Block.

## When to use

Any node that represents a technology, service, or named component.

## Geometry

- Container rectangle: `180 × 80`.
- Icon: `24 × 24`, anchored at `x + 8, y + 8` (top-left inset).
- Label: `text` element starting at `x + 40, y + 28` (right of icon, vertically centered to it).

```
+--------------------------+
| [icon]  Label Text       |
+--------------------------+
  ↑ 8,8     ↑ 40,28
```

## JSON skeleton

```json
[
  {
    "type": "rectangle",
    "x": 200, "y": 200, "width": 180, "height": 80,
    "backgroundColor": "#3b82f6", "strokeColor": "#1e3a5f",
    "roughness": 0, "roundness": { "type": 3 }
  },
  {
    "type": "image",
    "x": 208, "y": 208, "width": 24, "height": 24,
    "fileId": "<icon-file-id>"
  },
  {
    "type": "text",
    "x": 240, "y": 228, "text": "Component Name",
    "fontSize": 20, "fontFamily": 3, "strokeColor": "#1e40af"
  }
]
```

## Variants

- **Brand-colored:** swap `backgroundColor` / `strokeColor` to the brand palette (e.g., Databricks `#fed7aa` / `#c2410c`).
- **Endpoint marker:** Start (`#fed7aa`) for entry points, End/Success (`#a7f3d0`) for terminal nodes.
- **Wide label:** if the label exceeds ~14 monospace chars, widen the container in 20px steps; keep height at 80.

## Notes

- Center text vertically by `y + 28` for `fontSize: 20`. For different font sizes use `y + (height - fontSize) / 2` rounded to a multiple of 4.
- The icon-then-label proximity rule is what makes a node legible at a glance; do not separate them.
