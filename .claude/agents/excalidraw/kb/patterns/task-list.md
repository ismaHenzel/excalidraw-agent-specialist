# Pattern: Task List

> Used by types: activity

A **vertical stack of task nodes inside a container** that represents an ordered procedure (a job, a function body, a runbook). Distinct from a linear pipeline — execution direction is *vertical*, and tasks routinely reach **sideways out of the container** to external resources (databases, APIs).

## When to use

Job orchestration where step order matters and several steps need external I/O. A workflow with side effects. A function decomposed into its operations.

## Geometry

- Outer container: tall rounded rectangle, ~`360 × (60 + N * 60)`. No internal title; the parent container of *this* container supplies the technology context.
- Task nodes: small Icon Block variants — `260 × 40`, stacked vertically with `20px` gap (y-step `60`).
- Each task at `(x_c + 50, y_c + 40 + i * 60)`, leaving 50px left margin for in-coming arrows and 50px right margin for out-going arrows.
- External resource nodes (databases, APIs) live **outside** the container at the same `y` as the task they connect to.

```
┌─────────────────────────────┐
│                             │
│  ──▶ [ Read metadata     ]  │
│  ──▶ [ Read Control Tbl  ]  │
│  ──▶ [ Verify Outdated   ]  │
│      [ Refresh PBIs (async)]──▶ [ PowerBI API ]
│      [ Verify PBI Status ]──▶
│  ──▶ [ Update Control    ]  │
│      [ Send Email        ]  │
│                             │
└─────────────────────────────┘
```

## Side I/O arrows

- **In** (reading a resource): arrow originates from the external resource's right edge and enters the container *through its left border* into the task's left edge. The arrow visually pierces the container — that's intentional; it conveys "this task reads from outside."
- **Out** (writing to a resource): arrow exits the container *through its right border* from the task's right edge into the resource's left edge.

Use straight horizontal segments where possible; only elbow when the resource is at a different y than the task.

## Async badge

For asynchronous tasks, place a small `(async)` text above the task node, in Body/Detail color `#64748b`, `fontSize: 12`, italic style if available.

```json
{
  "type": "text",
  "x": 280, "y": 350,
  "text": "(async)",
  "fontSize": 12, "fontFamily": 3,
  "strokeColor": "#64748b"
}
```

## See in examples

- `examples/process_decision.png` — canonical example. Vertical task stack `Lint → Unit Tests → Integration → Package → Release` inside a GitLab CI container, with side I/O arrows to the `Test API` (left) and `Image Registry` (right).

## Notes

- Order is *visual* — the implicit reading direction is top-to-bottom; do not add a sequence number unless the order is not strictly linear (e.g., some tasks run in parallel).
- A task list is usually wrapped in a Group Container that owns the technology context (Databricks job, Airflow DAG, Lambda function).
- If any single task has more than 2 side resources, promote it to a sub-flow on a separate row of the diagram — task-list nodes should stay simple.
