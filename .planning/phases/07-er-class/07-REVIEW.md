---
phase: 07-er-class
reviewed: 2026-06-07T00:00:00Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - .claude/agents/excalidraw/diagram-types/class.md
  - .claude/agents/excalidraw/diagram-types/README.md
  - .claude/agents/excalidraw/examples_excalidraw/class_order_domain.excalidraw
  - .claude/agents/excalidraw/kb/relationship-endpoint.md
  - .claude/agents/excalidraw/scripts/render/excalidraw_validator.py
findings:
  critical: 3
  warning: 4
  info: 2
  total: 9
status: issues_found
---

# Phase 07: Code Review Report

**Reviewed:** 2026-06-07
**Depth:** standard
**Files Reviewed:** 5
**Status:** issues_found

## Summary

Five source files from Phase 7 Plan 03 were reviewed: the class diagram recipe (`class.md`), the type-layer resolver (`README.md`), the canonical example source (`class_order_domain.excalidraw`), the shared relationship-endpoint primitive (`relationship-endpoint.md`), and the Python structural validator (`excalidraw_validator.py`).

The recipe documentation and the resolver table are internally consistent and correctly wired. The canonical example passes basic structural checks (legal arrowhead tokens only, no label properties in shapes, correct grouping of diamond glyphs). Arrow bindings target rectangle elements; composition and aggregation diamonds center correctly on their connector start-points.

Three critical issues were found: a systematic off-by-10 divergence between the recipe formula and every attr-divider position in the example (creating a template that contradicts its own documented formula), a missing `isDeleted` filter in the validator that will cause false-positive arrowhead errors on soft-deleted elements, and the validator silently omitting the `arrow_endpoint_unanchored` check that both recipe files explicitly claim it enforces. Four warnings cover additional validator gaps and a semantic modeling problem in the canonical example.

---

## Critical Issues

### CR-01: Attr-divider Y position diverges from recipe formula in all six boxes

**File:** `.claude/agents/excalidraw/examples_excalidraw/class_order_domain.excalidraw` — all six `*-div-attr` line elements

**Issue:** The recipe (`class.md` line 49) states:

> Second divider Y = `box.y + 40 + 20*k` (k = number of attribute rows)

Every box in the example places the attr-divider 10 pixels lower than this formula predicts:

| Box | rect.y | k_attrs | Formula → expected | Actual attr_div.y | Delta |
|-----|--------|---------|-------------------|-------------------|-------|
| pay | 40 | 1 | 100 | 110 | +10 |
| cust | 240 | 3 | 340 | 350 | +10 |
| ord | 240 | 3 | 340 | 350 | +10 |
| ol | 240 | 2 | 320 | 330 | +10 |
| pc | 500 | 1 | 560 | 570 | +10 |
| disc | 500 | 2 | 580 | 590 | +10 |

Reverse-engineering the example reveals the implementation uses an undocumented 8 px top-pad + 2 px bottom-pad per compartment boundary (first row text sits 8 px below its divider), yielding an effective formula of `rect.y + 40 + 10 + 20*k`. The recipe formula is therefore wrong, not the example — but both the recipe (`class.md`) and `compartmented-box.md` (referenced source of truth) specify `box.y + 40 + 20*k`. An agent following the recipe verbatim will place the attr-divider 10 px too high, causing method rows to overlap the divider line visually.

**Fix:** One of these two changes must be made (pick one and keep them consistent):

Option A — Update the recipe formula to match the example:
```
Second divider Y = box.y + 40 + 10 + 20*k
```
and update the locked offset table in `class.md` and `compartmented-box.md` accordingly.

Option B — Correct the example to match the recipe:
Change all six `*-div-attr` elements: set `"y"` to `rect.y + 40 + 20*k` (remove the +10).
For example, `pay-div-attr` changes from `"y":110` to `"y":100`,
`cust-div-attr`/`ord-div-attr` change from `"y":350` to `"y":340`, etc.

---

### CR-02: Validator does not filter `isDeleted` elements — will produce false-positive arrowhead errors

