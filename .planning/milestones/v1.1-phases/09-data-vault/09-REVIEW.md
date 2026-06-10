---
phase: 09-data-vault
reviewed: 2026-06-09T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - .claude/agents/excalidraw/diagram-types/data-vault.md
  - .claude/agents/excalidraw/diagram-types/README.md
  - .claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw
  - .claude/agents/excalidraw/kb/convergence.md
  - .claude/agents/excalidraw/kb/fan-out.md
  - .claude/agents/excalidraw/kb/group-container.md
  - .claude/agents/excalidraw/kb/tree-hierarchy.md
findings:
  critical: 4
  warning: 5
  info: 2
  total: 11
status: issues_found
---

# Phase 09: Code Review Report

**Reviewed:** 2026-06-09T00:00:00Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

Seven files were reviewed: the `data-vault.md` TYPE recipe, the `diagram-types/README.md` resolver table, the canonical `data_vault_sales.excalidraw` example, and four `kb/` primitives it composes. The KB primitive files (`convergence.md`, `fan-out.md`, `group-container.md`, `tree-hierarchy.md`) are clean — no defects found. The `data-vault.md` recipe itself is internally consistent and well-specified. All defects are concentrated in the canonical example file (`data_vault_sales.excalidraw`) and one documentation gap in the `README.md` resolver table.

The most serious issues are: (1) three arrow `points` arrays that produce straight lines rather than true elbow paths, violating the mandatory ≥3-orthogonal-point rule and causing the `elbowed: true` flag to be functionally meaningless; (2) the satellite role label rendered at `fontSize: 10` instead of the mandated `fontSize: 14`; (3) all six hash-key column names drop their mandatory table-class prefix (`HUB_`, `LINK_`) in violation of the naming convention in the recipe. A structural documentation gap in the resolver table is also recorded.

---

## Critical Issues

### CR-01: Satellite role-label `fontSize` is 10, not the mandated 14

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:953`
**Issue:** `sat_customer_role` carries `"fontSize": 10`. The `data-vault.md` SC-2 section mandates `"fontSize": 14` for every role-label text (`«hub»`, `«link»`, `«sat»`). The hub and link role labels in this same file both correctly use `fontSize: 14`. The satellite label being half-sized breaks visual parity, undermines the SC-2 grayscale-safety requirement (the label IS the SC-2 carrier), and contradicts the spec explicitly.

**Fix:**
```json
{
  "id": "sat_customer_role",
  "fontSize": 14,
  "height": 20
}
```
Change `"fontSize": 10` to `"fontSize": 14` and correct `"height"` from `14` to `20` to match the hub/link role-label geometry.

---

### CR-02: `arr_prod_link` points are collinear — no actual elbow

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:1265`
**Issue:** `arr_prod_link` has `"points": [[0,0],[0,60],[0,120]]`. All three points share x=0, making this a straight vertical line. The recipe mandates `elbowed: true` with ≥3 **orthogonal** points (i.e., points that form actual right-angle turns). Three collinear points produce a degenerate path: no horizontal segment, no elbow, despite `"elbowed": true`. The fan-out/convergence KB patterns both show that a hub-to-link spine connector must include a horizontal travel segment to the shared rail before turning toward the target. This connector arrives at `link_order_box` (x=400–660) from directly above — which only works by accident of shared x-center — but fails the structural requirement and will mis-render if either box moves.

**Fix:** Replace with a proper elbow that travels to a shared rail. Given `hub_product_box` right edge at x=660 and `link_order_box` top at y=320:
```json
"points": [[0, 0], [80, 0], [80, 120], [0, 120]]
```
Adjust the arrow's `x`/`y` origin and binding to exit the hub's right or bottom edge, travel to the rail, then turn into the link's top edge.

---

### CR-03: `arr_cust_sat` points are collinear — no actual elbow

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:1299`
**Issue:** `arr_cust_sat` has `"points": [[0,0],[0,60],[0,120]]` — same defect as CR-02. The satellite attachment arrow goes straight down with no horizontal segment, rendering `"elbowed": true` meaningless. The `tree-hierarchy.md` skeleton shows satellite connectors dropping from the parent's bottom and turning into the child's left edge with a horizontal segment: `[[0, 0], [0, 32], [48, 32]]`. This file's implementation omits the required horizontal turn.

**Fix:**
```json
"points": [[0, 0], [0, 80], [0, 120]]
```
Replace with a three-point path that includes a horizontal turn, e.g.:
```json
"points": [[0, 0], [0, 100], [-130, 100]]
```
Route from `hub_customer_box` bottom-center downward, then left into `sat_customer_box` right edge (or from the hub's left edge downward to the sat's top edge), ensuring the path makes at least one right-angle turn.

---

### CR-04: Hash-key column names drop mandatory table-class prefix in all six boxes

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:166,439,713,748,783,1021`
**Issue:** The `data-vault.md` recipe specifies the following canonical column names:
- Hub: `HUB_<BIZ>_HK PK` (e.g., `HUB_CUSTOMER_HK PK`)
- Link: `LINK_<REL>_HK PK` + foreign keys `HUB_*_HK`
- Satellite: `HUB_*_HK FK` (parent hub hash key)

