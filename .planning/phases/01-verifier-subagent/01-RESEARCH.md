# Phase 1: Verifier Subagent - Research

**Researched:** 2026-05-21
**Domain:** Claude Code subagent authoring + Excalidraw JSON structural inspection + multimodal PNG verification
**Confidence:** HIGH on subagent format & repo patterns; MEDIUM on Excalidraw arrow/text math (verified against deepwiki source-of-truth, but render-pipeline uses CDN bundle so empirical confirmation requires running the render); HIGH on emoji codepoint detection.

## Summary

This phase ships a standalone `excalidraw_verifier` subagent and a deterministic `scripts/verifier_structural.py` helper. The work is **narrow and well-bounded**: every interface contract is locked in CONTEXT.md (D-01…D-16), the YAML frontmatter format mirrors `excalidraw_specialist.md` line-for-line, and the codebase already provides the canonical patterns for JSON loading, error/warning vocabulary, and helper-script structure. There are no novel architectural decisions; this is execution against a fully-specified contract.

The only research questions worth investigation are: (1) the exact `tools:` syntax for a Claude Code subagent (resolved — comma-separated single line, identical to specialist), (2) the math for arrow-endpoint-on-border and text-width-fits-container (resolved — local→global coord conversion plus shape-specific border hit test with 8 px tolerance; monospace ratio empirically ~0.6 × fontSize for Cascadia at fontFamily 3), (3) emoji regex coverage (resolved — three Unicode ranges, well-documented Python pattern), and (4) how to make a subagent reliably emit a fenced ```json block last (resolved — explicit imperative + the file-as-canonical-source contract makes message-parsing a backup, not the critical path).

**Primary recommendation:** Build `scripts/verifier_structural.py` first as a pure-Python deterministic helper (host-side testable). Then write `excalidraw_verifier.md` as a thin orchestrator subagent whose body is mostly a fenced operational playbook (the seven numbered steps in §Subagent Body Architecture below) plus a hard-coded output schema. Fixtures are dirt-cheap: three tiny `.excalidraw` files crafted by hand, each ≤ 12 elements, rendered via the existing `validate_and_render.sh` pipeline. Self-test is a single bash one-liner per fixture using `jq` (already installed).

## User Constraints (from CONTEXT.md)

### Locked Decisions

**Report Transport & Parsing**
- **D-01:** Canonical report at `<basename>.verifier-report.json` (sibling of the `.excalidraw` file), overwritten each run (no version suffix). Per LOOP-03.
- **D-02:** Same JSON object ALSO echoed in a ```json ... ``` fenced block as the last segment of the assistant message. File and block must be byte-identical (same `json.dumps` invocation feeds both).
- **D-03:** Schema (5 mandatory keys per issue: `check`, `element_id`, `severity`, `detail`, `suggested_fix`). `passed = true` iff `issues` is empty OR every issue has `severity: "warning"`.

**Structural Check Scope**
- **D-04:** Required structural ERROR checks (4): `arrow_endpoint_unanchored` (8 px tolerance on rectangle/ellipse/diamond border), `text_overflow_static` (using `0.6 × fontSize` monospace metric at `fontFamily: 3`), `image_path_unresolvable` (resolves under `.claude/agents/excalidraw/icons/` or absolute), `raw_emoji_in_text` (emoji codepoints + `fontFamily == 3`).
- **D-05:** Required style WARNING checks (4): `roughness_nonzero`, `fontfamily_nonmonospace`, `arrow_points_too_few` (<3), `arrow_missing_elbow_roundness` (no `roundness: { type: 2 }`).
- **D-06:** Verifier MUST NOT duplicate `scripts/excalidraw_validator.py` rules (label-on-shape, metadata, color contrast).

**Visual Review Strategy**
- **D-07:** Per-diagram absolute judgment ONLY. NO pixel-diff vs `examples/*.png`.
- **D-08:** Five visual `check` values: `text_overflow_visual`, `arrow_disconnected_visual`, `icon_blank`, `missing_glyph_box`, `layout_collision`. All `error` severity.
- **D-09:** Visual `suggested_fix` references JSON ids, not PNG coordinates.

**Suggested-Fix Specificity**
- **D-10:** Free-text imperative-verb hints. Phase 2 consumer is an LLM; structured patch hints rejected.
- **D-11:** Every fix references a primary `element_id`; multi-element fixes inline additional ids in text.

**Verifier Tool Set & Inputs**
- **D-12:** YAML `tools:` = `Read, Glob, Grep, Bash, Write`. No Edit, no Task, no MCP tools.
- **D-13:** Spawn contract = ONE arg (absolute path to `.excalidraw` file). Verifier derives `<basename>.png` and errors immediately if missing.
- **D-14:** `scripts/verifier_structural.py` exits 0 ALWAYS, prints a JSON array of issue objects to stdout. Subagent merges with visual issues.

**Fixture Strategy**
- **D-15:** Three fixtures under `.claude/agents/excalidraw/fixtures/verifier/`: `good/`, `raw-emoji/`, `text-overflow/`. Each with `.excalidraw` + `.png`.
- **D-16:** Each ships `expected-report.json`. Success-criteria test: run verifier on fixture, `diff` against expected ignoring `checked_at`.

### Claude's Discretion

- Exact severity ordering (decision: `error` > `warning`; no `info`).
- Visual-check prompt wording inside the subagent body (must produce documented schema).
- Whether to inline structural Python in subagent vs keep separate (decision: keep separate at `scripts/verifier_structural.py`, invoked via Bash).
- Whether verifier ever rejects work without producing a report (decision: NEVER; on internal error it emits a report with a `verifier_internal_error` issue).

### Deferred Ideas (OUT OF SCOPE)

- Pixel-diff visual regression against `examples/*.png`.
- A `verifier_internal_error` recovery report polish — for v1, if the subagent itself crashes the caller surfaces the crash; the always-produce-a-report rule applies to runtime errors inside the verifier body, not to subagent-runtime crashes.
- Configurable severity thresholds.
- A polished `verifier_self_test.sh` (manual recipe is acceptable; if a script is added, treat as polish).
- Multi-page / multi-frame `.excalidraw` files.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| **VRFY-01** | New subagent file at `.claude/agents/excalidraw/excalidraw_verifier.md` performing structural pre-check (4 checks) + multimodal visual review (5 checks). | YAML frontmatter format verified against [official subagent docs](https://code.claude.com/docs/en/sub-agents) and `excalidraw_specialist.md`. Structural check math worked out below. Multimodal `Read` on PNG is the default behavior — no special syntax needed (subagent inherits multimodal capability from model). |
| **VRFY-02** | Verifier returns structured pass/fail report `{ passed, issues: [{ check, element_id, severity, detail, suggested_fix }] }`. | Schema specified in D-03. File-canonical + message-fenced redundancy (D-01/D-02). `python -m json.tool` validates the file matches schema; `jq -e` validates required keys in self-test. |
| **CONT-01 (structural half)** | Raw Unicode emoji codepoints in `text` elements forbidden under `fontFamily: 3`; pre-check enforces. | Emoji ranges `U+1F300–U+1FAFF`, `U+2600–U+27BF`, plus regional-indicator pairs `U+1F1E6–U+1F1FF`. Python regex pattern verified ([advertools docs](https://advertools.readthedocs.io/en/master/advertools.emoji.html), [Kaggle reference](https://www.kaggle.com/code/eliasdabbas/how-to-create-a-python-regex-to-extract-emoji)). |

## Project Constraints (from CLAUDE.md)

**No `./CLAUDE.md` exists at the project root or in the agent directory.** Therefore the planner has no project-wide directive overlay beyond:

- `.planning/codebase/CONVENTIONS.md` — the Python-helper script-shape (`excalidraw_validator.py` shape: raw `sys.argv`, no `argparse`, no type hints, terse linter style) is the right model for `verifier_structural.py` since this is a one-off linter, not a production tool. Don't import the renderer's `argparse`+typed shape.
- `.planning/codebase/CONVENTIONS.md` (shell): `#!/bin/bash` always, `set -e`, `SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"` idiom. **Not relevant here** — verifier invokes Python directly via Bash inside the subagent; no new shell wrapper is needed (and CONTEXT.md does not request one).
- `.planning/codebase/CONVENTIONS.md` (subagent): YAML frontmatter has `name`, `description`, `tools` keys; `tools:` is a single comma-separated line; section ordering inside body uses XML-style tags. See §Subagent File Format below.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Receive `.excalidraw` path, derive PNG path, gate-check both exist | Subagent (`excalidraw_verifier.md` body) | — | Subagent's spawn contract owns input validation per D-13. |
| Parse `.excalidraw` JSON | Python helper (`scripts/verifier_structural.py`) | — | Pure-data work; deterministic; testable on host without spawning a subagent. |
| Structural checks (4 errors + 4 warnings) | Python helper | — | Same as above. JSON array to stdout. |
| Multimodal visual review (5 checks) | Subagent (LLM with multimodal `Read`) | — | Vision tokens are unavoidable; can't be done in pure Python. |
| Merge structural + visual issues into final report | Subagent (small Bash + Write step) | — | Subagent already has both halves in its context after the merge. |
| Emit canonical sibling JSON file | Subagent (`Write` tool) | — | Tools list explicitly includes `Write` (D-12). |
| Emit fenced ```json block in last assistant message | Subagent (final message) | — | Same payload; redundancy. |
| Self-test execution (fixture comparison) | Bash + `jq` (manual recipe) | Helper script (polish, optional) | Fixture diff is a 3-line recipe; no agent orchestration needed. |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python 3.11+ stdlib (`json`, `sys`, `os`, `re`, `pathlib`) | system | All structural-check logic | Already used by `excalidraw_validator.py` and `render_excalidraw.py`. **Zero new dependencies.** Lockfile `scripts/pyproject.toml` requires Python ≥3.11 already. |
| `python3` (CLI) | 3.11+ | Invoke helper from subagent Bash | Available on this machine (`/usr/bin/python3` -> `Python 3.14.4`). The wider repo uses bare `python` in `validate_and_render.sh:14` — see §Common Pitfalls re: which to invoke. |
| `jq` (CLI) | 1.7+ | Self-test report comparison (ignore `checked_at`) | Available on this machine (`/usr/bin/jq` -> `jq-1.8.1`). [VERIFIED: shell `which jq`] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `bash` | 4.0+ | Subagent's `Bash` tool invokes `python3 scripts/verifier_structural.py <path>` and captures stdout | Inside the subagent's operational sequence only. |
| `Write` (Claude Code tool) | — | Sibling JSON file emission | Subagent uses this exactly once per run, on the report path. |
| `Read` (Claude Code tool) | — | PNG (multimodal, vision tokens) + JSON (text) | Verified: Claude Code's `Read` natively supplies image content to the multimodal model. No special syntax. Confirmed in `excalidraw_specialist.md` line 99 ("Read the PNG"). |
| `Glob` (Claude Code tool) | — | `.claude/agents/excalidraw/icons/*.png` listing for emoji-to-icon suggestion | Used by `excalidraw_specialist.md:148` the same way. |
| `Grep` (Claude Code tool) | — | Optional convenience for grepping text content for emoji ranges in the subagent body if Python helper output is ambiguous | Probably unused at runtime; D-12 lists it for tool-allowlist completeness. |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Pure-Python `verifier_structural.py` (separate file) | Inline all structural logic in the subagent prompt as instructions to compute | Subagent would burn input tokens parsing JSON in-prompt and would produce non-deterministic results (LLMs are bad at exact arithmetic over coordinate arrays). The separate-helper choice is explicitly locked by D-14 and CONTEXT.md "Claude's Discretion" notes. |
| `argparse` for the helper CLI | Raw `sys.argv[1]` access | Per `CONVENTIONS.md`, the validator's terse shape (raw argv, no type hints) is the project convention for linter-style scripts. Keep consistency. |
| `regex` package (third-party) for emoji detection | Stdlib `re` with Unicode escapes | The `\U0001F300-\U0001FAFF` class works in stdlib `re` since Python 3.3. Avoid the dependency. |
| Pillow / image-analysis libraries for visual checks | Multimodal `Read` (let the LLM see the PNG) | Multimodal `Read` is the entire point of the visual half. Pillow can't tell you "this icon rendered blank" without OCR/heuristics. |
| Separate `verifier_self_test.sh` script | Inline 3-line bash recipe per fixture | Deferred in CONTEXT.md; manual recipe in PLAN.md is acceptable. A script can ship as polish without changing the contract. |

**Installation:**
```bash
# No new packages. python3 and jq are already on the system.
# Verify with:
python3 --version  # -> Python 3.11+
jq --version       # -> jq-1.6+
```

**Version verification:**
- `python3 --version` → `Python 3.14.4` [VERIFIED: bash on dev machine 2026-05-21]
- `jq --version` → `jq-1.8.1-dirty` [VERIFIED: bash on dev machine 2026-05-21]
- Python `re` Unicode escape support: ≥ 3.3, current 3.14 ✓

## Package Legitimacy Audit

**Not applicable.** This phase installs zero external packages — all functionality uses Python stdlib + already-installed system binaries (`python3`, `jq`, `bash`). No `pip install`, no `npm install`. The Package Legitimacy Gate is skipped per protocol ("Required whenever this phase installs external packages").

## Subagent File Format

[VERIFIED: [official Claude Code subagent docs](https://code.claude.com/docs/en/sub-agents) fetched 2026-05-21]

```markdown
---
name: excalidraw_verifier
description: <one-line capability statement — when Claude should delegate to this subagent>
tools: Read, Glob, Grep, Bash, Write
---

<role>
...
</role>

<inputs>
...
</inputs>

<operational_sequence>
1. ...
2. ...
</operational_sequence>

<output_contract>
...
</output_contract>
```

**Field notes** (from official docs):

- `name`: required, lowercase + hyphens or underscores. The filename does NOT have to match `name`, but matching them is the convention (`excalidraw_specialist.md` matches `name: excalidraw_specialist`).
- `description`: required. Used by Claude's delegation logic to decide when to invoke. Should describe **when** to use the subagent, not just what it does. Example draft: `"Static + visual verifier for Excalidraw diagrams. Use after rendering a .excalidraw to PNG to get a structured pass/fail report on text overflow, arrow connectivity, icon presence, and emoji policy."`
- `tools`: optional but required by D-12. Comma-separated single line. Allowlist (subagent can ONLY use these). `excalidraw_specialist.md:4` is the exact reference shape.
- **Multimodal**: no special field. `Read` on a `.png` automatically supplies image content to the multimodal model. The subagent inherits multimodal capability from its model. [VERIFIED: official docs; confirmed by reading `excalidraw_specialist.md` operational mandate #2 which uses Read on examples/*.png the same way.]
- `model`: optional. Defaults to `inherit` (uses the same model as the main conversation). **Recommendation:** omit it (let it inherit). Vision quality matters here, so don't force `haiku`.
- **Section ordering inside body** per `CONVENTIONS.md`: XML-style tags. For a verifier (not a generator) the natural sections are `<role>`, `<inputs>`, `<operational_sequence>`, `<output_contract>`, `<failure_modes>`. The specialist's `<capabilities>` / `<asset_paths>` / `<visual_standards>` / `<drawing_methodology>` / `<style_principles>` / `<operational_mandates>` ordering does not apply 1-for-1 (those are author-side concerns).

## Architecture Patterns

### System Architecture Diagram

```
        caller (Phase-2 specialist, in Phase 1: human)
                          │
                          │  single arg:
                          │  absolute path to .excalidraw
                          ▼
        ┌──────────────────────────────────────────┐
        │   excalidraw_verifier.md (subagent body) │
        │   tools: Read, Glob, Grep, Bash, Write   │
        └──┬────────┬────────────┬────────────┬────┘
           │        │            │            │
   step 1  │   step 2          step 3       step 5
   derive  │   Bash invoke     Read PNG     Write report
   PNG     │   structural      (vision      to sibling
   path,   │   helper          tokens)      .verifier-
   gate    │   ──────────►                  report.json
   exist   ▼                                & emit fenced
        ┌──────────────────────────┐       ```json block
        │ scripts/verifier_        │       (D-01, D-02)
        │   structural.py          │
        │ ─ JSON parse             │
        │ ─ 4 error checks         │
        │ ─ 4 warning checks       │
        │ ─ exit 0 always          │
        │ ─ stdout: JSON array     │
        │   of issue objects       │
        └──────────────────────────┘
                  │
                  │ stdout captured by Bash tool
                  ▼
        ┌──────────────────────────┐
        │ subagent merges          │
        │  structural issues       │
        │  +                       │
        │  visual issues           │
        │ ──► single report obj    │
        │ ──► json.dumps once      │
        │ ──► piped to BOTH        │
        │     Write tool AND       │
        │     last message         │
        └──────────────────────────┘
```

Entry: subagent spawn with one path. Exit: sibling `.verifier-report.json` file on disk + final assistant message ending in a fenced ```json block.

### Recommended Project Structure

```
.claude/agents/excalidraw/
├── excalidraw_specialist.md           # existing, unchanged
├── excalidraw_verifier.md             # NEW (this phase)
├── scripts/
│   ├── excalidraw_validator.py        # existing, unchanged
│   ├── verifier_structural.py         # NEW (this phase)
│   └── ... (other existing scripts)
└── fixtures/                          # NEW directory
    └── verifier/
        ├── good/
        │   ├── good.excalidraw
        │   ├── good.png               # pre-rendered via validate_and_render.sh
        │   └── expected-report.json   # passed: true, issues: []
        ├── raw-emoji/
        │   ├── raw-emoji.excalidraw   # contains text "✅" w/ fontFamily 3
        │   ├── raw-emoji.png          # tofu box visible
        │   └── expected-report.json   # one raw_emoji_in_text issue
        └── text-overflow/
            ├── text-overflow.excalidraw   # 280-px text in 180-px rect
            ├── text-overflow.png          # text visibly overflows
            └── expected-report.json       # one text_overflow_static issue
```

### Pattern 1: Helper-script JSON parse + checks

**What:** Pure-Python deterministic linter. Reads one `.excalidraw` JSON path from `sys.argv[1]`, runs every check, prints a JSON array of issue objects, exits 0.

**When to use:** Always — D-14 mandates this is the only source of structural issues.

**Example structure (sketch, NOT prescriptive line count):**

```python
# Source: pattern derived from scripts/excalidraw_validator.py (existing repo file)
# Mirrors the validator's: simple structure, raw sys.argv, no type hints, no argparse.
import json
import sys
import os
import re
from pathlib import Path

MONOSPACE_ADVANCE_RATIO = 0.6  # Cascadia/Fira Code average advance width per em
ENDPOINT_TOLERANCE_PX = 8       # per D-04

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF"   # Misc Symbols & Pictographs + Supplemental
    "☀-➿"              # Misc Symbols + Dingbats
    "\U0001F1E6-\U0001F1FF"      # Regional indicators (flag halves)
    "]"
)

EMOJI_TO_ICON = {
    "✅": "success_icon.png",   # ✅
    "❌": "failure_icon.png",   # ❌
    "⚠": "failure_icon.png",   # ⚠ (no warning icon exists; failure is closest)
    # ... small static dict per CONTEXT.md specifics
}

def issue(check, element_id, severity, detail, suggested_fix):
    return {
        "check": check,
        "element_id": element_id,
        "severity": severity,
        "detail": detail,
        "suggested_fix": suggested_fix,
    }

def check_raw_emoji_in_text(elements):
    out = []
    for el in elements:
        if el.get("type") != "text":
            continue
        if el.get("fontFamily") != 3:
            continue
        text = el.get("text", "")
        for m in EMOJI_RE.finditer(text):
            cp = ord(m.group(0))
            icon = EMOJI_TO_ICON.get(m.group(0))
            fix = (
                f"Replace text element id: {el.get('id','?')} (raw emoji U+{cp:04X}) "
                f"with an image element pointing to "
                f".claude/agents/excalidraw/icons/{icon}."
                if icon else
                f"Replace text element id: {el.get('id','?')} (raw emoji U+{cp:04X}) "
                f"with an image element pointing to a matching PNG in "
                f".claude/agents/excalidraw/icons/."
            )
            out.append(issue(
                "raw_emoji_in_text",
                el.get("id", "unknown"),
                "error",
                f"Text element contains raw emoji codepoint U+{cp:04X}.",
                fix,
            ))
    return out

# ... (one function per check; see §Common Pitfalls for arrow-anchor math)

def main():
    path = sys.argv[1]
    with open(path) as f:
        data = json.load(f)
    elements = data.get("elements", [])
    issues = []
    issues.extend(check_raw_emoji_in_text(elements))
    issues.extend(check_text_overflow_static(elements))
    issues.extend(check_arrow_endpoint_unanchored(elements))
    issues.extend(check_image_path_unresolvable(elements, Path(path).parent))
    issues.extend(check_roughness_nonzero(elements))
    issues.extend(check_fontfamily_nonmonospace(elements))
    issues.extend(check_arrow_points_too_few(elements))
    issues.extend(check_arrow_missing_elbow_roundness(elements))
    print(json.dumps(issues))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Pattern 2: Subagent body as a 7-step operational sequence

**What:** A `<operational_sequence>` block that is a numbered, imperative list of exactly the steps the subagent must perform on every invocation.

**When to use:** This phase. Subagent bodies that drift from an explicit sequence produce unreliable output schemas. The numbered sequence is the contract.

**The seven steps (recommended):**

1. **Validate input.** Confirm exactly one argument was passed. Derive `<basename>.png` from `<basename>.excalidraw`. If either file is missing, write a report containing one `verifier_internal_error` issue to the expected sibling path AND emit the fenced ```json block, then stop.
2. **Run structural helper.** `bash`: `python3 .claude/agents/excalidraw/scripts/verifier_structural.py <absolute-path>`. Capture stdout. If non-empty, parse as JSON array (it always is — exit 0 always per D-14). If exit code ≠ 0 (helper crashed), emit a `verifier_internal_error` issue with the stderr captured.
3. **Read PNG (multimodal).** `Read` the derived PNG path. This puts the image into the model's context for the visual review.
4. **Apply the 5 visual checks.** Use the inlined visual-check rubric (see §Visual-Check Rubric below). Produce a JSON array of issue objects mirroring the helper's schema.
5. **Merge.** Concatenate structural-issues array + visual-issues array. Compute `passed` = (every issue has `severity: "warning"` OR list is empty).
6. **Emit canonical file.** Build the full report object: `{ passed, checked_at (UTC ISO 8601), source, png, issues }`. Serialize ONCE with `json.dumps(report, indent=2)`. Use `Write` to emit to `<basename>.verifier-report.json`.
7. **Echo in message.** End the assistant message with a fenced ```json block containing the byte-identical serialization.

**Example (sketch):**
```markdown
<operational_sequence>

1. **Validate input.** ...

2. **Run structural helper.** Execute:
   ```bash
   python3 .claude/agents/excalidraw/scripts/verifier_structural.py "$ARG"
   ```
   ...

[etc.]

</operational_sequence>
```

### Anti-Patterns to Avoid

- **Embedding the structural-check logic in the subagent prompt as natural-language instructions.** The LLM will compute approximate widths, miss elements, and emit non-deterministic issue arrays. Locked out by D-14.
- **Computing visual checks in Python via image-processing libs.** Pillow / OpenCV can't reliably detect "this icon rendered blank" without OCR + heuristics that would need their own verification. The whole point of the visual half is multimodal vision.
- **Letting the subagent decide its own report path.** Locked by D-01: always `<basename>.verifier-report.json`. The subagent derives the path; the caller does not pass it.
- **Producing a markdown narrative as the primary output.** Locked by VRFY-02 and D-02/D-03: structured JSON only. The fenced ```json block must be the **last** segment of the message, with no trailing prose.
- **Using `python` (bare) instead of `python3`.** `validate_and_render.sh:14` uses bare `python` and this is flagged in CONCERNS.md #7 as a real inconsistency. The new helper invocation should use `python3` for portability.
- **Cross-referencing `examples/*.png` during visual review.** Locked by D-07. No pixel-diff, no "does this look like governance.png?" checks.
- **Hand-rolling JSON serialization.** Use `json.dumps` (Python helper) and the same `json.dumps`-style output for the subagent. Don't string-format JSON.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Emoji detection | A custom char-range loop with manual Unicode tables | Compiled `re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF]")` | Stdlib `re` handles supplementary-plane codepoints correctly since Python 3.3. Manual loops miss surrogate pair quirks and variation selectors. |
| JSON serialization for the report | `f"{{'passed': {passed}, ...}}"` string formatting | `json.dumps(report, indent=2, sort_keys=False)` | Must be byte-identical between the file and the fenced block. Hand-formatted JSON drifts (quote escaping, bool casing, trailing commas). |
| Path resolution for image elements | Re-implement absolute/relative/asset-dir fallback | Mirror the resolution order from `scripts/render_excalidraw.py:84-94` (absolute → input dir → `EXCALIDRAW_ASSETS_DIR`); but for the verifier the asset dir IS `.claude/agents/excalidraw/icons/` and the input dir is the `.excalidraw` parent | Re-implementing diverges from the renderer; if the renderer fails to find an icon, the verifier should also fail to find it (consistency is the contract). |
| Arrow-endpoint-on-border math from scratch | A new geometry library | Inline shape-specific tests (rectangle: 4 line-segments + 8 px tolerance; ellipse: parametric distance to ellipse boundary; diamond: 4 line-segments rotated 45°) | See §Common Pitfalls for the math. ~30 lines of pure stdlib Python. Pulling in `shapely` for 8 px tolerance is overkill. |
| Self-test runner | A bespoke test framework | `bash` + `jq` one-liner (see §Self-Test Recipe) | Three fixtures, one comparison rule (ignore `checked_at`). Pytest infrastructure for three asserts is over-engineered. |
| Date / timestamp formatting | Manual `f"{year}-..."` | `datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')` | One stdlib call. Don't reinvent. |

**Key insight:** This phase is small enough that any "framework" or "abstraction layer" is friction. Pure stdlib + repo conventions = correct shape.

## Runtime State Inventory

> Not applicable. This phase is greenfield: no rename, no refactor, no migration. New files only:
>
> - `excalidraw_verifier.md` (NEW file)
> - `scripts/verifier_structural.py` (NEW file)
> - `fixtures/verifier/{good,raw-emoji,text-overflow}/` (NEW directory + 9 files)
>
> No stored data, live service config, OS-registered state, secrets, or build artifacts are affected. Step 2.5 — SKIPPED with reason.

## Common Pitfalls

### Pitfall 1: Arrow endpoint absolute coordinates

**What goes wrong:** Author assumes `arrow.points[-1]` is in absolute scene coordinates and checks it against shape borders directly. Result: every arrow flags as unanchored.

**Why it happens:** Per [DeepWiki / Excalidraw source](https://deepwiki.com/excalidraw/excalidraw/3.1-element-binding-and-geometry), arrow `points` are in **element-local coordinates**, with `points[0]` always `[0, 0]`. The absolute scene coordinate of the last point is `(arrow.x + points[-1][0], arrow.y + points[-1][1])`. Rotation (non-zero `angle`) further transforms this — but the Architect's Precision style produces axis-aligned elbows only, so `angle == 0` is the practical case.

**How to avoid:**
```python
# Source: derived from DeepWiki Excalidraw element-binding docs (verified 2026-05-21)
def arrow_last_point_abs(arrow):
    pts = arrow.get("points", [])
    if not pts:
        return None
    px, py = pts[-1]
    return (arrow.get("x", 0) + px, arrow.get("y", 0) + py)
```

**Warning signs:** Helper flags every arrow in a known-good fixture. Likely missed the `x, y` offset.

### Pitfall 2: Shape border hit test for the three shape types

**What goes wrong:** Author uses bounding-box containment instead of border-touch test, OR uses border-touch test without the 8 px tolerance, OR uses the same test for ellipses and diamonds as for rectangles.

**Why it happens:** Each shape has a different "border":

- **rectangle** with bounds `(x, y, w, h)`: border is the union of 4 line segments. Point `(px, py)` is "on border within tolerance" if `min(distance_to_each_segment) ≤ 8`. A simpler, equally-correct test: `(x − 8 ≤ px ≤ x + w + 8)` AND `(y − 8 ≤ py ≤ y + h + 8)` AND NOT `(x + 8 < px < x + w − 8 AND y + 8 < py < y + h − 8)` — i.e., inside the outer 8-px-padded bbox but not inside the inner 8-px-shrunk bbox.
- **ellipse** with bounds `(x, y, w, h)` (centered at `(x+w/2, y+h/2)` with semi-axes `w/2, h/2`): point is on border if `|sqrt(((px-cx)/(w/2))² + ((py-cy)/(h/2))²) − 1| × min(w/2, h/2) ≤ 8`. (Normalized-distance-to-1 approximation; acceptable for 8 px tolerance on shapes of typical sizes.)
- **diamond** with bounds `(x, y, w, h)`: 4 line segments connecting midpoints of the bbox edges. Point is on border if `min(distance_to_each_diamond_segment) ≤ 8`.

**How to avoid:** Implement one function per shape type. Don't try to abstract over them — the math is genuinely different and the indirection costs readability.

**Warning signs:** Arrow endpoints that visibly land inside a shape (per visual review) are flagged as unanchored. Likely missing the "inside the shape counts as anchored" allowance — per D-04, `arrow_endpoint_unanchored` fires only when the endpoint does NOT touch the border within 8 px. An endpoint deep inside a shape is also unanchored visually (the arrow head is hidden), but for v1 the simpler "within 8 px of border" test suffices. **Recommendation:** treat any point inside the padded-by-8 bbox AND outside the shrunk-by-8 bbox as "on border", and ignore strict-interior points (they're already covered by `endBinding` if present). Note: per [DeepWiki binding docs](https://deepwiki.com/excalidraw/excalidraw/3.2-element-binding-system), Excalidraw applies an `effectiveGap = BASE_BINDING_GAP_ELBOW + strokeWidth/2` at render time, so a "good" bound arrow's endpoint is ~outside the border by a few pixels — the 8-px tolerance accommodates this gap.

### Pitfall 3: Containing-shape lookup for text-overflow

**What goes wrong:** Author iterates shapes in declaration order and takes the first match, picking an outer container instead of the immediate parent.

**Why it happens:** The text element may be inside multiple nested rectangles (Group Container → Icon Block). The "containing shape" for the overflow check should be the **smallest** rectangle/ellipse/diamond whose bounding box encloses the text bounding box (CONTEXT.md D-04 explicitly: "the smallest rectangle/ellipse/diamond whose bounding box encloses the text element's bounding box").

**How to avoid:**
```python
def find_containing_shape(text_el, elements):
    tx, ty = text_el.get("x", 0), text_el.get("y", 0)
    tw = estimated_text_width(text_el)
    th = text_el.get("fontSize", 20)  # approximate height = fontSize
    candidates = []
    for el in elements:
        if el.get("type") not in ("rectangle", "ellipse", "diamond"):
            continue
        sx, sy = el.get("x", 0), el.get("y", 0)
        sw, sh = el.get("width", 0), el.get("height", 0)
        # bounding box containment
        if sx <= tx and sy <= ty and sx + sw >= tx + tw and sy + sh >= ty + th:
            candidates.append((sw * sh, el))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[0])  # smallest area first
    return candidates[0][1]
```

**Warning signs:** Text-overflow check fires on text that visibly fits inside its immediate container. Likely matched against the outer Group Container.

### Pitfall 4: Monospace text-width metric is approximate

**What goes wrong:** The 0.6 × fontSize × char-count formula over-estimates or under-estimates real Cascadia advance width by 5–15%.

**Why it happens:** Cascadia Code's actual advance width per em varies slightly by character (digits and spaces are 0.6 em, some Unicode characters are wider). [VERIFIED: Cascadia is monospaced — [Microsoft Cascadia Code wiki](https://en.wikipedia.org/wiki/Cascadia_Code) — but the exact em ratio is not published as a constant.] Empirically across monospace coding fonts (Cascadia, Fira Code, Consolas), the average advance is ~0.58–0.62 em.

**How to avoid:**
1. Hard-code `MONOSPACE_ADVANCE_RATIO = 0.6` as a module constant per CONTEXT.md "specifics" section.
2. Add a docstring comment explaining the empirical derivation.
3. Accept the ~10% error: the visual check (`text_overflow_visual`) is the safety net for cases the metric misses.

**Warning signs:** A diagram with text that visibly fits is flagged by the structural check. Acceptable false-positive rate; lift the rectangle width on the suggested-fix.

### Pitfall 5: Subagent must ALWAYS produce a report

**What goes wrong:** Verifier crashes mid-run, leaves no report, caller is stuck.

**Why it happens:** Several failure paths:
- Missing PNG (D-13).
- Helper script crashes (should be impossible per D-14 exit-0-always, but defensive coding matters).
- `.excalidraw` JSON is malformed.
- `Read` on the PNG fails (image is corrupt).
- `Write` permission denied.

**How to avoid:** Step 1 of the operational sequence (see §Pattern 2) explicitly handles missing-input cases by emitting a `verifier_internal_error` report. The subagent body should include a **terminal "if anything went wrong above, emit error report and stop"** instruction. Use the same five-key schema, with `check: "verifier_internal_error"`, `element_id: "—"`, `severity: "error"`, `detail: "<what went wrong>"`, `suggested_fix: "Investigate; this is a verifier bug, not a diagram bug."`

**Warning signs:** A Phase-2 auto-fix loop hangs because the caller is waiting for a file that never appeared. Verifier's invariant is violated.

### Pitfall 6: `python` vs `python3` portability

**What goes wrong:** Subagent invokes `python scripts/verifier_structural.py`, which on minimal systems (or systems where `python` is Python 2) fails.

**Why it happens:** `scripts/validate_and_render.sh:14` uses bare `python`, and CONCERNS.md #7 already flags this as a real inconsistency. Don't propagate it.

**How to avoid:** Use `python3` in the subagent's Bash invocation. Verified available on this dev machine; standard on all Linux/macOS in 2026.

### Pitfall 7: Report file vs. message must be byte-identical

**What goes wrong:** Subagent serializes the dict twice — once for `Write`, once for the message — and the two outputs differ (key ordering, indentation, trailing newline).

**Why it happens:** `json.dumps(d)` is deterministic given identical args, but if the subagent runs it twice with different settings (one with `indent=2`, one without), the file and the block diverge. Phase 2 then sees different content depending on which one it parses.

**How to avoid:** Serialize **once** in a single Bash invocation, capture the string into a variable, write it via `Write`, and echo the same string into the fenced block. Practical pattern:
```bash
# inside the subagent's Bash step
REPORT_JSON=$(python3 -c '
import json, sys
report = json.loads(sys.stdin.read())
print(json.dumps(report, indent=2, sort_keys=False))
' <<<'<merged report dict as one-line JSON>')
# then: Write tool with content=$REPORT_JSON, and message ends with ```json\n$REPORT_JSON\n```
```

## Code Examples

### Subagent YAML frontmatter (verified format)

```yaml
---
name: excalidraw_verifier
description: Static + visual verifier for Excalidraw diagrams. Use after rendering a .excalidraw to PNG to get a structured pass/fail report covering arrow endpoint anchoring, text overflow, image-path resolution, raw-emoji bans, and visible render defects (text overflow, blank icons, missing-glyph boxes, layout collisions). Always emits a sibling <basename>.verifier-report.json file.
tools: Read, Glob, Grep, Bash, Write
---
```

[VERIFIED against [official subagent docs](https://code.claude.com/docs/en/sub-agents) and `excalidraw_specialist.md:1-5`]

### Emoji regex (Python)

```python
# Source: advertools docs + Kaggle reference (Eliasdabbas) verified 2026-05-21
import re

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"   # Miscellaneous Symbols and Pictographs through Symbols and Pictographs Extended-A
    "☀-➿"             # Miscellaneous Symbols + Dingbats (✅ U+2705 lives here)
    "\U0001F1E6-\U0001F1FF"     # Regional Indicator Symbols (flag halves)
    "]"
)
# Use: EMOJI_RE.search(text_element["text"]) -> Match | None
# Use: EMOJI_RE.findall(text) -> list of single-char strings
```

Note: `✅` is U+2705, which falls in `U+2600-U+27BF`. `❌` is U+274C, same range. `🚀` is U+1F680, which falls in `U+1F300-U+1FAFF`. All three are covered.

### `datetime` for `checked_at`

```python
# Source: Python 3 stdlib (datetime module)
import datetime
checked_at = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
# => "2026-05-21T12:34:56Z"
```

### Bash invocation from subagent

```bash
# inside the subagent's Step 2
SOURCE="$1"   # the absolute .excalidraw path passed by caller
PNG="${SOURCE%.excalidraw}.png"
test -f "$SOURCE" || { echo "missing .excalidraw"; exit 2; }
test -f "$PNG"    || { echo "missing PNG (run validate_and_render.sh first)"; exit 2; }

STRUCT_JSON=$(python3 /home/.../scripts/verifier_structural.py "$SOURCE")
# STRUCT_JSON is a JSON array of issue objects, possibly empty: "[]"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single-step "validate then render" pipeline that prints "now look at the PNG" as an instruction | Validate → render → **subagent-driven structured verification** | This phase | Replaces an unenforced instruction with a structured contract Phase 2 can consume programmatically |
| LLM self-review (main agent inspects its own output) | Separate **fresh-eyes** verifier subagent | Pre-roadmap key decision (PROJECT.md) | Reduces confirmation bias on visual inspection |
| Pixel-diff regression against canonical examples | Per-diagram absolute judgment | Pre-roadmap (PROJECT.md Out of Scope) | Examples remain ground truth for the *generator*, not test oracle for the verifier |
| Inline structural logic in subagent prompt | Pure-Python deterministic helper invoked via Bash | This phase (D-14) | Deterministic, host-side testable, no vision tokens burned on cheap defects |

**Deprecated/outdated:**
- `excalidraw_specialist.md` operational mandate #7 ("use `mcp__excalidraw__create_view` to verify the visual result") will be **complemented** (not replaced) by the verifier in Phase 2. The MCP canvas check is not the same as inspecting the Docker-rendered PNG. For Phase 1, the existing specialist remains untouched.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `0.6 × fontSize` is an acceptable monospace advance-width ratio for fontFamily 3 (Cascadia) | Standard Stack / Pattern 1 / Pitfall 4 | False positives on text-overflow check (text that visibly fits flagged as too wide) or false negatives (text that visibly overflows missed). Mitigated by the visual `text_overflow_visual` check as safety net. CONTEXT.md "specifics" section explicitly approves this constant. [VERIFIED: Cascadia is monospaced; ratio is empirical, derived from typical coding-font advance widths in the 0.58–0.62 range.] |
| A2 | The 8 px tolerance for `arrow_endpoint_unanchored` covers Excalidraw's `BASE_BINDING_GAP_ELBOW + strokeWidth/2` render-time offset | Common Pitfalls #2 | If Excalidraw's actual elbow-binding gap exceeds 8 px (it does not in 0.17.3 per DeepWiki — base gap is small + 1 px for strokeWidth/2), bound arrows would falsely flag. CONTEXT.md D-04 explicitly locks the 8 px tolerance. [CITED: [DeepWiki binding docs](https://deepwiki.com/excalidraw/excalidraw/3.2-element-binding-system)] |
| A3 | Multimodal `Read` on a PNG inside a Claude Code subagent supplies image content to the model without special configuration | Subagent File Format | If subagent context loading strips image data, the visual half is impossible. The existing `excalidraw_specialist.md` operational mandate #2 already does this on `examples/*.png`, and the official subagent docs list `Read` as a normal tool — image handling is a model capability, not a tool capability. [VERIFIED: [official docs](https://code.claude.com/docs/en/sub-agents); [ASSUMED] that this works identically in subagent contexts — confirmed by repo precedent.] |
| A4 | The `EMOJI_TO_ICON` mapping table is a small static dict authored at helper time (✅→success_icon, ❌→failure_icon, etc.) and acceptable to ship hard-coded | Pattern 1 / CONTEXT.md "specifics" | Mapping drift if icon library changes filenames. Low risk; CONCERNS.md #9-10 documents pending `icons/` cleanup but those are Phase-2-deferred. [ASSUMED based on CONTEXT.md guidance.] |
| A5 | The verifier subagent's spawn-prompt is established by the caller passing a single absolute path; no other invocation modality exists | D-13 | Caller could invoke without the path argument. The subagent's Step 1 must handle this (emit `verifier_internal_error`). [VERIFIED in D-13.] |

## Open Questions

1. **What model should the subagent inherit/use for the visual half?**
   - What we know: D-12 specifies tools but not model. Default is `inherit`. Vision quality matters for catching missing-glyph boxes and icon blanks.
   - What's unclear: Whether Phase-2 callers will sometimes be running Haiku (cheap inheritance) and degrade the visual half.
   - Recommendation: Omit the `model:` field (default `inherit`); add a §Notes for Phase 2 stating "if the parent runs Haiku, consider passing `model: sonnet` at invocation". Not a blocker for Phase 1.

2. **Should the subagent body include a worked example of a "good" report and a "failing" report?**
   - What we know: D-03 fixes the schema. Concrete examples reduce schema drift.
   - What's unclear: Whether the example bloats the prompt enough to matter.
   - Recommendation: Include one good and one failing example, both ≤ 20 lines, inside the `<output_contract>` section. Documented schema + example beats schema alone for output reliability.

3. **The fixture's `expected-report.json` files contain absolute paths in `source` and `png` — but the fixture is meant to be portable. How is this reconciled?**
   - What we know: D-13 mandates absolute paths in the report; D-16 says the diff ignores `checked_at`.
   - What's unclear: The diff must also normalize `source` and `png` paths (they vary by checkout location).
   - Recommendation: Either (a) commit `expected-report.json` with PLACEHOLDER paths (`<SOURCE_ABS>`, `<PNG_ABS>`) that the self-test script substitutes before diffing, OR (b) extend the diff-ignore rule to include `source`, `png`, AND `checked_at`. Option (b) is simpler. **Recommendation:** Adopt option (b) — diff ignores `checked_at`, `source`, `png`. Document in the self-test recipe (§Self-Test Recipe below). This should be raised with planner for explicit confirmation, but is well within Claude's discretion per CONTEXT.md.

4. **Does the subagent need to handle text elements with `containerId` (i.e., text bound to a shape via Excalidraw's containment mechanism, where text uses the container's geometry)?**
   - What we know: Architect's Precision style prohibits the `label` property on shapes (validator enforces). But Excalidraw also supports `containerId` for bound text — the text auto-wraps within the container.
   - What's unclear: Whether existing Architect's Precision diagrams ever use `containerId`. Repo examples all use freestanding text elements (see kb/icon-block.md — text is separate, no `containerId`).
   - Recommendation: Phase 1 — ignore `containerId`. If a text element has `containerId`, skip the `text_overflow_static` check for it (the container auto-wraps so overflow is impossible by Excalidraw's design). Document this exclusion in the helper code.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3 (`python3`) | `verifier_structural.py` helper | ✓ | 3.14.4 | — (hard requirement; renderer already uses Python 3.11+) |
| `bash` | Subagent invocation; existing scripts | ✓ | system default | — |
| `jq` | Self-test recipe (report diff ignoring `checked_at`) | ✓ | 1.8.1 | `python3 -c 'import json; ...'` as inline alternative |
| Docker | Render pipeline (NOT this phase — fixtures use already-rendered PNGs) | ✓ | n/a verified separately | Render fixtures manually with `validate_and_render.sh` once at fixture-author time; never at verifier runtime |
| `validate_and_render.sh` | Producing fixture PNGs at fixture-creation time | ✓ | repo file | — |
| `@excalidraw/excalidraw@0.17.3` (via esm.sh CDN) | Render pipeline only, NOT verifier | n/a at runtime | — | Verifier reads pre-rendered PNG; CDN failure doesn't affect verifier |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None.

This phase has **zero new environment requirements** — every binary it depends on (python3, bash, jq) is already installed and used elsewhere in the repo.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | None (Bash + `jq` fixture diff) |
| Config file | None — see Wave 0 |
| Quick run command | `bash scripts/verifier_self_test.sh good` (after phase ships) — or manual one-liner per fixture |
| Full suite command | `bash scripts/verifier_self_test.sh` (loops over all 3 fixtures) — or 3 manual one-liners |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| VRFY-01 | Subagent file exists with valid frontmatter | fixture-existence | `test -f .claude/agents/excalidraw/excalidraw_verifier.md && head -5 .claude/agents/excalidraw/excalidraw_verifier.md \| grep -q 'name: excalidraw_verifier'` | ❌ Wave 0 |
| VRFY-01 | Helper script exists and runs without error on a good fixture | unit | `python3 .claude/agents/excalidraw/scripts/verifier_structural.py .claude/agents/excalidraw/fixtures/verifier/good/good.excalidraw \| jq 'length == 0'` → expects `true` | ❌ Wave 0 |
| VRFY-02 | Verifier on good fixture produces `passed: true, issues: []` | fixture-based | Spawn `excalidraw_verifier` subagent on `good/good.excalidraw`; diff resulting `good.verifier-report.json` against `good/expected-report.json` ignoring `checked_at`, `source`, `png` | ❌ Wave 0 |
| VRFY-02 | Every issue carries the 5 mandatory keys | unit | `jq -e '.issues \| all(. \| (has("check") and has("element_id") and has("severity") and has("detail") and has("suggested_fix")))' raw-emoji/expected-report.json` | ❌ Wave 0 |
| CONT-01 | Raw-emoji fixture produces ≥1 `raw_emoji_in_text` issue without vision tokens | unit (helper-level) | `python3 ... raw-emoji.excalidraw \| jq -e 'any(.[]; .check == "raw_emoji_in_text")'` | ❌ Wave 0 |
| VRFY-02 | Text-overflow fixture produces ≥1 text-overflow-related issue with a `suggested_fix` | fixture-based | `python3 ... text-overflow.excalidraw \| jq -e 'any(.[]; .check == "text_overflow_static" and (.suggested_fix \| length > 0))'` | ❌ Wave 0 |

### Sampling Rate

- **Per task commit:** Run the helper directly against the relevant fixture(s) (`python3 scripts/verifier_structural.py <fixture-path> \| jq .`). < 1 sec each.
- **Per wave merge:** Run the helper against all 3 fixtures + parse the helper output to confirm severity counts match expected. < 3 sec total.
- **Phase gate:** Spawn the full `excalidraw_verifier` subagent on each of the 3 fixtures; diff each generated `.verifier-report.json` against the fixture's `expected-report.json` ignoring `checked_at`, `source`, `png`. Requires interactive Claude Code session — manual.

### Wave 0 Gaps

- [ ] `.claude/agents/excalidraw/scripts/verifier_structural.py` — implements 4 error + 4 warning checks, JSON-array stdout, exit 0
- [ ] `.claude/agents/excalidraw/excalidraw_verifier.md` — subagent definition with YAML frontmatter + 7-step operational sequence + output contract
- [ ] `.claude/agents/excalidraw/fixtures/verifier/good/good.excalidraw` + `good.png` + `expected-report.json`
- [ ] `.claude/agents/excalidraw/fixtures/verifier/raw-emoji/raw-emoji.excalidraw` + `raw-emoji.png` + `expected-report.json`
- [ ] `.claude/agents/excalidraw/fixtures/verifier/text-overflow/text-overflow.excalidraw` + `text-overflow.png` + `expected-report.json`
- [ ] **Optional polish:** `scripts/verifier_self_test.sh` — runs the helper against all 3 fixtures + emits pass/fail summary. Per CONTEXT.md, can be a manual recipe in PLAN.md instead.

**Coverage rationale:** Three fixtures cover both severities and the good-case baseline. `good` exercises the empty-issues happy path (false-positive detection: if `good` ever produces issues, the helper has a logic bug). `raw-emoji` exercises the error-severity branch and the file/icons cross-reference. `text-overflow` exercises the geometric containing-shape lookup AND the suggested-fix string generation. Adding a 4th fixture (e.g., for image-path-unresolvable) is acceptable polish but not required by D-15.

**Signal-to-noise pattern:** The fixture-diff comparison is a single-source-of-truth test — `expected-report.json` is a stable file in the repo, and the diff rule (`ignore checked_at, source, png`) is deterministic. No flaky LLM-side assertions; the LLM's role is to faithfully echo the helper's output and apply the deterministic visual rubric.

**What "passing" means:** For each fixture, the generated `.verifier-report.json` matches the committed `expected-report.json` byte-for-byte after normalizing `checked_at`, `source`, `png`. For the helper alone, `python3 ... <fixture> | jq .` returns the expected issue array.

**What "false-positive passing" looks like:** (a) the report is empty when the fixture has known defects — schema validation passes but content is wrong; (b) missing required keys in issue objects — schema test must fire; (c) issue `check` strings drift from the documented vocabulary — `expected-report.json` diff fires; (d) `passed` field flipped (true when issues are errors) — fixture diff fires.

### Self-Test Recipe

```bash
#!/bin/bash
# Recipe — manual or scripted as scripts/verifier_self_test.sh

FIXTURES=(good raw-emoji text-overflow)
ROOT=".claude/agents/excalidraw/fixtures/verifier"
PASS=0; FAIL=0

for f in "${FIXTURES[@]}"; do
    # Step 1: invoke verifier (manually via Claude Code subagent spawn, or via a Phase-2 orchestrator)
    # In Phase 1 self-test, this step is the human running the verifier subagent
    # The verifier writes $ROOT/$f/$f.verifier-report.json

    GEN="$ROOT/$f/$f.verifier-report.json"
    EXP="$ROOT/$f/expected-report.json"

    # Step 2: compare ignoring volatile fields
    DIFF=$(diff \
        <(jq 'del(.checked_at, .source, .png)' "$EXP") \
        <(jq 'del(.checked_at, .source, .png)' "$GEN"))

    if [ -z "$DIFF" ]; then
        echo "PASS: $f"
        PASS=$((PASS + 1))
    else
        echo "FAIL: $f"
        echo "$DIFF"
        FAIL=$((FAIL + 1))
    fi
done

echo "Summary: $PASS pass / $FAIL fail"
exit $FAIL
```

## Security Domain

The repo project is a local-only developer tool (Excalidraw diagram authoring subagent). `security_enforcement` configuration is **not present** in `.planning/config.json` — neither key is set. Per protocol: include this section since the workflow.security_enforcement key is absent (treat as enabled).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Local dev tool; no authentication surface |
| V3 Session Management | no | No sessions |
| V4 Access Control | no | No multi-user access |
| V5 Input Validation | **yes** | `verifier_structural.py` validates `.excalidraw` JSON before processing — handle malformed JSON with `try/except json.JSONDecodeError`, emit a `verifier_internal_error` issue rather than crashing |
| V6 Cryptography | no | No crypto |
| V12 Files & Resources | **yes** (low priority — defense-in-depth, not active threat) | `image_path_unresolvable` check inherits the path-traversal surface flagged in CONCERNS.md #5. The verifier should NOT canonicalize and validate paths beyond what the renderer already does — that would diverge from the renderer's actual behavior (the verifier's job is to flag what the renderer can't load, not to enforce a stricter policy). |

### Known Threat Patterns for {stack}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Malformed JSON input crashing the helper | Denial of service | `try/except json.JSONDecodeError` → emit one `verifier_internal_error` issue, exit 0 (D-14) |
| `.excalidraw` referencing absolute host paths (`/etc/passwd`) in image elements | Information disclosure (inherited from renderer, not introduced by verifier) | Out of scope — CONCERNS.md #5 documents this for the renderer. Verifier merely reports unresolvable paths; it does NOT add path-traversal enforcement (that belongs to the renderer per HARD-03 in v2 roadmap) |
| Subagent emits a partial report mid-failure leaving the caller stuck | Repudiation / hang | Step 1 of operational sequence + the "always emit a report" invariant; `verifier_internal_error` issue on any internal failure |
| Schema drift between fixture-author intent and actual emitted JSON | Tampering (with downstream Phase-2 consumer assumptions) | Self-test recipe diff against `expected-report.json` catches drift before merge |

## Sources

### Primary (HIGH confidence)

- **Repo files (read directly):**
  - `.claude/agents/excalidraw/excalidraw_specialist.md` — YAML frontmatter reference for `tools:` format and section ordering
  - `.claude/agents/excalidraw/scripts/excalidraw_validator.py` — JSON-loading + error/warning pattern to mirror
  - `.claude/agents/excalidraw/scripts/render_excalidraw.py` — image-path resolution order at lines 84-94
  - `.claude/agents/excalidraw/scripts/validate_and_render.sh` — pipeline that produces the PNG (and the `python` vs `python3` inconsistency to avoid)
  - `.claude/agents/excalidraw/.planning/phases/01-verifier-subagent/01-CONTEXT.md` — locked decisions D-01…D-16
  - `.claude/agents/excalidraw/.planning/codebase/CONVENTIONS.md` — Python and shell script conventions
- **Official Claude Code subagent docs:** [https://code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) — verified frontmatter schema, tool-allowlist semantics, multimodal capability inheritance

### Secondary (MEDIUM confidence)

- **DeepWiki Excalidraw codebase docs:**
  - [Element Types and Creation](https://deepwiki.com/excalidraw/excalidraw/3.1-element-binding-and-geometry) — arrow `points` local-coordinate semantics
  - [Element Binding System](https://deepwiki.com/excalidraw/excalidraw/3.2-element-binding-system) — `startBinding`/`endBinding` structure, `effectiveGap` formula
  - [Text Rendering and Font Management](https://deepwiki.com/excalidraw/excalidraw/5.3-text-elements-and-text-rendering) — Cascadia font metadata (unitsPerEm: 2048, ascender: 1900, descender: -480, lineHeight: 1.2; no published advance-width ratio)
  - [Font Management](https://deepwiki.com/excalidraw/excalidraw/5.2-font-management) — `fontFamily: 3` = Cascadia in Excalidraw's enum
- **Python emoji-detection references:**
  - [advertools emoji documentation](https://advertools.readthedocs.io/en/master/advertools.emoji.html)
  - [Kaggle: How to Create a Python Regex to Extract Emoji](https://www.kaggle.com/code/eliasdabbas/how-to-create-a-python-regex-to-extract-emoji)
  - [Wikipedia: Cascadia Code](https://en.wikipedia.org/wiki/Cascadia_Code) — confirms monospaced uniform character widths

### Tertiary (LOW confidence)

- **Microsoft Cascadia Code GitHub repo** ([https://github.com/microsoft/cascadia-code](https://github.com/microsoft/cascadia-code)) — documents Cascadia as monospaced but does not publish the exact em ratio. The 0.6 ratio in CONTEXT.md is empirical, not vendor-documented.

## Metadata

**Confidence breakdown:**
- Subagent file format & section ordering: HIGH — verified against official docs and existing `excalidraw_specialist.md`
- Structural-check Python helper shape: HIGH — mirrors `excalidraw_validator.py` pattern that already ships
- Arrow endpoint math (local→global coords, 8 px tolerance): MEDIUM — DeepWiki source-of-truth verified; actual `BASE_BINDING_GAP_ELBOW` constant not numerically extracted (CONTEXT.md fixes the tolerance at 8 px regardless)
- Monospace advance-width ratio: MEDIUM (empirical) — CONTEXT.md "specifics" section explicitly approves `0.6 × fontSize` as an empirical heuristic; visual check is the safety net
- Emoji codepoint ranges: HIGH — multiple Python references concur on `[\U0001F300-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF]`
- Multimodal `Read` in subagent context: HIGH (verified by repo precedent + official docs)
- Self-test recipe: HIGH — `bash` + `jq` are installed; `diff <(jq ...) <(jq ...)` is a standard idiom

**Research date:** 2026-05-21
**Valid until:** 2026-06-21 (30 days; stable domain — Excalidraw 0.17.3 is the locked render-pipeline version, Claude Code subagent format is the documented contract, Python stdlib emoji regex is stable since 3.3)
