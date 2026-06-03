# Phase 1: Verifier Subagent - Pattern Map

**Mapped:** 2026-05-21
**Files analyzed:** 9 new files (1 subagent .md, 1 Python helper, 6 fixture files, 1 optional shell script)
**Analogs found:** 9 / 9 (every new file has a strong in-repo analog)

## File Classification

| New / Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `excalidraw_verifier.md` | subagent prompt (Claude Code subagent definition) | LLM orchestration (prompt → multimodal `Read` → `Bash` → `Write`) | `excalidraw_specialist.md` | exact (same file type, same plugin dir, same YAML frontmatter schema) |
| `scripts/verifier_structural.py` | utility / one-off linter helper | stdin-path → stdout JSON array (exit 0 always) | `scripts/excalidraw_validator.py` (primary, shape) + `scripts/render_excalidraw.py:69-118` (image-path resolution sub-pattern) | role-match (linter shape matches, but output format = JSON array instead of human-readable banners) |
| `fixtures/verifier/good/good.excalidraw` | fixture data (well-formed Excalidraw JSON) | static asset | `databricks_orchestration_pipeline_star_schema_gitlab.excalidraw` (element shape) + `kb/icon-block.md` (canonical icon-block JSON skeleton) | exact (same JSON schema, smaller in element count) |
| `fixtures/verifier/good/good.png` | fixture data (rendered PNG) | static asset (produced once by `validate_and_render.sh`) | `examples/*.png` (file format, render pipeline output) | exact |
| `fixtures/verifier/good/expected-report.json` | fixture data (expected verifier output) | static asset (committed) | **none in repo** — first JSON-report fixture in the codebase; schema is locked by CONTEXT.md D-03 | no analog (schema-only reference) |
| `fixtures/verifier/raw-emoji/raw-emoji.{excalidraw,png}` + `expected-report.json` | fixture data (defect case: raw emoji codepoint) | static asset | `databricks_orchestration_pipeline_star_schema_gitlab.excalidraw` (element shape; mutate one text element) | role-match (intentional defect injection has no in-repo precedent) |
| `fixtures/verifier/text-overflow/text-overflow.{excalidraw,png}` + `expected-report.json` | fixture data (defect case: oversized text in undersized container) | static asset | `kb/icon-block.md` (canonical 180×80 rectangle to violate) | role-match |
| `scripts/verifier_self_test.sh` (optional polish) | shell test runner / orchestration wrapper | bash + `jq` + `diff` | `scripts/validate_and_render.sh` (bash wrapper convention) + `scripts/render_docker.sh` (`set -e`, `SCRIPT_DIR` idiom) | role-match (orchestration wrapper, but exits with `$FAIL` count rather than first-error short-circuit) |

## Pattern Assignments

### `excalidraw_verifier.md` (subagent prompt, LLM orchestration)

**Analog:** `excalidraw_specialist.md`

**Imports / YAML frontmatter pattern** (`excalidraw_specialist.md:1-5`):
```yaml
---
name: excalidraw_specialist
description: Expert AI visual architect specialized in creating professional Excalidraw diagrams with architectural precision, elbow arrows, and brand-consistent assets.
tools: Read, Bash, Grep, Glob, mcp__excalidraw__read_me, mcp__excalidraw__create_view, mcp__excalidraw__export_to_excalidraw, mcp__excalidraw__save_checkpoint, mcp__excalidraw__read_checkpoint
---
```