The example uses abbreviated names throughout:
- `hub_customer_row1`: `"CUSTOMER_HK PK"` — should be `"HUB_CUSTOMER_HK PK"`
- `hub_product_row1`: `"PRODUCT_HK PK"` — should be `"HUB_PRODUCT_HK PK"`
- `link_order_row1`: `"ORDER_HK PK"` — should be `"LINK_ORDER_HK PK"`
- `link_order_row2`: `"CUSTOMER_HK FK"` — should be `"HUB_CUSTOMER_HK FK"`
- `link_order_row3`: `"PRODUCT_HK FK"` — should be `"HUB_PRODUCT_HK FK"`
- `sat_customer_row1`: `"CUSTOMER_HK FK"` — should be `"HUB_CUSTOMER_HK FK"`

This is the canonical example that the specialist and users copy from. Using wrong column names as ground truth teaches incorrect Data Vault naming conventions and contradicts the explicit recipe spec. The `data-vault.md` width-rule example (line 64) even uses `HUB_CUSTOMER_HK PK` as the reference string — the example file disagrees with its own recipe's example.

**Fix:** Update all six `text` / `originalText` fields to include the mandatory prefix. Also re-check `width` values: `HUB_CUSTOMER_HK PK` is 19 chars → `19 * 9.6 ≈ 182` → box width ≥ 200. Current box width 260 remains adequate. `LINK_ORDER_HK PK` is 16 chars → 154px → box width 260 still covers it.

---

## Warnings

### WR-01: `hub_customer_role` and `hub_customer_title` placed at nearly identical y-coordinates, causing render overlap

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:71,108`
**Issue:** `hub_customer_role` is at `y: 70`, `height: 20` (occupies y=70..90). `hub_customer_title` is at `y: 68`, `height: 24` (occupies y=68..92). Both share the same `groupIds` and virtually identical vertical positions — they will render on top of each other. The title (`containerId: "hub_customer_box"`) and the role label (`containerId: null`) serve different functions but their bounding boxes are almost fully overlapping. The same overlap exists for `hub_product_role` (y=70) and `hub_product_title` (y=68). The `link_order_role` (y=330) and `link_order_title` (y=328) have the same 2px offset and same overlap.

**Fix:** Place the role label at the top-left of the header without `containerId` (already correct), and position the title centered in the header vertically. Given box.y=60, header height=40, title midpoint at y=80: set `hub_customer_title.y = 68` is marginally acceptable if the title anchors to the container's center, but the role label must be offset — move it to `y: 62` (top-left corner, inside header with 2px top padding) or above the box at `y: 46`. Confirm the two texts no longer share overlapping pixel rows.

---

### WR-02: `sat_customer_box` content overflows the bottom boundary

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:863,1171`
**Issue:** `sat_customer_box` has `y: 320`, `height: 180`, so its bottom edge is at y=500. `sat_customer_row6` (RECORD_SRC) is at `y: 470`, `height: 20`, so it occupies y=470..490 — still inside. However, `sat_customer_row5` (EMAIL) occupies y=450..470 and row6 y=470..490. The header is at y=320..360 (40px), divider at y=360. Body rows start at y=370. Six rows at 20px pitch: y=370, 390, 410, 430, 450, 470 — last row ends at y=490. Box bottom is y=500. That gives only 10px padding at the bottom, which is tight but technically within bounds. No overflow — this finding is withdrawn. No issue here.

---

### WR-02: Legend box bottom clips the `sw_sat` swatch row

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:1308,1494`
**Issue:** `legend_box` has `y: 560`, `height: 110` — its bottom edge is at y=670. `sw_sat` (and `lbl_sat`) are at `y: 652`, `height: 20` — they occupy y=652..672. The swatch overflows the legend box by 2px (672 > 670). On a 20px grid, this is likely an authoring error: the legend box should be `height: 120` to contain all three swatch rows with consistent padding (legend_title at y=566 leaves 6px top padding; last swatch bottom at y=672 should have ~8px bottom padding → box needs height ≥ 112 on next grid step = 120).

**Fix:**
```json
{ "id": "legend_box", "height": 120 }
```
Change `"height": 110` to `"height": 120`.

---

### WR-03: `arr_prod_link` not listed in `hub_product_box.boundElements`... wait — it is. Withdrawn.

---

### WR-03: `arr_cust_link` elbow points route through unrelated spatial territory

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:1231`
**Issue:** `arr_cust_link` uses `"points": [[0,0],[40,0],[40,270],[80,270]]` starting at `x: 320, y: 130`. This routes: right 40px to x=360 (the rail), then down 270px to y=400, then right 40px to x=400 (link box left edge). The link box left edge is at x=400, y=320..480, so y=400 is within the box body — the arrow terminates mid-body rather than at the box edge. With `endBinding: { "elementId": "link_order_box", "gap": 4 }`, Excalidraw will snap the endpoint to the nearest box edge. The geometric end of the path (320+80=400, 130+270=400) lands at the left edge of `link_order_box` at y=400, which is 80px below the box top (y=320). This is inside the box body zone below the header — the arrow visually pierces the header area. This is not catastrophic but produces a non-standard attachment point that bypasses the header entirely.

