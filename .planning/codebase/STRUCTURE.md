# STRUCTURE

> Generated: 2026-05-20
> Scope: full repo

## Directory layout

```
.claude/agents/excalidraw/
├── excalidraw_specialist.md   ← Agent definition: YAML frontmatter, role,
│                                visual standards, color palette, JSON
│                                templates, drawing methodology, mandates
├── README.md                  ← Install/usage/extend the plugin
├── kb/                        ← Layout-pattern knowledge base (13 patterns)
│   ├── README.md              ← Pattern index + reference-example index
│   ├── group-container.md     ← Macro: bordered scope with brand identity
│   ├── multi-zoom-overview.md ← Macro: multi-facet system overview
│   ├── linear-pipeline.md     ← Flow: sequential L-to-R steps
│   ├── fan-out.md             ← Flow: one source, N destinations
│   ├── convergence.md         ← Flow: N sources, one sink
│   ├── task-list.md           ← Flow: vertical stack with side I/O
│   ├── feedback-loop.md       ← Flow: retry/restart arrows around forward flow
│   ├── timeline.md            ← Flow: events along a horizontal time axis
│   ├── decision-branch.md     ← Decision: diamond with ≥ 2 labelled outcomes
│   ├── decision-marker.md     ← Decision: inline ✗/✓ binary gate
│   ├── icon-block.md          ← Structure: atomic node (rectangle + icon + label)
│   ├── tree-hierarchy.md      ← Structure: folder / catalog / namespace tree
│   └── evidence-card.md       ← Structure: card with real data / metrics
├── examples/                  ← Canonical PNG references (visual ground truth)
│   ├── governance.png         ← Nested containers · feedback-loop · ✗/✓
│   ├── orchestrator.png       ← Tree on left · colour-coded fan-out · convergence
│   ├── refresh_bi.png         ← Vertical task list · side I/O · async badge
│   └── dlt.png                ← Multi-zoom · evidence cards · persona example
├── icons/                     ← 73 brand / tech logo PNGs
└── scripts/                   ← Validation + rendering helpers
    ├── excalidraw_validator.py  ← Static lint of .excalidraw JSON
    ├── render_excalidraw.py     ← Playwright-driven PNG renderer
    ├── render_template.html     ← Browser-side: imports Excalidraw lib + exportToSvg
    ├── render_docker.sh         ← Wrapper: build image if needed, mount + run
    ├── validate_and_render.sh   ← Phase orchestrator: validate → render → visual
    ├── Dockerfile               ← Playwright Python base + uv-managed deps
    ├── pyproject.toml           ← Python project manifest
    └── uv.lock                  ← Frozen dependency lockfile
```

## Per-directory detail

### Root (`./`)

| File | Purpose | Notes |
|---|---|---|
| `excalidraw_specialist.md` | Subagent definition | YAML frontmatter declares `name`, `description`, and `tools` (Read, Bash, Grep, Glob, 5 × `mcp__excalidraw__*`). Body is the full system prompt. |
| `README.md` | Human-facing install + usage docs | Authoritative for install / MCP registration / extension |

### `kb/` — Layout pattern knowledge base

- **Naming:** `kebab-case.md`. Slug matches the pattern name in `kb/README.md`.
- **Categories** (from `kb/README.md`):
  - **Macro** (composition / scope) — `group-container`, `multi-zoom-overview`
  - **Flow** (control / data) — `linear-pipeline`, `fan-out`, `convergence`, `task-list`, `feedback-loop`, `timeline`
  - **Decision** — `decision-branch`, `decision-marker`
  - **Structure** (atomic / reference) — `icon-block`, `tree-hierarchy`, `evidence-card`
- **Mandatory sections per pattern file:** `When` → `Geometry` → `JSON skeleton` → `Notes`,
  with optional `Variants` and `See in examples`. See [[CONVENTIONS.md]].
- **Index file:** `kb/README.md` carries the pattern table and the reference-example table.

### `examples/` — Canonical visual references