**Copy and adapt:**
- Keep the `---` fence syntax exactly.
- Replace `name:` value with `excalidraw_verifier` (lowercase + underscore — matches `excalidraw_specialist` convention).
- Replace `description:` with a *when-to-delegate* statement per the verified frontmatter docs (e.g., research §Code Examples line 536).
- Replace `tools:` with exactly the D-12 allowlist: `Read, Glob, Grep, Bash, Write` — **no MCP tools** (verifier has no canvas-side responsibilities; specialist's MCP tools do NOT apply).

**Section-ordering pattern** (`excalidraw_specialist.md:7-151` → XML-tag sections in fixed order):
- specialist uses: `<role>` → `<capabilities>` → `<asset_paths>` → `<visual_standards>` → `<drawing_methodology>` → `<style_principles>` → `<operational_mandates>`
- **Verifier-appropriate adaptation** (per RESEARCH.md §Subagent File Format Field Notes — verifier is *not* a generator, so the section names differ):
  - `<role>` — verifier persona ("Static + visual fresh-eyes verifier")
  - `<inputs>` — single absolute path to `.excalidraw`; derives sibling `.png`
  - `<operational_sequence>` — the 7 numbered steps (RESEARCH.md §Pattern 2)
  - `<output_contract>` — schema + 1 passing example + 1 failing example
  - `<failure_modes>` — terminal "always emit a report" invariant (Pitfall 5)
- The XML-tag-section convention itself is non-negotiable (CONVENTIONS.md:26).

**Relative-asset-path pattern** (`excalidraw_specialist.md:21-28`):
```markdown
All paths are **relative to the project working directory** (where you were invoked). This keeps the agent portable across any project that vendors the plugin under its `.claude/` folder.

- **Icons:** `.claude/agents/excalidraw/icons/` — technology and brand logos. Use `Glob` to discover what's available.
```
**Apply to verifier:** Same prefix convention. The verifier's `<inputs>` section must specify that the caller passes an absolute path (D-13) AND that the helper script is at `.claude/agents/excalidraw/scripts/verifier_structural.py` (relative invocation).

**Operational-mandate pattern** (`excalidraw_specialist.md:142-151`):
```markdown
<operational_mandates>
1. **Pattern First:** Before drawing, decompose the request into patterns from `kb/README.md`...
2. **Reference the Examples:** Before producing a diagram, Read the relevant PNG(s)...
[etc., 8 numbered imperatives]
</operational_mandates>
```
**Apply to verifier `<operational_sequence>`:** Numbered, imperative, terse — same shape. Each step is a verb-first command, not a description. Research §Pattern 2 enumerates the seven steps verbatim.

**Multimodal-Read precedent** (`excalidraw_specialist.md:144`): operational mandate #2 already uses `Read` on `examples/*.png` to consume image data. This confirms the verifier's Step 3 (Read the rendered PNG) works without any special syntax — the model's multimodal capability is inherited.

**Pitfall the analog reveals (DO NOT copy):**
- The specialist's `<visual_standards>` section embeds the Architect's Precision rules (roughness 0, fontFamily 3, elbow arrows). The verifier consumes these rules but **must not re-author them inline** — instead, reference them by name in check identifiers (`roughness_nonzero`, `fontfamily_nonmonospace`, `arrow_missing_elbow_roundness`). Per D-06, the verifier extends — does not duplicate — existing rule sources.
- The specialist's `tools:` line ends with `mcp__excalidraw__*` MCP tools (`excalidraw_specialist.md:4`). The verifier must NOT inherit any of these. D-12 explicitly restricts the verifier to `Read, Glob, Grep, Bash, Write`.

---

### `scripts/verifier_structural.py` (utility / one-off linter, JSON-array stdout)

**Primary analog:** `scripts/excalidraw_validator.py` (script shape, terse style)
**Secondary analog:** `scripts/render_excalidraw.py:69-118` (image-path resolution sub-pattern, ONLY)

**Imports pattern** (`scripts/excalidraw_validator.py:1-3`):
```python
import json
import sys
import os
```
**Apply to verifier:** Add `re` (for emoji regex), `pathlib.Path` (for path resolution), and `datetime` is NOT needed here (the subagent stamps `checked_at`, not the helper). Keep imports flat at module top; **do NOT add `from __future__ import annotations`** — the validator deliberately omits it (CONVENTIONS.md:144 "no `from __future__`"). Mirror the validator's terse shape, not the renderer's typed shape.

**CLI entrypoint pattern** (`scripts/excalidraw_validator.py:71-77`):
```python
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python excalidraw_validator.py <path_to_excalidraw_file>")
        sys.exit(1)

    success = validate_excalidraw(sys.argv[1])
    sys.exit(0 if success else 1)
```
**Apply to verifier (with D-14 modification):**
- Same `sys.argv[1]` raw access (no `argparse` — that's renderer-shape per CONVENTIONS.md:145).
- **Critical divergence from analog:** Exit `0` ALWAYS (D-14). Errors emit a `verifier_internal_error` issue object to stdout and still exit 0. The validator's `0 if success else 1` convention is REPLACED.
- **Critical divergence from analog:** stdout is a JSON array (`print(json.dumps(issues))`), NOT human-readable banners. The `[X]`/`[!]`/`[✓]` vocabulary from `excalidraw_validator.py:58-63` is replaced by the structured `severity: "error" | "warning"` strings (CONVENTIONS.md:146-150 documents the two-tier hierarchy already; verifier just encodes it differently).

**JSON-load + try/except pattern** (`scripts/excalidraw_validator.py:6-15`):
```python
def validate_excalidraw(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return False

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not a valid JSON file.")
        return False
```
**Apply to verifier:**
- Same `os.path.exists` + `open` + `json.load` + `except json.JSONDecodeError` chain.
- Replace each `return False` with: emit a single-issue array `[{ "check": "verifier_internal_error", ... }]` to stdout, then `sys.exit(0)`. This satisfies D-14 (always exit 0) AND the always-produce-a-report invariant (Pitfall 5).

**Element iteration + per-element issue accumulation pattern** (`scripts/excalidraw_validator.py:28-37`):
```python
elements = data.get("elements", [])

# 2. Check for 'label' property in shapes
shapes_with_labels = []
for el in elements:
    if el.get("type") in ["rectangle", "ellipse", "diamond"] and "label" in el:
        shapes_with_labels.append(el.get("id", "unknown"))

if shapes_with_labels:
    errors.append(f"Found 'label' property in shapes: {', '.join(shapes_with_labels)}...")
```
**Apply to verifier (with per-element granularity):**
- Same `data.get("elements", [])` + `for el in elements` + `el.get("type")` + `el.get("id", "unknown")` pattern.
- **Divergence:** the validator aggregates IDs into one error message; the verifier emits **one issue per offending element** (D-11: every fix references an `element_id`). So the per-check function returns a `list[issue_dict]`, not a single error string.

**Image-path resolution pattern** (`scripts/render_excalidraw.py:69-94`):
```python
def embed_images(data: dict, excalidraw_dir: Path):
    """Embed local images from 'file_path' into the 'files' object as Base64.

    Relative image paths are resolved in this order:
      1. Against the input .excalidraw file's directory.
      2. Against $EXCALIDRAW_ASSETS_DIR (used by render_docker.sh to expose the
         agent's icons/ folder regardless of where the input file lives).
    """
    # ...
    assets_dir_env = os.environ.get("EXCALIDRAW_ASSETS_DIR")
    assets_dir = Path(assets_dir_env) if assets_dir_env else None

    elements = data.get("elements", [])
    for el in elements:
        if el.get("type") == "image" and "file_path" in el:
            raw_path = Path(el["file_path"])
            if raw_path.is_absolute():
                file_path = raw_path
            else:
                file_path = excalidraw_dir / raw_path
                if not file_path.exists() and assets_dir is not None:
                    fallback = assets_dir / raw_path
                    if fallback.exists():
                        file_path = fallback
```
**Apply to verifier's `image_path_unresolvable` check:**
- **Mirror exactly** the absolute → input-dir → `EXCALIDRAW_ASSETS_DIR` fallback order. RESEARCH.md "Don't Hand-Roll" table is explicit: diverging from this order means the verifier flags paths the renderer would have loaded (or vice versa) — consistency with the renderer IS the contract.
- **Divergence:** the renderer logs a warning to stderr and continues; the verifier returns an `error`-severity issue object (D-04: image path unresolvable is an ERROR for the verifier). It does NOT print to stderr — only stdout JSON.

**Error/warning vocabulary pattern** (`scripts/excalidraw_validator.py:55-67` + CONVENTIONS.md:146-150):
- Validator: `[X]` = error, `[!]` = warning, `[✓]` = pass — printed to a banner.
- Verifier: `severity: "error"` | `severity: "warning"` — encoded in each issue dict (D-03 schema). Same two-tier hierarchy, machine-parseable encoding.

**Pitfalls the analog reveals (DO NOT copy):**
- **D-06 explicit constraint:** the validator's three rules (`label` property on shapes, `version` metadata, low-contrast text strokeColor) are ALREADY enforced by `validate_and_render.sh` pre-render. The verifier MUST NOT duplicate them. The verifier covers a disjoint rule set (the 4 errors + 4 warnings in D-04/D-05).
- **Bare `python` vs `python3`:** `scripts/validate_and_render.sh:14` invokes `python "$SCRIPT_DIR/excalidraw_validator.py"` (bare `python`). RESEARCH.md Pitfall 6 + CONCERNS.md #7 flag this as a real inconsistency. The verifier's Bash invocation must use `python3` — do not propagate the bug.
- **`pathlib.Path` mixing:** the renderer uses `pathlib.Path` throughout; the validator uses `os.path.exists` + plain strings. The verifier should follow the validator's terser style for filesystem checks BUT use `pathlib.Path` for the image-path-resolution sub-pattern (to mirror the renderer's logic byte-for-byte). Mixing the two within one file is acceptable because the image-resolution block is a verbatim port of the renderer's logic.

---

### `fixtures/verifier/good/good.excalidraw` (fixture data, well-formed Excalidraw JSON)

**Primary analog:** `databricks_orchestration_pipeline_star_schema_gitlab.excalidraw` (real in-repo Excalidraw file, element shape reference)
**Secondary analog:** `kb/icon-block.md` (canonical icon-block JSON skeleton)

**Top-level envelope pattern** (`databricks_orchestration_pipeline_star_schema_gitlab.excalidraw:1-5`):
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
```
**Apply to fixture:** Same envelope. `type`, `version`, `elements` are REQUIRED (enforced by `excalidraw_validator.py:21-26`). `source` is conventional.

**Text element shape** (`databricks_orchestration_pipeline_star_schema_gitlab.excalidraw:6-42`):
```json
{
  "id": "title",
  "type": "text",
  "x": 480,
  "y": 10,
  "width": 849,
  "height": 30,
  "angle": 0,
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  ...
  "text": "Databricks Orchestration — Star Schema, Versioned in GitLab",
  "fontSize": 24,
  "fontFamily": 3,
  ...
}
```
**Apply to fixture:** Mirror the schema. For the *good* fixture, keep `roughness: 0`, `fontFamily: 3`, and short text that fits its bounding box. Use the canonical icon-block geometry from `kb/icon-block.md` (rectangle `180×80`, icon `24×24` at `(x+8, y+8)`, label at `(x+40, y+28)`).

**Arrow element shape** (`databricks_orchestration_pipeline_star_schema_gitlab.excalidraw:508-552`):
```json
{
  "id": "a_repo_mr",
  "type": "arrow",
  "x": 280,
  "y": 220,
  ...
  "roughness": 0,
  ...
  "roundness": {
    "type": 2
  },
  ...
  "points": [
    [0, 0],
    [20, 0]
  ],
  ...
  "endArrowhead": "arrow",
  "elbowed": false
}
```
**Apply to fixture (good case):** For the good fixture's arrow to pass the verifier's `arrow_points_too_few` warning check, use **≥ 3 points** (e.g., `[[0,0], [60,0], [60,40]]`) — the in-repo example uses 2 points, which is a *real* style-warning case the verifier would flag. The good fixture must be defect-free.

**Image element shape** (`databricks_orchestration_pipeline_star_schema_gitlab.excalidraw:6079-6112`):
```json
{
  "id": "gl_brand",
  "type": "image",
  "x": 56,
  "y": 94,
  "width": 32,
  "height": 32,
  ...
  "roughness": 0,
  ...
  "status": "saved",
  "fileId": null,
  "scale": [1, 1],
  "file_path": "icons/gitlab_logo.png"
}
```
**Apply to fixture (good case):** Use a real path that resolves under `.claude/agents/excalidraw/icons/`. Use `icons/databricks_logo.png` or similar (verify against the actual `icons/` listing). The `file_path` field is the verifier's input for `image_path_unresolvable`.

**Rectangle element shape** (canonical 180×80 from `kb/icon-block.md:24-43`):
```json
{
  "type": "rectangle",
  "x": 200, "y": 200, "width": 180, "height": 80,
  "backgroundColor": "#3b82f6", "strokeColor": "#1e3a5f",
  "roughness": 0, "roundness": { "type": 3 }
}
```
**Apply to fixture:** Use this exact geometry for the good fixture so the text-overflow heuristic has a known good case. For the text-overflow fixture, shrink width to 180 but place text of ~280-px estimated width inside.

---

### `fixtures/verifier/raw-emoji/raw-emoji.excalidraw` (fixture data, defect: raw emoji)

**Analog:** Same as `good.excalidraw`, with one text element mutated.

**Mutation pattern:** Take a passing text element and change its `text` field to `"✅"` (or any single character in `U+1F300-U+1FAFF` / `U+2600-U+27BF`). Keep `fontFamily: 3`. The verifier's `raw_emoji_in_text` check (D-04) must flag it. Expected report contains exactly one issue: `check: "raw_emoji_in_text"`, `severity: "error"`, `element_id: <the text element id>`, `suggested_fix: "Replace text element id: <id> (raw emoji U+2705) with an image element pointing to .claude/agents/excalidraw/icons/success_icon.png."` (using the static `EMOJI_TO_ICON` table per RESEARCH.md §Pattern 1).

---

### `fixtures/verifier/text-overflow/text-overflow.excalidraw` (fixture data, defect: overflow)

**Analog:** Same as `good.excalidraw`, with one rectangle shrunk OR one text widened.

**Mutation pattern:** Inside the canonical 180×80 rectangle (kb/icon-block.md geometry), place a `text` element of ~23 characters at `fontSize: 20` so estimated width = `23 × 0.6 × 20 = 276 px` > `180 px` container width. The verifier's `text_overflow_static` check fires; expected report contains one error-severity issue referencing the text element id and suggesting either "increase rectangle width to ≥ ~280" or "shorten label".

---

### `fixtures/verifier/*/expected-report.json` (fixture data, expected verifier output)

**Analog:** **none in repo** — first JSON-report fixture.

**Schema source:** CONTEXT.md D-03 (locked) + RESEARCH.md §User Constraints D-03.

**Self-test diff-ignore convention** (RESEARCH.md §Open Questions #3, §Self-Test Recipe):
Three fields vary by environment and MUST be excluded from the fixture diff:
- `checked_at` — timestamp (always changes)
- `source` — absolute path to `.excalidraw` (varies by checkout location)
- `png` — absolute path to PNG (varies by checkout location)

`expected-report.json` files MAY ship with placeholder strings or omit these three fields entirely; the diff command must `jq 'del(.checked_at, .source, .png)'` on both sides.

**Concrete example** for `good/expected-report.json`:
```json
{
  "passed": true,
  "checked_at": "<IGNORED-IN-DIFF>",
  "source": "<IGNORED-IN-DIFF>",
  "png": "<IGNORED-IN-DIFF>",
  "issues": []
}
```

---

### `scripts/verifier_self_test.sh` (optional polish, shell test runner)

**Primary analog:** `scripts/validate_and_render.sh`
**Secondary analog:** `scripts/render_docker.sh` (idioms: `set -e`, `SCRIPT_DIR`, stderr usage)

**Shebang + arg-check pattern** (`scripts/validate_and_render.sh:1-9`):
```bash
#!/bin/bash
# Master script for Excalidraw Validation and Rendering

EXCALIDRAW_FILE="$1"

if [ -z "$EXCALIDRAW_FILE" ]; then
    echo "Usage: bash scripts/validate_and_render.sh <path_to_file.excalidraw>"
    exit 1
fi
```
**Apply to verifier_self_test:** Same shebang. The self-test takes either ZERO args (runs all 3 fixtures) or ONE fixture name (`good` | `raw-emoji` | `text-overflow`). Print a `Usage:` line if an unrecognized arg appears.

**SCRIPT_DIR idiom** (`scripts/render_docker.sh:10` and CONVENTIONS.md:162):
```bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
```
**Apply:** Mandatory by convention. Resolve `FIXTURES_DIR="$( cd "$SCRIPT_DIR/.." && pwd )/fixtures/verifier"` from there.

**Phase-marker + exit-propagation pattern** (`scripts/validate_and_render.sh:13-23`):
```bash
echo "--- Phase 1: Technical Validation ---"
python "$SCRIPT_DIR/excalidraw_validator.py" "$EXCALIDRAW_FILE"
VALIDATION_EXIT=$?

if [ $VALIDATION_EXIT -ne 0 ]; then
    echo "ERROR: Technical validation failed. Please fix the JSON before rendering."
    exit $VALIDATION_EXIT
fi
```
**Apply to verifier_self_test:** Echo `--- Fixture: <name> ---` per iteration. Capture per-fixture exit via diff (`if [ -z "$DIFF" ]; then PASS=...; else FAIL=...; fi`). Final exit is `$FAIL` count (per RESEARCH.md §Self-Test Recipe — does NOT short-circuit on first failure; accumulates).

**`set -e` policy** (`scripts/render_docker.sh:8` + CONVENTIONS.md:160):
**Divergence from the analog:** `validate_and_render.sh` does NOT use `set -e` (it does manual `$?` checks). The verifier_self_test should ALSO not use `set -e` because it must continue past per-fixture failures to accumulate the final count. Match `validate_and_render.sh`'s shape exactly here, NOT `render_docker.sh`'s.

**Pitfalls the analog reveals (DO NOT copy):**
- `validate_and_render.sh:14` invokes `python` (bare) — see Pitfall 6 above. Use `python3` in the verifier's Bash steps.
- `validate_and_render.sh:30` prints a free-text instruction to the user (`"Now use 'read_file' on the .png..."`). The self-test should NOT print such instructions — its only output is per-fixture `PASS`/`FAIL` lines + a summary line. Structured, parseable output.

---

## Shared Patterns

### YAML Frontmatter (subagent definition)

**Source:** `excalidraw_specialist.md:1-5`
**Apply to:** `excalidraw_verifier.md` (the only subagent file in this phase)
```yaml
---
name: <lowercase_underscored_name>
description: <one-line capability statement: when to delegate>
tools: <comma-separated single line; built-ins first, then MCP if any>
---
```
**Rule:** `tools:` is allowlist semantics. Subagent can ONLY use listed tools. D-12 locks the verifier's list to `Read, Glob, Grep, Bash, Write`.

### XML-tag body sections (subagent definition)

**Source:** `excalidraw_specialist.md:7-151` (specialist's seven sections) + CONVENTIONS.md:26-35 (section-ordering doctrine)
**Apply to:** `excalidraw_verifier.md` body
**Rule:** Body is divided into XML-tagged sections in a fixed order. For a *verifier* (not generator), the appropriate sections are `<role>`, `<inputs>`, `<operational_sequence>`, `<output_contract>`, `<failure_modes>`. The XML-tag wrapping itself is the non-negotiable part; section names follow the role.

### Python helper script shape (one-off linter)

**Source:** `scripts/excalidraw_validator.py` (entire file; especially:1-3 imports, :5-15 JSON-load+except, :71-77 CLI entrypoint) + CONVENTIONS.md:142-155 (terse-shape doctrine)
**Apply to:** `scripts/verifier_structural.py`
**Rule:**
- No `from __future__ import annotations`; no type hints; no `argparse`.
- Raw `sys.argv[1]` access.
- Single-function-per-concern with a simple `main()`.
- Module-level constants for tuning knobs (`MONOSPACE_ADVANCE_RATIO = 0.6`, `ENDPOINT_TOLERANCE_PX = 8`, `EMOJI_RE`).
- Filesystem checks via `os.path.exists` + `open()`; reserve `pathlib.Path` for the verbatim port of the renderer's image-path-resolution block.
- **Divergence from analog:** stdout is `json.dumps(issues)` (JSON array); exit code is ALWAYS 0 (D-14).

### Image-path resolution order (CRITICAL — must mirror renderer)

**Source:** `scripts/render_excalidraw.py:69-94`
**Apply to:** `scripts/verifier_structural.py` — `image_path_unresolvable` check ONLY
**Rule:** Absolute → input-dir-relative → `$EXCALIDRAW_ASSETS_DIR`-relative. The verifier's job is to flag paths the renderer cannot load; diverging from the renderer's resolution order produces false positives or false negatives. Treat lines 69-94 as a verbatim porting reference.

### Severity vocabulary

**Source:** `scripts/excalidraw_validator.py:55-67` (`[X]` / `[!]` / `[✓]`) + CONVENTIONS.md:146-150
**Apply to:** all verifier output (helper stdout + subagent report)
**Rule:** Two-tier hierarchy: `error` (was `[X]`) and `warning` (was `[!]`). No `info` for v1 (CONTEXT.md "Claude's Discretion"). `passed = true` iff every issue is `warning` OR list is empty (D-03 + CONTEXT.md "specifics").

### Element-iteration idiom

**Source:** `scripts/excalidraw_validator.py:28-37` (`elements = data.get("elements", [])` + `for el in elements:` + `el.get("type")` + `el.get("id", "unknown")`)
**Apply to:** every check function in `scripts/verifier_structural.py`
**Rule:** Defensive `.get()` access throughout — never assume keys exist. Default `id` to `"unknown"`. **Divergence:** per-element issues, not aggregated.

### Bash wrapper convention

**Source:** `scripts/validate_and_render.sh` (full file) + `scripts/render_docker.sh:8-10` + CONVENTIONS.md:158-166
**Apply to:** `scripts/verifier_self_test.sh` (optional polish)
**Rule:** `#!/bin/bash`; `SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"`; `Usage:` line on missing args; phase markers via `echo "--- Phase N: ... ---"`. **Divergence from `render_docker.sh`:** NO `set -e` for the self-test (must accumulate per-fixture failures, not short-circuit).

### Fixture path convention

**Source:** No exact in-repo analog (first time committing fixtures), but RESEARCH.md §Recommended Project Structure + CONTEXT.md D-15
**Apply to:** all six fixture files
**Rule:** `.claude/agents/excalidraw/fixtures/verifier/<case>/<case>.{excalidraw,png}` + `expected-report.json` sibling. The `<case>` directory name and the file basenames match (`good/good.excalidraw`, etc.). PNG is pre-rendered at fixture-author time via `validate_and_render.sh`; the verifier never re-renders.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| `fixtures/verifier/*/expected-report.json` | fixture data (committed expected verifier output) | static asset | First JSON-report fixture in the repo. Schema is defined by CONTEXT.md D-03 (locked); diff-ignore rule (`checked_at`, `source`, `png`) is defined by RESEARCH.md §Open Questions #3. Use these spec documents directly — no in-repo file to copy from. |

Files in this category should be implemented from the schema in D-03, with the planner referencing the RESEARCH.md self-test recipe for the diff rule.

---

## Metadata

**Analog search scope:**
- `/home/linuxzinho/coding/excaildraw-claude/.claude/agents/excalidraw/` (plugin directory: subagent .md, scripts/, kb/, icons/, examples/)
- `/home/linuxzinho/coding/excaildraw-claude/` (project root, for one real-world `.excalidraw` example file)
- `/home/linuxzinho/coding/excaildraw-claude/.claude/agents/excalidraw/.planning/codebase/` (CONVENTIONS.md, STRUCTURE.md for conventions cross-reference)

**Files scanned (read in full or via targeted Read offsets):**
- `excalidraw_specialist.md` (151 lines, full read)
- `scripts/excalidraw_validator.py` (78 lines, full read)
- `scripts/render_excalidraw.py` (243 lines, full read)
- `scripts/validate_and_render.sh` (34 lines, full read)
- `scripts/render_docker.sh` (48 lines, full read)
- `scripts/pyproject.toml` (7 lines, full read)
- `kb/icon-block.md` (55 lines, full read)
- `kb/feedback-loop.md` (68 lines, full read)
- `.planning/codebase/CONVENTIONS.md` (210 lines, full read)
- `.planning/phases/01-verifier-subagent/01-CONTEXT.md` (180 lines, full read — required reading)
- `.planning/phases/01-verifier-subagent/01-RESEARCH.md` (793 lines, full read — required reading)
- `databricks_orchestration_pipeline_star_schema_gitlab.excalidraw` (only three targeted Read windows: lines 1-100, 505-575, 6075-6120 — large file, sampled for element-shape examples only)

**Pattern extraction date:** 2026-05-21
**Pattern map valid through:** 2026-06-21 (no repo refactors expected; subagent format + validator shape are stable contracts)
