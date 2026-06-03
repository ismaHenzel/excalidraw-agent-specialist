# CONVENTIONS

> Generated: 2026-05-20
> Scope: full repo

Coding and authoring conventions extracted from the source. These are the implicit rules
to follow when extending the agent, its KB, the renderer, or the icon library.

## Agent definition (`excalidraw_specialist.md`)

### YAML frontmatter

```yaml
---
name: excalidraw_specialist
description: <one-line capability statement>
tools: Read, Bash, Grep, Glob, mcp__excalidraw__read_me, mcp__excalidraw__create_view, mcp__excalidraw__export_to_excalidraw, mcp__excalidraw__save_checkpoint, mcp__excalidraw__read_checkpoint
---
```

- `tools:` is a single comma-separated line — built-in tools first, then MCP tools.
- Adding an MCP capability means appending here.

### Section ordering inside the agent body

XML-style section tags, in this order:

1. `<role>` — persona statement.
2. `<capabilities>` — bulleted, present tense.
3. `<asset_paths>` — relative-to-project paths only.
4. `<visual_standards>` — Architect's Precision rules, colour palette, text hierarchy,
   brand stroke colours, canonical JSON templates.
5. `<drawing_methodology>` — numbered principles.
6. `<style_principles>` — house-style conventions derived from `examples/`.
7. `<operational_mandates>` — numbered, imperative.

**Inlining policy:** Anything cross-cutting (palette, JSON templates, mandates) is inlined
in the agent prompt, not in `kb/`. Only pattern-specific geometry lives in `kb/*.md`.
This prevents the agent from needing to read multiple files just to apply baseline rules.

## Knowledge base files (`kb/*.md`)

### Filenames

- `kebab-case.md`.
- Slug must match the pattern name in `kb/README.md`'s index.
- One pattern per file; no compound files.

### Mandatory section order

```markdown
# Pattern: <Title-Cased Name>

<one-sentence what-it-is>

## When to use
…

## Geometry
…  (coordinates in multiples of 20)

## JSON skeleton
```json
[ … ]
```

## Notes
…
```

Optional sections:
- `## Variants` — colour / size swaps that don't change geometry.
- `## See in examples` — pointer to `../examples/<name>.png` and which detail to look at.

### Coordinate conventions

- **All coordinates are multiples of 20** (`kb/README.md:48`). This is the project-wide
  grid alignment. Patterns publish illustrative coordinates; callers translate the whole
  pattern rigidly when placing at a different origin (`kb/README.md:51`).
- Icon Block geometry (`kb/icon-block.md`): rectangle `180×80`, icon `24×24` at
  `(x+8, y+8)`, label at `(x+40, y+28)`.
- Text vertical centering rule: `y + (height - fontSize) / 2`, rounded to multiple of 4.

### JSON skeleton conventions

Every element in a kb skeleton must include:

- `"roughness": 0` (no hand-drawn effect).
- For text: `"fontFamily": 3` (monospace).
- For arrows: `"roundness": { "type": 2 }` with ≥ 3 points to form an elbow.
- For shape-with-label compositions: text is a *separate* element, never a `label`
  property on the shape. (The validator hard-fails the latter — see `excalidraw_validator.py:32-37`.)

### Updating the pattern index

When adding `kb/<new-pattern>.md`, add a row to the correct subtable in `kb/README.md`:

```markdown
| <Pattern> | `<new-pattern>.md` | <When to use, one short clause> |
```

The "Adding a new pattern" checklist at the bottom of `kb/README.md` is the source of
truth for this process.

## Icon library (`icons/`)

### Naming

- `lowercase_with_underscores.png`.
- **Brand technologies:** `<tool>_logo.png` is the canonical form
  (`databricks_logo.png`, `gitlab_logo.png`).
- **Functional / generic icons:** `<concept>_icon.png` (`database_icon.png`,
  `folder_icon.png`, `developer_icon.png`).
- **Variant suffixes** in order of preference:
  - Colour: `_black`, `_white`, `_blue`.
  - Numbered alternates: `_2`, `_3`, `_4`, `_5`.
