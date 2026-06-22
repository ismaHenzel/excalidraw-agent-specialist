# Diagram Type: Use-Case

> Layer: TYPE recipe. Composes primitives from [`../patterns/`](../patterns/README.md) and shared notation conventions; does not re-derive their geometry. Indexed in [`README.md`](./README.md).

## Purpose

A **Use-Case** diagram shows the functional scope of a system from the perspective of its users (actors): what the system *does*, who initiates each behaviour, and any inclusion/extension relationships between use cases. Use it when the audience needs to understand *who can do what* — stakeholder walkthroughs, requirements validation, system boundary clarification, and sprint-backlog seeding.

Reach for this type when a request is about: system scope for a product or service, actor-to-feature mapping, capturing functional requirements visually, or communicating what is inside vs. outside a system boundary. Use-Case is the UML-03 type — it composes only existing `kb/` primitives and introduces no new notation.

## How to draw it

Assemble the diagram from the composed primitives below — do not improvise coordinate math here; defer all geometry to the primitive files.

- **Actor = labelled box (NOT stick-figure, NOT emoji).** The committed convention per `@./notation-conventions.md` DTKB-04 is: a `rectangle` (100px wide, 60px high), `roughness: 0`, `roundness: null`, `backgroundColor: "transparent"`, plus two sibling `text` elements sharing one `groupId` with the box: `«actor»` stereotype label (`fontFamily: 3`, `fontSize: 14`) and the actor name label (`fontFamily: 3`, `fontSize: 16`). Group all three elements (box + stereotype text + name text) under a single `groupId`. Place actors **outside** the system-boundary rectangle.

- **Use-case oval = native `ellipse`.** Each use case is a native `ellipse` element with `roughness: 0`, `strokeStyle: "solid"`, `backgroundColor: "transparent"`, and **no `roundness` override** (ellipses are inherently round; adding `roundness: null` is wrong — omit the field entirely or leave it at the ellipse default). Pair each oval with a sibling `text` label; group oval + label under a single `groupId`. Place all use-case ovals **inside** the system boundary.

- **System boundary = `@../patterns/group-container.md` rectangle.** The system boundary is a `group-container` rounded rectangle: `roundness: {"type": 3}` (the one place where a rounded rectangle is intentional and correct), `strokeColor: "#1e3a5f"`, `strokeWidth: 2`, `roughness: 0`, `backgroundColor: "transparent"`. Add a `text` element near the top of the boundary for the system name. This is the only rounded rectangle in a use-case diagram.

- **Association (actor to oval) = undirected arrow.** Actor–use-case associations use `arrow` with `endArrowhead: null`, `startArrowhead: null`, `strokeStyle: "solid"`, `elbowed: true`, `roundness: null`, `roughness: 0`. Bind via `startBinding` to the actor `rectangle` id and `endBinding` to the oval `ellipse` id (both with `gap: 4`). This is the plain "line" that connects an actor to a use case.

- **Include/extend = dashed arrow + stereotype text label.** Include and extend relationships use `arrow` with `endArrowhead: "arrow"`, `startArrowhead: null`, `strokeStyle: "dashed"`, `elbowed: true`, `roundness: null`, `roughness: 0` per `@./notation-conventions.md` Dependency row. Add a sibling `text` element (`«include»` or `«extend»`, `fontFamily: 3`, `fontSize: 14`) near the midpoint of the arrow. The arrow runs from the base use-case oval to the included/extended oval (Place Order → Process Payment for `«include»`).

- **All connectors are sharp elbow arrows.** Every arrow uses `elbowed: true`, `roundness: null`. No soft curves.

- **Legal arrowhead tokens only.** The five legal values are `arrow | bar | dot | triangle | null`. Never use `crowsfoot`, `diamond`, `hollow`, `open`, or any invented token — they render silently as plain lines and destroy relationship semantics.

- **All text uses `fontFamily: 3` (Cascadia monospace) and carries explicit `width` and `height`.** Set both fields on every `text` element to avoid verifier `text_overflow_static` errors.

- **Keep coordinates on the 20-grid** and `roughness: 0` for all elements.

## Composes (primitive layer)

- [`@../patterns/group-container.md`](../patterns/group-container.md) — system boundary: a bordered rounded rectangle (`roundness: {"type": 3}`) that scopes all use-case ovals inside it. The one place where a rounded rectangle is correct and intentional in this diagram type.
- [`@./notation-conventions.md`](./notation-conventions.md) — actor=labelled-box convention (DTKB-04; NOT stick-figure, NOT emoji); legal arrowhead tokens (`arrow | bar | dot | triangle | null`); Association encoding (undirected: `endArrowhead: null`, `startArrowhead: null`, solid); Dependency encoding (include/extend: `endArrowhead: "arrow"`, dashed + stereotype text label).

## Ground truth

- [`./use_case_checkout.png`](./use_case_checkout.png) — the canonical Use-Case reference (authored this phase). Imitate its actor placement (labelled boxes outside the boundary), use-case oval layout (inside the boundary), system-boundary group-container, association lines, and the `«include»` dashed arrow from Place Order to Process Payment.