**File:** `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py:28`

**Issue:** The validator iterates `elements = data.get("elements", [])` without filtering out soft-deleted elements (`"isDeleted": true`). Excalidraw preserves deleted elements in the JSON for undo history. If a deleted arrow element has a non-null, non-legal `startArrowhead` or `endArrowhead` value (e.g., a legacy `"diamond"` token from a previous author attempt), the validator reports it as an error even though the element is invisible and inert at render time. This will cause valid diagrams to fail CI validation.

Additionally, deleted shape elements with a `"label"` property (Section 2 check) will likewise generate false-positive errors.

**Fix:**
```python
# Line 28 — filter deleted elements before any check
elements = [el for el in data.get("elements", []) if not el.get("isDeleted", False)]
```

---

### CR-03: Validator claims to enforce `arrow_endpoint_unanchored` and `arrow_not_elbow` but does neither

**File:** `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py` (entire file)

**Issue:** Both `class.md` (lines 116, 125) and `kb/relationship-endpoint.md` (lines 86-87, 212) explicitly state that "the structural verifier raises `arrow_endpoint_unanchored`" and "Non-elbow connectors trigger `arrow_not_elbow` warnings in the structural verifier." These are load-bearing contract statements — authors rely on the validator to catch binding and elbow violations. The validator contains neither check. Searching the full source confirms:

- `arrow_endpoint_unanchored` — absent
- `arrow_not_elbow` — absent
- `elbowed` — absent
- `groupIds` — absent

An arrow with `startBinding: null` (unanchored) or `elbowed: false` (curved) passes validation silently. The docs' promises of these checks are false.

**Fix:** Add the missing checks. Minimum viable additions:

```python
# After section 3 arrowhead checks, add section 4:

# 4. Check for unanchored arrows and non-elbow connectors
unanchored_arrows = []
non_elbow_arrows = []
for el in elements:
    if el.get("type") == "arrow":
        if el.get("startBinding") is None or el.get("endBinding") is None:
            unanchored_arrows.append(el.get("id", "unknown"))
        if not el.get("elbowed", False):
            non_elbow_arrows.append(el.get("id", "unknown"))

if unanchored_arrows:
    for aid in unanchored_arrows:
        errors.append(f"arrow_endpoint_unanchored — arrow '{aid}' has null startBinding or endBinding.")
if non_elbow_arrows:
    for aid in non_elbow_arrows:
        warnings.append(f"arrow_not_elbow — arrow '{aid}' is not elbowed (elbowed: true required).")
```

---

## Warnings

### WR-01: Validator section numbering skips section 4 — indicates a planned check was dropped

**File:** `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py`

**Issue:** The numbered comment blocks run `# 1.`, `# 2.`, `# 3.`, `# 5.`, `# 6.` — section 4 is absent. This implies a groupIds-coherence or binding check was planned but never implemented, consistent with CR-03. The gap makes the code harder to audit and confirms the validator is incomplete relative to its documentation contract.

**Fix:** Either add the missing section 4 (groupIds coherence check, as implied by the gap — see CR-03 fix), or re-number the sections sequentially if the check is intentionally deferred.

---

### WR-02: Validator does not check `groupIds` coherence for compartmented boxes

**File:** `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py`

**Issue:** The recipe (`class.md` line 56) states: "All elements of a box (the rectangle frame, both line dividers, the title text, and every row text) share ONE `groupIds` id." The validator never inspects `groupIds`. An authored box where a row text's `groupIds` is empty — making it a free-floating orphan — passes validation silently. This is the single most common authoring error (the legacy `star_schema.excalidraw` has 0 grouped elements) and the validator provides no protection against it.

**Fix:**
```python
# 4. Check groupIds coherence — every non-connector element should belong to at least one group
from collections import defaultdict
ungrouped_non_arrows = [
    el.get("id", "unknown") for el in elements
    if el.get("type") not in ("arrow",) and not el.get("groupIds")
]
if ungrouped_non_arrows:
    warnings.append(
        f"Elements with empty groupIds (likely orphaned box parts): "
        f"{', '.join(ungrouped_non_arrows)}"
    )
```