- The agent's `Glob` discovery treats variants as equivalent — pick the variant whose
  contrast and palette best fit the diagram's container colour.

### When adding an icon

1. Prefer the canonical form `<tool>_logo.png` if a slot is free.
2. If adding a colour variant, follow `<tool>_logo_<color>.png`.
3. Use PNG with transparent background and a square aspect ratio — `24×24` is the
   default render size.
4. Do not delete numbered variants without checking whether existing diagrams reference
   them by `file_path`.

## Python scripts (`scripts/*.py`)

### `render_excalidraw.py` — production-shape

- **PEP 604 type hints** via `from __future__ import annotations` (`scripts/render_excalidraw.py:7`).
- Returns / parameters typed (`list[str]`, `tuple[float, float, float, float]`, `Path`).
- `pathlib.Path` over string paths.
- **`argparse`** for the CLI surface (`scripts/render_excalidraw.py:226-238`).
- **Errors to `stderr`** with `print(..., file=sys.stderr)` followed by `sys.exit(1)`.
- Module-level docstring with a usage line at top of the file.
- Defensive import of Playwright **after** validation, so JSON errors surface before
  import errors (`scripts/render_excalidraw.py:128-133`).

### `excalidraw_validator.py` — simpler script-shape

- No type hints, no `from __future__`.
- Raw `sys.argv` access instead of `argparse` (`scripts/excalidraw_validator.py:71-76`).
- **Report format:**
  - `[X]` — error
  - `[!]` — warning
  - `[✓]` — pass
- Single `validate_excalidraw(file_path)` function returns `bool`; main prints a banner
  and exits `0` on success, `1` on any error (warnings don't fail).

The two scripts are stylistically different. New scripts should follow whichever shape
matches their role: the renderer's typed-CLI shape for production-grade tools, the
validator's terse shape for one-off linters.

## Shell scripts (`scripts/*.sh`)

- Shebang: `#!/bin/bash` (always; never `sh`).
- `set -e` on every script that runs multi-step operations.
- Phase markers via `echo "--- Phase N: <Name> ---"` so the user can see progress.
- `SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"` idiom to resolve the
  script's own directory.
- Exit codes propagate: capture in `VALIDATION_EXIT=$?`, then `exit $VALIDATION_EXIT` on
  the wrapper.
- Helpful `Usage:` line printed when called with no args.

## Markdown documentation

### Agent docs (`README.md`)

- Top-level H1 with a one-paragraph summary.
- Folder layout in a fenced code block.
- Markdown tables for any two-column reference (palette, brand strokes, examples).
- Closing horizontal rule `---` then an italic provenance line
  (`*Adapted from the Gemini-CLI Excalidraw Visual Architect; restructured for Claude Code.*`).

### Pattern docs (`kb/*.md`)

- H1 title in the form `# Pattern: <Name>`.
- Geometry is always followed by an ASCII / text diagram showing anchor points before the
  JSON skeleton.

## Excalidraw JSON rules (enforced by the validator)

Codified in `scripts/excalidraw_validator.py`:

| Rule | Severity | Source |
|---|---|---|
| `type` must equal `"excalidraw"` | Error | line 21-22 |
| `version` must be present | Error | line 23-24 |
| `elements` array must be present | Error | line 25-26 |
| `rectangle`/`ellipse`/`diamond` MUST NOT carry a `label` field | Error | line 32-37 |
| Diagrams with `>2` elements should have at least one `text` element | Warning | line 40-42 |
| Text `strokeColor` should be `#1e1e1e`, `#000000`, or `#000` | Warning | line 45-52 |

`scripts/render_excalidraw.py` adds (at render time):

| Rule | Severity |
|---|---|
| `type == "excalidraw"` | Error (refuse to render) |
| `elements` is a list and non-empty | Error |
| Image `file_path` that fails to resolve | Warning printed to stderr; render continues with broken refs |

## Related

- [[ARCHITECTURE.md]] — the visual standards live in the agent prompt by design.
- [[TESTING.md]] — the validator is the convention-enforcement mechanism.
- [[STRUCTURE.md]] — where to put new files.
