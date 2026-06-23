# Diagram Type: Activity

> Layer: TYPE recipe. Composes primitives from [`../../patterns/`](../../patterns/README.md); does not re-derive their geometry. Indexed in [`README.md`](../README.md).

## Purpose

An **Activity** diagram shows the step-by-step behavioural flow of a process or workflow — the sequence of actions, the decisions that branch the flow, and the optional role-based partitioning (swimlanes) that assigns each action to a responsible party. Use it when the audience needs to understand *what happens and in what order*, as opposed to Tech Architecture's "what are the parts and how do they connect."

Reach for this type when a request is about: a business process walkthrough, an order fulfilment or approval flow, a request lifecycle, an algorithm's control flow, or any scenario where the diagram must answer "then what?" at every step. Activity is the UML-04 type — it composes only existing `kb/` primitives and introduces no new notation.

## How to draw it

Assemble the diagram from the composed primitives below — do not improvise coordinate math here; defer all geometry to the primitive files.

- **Start with a filled ellipse (initial node) and end with a ring ellipse (final node).** The initial node is a solid `ellipse` shape; the final node is an `ellipse` with a visually distinct fill or border. Both are verifier-anchorable shapes.
- **Represent each action as a rectangle with an explicit text label.** Every action node is a standalone `rectangle` with a separate `text` element carrying an explicit `width` and `height` — never a single multi-line text block squeezed into one node. Use `linear-pipeline` for a horizontal chain of sequential actions, and `task-list` for a vertical action stack with side I/O annotations.
- **Use a real `diamond` for decision gates.** The `diamond` shape is a first-class, verifier-anchorable type in the Excalidraw element schema — the `decision-branch` primitive's rotated-rectangle hedge does **not** apply here. Use `diamond` directly. Label each outgoing branch (`Yes`/`No`, condition text) with a `text` element carrying explicit dimensions.
- **Use `decision-marker` for inline binary pass/fail gates.** When a step has a simple ✓/✗ outcome with no branch label, prefer `decision-marker` over a full diamond.
- **Route loop-backs with `feedback-loop`.** Any arc returning to an earlier action must go *around* the forward flow, never crossing it — the `feedback-loop` primitive encodes this orthogonal routing rule.
- **Optional swimlanes are N adjacent `group-container` lanes.** When the diagram partitions actions by role, system, or team, express each partition as a parallel `group-container` lane — one per role, titled top-left, non-overlapping, with clear gutters between lanes. Cross-lane transitions are arrows that cross the shared lane border. Do **not** create a new `swimlane.md` primitive; lanes are just side-by-side group containers.
- **All connectors are sharp elbow arrows.** Every flow arrow uses `elbowed: true`, `roundness: null`, and orthogonal points per the house convention — the geometry lives in the primitive files.
- **Every text carries explicit `width` and `height`.** This is a hard verifier contract: any `text` element missing explicit dimensions will trip the `text_missing_dimensions` error. Set both fields; defer to the primitive files for canonical values.
- **Keep coordinates on the 20-grid** and `roughness: 0`, `fontFamily: 3` (monospace) for all text, exactly as the primitives specify.

## Composes (primitive layer)

- [`@../../patterns/linear-pipeline.md`](../../patterns/linear-pipeline.md) — sequential left-to-right chain of action nodes.
- [`@../../patterns/task-list.md`](../../patterns/task-list.md) — vertical action stack with side I/O annotations.
- [`@../../patterns/decision-branch.md`](../../patterns/decision-branch.md) — labelled decision diamond with two or more outgoing branches.
- [`@../../patterns/decision-marker.md`](../../patterns/decision-marker.md) — inline binary pass/fail gate (✓/✗) without a full diamond.
- [`@../../patterns/feedback-loop.md`](../../patterns/feedback-loop.md) — loop-back arc routed around the forward flow, never crossing it.
- [`@../../patterns/group-container.md`](../../patterns/group-container.md) — swimlane lanes: N adjacent bordered containers, one per role or partition.

## Ground truth

- [`./activity_order_fulfillment.png`](./activity_order_fulfillment.png) — the canonical Activity reference (authored this phase). Imitate its start/end node placement, action-chain composition, decision-diamond labelling, and (optionally) swimlane partitioning.