- **Naming:** `<diagram-slug>.png`.
- **Role:** treated as visual ground truth by the agent (`excalidraw_specialist.md:26`,
  operational mandate #2). The agent `Read`s the PNG before drawing.
- **Index:** each row is also referenced in `kb/README.md`'s reference-example table,
  mapped to the patterns it demonstrates.

### `icons/` — Brand / tech logo library

- **Naming convention:** `lowercase_with_underscores.png`. Variant suffixes:
  - `_black`, `_white` — colour variants
  - `_2`, `_3`, `_4`, `_5` — alternate versions of the same logo
  - `_logo` — base form for branded technologies
  - `_icon` — generic / functional icons (e.g. `database_icon`, `folder_icon`)
- **Examples:**
  - `databricks_logo.png`, `databricks_logo_black.png`, `databricks_logo_2.png` … `_5.png`
  - `apache_airflow_logo.png`, `apache_airflow_full.png`, `apache_airflow_full_2.png`
  - `great_expectations_logo.png`, `great_expectations_logo_black.png`, `great_expectations_logo_white.png`
- **Total:** 73 PNG files (mostly logos; a handful of generic glyphs and a few
  out-of-place "diagram" PNGs — see [[CONCERNS.md]]).
- **Discovery:** agent uses `Glob` to enumerate (`excalidraw_specialist.md:148`).

### `scripts/` — Render pipeline

| File | Lang | Role |
|---|---|---|
| `excalidraw_validator.py` | Python | Lints `.excalidraw` JSON — metadata, banned `label` field, contrast warnings |
| `render_excalidraw.py` | Python | Playwright + Chromium renderer; embeds images, computes bounding box, screenshots SVG |
| `render_template.html` | HTML / JS | Loaded into Chromium; ES-imports `@excalidraw/excalidraw@0.17.3` from `esm.sh`, exposes `window.renderDiagram` |
| `render_docker.sh` | Bash | Build image on demand, mount input dir + agent dir, run container |
| `validate_and_render.sh` | Bash | 3-phase pipeline: validate → render → instruct visual review |
| `Dockerfile` | — | `mcr.microsoft.com/playwright/python:v1.49.1-jammy` base + uv binary from `ghcr.io/astral-sh/uv:latest` |
| `pyproject.toml` | TOML | `name = "excalidraw-render"`, `requires-python = ">=3.11"`, `dependencies = ["playwright>=1.40.0"]` |
| `uv.lock` | TOML | Frozen lockfile (resolved Playwright 1.59.0) |

## Where to add new code

| Task | Where | What to update |
|---|---|---|
| Add a new layout pattern | `kb/<pattern-slug>.md` | (1) pattern file with the 4 mandatory sections, (2) row in `kb/README.md` Index, (3) optional `kb/<slug>.png` |
| Add a new brand / tool icon | `icons/<tool>_logo.png` | None required — agent discovers via `Glob`. Match existing variant suffix conventions if multiple |
| Add a new reference example | `examples/<name>.png` | Add a row in `kb/README.md`'s reference-example table mapping to the patterns it demonstrates |
| Change a visual standard (colour, font, grid) | `excalidraw_specialist.md`'s `<visual_standards>` block | Update the canonical tables; check existing kb/ files for collisions |
| Add a renderer option | `scripts/render_excalidraw.py` (argparse) | Propagate through `render_docker.sh` if needed |
| Add a validator rule | `scripts/excalidraw_validator.py` | Append to `errors`/`warnings` lists |

## Naming-pattern cheat sheet

| Artefact | Pattern | Example |
|---|---|---|
| Pattern file | `kb/<slug>.md` | `kb/decision-marker.md` |
| Reference PNG | `examples/<name>.png` | `examples/orchestrator.png` |
| Icon (brand) | `icons/<tool>_logo[_variant].png` | `icons/databricks_logo_black.png` |
| Icon (functional) | `icons/<concept>_icon[_variant].png` | `icons/folder_icon_2.png` |
| Generated diagram | `<your-name>.excalidraw` (in CWD, not in this dir) | `my-pipeline.excalidraw` |

## Notable absences

- **No `.git/`** at this path — the directory is not a checked-out repo of its own.
  See [[CONCERNS.md]].
- **No `.gitignore` / `.dockerignore`.**
- **No `tests/`** directory; quality gate is the validator + visual review loop.
  See [[TESTING.md]].
- **No `.claude/commands/excalidraw.md`** in this directory — the slash command lives at
  the project-level `.claude/commands/`, outside the agent bundle (`README.md:5-6`).

## Related

- [[ARCHITECTURE.md]] — how layers interact.
- [[CONVENTIONS.md]] — file-internal conventions (section ordering, frontmatter).
- [[STACK.md]] — language / dependency view of the same layout.
