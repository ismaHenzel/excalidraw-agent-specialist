# STACK

> Generated: 2026-05-20
> Scope: full repo

## Summary

This is a Claude Code subagent plugin for authoring **Excalidraw** technical diagrams.
The "code" is mostly markdown (the agent prompt + a layout-pattern knowledge base) plus a
small Python rendering pipeline that converts `.excalidraw` JSON to PNG via headless
Chromium. Rendering is containerised via Docker.

## Languages & runtimes

| Language / runtime | Where | Notes |
|---|---|---|
| **Markdown** (primary content) | `excalidraw_specialist.md`, `kb/*.md`, `README.md` | Agent definition, knowledge base, docs |
| **Python ≥ 3.11** | `scripts/render_excalidraw.py`, `scripts/excalidraw_validator.py` | Renderer & static validator |
| **Bash** | `scripts/render_docker.sh`, `scripts/validate_and_render.sh` | Orchestration |
| **HTML + ES module JS** | `scripts/render_template.html` | Loaded by Playwright inside Chromium; imports `@excalidraw/excalidraw@0.17.3` from `esm.sh` |
| **JSON** (Excalidraw schema) | runtime artefacts | Diagrams the agent produces — not stored in this repo |

`scripts/pyproject.toml` pins `requires-python = ">=3.11"`.

## Package management

- **uv** (Astral) with a frozen lockfile at `scripts/uv.lock`.
- Python dependency manifest at `scripts/pyproject.toml`:

  ```toml
  [project]
  name = "excalidraw-render"
  version = "0.1.0"
  requires-python = ">=3.11"
  dependencies = [
      "playwright>=1.40.0",
  ]
  ```

- The Dockerfile installs from the frozen lockfile (`uv sync --frozen`) — host needs only Docker.

## Python dependencies (resolved from `scripts/uv.lock`)

| Package | Resolved version | Role |
|---|---|---|
| `playwright` | 1.59.0 | Drives headless Chromium for SVG export |
| `greenlet` | transitive (playwright) | Playwright runtime |
| `pyee` | transitive (playwright) | Playwright event-emitter |
| `typing-extensions` | transitive | Stdlib polyfill |

No direct dev dependencies, no test framework, no linter, no formatter declared.

## JavaScript / browser-side dependencies

The renderer template (`scripts/render_template.html`) imports the Excalidraw library
at render time from a CDN:

```js
const mod = await import("https://esm.sh/@excalidraw/excalidraw@0.17.3?bundle");
```

This is pinned to `@excalidraw/excalidraw@0.17.3`. No `package.json`, no local
JS dependency lock.

## Container stack

`scripts/Dockerfile`:

```Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv
RUN uv sync --frozen
RUN uv run playwright install chromium
ENTRYPOINT ["uv", "--project", "/app", "run", "python", "/app/render_excalidraw.py"]
```

- Base image: Microsoft Playwright Python image, Ubuntu Jammy, Playwright `v1.49.1`.
- `uv` binary copied from `ghcr.io/astral-sh/uv:latest` (unpinned tag — see [[CONCERNS.md]]).
- Chromium re-installed in the container so it's accessible to uv's venv.
- Image is built lazily by `scripts/render_docker.sh` when not present locally.

## MCP tools the agent depends on

Declared in `excalidraw_specialist.md` frontmatter:

| Tool | Used for |
|---|---|
| `mcp__excalidraw__read_me` | Bootstrap / capability check |
| `mcp__excalidraw__create_view` | Render preview inside the MCP server for visual verification |
| `mcp__excalidraw__export_to_excalidraw` | Persist a view back to `.excalidraw` JSON |
| `mcp__excalidraw__save_checkpoint` | Snapshot in-progress diagrams |
| `mcp__excalidraw__read_checkpoint` | Restore checkpoints |

These names are hard-coded in the agent prompt; if the MCP server is registered under a
different name (default in `README.md`: `excalidraw`), the tool prefix must match.
See [[CONCERNS.md]].

## Built-in Claude Code tools the agent uses

`Read, Bash, Grep, Glob` — declared in the agent frontmatter (`excalidraw_specialist.md:4`).
Used to:
- `Glob` the icons directory to discover available logos.
- `Read` pattern files from `kb/` and PNG references from `examples/`.

## Configuration surfaces

| Setting | Where | Default |
|---|---|---|
| `EXCALIDRAW_ASSETS_DIR` env var | Read by `scripts/render_excalidraw.py:80` | Set by `scripts/render_docker.sh` to `/excalidraw` (mounted agent dir) |
| Viewport max width | `--width` flag on `render_excalidraw.py` | `1920` |
| Device scale factor | `--scale` flag on `render_excalidraw.py` | `2` |
| Output path | `--output` flag, defaults to sibling `.png` | sibling of input |
| MCP server name | `tools:` line of `excalidraw_specialist.md` + `claude mcp add ...` | `excalidraw` |

## Build & install

- **Subagent install:** copy `.claude/agents/excalidraw/` and `.claude/commands/excalidraw.md`
  into the target project (or user-scope `~/.claude/`).
- **MCP server:** install [`excalidraw/excalidraw-mcp`](https://github.com/excalidraw/excalidraw-mcp)
  externally and register with `claude mcp add excalidraw -- <launch-cmd>`.
- **Renderer:** `bash scripts/validate_and_render.sh <file.excalidraw>` — builds the Docker
  image on first run, validates, renders.

## Not present

- No `package.json` (no Node tooling on host).
- No CI configuration (`.github/`, `.gitlab-ci.yml`, …).
- No test runner, no `tox.ini`, no `pytest.ini`.
- No linter / formatter config (`ruff`, `black`, `mypy`).
- No `.gitignore` / `.dockerignore` / no `.git` directory at all — see [[CONCERNS.md]].

## Related

- [[INTEGRATIONS.md]] — external services this stack reaches out to.
- [[ARCHITECTURE.md]] — how these layers fit together.