---

### WR-03: `«Payable»` interface box contains an instance attribute (`- id: Long`)

**File:** `.claude/agents/excalidraw/examples_excalidraw/class_order_domain.excalidraw:11`

**Issue:** The `«Payable»` box includes `- id: Long` as an attribute in the attributes compartment. UML interfaces do not hold instance attributes (they may hold constants, but these are modeled differently). The canonical example is the ground truth that agents imitate (`class.md` line 147: "Imitate its compartment layout"). An agent following this example may replicate the anti-pattern of placing instance attributes in interfaces. The `«Payable»` interface should have only the `+ pay(): void` method (and optionally a constant `id` marked as `{readOnly}`).

**Fix:** Remove `pay-a1` (`- id: Long`) from the `«Payable»` box, or replace it with a properly modeled constant: `+ MAX_ID: Long = 0 {readOnly}`. Also remove `pay-div-attr` (the attr-compartment divider is unnecessary if there are no attrs) or leave it empty to show the three-compartment structure explicitly.

---

### WR-04: `relationship-endpoint.md` UML aggregation skeleton omits the connector element

**File:** `.claude/agents/excalidraw/kb/relationship-endpoint.md:126-141`

**Issue:** The UML aggregation JSON skeleton block (lines 126-141) is labelled "UML aggregation (white-fill diamond at owner end)" but only shows two code objects: the connector arrow and the diamond glyph. However, the connector JSON in the skeleton block is placed under a comment reading `// Connector anchors to the PART box (not to the diamond)` — which is correct — but the connector JSON itself shows `"endArrowhead":null,"startArrowhead":null` without any visual arrowhead on either end. This is correct for the bare aggregation connector but is not stated explicitly. An author could reasonably wonder whether to add `endArrowhead:"arrow"` for direction. The composition skeleton (lines 144-153) is even more minimal — it shows only the diamond element with a comment "Same connector as aggregation — change only the diamond fill" but does not repeat the connector. This requires the author to scroll back to find the aggregation connector. If the aggregation skeleton is the wrong one to copy (e.g., CR-01 causes confusion), the composition connector is entirely undocumented standalone.

**Fix:** Add explicit connector JSON to the composition skeleton (do not rely on "same as above" cross-reference), and add a one-line comment to both connectors stating `// No arrowhead tokens on either end for agg/comp — visual direction comes from diamond placement`.

---

## Info

### IN-01: `README.md` wired-rows note is a single run-on sentence exceeding 250 words

**File:** `.claude/agents/excalidraw/diagram-types/README.md:30`

**Issue:** The entire wired-status history is crammed into one sentence in the block-quote below the resolver table. As phases accumulate this will become unreadable. The sentence already concatenates six compound clauses.

**Fix:** Convert to a bullet list:
```markdown
> **Wired types:**
> - **tech-architecture** — wired Phase 4 (smoke-test type)
> - **activity** — wired Phase 5; `activity_order_fulfillment.excalidraw` passes full loop
> - **star-schema** — wired Phase 6; resolver points at `star_schema_v2.png`; legacy de-indexed
> - **snowflake-schema** — wired Phase 6 Plan 02; resolver points at `snowflake_schema.png`
> - **er** — wired Phase 7 Plan 02; EX-03 visual gate approved 2026-06-07
> - **class** — wired Phase 7 Plan 03; EX-03 visual gate approved 2026-06-07
```

---

### IN-02: Validator prints Unicode checkmark `✓` which may not render in all terminal/CI environments

**File:** `.claude/agents/excalidraw/scripts/render/excalidraw_validator.py:76`

**Issue:** The success message uses `[✓]`. On some CI log viewers and non-UTF-8 terminals this renders as a question mark or box character, making the "all OK" output look like a failure indicator.

**Fix:** Replace with ASCII:
```python
print("  [OK] Metadata and core structure valid.")
```

---

_Reviewed: 2026-06-07_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
