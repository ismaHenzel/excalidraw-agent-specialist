# Diagram Type: Sequence

> Layer: TYPE recipe. Composes primitives from [`../../patterns/`](../../patterns/README.md) and [`../notation-conventions.md`](../notation-conventions.md); does not re-derive their geometry. Indexed in [`README.md`](../README.md).

Sequence **reuses `kb/lifeline-activation.md` VERBATIM** — do not re-derive participant
spacing (180px pitch), activation-bar width (12px), or message Y pitch (40px). All
geometry is pinned there. Participant head boxes reuse the 40px header height from
[`@../compartmented-box.md`](../compartmented-box.md) (INT-02) — no compartment dividers
are needed for participant heads.

## Purpose

A **Sequence Diagram** shows how objects or components interact **over time** by
exchanging messages. The vertical axis is time (top = earlier, bottom = later); each
participant has a vertical **lifeline** with **activation bars** that mark when it is
actively processing.

Use a sequence diagram when the request is about:
- A specific interaction scenario (login, checkout, API call chain, microservice
  request/response)
- Showing which participant calls which, in what order
- Making asynchronous or synchronous call patterns explicit (solid arrows = calls,
  dashed arrows = returns)
- Debugging or documenting a protocol or workflow that has a clear time dimension

## How to draw it

### Step 1 — Place participant head boxes

Per [`@../../patterns/lifeline-activation.md`](../../patterns/lifeline-activation.md):

- Each participant gets a `rectangle` of `width: 120`, `height: 40`
- `roughness: 0`, `roundness: null`, `strokeStyle: "solid"`, mild fill (e.g. `#e0f2fe`)
- Adjacent participants are spaced **180px** apart (center-to-center)
- Each participant has a sibling `text` label with `fontFamily: 3`, `fontSize: 16`
- All elements for a participant share one `groupIds` id

Typical starting positions: Participant 1 head at `x: 60`, Participant 2 at `x: 240`,
Participant 3 at `x: 420` (lifeline_center_x = head.x + 60).

### Step 2 — Draw dashed vertical lifelines

Per [`@../../patterns/lifeline-activation.md`](../../patterns/lifeline-activation.md):

- Each lifeline is a `line` element (NOT an `arrow`)
- `strokeStyle: "dashed"`, `roughness: 0`, `roundness: null`
- `x = participant_head.x + participant_head.width / 2` — this is `lifeline_center_x`
  (line width is 0, so x is simultaneously left edge and center)
- `points: [[0, 0], [0, lifeline_height]]` — vertical segment only
- Starts at `y = participant_head.y + participant_head.height` (bottom of head box)
- Shares the same `groupIds` as its participant

### Step 3 — Draw activation bar rectangles

Per [`@../../patterns/lifeline-activation.md`](../../patterns/lifeline-activation.md):

- Each activation bar is a `rectangle` of `width: 12`
- **Centering formula:** `x = lifeline_center_x - 6`
  (= `lifeline_center_x - ACTIVATION_BAR_WIDTH / 2`)
- `y` = y of the first message touching this activation
- `height` = span from first to last message on this activation, plus margin
- `roughness: 0`, `roundness: null`, `backgroundColor: "#ffffff"`, `strokeStyle: "solid"`
- This rectangle is the **bindable anchor** for message arrows

### Step 4 — Draw message arrows

Per [`@../notation-conventions.md`](../notation-conventions.md) Association + Dependency rows:

- **Synchronous call / message:** solid `arrow`, `endArrowhead: "arrow"`, `strokeStyle: "solid"`
- **Return / response:** dashed `arrow`, `endArrowhead: "arrow"`, `strokeStyle: "dashed"`
- All arrows: `elbowed: true`, `roundness: null`, `roughness: 0`
- Bind `startBinding` and `endBinding` to **activation-bar rectangle ids** (or
  participant-head rectangle ids when no activation bar is present) — **NEVER to `line`
  elements (lifelines)**
- Message Y values MUST be **monotonically non-decreasing**: first message at lowest Y,
  last message at highest Y (write messages top-to-bottom in temporal order)
- Minimum **40px** between consecutive message Y values

### Step 5 — Add message text labels

- One `text` element per message, placed just above the arrow
- `fontFamily: 3` (Cascadia monospace), `fontSize: 16`, `strokeColor: "#1e1e1e"`
- No `containerId` — labels are free-floating siblings of their arrow

### Binding rules (LOCKED)

- `endArrowhead: "arrow"` on all message arrows. Returns additionally use
  `strokeStyle: "dashed"`. No `crowsfoot`/`diamond`/`hollow`/`open` tokens —
  illegal tokens render silently as bare lines.
- Every arrow `startBinding`/`endBinding` must target an **activation-bar `rectangle`**
  (or participant-head `rectangle`). The structural verifier's
  `check_arrow_endpoint_unanchored` accepts only `rectangle`, `ellipse`, and `diamond`
  borders (8px tolerance). Lifeline `line` elements are **NOT** accepted — binding to
  a lifeline line will raise `arrow_endpoint_unanchored` on every structural pass.
- All arrows: `elbowed: true`, `roundness: null`, `roughness: 0`.
- The `check_sequence_activation_center_x` structural check (added Phase 8 Plan 01)
  asserts that each activation bar's center x equals the nearest lifeline line's x
  (tolerance 1px). Ensure `bar.x + bar.width/2 == lifeline_center_x` exactly.

## Composes (primitive layer)

- [`@../../patterns/lifeline-activation.md`](../../patterns/lifeline-activation.md) — all geometry:
  participant head sizing (120×40), lifeline placement, activation-bar centering
  formula (`x = lifeline_center_x − 6`), message Y pitch (min 40px), participant
  x pitch (180px), JSON skeletons for all element types.
- [`@../notation-conventions.md`](../notation-conventions.md) — legal arrowhead token
  set; Association row (call = `arrow`+solid); Dependency row (return = `arrow`+dashed);
  Actor convention (labelled-box — not used in sequence but locked here for consistency).
- [`@../compartmented-box.md`](../compartmented-box.md) — participant head box header
  height (40px) reused verbatim; no compartment dividers needed for participant heads
  (they are plain rectangles with a title, not multi-row boxes).

## Ground truth

- [`./sequence_login_flow.png`](./sequence_login_flow.png) — the
  canonical sequence diagram example: a login/authentication flow with participants
  `User`, `AuthService`, and `UserDB`; 4 ordered messages including dashed returns.
  Imitate its participant spacing, activation-bar placement, and message ordering.