**Fix:** Adjust the y-component of the last segment so the arrow arrives at the box center (y=320+160/2=400 is the vertical center of `link_order_box`, so y=400 is actually the box's vertical midpoint — this is acceptable). No change needed if intentional. Flag as informational concern only.

---

### WR-04: `README.md` resolver table omits `compartmented-box` and `notation-conventions` from data-vault's Composes column

**File:** `.claude/agents/excalidraw/diagram-types/README.md:24`
**Issue:** The resolver table's data-vault row lists `"group-container, fan-out, tree-hierarchy, convergence"` as composed kb sub-patterns. However, `data-vault.md` explicitly composes `compartmented-box.md` and `notation-conventions.md` (both documented in the "Composes" section of `data-vault.md`, lines 200–217). The resolver table is described as "the **single authoritative** family → type map" — if it is incomplete, downstream tooling or agents reading only the resolver table to enumerate dependencies will miss two composed primitives. This breaks the "two layers cross-reference each other so they cannot silently drift" invariant stated in the README itself.

**Fix:** Update the data-vault row in the resolver table:
```
| Data Modeling | data-vault | `data-vault.md` | compartmented-box, notation-conventions, group-container, fan-out, tree-hierarchy, convergence | `../examples/data_vault_sales.png` |
```

---

### WR-05: Legend box uses `roundness: null` (sharp corners) contrary to `group-container.md` which specifies `roundness: { "type": 3 }` (rounded)

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:1321`
**Issue:** `data-vault.md` instructs the legend to be "a `@../kb/group-container.md` bordered box." The `group-container.md` JSON skeleton specifies `"roundness": { "type": 3 }` (rounded rectangle). The legend box in the example uses `"roundness": null` (sharp corners). Agents reading `data-vault.md` and `group-container.md` and then comparing to this example will see an inconsistency about how group-container boxes should look. If `roundness: null` is intentional for the legend (to match the box recipe used in data-vault), it should be explicitly noted as a deviation from group-container defaults.

**Fix:** Either change `legend_box.roundness` to `{ "type": 3 }` to match group-container, or add a note in `data-vault.md` clarifying that the in-canvas legend uses sharp corners (`roundness: null`) rather than the group-container default, since `roundness: null` is the universal rule for all data-vault box elements.

---

## Info

### IN-01: `sat_customer_role` positioned 1px below box top edge — minor inconsistency with hub/link role placement

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:929`
**Issue:** `sat_customer_box` has `y: 320`. The role label `sat_customer_role` is at `y: 321` — just 1px inside the top edge. Hub role labels use `box.y + 10` (hub_customer_role: box y=60, role y=70). Link role label uses `box.y + 10` (link_order_role: box y=320, role y=330). The satellite role label using `y: 321` (= `box.y + 1`) breaks the consistent 10px inset pattern used by the other two roles.

**Fix:** Move `sat_customer_role.y` from `321` to `330` (`sat_customer_box.y + 10`) to match hub and link role-label placement.

---

### IN-02: `hub_customer_title` listed in `hub_customer_box.boundElements` as type "text" — redundant with `containerId` binding

**File:** `.claude/agents/excalidraw/examples_excalidraw/data_vault_sales.excalidraw:28-31,138`
**Issue:** `hub_customer_title` has `containerId: "hub_customer_box"`, and `hub_customer_box.boundElements` also contains `{"type": "text", "id": "hub_customer_title"}`. In Excalidraw v2, the `containerId` relationship is the authoritative binding; the `boundElements` back-reference entry is maintained for consistency but the combination is expected. However, `hub_product_title` (line 403) does NOT appear in `hub_product_box.boundElements` (lines 302–305 only list `arr_prod_link`). This asymmetry — one hub box lists its title in `boundElements`, the other does not — is inconsistent. Neither will cause a functional failure (Excalidraw uses `containerId` as the canonical direction), but the inconsistency is a quality defect.

**Fix:** Add `{"type": "text", "id": "hub_product_title"}` to `hub_product_box.boundElements` to match the pattern of `hub_customer_box`.

---

_Reviewed: 2026-06-09T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
