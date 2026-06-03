# Pattern: Evidence Card

A small card carrying **real data** — a cost, a metric, a real output sample. Turns "Diagrams ARGUE not DISPLAY" from a slogan into an artifact: the viewer sees actual numbers, not a label that *claims* numbers exist.

## When to use

Architectural diagrams about cost, throughput, scale, latency, or any decision that hinges on quantitative evidence. Also: pipeline diagrams where showing real output rows beats describing the schema.

## Geometry

- Card: `200 × 80` rounded rectangle.
- Two visual variants:

### A. Dark-header card (cost / metric)

- Top strip (`200 × 24`) in dark fill `#1e3a5f`, white text title.
- Body (`200 × 56`) in light fill `#f8fafc`, dark text for the data.
- Title on top strip: `fontSize: 12`, `fontFamily: 3`, color `#ffffff`.
- Headline number/value in body: `fontSize: 20`, color `#1e40af`.
- Sub-label or unit below the number: `fontSize: 12`, color `#64748b`.

```
┌──────────────────────────┐
│ DLT Core Classic         │
├──────────────────────────┤
│ Jun 25, 2025             │
│ $0.41                    │
└──────────────────────────┘
```

### B. Output-sample card (real data row)

- Single light card `200 × 60`, no header strip.
- Heading: pattern name (e.g., `Materialized view`), `fontSize: 12`, color `#64748b`.
- Body: row of `key: value` pairs from a real run (e.g., `dim_customers · Output records: 1996`).

## JSON skeleton (dark-header variant)

```json
[
  {
    "type": "rectangle",
    "x": 100, "y": 60, "width": 200, "height": 24,
    "backgroundColor": "#1e3a5f",
    "strokeColor": "#1e3a5f",
    "roughness": 0,
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "x": 112, "y": 66,
    "text": "DLT Core Classic Compute Price",
    "fontSize": 12, "fontFamily": 3,
    "strokeColor": "#ffffff"
  },
  {
    "type": "rectangle",
    "x": 100, "y": 84, "width": 200, "height": 56,
    "backgroundColor": "#f8fafc",
    "strokeColor": "#1e3a5f",
    "roughness": 0
  },
  {
    "type": "text",
    "x": 112, "y": 96,
    "text": "Jun 25, 2025",
    "fontSize": 12, "fontFamily": 3,
    "strokeColor": "#64748b"
  },
  {
    "type": "text",
    "x": 112, "y": 116,
    "text": "$0.41",
    "fontSize": 20, "fontFamily": 3,
    "strokeColor": "#1e40af"
  }
]
```

## See in examples

- `examples/architecture_overview.png` — evidence strip on top: four dark-header cards with real numbers (monthly compute $4,182.55, 1,996,344 gold rows, 3m 12s p95 latency, 99.7% data-quality pass rate).

## Notes

- Pull numbers from actual runs/queries — do not invent. The whole point is *unfakeable evidence*.
- Limit one card to one number + one supporting label. If you have three numbers, use three cards.
- Place cards as a row above an architectural diagram (the "evidence strip"), or inline next to the component they describe.
- Currency, dates, and units must be explicit. `$0.41/hr` is informative; `0.41` is noise.
