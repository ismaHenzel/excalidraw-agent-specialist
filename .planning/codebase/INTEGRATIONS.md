# INTEGRATIONS

> Generated: 2026-05-20
> Scope: full repo

External services, registries, libraries, and protocols this project depends on.
None require authentication or secrets — all are public reads at build/render time.

## Excalidraw MCP server

| | |
|---|---|
| **Source** | [`excalidraw/excalidraw-mcp`](https://github.com/excalidraw/excalidraw-mcp) (external, installed by the user) |
| **Registered under** | `excalidraw` (configurable; see `README.md:69-73`) |
| **Tool prefix** | `mcp__excalidraw__*` |

Called by the subagent (`excalidraw_specialist.md:4`):

| Call | Purpose |
|---|---|
| `mcp__excalidraw__read_me` | Capability handshake |
| `mcp__excalidraw__create_view` | Open / preview a diagram inside the MCP-backed canvas |
| `mcp__excalidraw__export_to_excalidraw` | Serialize the canvas back to `.excalidraw` JSON |
| `mcp__excalidraw__save_checkpoint` | Snapshot work-in-progress state |
| `mcp__excalidraw__read_checkpoint` | Restore a snapshot |

If the user registers the MCP server under a different name, the `tools:` line in
`excalidraw_specialist.md` must be edited to match. See [[CONCERNS.md]].

## CDN-hosted JavaScript library

`scripts/render_template.html:19` does a runtime ES-module import:

```js
await import("https://esm.sh/@excalidraw/excalidraw@0.17.3?bundle");
```

| | |
|---|---|
| **CDN** | `esm.sh` |
| **Library** | `@excalidraw/excalidraw` |
| **Version** | `0.17.3` (pinned) |

Network access is required **every render** unless the CDN response is cached at the OS /
proxy level. The Dockerfile does not pre-cache this module. See [[CONCERNS.md]].

## Container registries

| Image | Source | Pin |
|---|---|---|
| `mcr.microsoft.com/playwright/python:v1.49.1-jammy` | Microsoft Container Registry | Pinned to `v1.49.1-jammy` |
| `ghcr.io/astral-sh/uv:latest` | GitHub Container Registry | **Unpinned `latest` tag** — see [[CONCERNS.md]] |

Pulled by Docker on first `docker build` triggered by `scripts/render_docker.sh:22`.

## PyPI

Reached transitively via `uv sync --frozen` (`scripts/Dockerfile:13`). All packages
resolved in `scripts/uv.lock`:

| Package | Resolved | Provenance |
|---|---|---|
| `playwright` | 1.59.0 | Declared in `scripts/pyproject.toml` |
| `greenlet`, `pyee`, `typing-extensions` | transitive | playwright deps |

No authentication. Build-time only.

## Host binaries the scripts shell out to

| Binary | Used by | Failure mode if missing |
|---|---|---|
| `docker` | `scripts/render_docker.sh` and `scripts/validate_and_render.sh` (via `render_docker.sh`) | Render fails; agent cannot produce a PNG |
| `python` (system) | `scripts/validate_and_render.sh:14` (`python "$SCRIPT_DIR/excalidraw_validator.py" ...`) | Validation phase fails — note this calls *bare* `python`, not `uv run python`. See [[CONCERNS.md]] |
| `bash` | both wrapper scripts | — |
| `uv` | inside the container only | Container build fails |

## Claude Code platform

The agent itself is a first-class consumer of Claude Code's:

- **Subagent system** (file at `excalidraw_specialist.md` with YAML frontmatter).
- **Built-in tools** declared in frontmatter: `Read, Bash, Grep, Glob`.
- **Slash command** `/excalidraw` (defined externally at `.claude/commands/excalidraw.md`
  per `README.md:5-6`; not part of this directory).

## Filesystem boundaries

`scripts/render_excalidraw.py:69-118` reads image files referenced by diagram elements'
`file_path` field, resolving in this order:
1. Absolute path as-is.
2. Relative to the input `.excalidraw` file's directory.
3. Relative to `$EXCALIDRAW_ASSETS_DIR` (set by `render_docker.sh` to the mounted agent
   directory at `/excalidraw`).

This is the integration point between Excalidraw JSON `image` elements and the icon library
under `icons/`. See [[ARCHITECTURE.md]] for the resolution sequence.

## No-auth / no-secrets posture

- No API keys, no OAuth, no service accounts.
- No outbound webhooks, no telemetry calls in the rendering pipeline.
- All external reads are public (esm.sh, MCR, ghcr, PyPI).

## Related

- [[STACK.md]] — versions and runtime details.
- [[CONCERNS.md]] — risks around the unpinned `uv:latest`, CDN dependency, and MCP name coupling.
