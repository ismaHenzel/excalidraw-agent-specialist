# Pattern: Lifeline + Activation Bar

> Used by types: sequence

Shared primitive for lifeline + activation-bar geometry used in UML sequence diagrams:
participant head boxes, dashed vertical lifelines, activation-bar rectangles centered on
the lifeline x, message Y pitch, and participant x pitch. Authors of `sequence.md`
`@`-reference this file for geometry and JSON skeletons rather than re-deriving them.

The message-encoding conventions (Association=`arrow`+solid for calls;
Dependency=`arrow`+dashed for returns) are locked in
`@../diagram-types/notation-conventions.md` (DTKB-04). The participant head box header
height (40px) matches the compartmented-box header height locked in
`@../diagram-types/compartmented-box.md` (INT-02). Do NOT re-derive either here.

## When to use

Use this primitive for every element in a sequence diagram that relates to participant
positioning, lifeline placement, activation-bar sizing, or message Y ordering.

## Legal arrowhead tokens

Excalidraw 0.17.3 exposes **exactly five** arrowhead values. Any other token renders
**silently as a bare line** — no error, no warning (Pitfall 1 in RESEARCH.md):

    arrow | bar | dot | triangle | null

Tokens that are ILLEGAL and must NEVER appear in authored JSON:

    crowsfoot  diamond  hollow  open  (and any other invented name)

The Phase-1 validator (`excalidraw_validator.py`) rejects any `startArrowhead` or
`endArrowhead` outside the legal set, exiting with code 1. Do not attempt to use
illegal tokens as workarounds — use the message-encoding conventions in
`@../diagram-types/notation-conventions.md` instead.

Sequence diagrams use:
- `endArrowhead: "arrow"` + `strokeStyle: "solid"` — synchronous call/message (Association)
- `endArrowhead: "arrow"` + `strokeStyle: "dashed"` — return/response (Dependency)

Both are legal tokens.

## Geometry

All values below are [ASSUMED] — first-pass design numbers from the project's 20-grid
convention and compartmented-box precedent (RESEARCH.md A1). The authoring agent confirms
or adjusts through the render loop.

### Participant head box

- **Width:** 120px  **Height:** 40px (matches `@../diagram-types/compartmented-box.md` header height)
- `roughness: 0`, `roundness: null`, `strokeStyle: "solid"`
- One `groupIds` id per participant — the head box, lifeline, and all activation bars for
  that participant share the same group id

### Lifeline

- A `line` element (NOT an `arrow` — lifelines carry no arrowhead and must not be bound
  targets for message arrows)
- `strokeStyle: "dashed"`, `roughness: 0`, `roundness: null`
- **Position:** `x = participant_head.x + participant_head.width / 2` — this x IS
  `lifeline_center_x` because the line element's width is 0 (its x is simultaneously its
  left edge and its center)
- **Points:** `[[0,0],[0,lifeline_height]]` — vertical segment only
- Starts at `y = participant_head.y + participant_head.height` (bottom of head box)

### Activation bar

- A `rectangle` element, **width: 12px**, height = span of the activation (from y of first
  message touching this activation to y of last message, plus margin)
- **CRITICAL centering formula:** `x = lifeline_center_x - 6`
  (i.e. `x = lifeline_center_x - ACTIVATION_BAR_WIDTH / 2`)
- `y` = y of first message touching this activation
- `roughness: 0`, `roundness: null`, `backgroundColor: "#ffffff"`, `strokeStyle: "solid"`
- This is the **BINDABLE shape** for message arrows — bind `startBinding`/`endBinding` to
  the activation bar rectangle id, NEVER to the lifeline `line` element

### Message Y pitch

- Minimum **40px** between consecutive message Y values
- Message Y values MUST be monotonically non-decreasing (top = first message, bottom = last)
- Write message arrows in temporal order from top to bottom — never group by participant
  first (that produces out-of-order Y values)

### Participant x pitch

- **180px** between adjacent participant `lifeline_center_x` values
- This leaves a ~60px corridor on each side of the 120px participant head for message routing

## JSON skeleton

### Participant head rectangle

```jsonc
// Source: derived from compartmented-box.md header (40px), 20-grid convention
// Participant head: a plain rectangle (no compartment dividers needed)
{ "type": "rectangle", "x": 200, "y": 60, "width": 120, "height": 40,
  "roughness": 0, "roundness": null, "strokeStyle": "solid",
  "backgroundColor": "#e0f2fe", "strokeColor": "#1e1e1e",
  "groupIds": ["participant_user"],
  "id": "ptcpt_user_head" }
{ "type": "text", "text": "User", "fontFamily": 3, "fontSize": 16,
  "strokeColor": "#1e1e1e", "x": 220, "y": 70, "width": 80, "height": 20,
  "groupIds": ["participant_user"] }
```

### Lifeline line

```jsonc
// Source: PITFALLS.md Pitfall 4, RESEARCH.md
// Lifeline: dashed vertical line from bottom of participant head to bottom of diagram
// lifeline_center_x = participant_head.x + participant_head.width / 2 = 200 + 60 = 260
// line.x == lifeline_center_x because width is 0
{ "type": "line", "x": 260, "y": 100, "width": 0, "height": 400,
  "points": [[0, 0], [0, 400]],
  "roughness": 0, "strokeStyle": "dashed", "strokeColor": "#1e1e1e",
  "roundness": null,
  "groupIds": ["participant_user"] }
```

### Activation bar rectangle

```jsonc
// Source: PITFALLS.md Pitfall 4
// Activation bar centered on lifeline: x = lifeline_center_x - ACTIVATION_BAR_WIDTH / 2
// ACTIVATION_BAR_WIDTH = 12px; lifeline_center_x = 260; activation_bar_x = 260 - 6 = 254
{ "type": "rectangle", "x": 254, "y": 140, "width": 12, "height": 80,
  "roughness": 0, "roundness": null, "strokeStyle": "solid",
  "backgroundColor": "#ffffff", "strokeColor": "#1e1e1e",
  "groupIds": ["participant_user_activation_1"],
  "id": "activation_user_1" }
```

### Solid message arrow (synchronous call)

```jsonc
// Source: notation-conventions.md — Association row (arrow + solid)
// Message arrow binds to activation bar rectangles (NOT to the lifeline line element)
{ "type": "arrow", "elbowed": true, "roundness": null, "roughness": 0,
  "endArrowhead": "arrow", "startArrowhead": null, "strokeStyle": "solid",
  "strokeColor": "#1e1e1e",
  "startBinding": { "elementId": "activation_user_1", "gap": 4 },
  "endBinding": { "elementId": "activation_server_1", "gap": 4 },
  "x": 266, "y": 160, "points": [[0, 0], [130, 0]],
  "groupIds": [] }
{ "type": "text", "text": "login(username, pwd)", "fontFamily": 3, "fontSize": 16,
  "strokeColor": "#1e1e1e", "x": 280, "y": 145, "width": 200, "height": 20 }
```

### Dashed return arrow (response)

```jsonc
// Source: notation-conventions.md — Dependency row (arrow + dashed)
{ "type": "arrow", "elbowed": true, "roundness": null, "roughness": 0,
  "endArrowhead": "arrow", "startArrowhead": null, "strokeStyle": "dashed",
  "strokeColor": "#1e1e1e",
  "startBinding": { "elementId": "activation_server_1", "gap": 4 },
  "endBinding": { "elementId": "activation_user_1", "gap": 4 },
  "x": 396, "y": 200, "points": [[0, 0], [-130, 0]],
  "groupIds": [] }
{ "type": "text", "text": "token", "fontFamily": 3, "fontSize": 16,
  "strokeColor": "#1e1e1e", "x": 320, "y": 185, "width": 60, "height": 20 }
```

## See in examples

- `../examples/sequence_login_flow.png` — canonical UML sequence diagram example: a
  login/authentication flow with participants `User`, `AuthService`, and `UserDB`; 4
  ordered messages including two dashed returns (`userRecord`, `token`). Passes the full
  validate→render→verify loop; EX-03 visual gate cleared 2026-06-08.

## Notes

- **Message arrows MUST bind to the activation-bar `rectangle` (or participant-head
  `rectangle`), NEVER to the lifeline `line` element.** The structural verifier's
  `check_arrow_endpoint_unanchored` function accepts only `rectangle`, `ellipse`, and
  `diamond` borders as valid anchor targets (8px tolerance). A lifeline `line` element is
  NOT in that set — binding to a lifeline line will raise `arrow_endpoint_unanchored`
  error in every structural pass.

- **`lifeline_center_x = line.x`** — the lifeline `line` element's x is its LEFT edge;
  because `width == 0`, the left edge IS the center. Do not add `width / 2` to a lifeline
  line's x to get the center (it is already the center). The activation bar centering
  formula is therefore `activation_bar.x = line.x - ACTIVATION_BAR_WIDTH / 2`
  (i.e. `line.x - 6` for the standard 12px bar).

- **Self-message route** — a participant messaging itself requires a 3-point elbow: from
  the activation bar's RIGHT edge, go `+40px` right (horizontal arm), then `+40px` down
  (vertical drop), then back to the same bar's right edge at a lower y (horizontal return
  arm). Never use two collinear points at the same x — that produces a zero-width
  invisible route.

- **Do NOT re-derive compartmented-box offsets here.** Header height (40px) is finalized
  in `@../diagram-types/compartmented-box.md` (INT-02). Participant head boxes reuse that
  height without compartment dividers (no rows needed — just the outer rectangle).

- **Do NOT re-derive the convention table.** The binding encoding for message arrows
  (Association=`arrow`+solid; Dependency=`arrow`+dashed) is locked in
  `@../diagram-types/notation-conventions.md` (DTKB-04).
