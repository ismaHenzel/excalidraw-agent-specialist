# CONCERNS

> Generated: 2026-05-20
> Scope: full repo

Risks, fragile coupling, technical debt, and silent-failure modes. Findings are graded
by impact, not by likelihood. None blocks normal use — they shape what to be careful
about when extending.

## High impact

### 1. No version control at all

There is no `.git/` at `/home/linuxzinho/coding/excaildraw-claude/`, none at
`/home/linuxzinho/coding/excaildraw-claude/.claude/agents/excalidraw/`, no `.gitignore`,
no `.dockerignore`. Edits to the agent prompt, kb, icon set, or renderer cannot be
audited or rolled back. There is no history to attribute behaviour changes to.

**Mitigation:** `git init` at the project root, commit current state as a baseline,
add a `.gitignore` for `.planning/`, `*.png` build artefacts, `__pycache__/`.

### 2. CDN dependency at every render

`scripts/render_template.html:19` does a runtime ES-module import from `esm.sh`:

```js
await import("https://esm.sh/@excalidraw/excalidraw@0.17.3?bundle");
```

The Dockerfile does not pre-cache this module. Rendering requires:
- Outbound HTTPS to `esm.sh`.
- `esm.sh` continuing to host `@excalidraw/excalidraw@0.17.3`.
- The bundled response remaining schema-compatible (`esm.sh` can change CDN routing).

If any of these fail, the validator passes but rendering returns "Import failed: …" with
no actionable error in the wrapper script.

**Mitigation:** vendor the bundle into the Docker image at build time (e.g. `npm pack`
or `curl` the bundled JS), serve via `file://` in `render_template.html`.

### 3. `uv:latest` Docker base is unpinned

`scripts/Dockerfile:6`:

```Dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv
```

`latest` is a moving tag. A breaking change in uv (lockfile format, `sync --frozen`
semantics) would silently make the image unbuildable. The first user to rebuild the
image (because `docker images -q excalidraw-renderer` returns empty) would discover it.

**Mitigation:** pin to `ghcr.io/astral-sh/uv:0.x.y` to match the lockfile-format
generation that produced `scripts/uv.lock`.

### 4. MCP tool names hard-coded in two places

The agent's `tools:` line (`excalidraw_specialist.md:4`) lists five
`mcp__excalidraw__*` tools. If a user registers the MCP server with a different name
(`claude mcp add my_excalidraw ...`), the agent will silently fail to call them. There
is no validator for "does the MCP server expose these tools".

If the upstream MCP server (`excalidraw/excalidraw-mcp`) renames a tool, e.g.
`create_view` → `render_view`, the same silent break occurs.

**Mitigation:** README already documents that the server must be registered under
`excalidraw`; consider an early `mcp__excalidraw__read_me` capability check in the
agent's startup sequence to fail loudly when the tool surface drifts.

### 5. Path-traversal surface in image embedding

`scripts/render_excalidraw.py:84-94` resolves an element's `file_path` field:

```python
raw_path = Path(el["file_path"])
if raw_path.is_absolute():
    file_path = raw_path
else:
    file_path = excalidraw_dir / raw_path
    if not file_path.exists() and assets_dir is not None:
        fallback = assets_dir / raw_path
```

A `.excalidraw` file authored or modified by an untrusted source can:
- Point at absolute host paths (`/etc/passwd`, `~/.ssh/id_rsa`) — the file is read
  and **base64-encoded into the rendered SVG / PNG**.
- Traverse out of the assets directory with `../../...`.

No path normalisation, no allowlist check, no whitelist of file extensions.

**Trust model:** the script is intended to run on user-authored `.excalidraw` files.
But if these scripts are ever invoked as a service against externally-supplied JSON,
this is an information-disclosure vector.

**Mitigation:** reject absolute paths; canonicalise relative paths and reject those
that resolve outside `excalidraw_dir` and `EXCALIDRAW_ASSETS_DIR`.

## Medium impact

### 6. Docker container runs as root

`scripts/Dockerfile` does not create or `USER`-switch to a non-root user. The
container also launches Chromium with `--no-sandbox` (`scripts/render_excalidraw.py:176`):

```python
browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
```

`--no-sandbox` is necessary because the container runs as root, and root-Chromium
refuses the sandbox by default. Combined with the path-traversal surface (#5), this is
a defence-in-depth gap rather than an active vulnerability.

**Mitigation:** add a non-root user in the Dockerfile, drop `--no-sandbox`.

### 7. `validate_and_render.sh` calls bare `python`

`scripts/validate_and_render.sh:14`:

```bash
python "$SCRIPT_DIR/excalidraw_validator.py" "$EXCALIDRAW_FILE"
```

The renderer script and the Dockerfile use `uv run python`. The validator wrapper does
not. On a system where `python` resolves to Python 2 or to a venv without `json`-stdlib
(very unlikely but possible on minimal Linux), validation silently fails or behaves
unexpectedly. The validator script itself uses only `json`, `sys`, `os` from stdlib,
so the practical exposure is small — but the inconsistency is real.

**Mitigation:** change to `uv run python` or `python3` for consistency.

### 8. Stale Docker image detection is presence-only

`scripts/render_docker.sh:20-23`:

```bash
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "Building Docker image $IMAGE_NAME..."
    docker build -t $IMAGE_NAME "$SCRIPT_DIR"
fi
```

Once the image exists, it is never rebuilt. Editing the Dockerfile, `pyproject.toml`, or
`uv.lock` does not trigger a rebuild. Users hit confusing "but I changed it" loops.

**Mitigation:** compare the image's digest against a fingerprint of the build context
(or expose a `--rebuild` flag).

### 9. Icon library has duplicate / near-duplicate entries

`ls icons/` shows multiple variants per brand:

- **Databricks:** `databricks.png`, `databricks_logo.png`, `databricks_logo_2.png`,
  `databricks_logo_3.png`, `databricks_logo_4.png`, `databricks_logo_5.png`,
  `databricks_logo_black.png`, `databricks_logo_black_2.png` (8 files).
- **Great Expectations:** `great_expectations_logo.png`, `great_expectations_logo_2.png`,
  `great_expectations_logo_black.png`, `great_expectations_logo_white.png`.
- **GitLab:** `gitlab_logo.png`, `gitlab_logo_2.png`.
- **Delta Lake:** `delta_lake_logo_1.png`, `delta_lake_logo_2.png`.
- **Failure / folder icons:** `failure_icon.png` + `failure_icon_2.png`,
  `folder_icon.png` + `folder_icon_2.png`.

The agent's `Glob` discovery is told to pick what fits, but with 8 Databricks files the
choice is non-deterministic and downstream consistency suffers.

**Mitigation:** audit `icons/`, mark a canonical `<tool>_logo.png` per brand, prune the
rest, document the variants kept in `kb/README.md`.

### 10. Non-icon "diagram" PNGs mixed into `icons/`

`icons/` contains four PNGs that are clearly *diagrams*, not logos:

- `bigquery_warning_text.png`
- `data_lineage_diagram.png`
- `data_pipeline_detail.png`
- `git_flow_diagram.png`

They will be returned by `Glob icons/*.png` alongside true logos, and the agent has no
metadata to know they shouldn't be used as 24×24 brand markers.

**Mitigation:** move to a separate folder (e.g. `icons/diagrams/` or `examples/extras/`)
or rename with a clear prefix.

### 11. Frozen `playwright` may drift from the base image's Chromium

The base image is `playwright/python:v1.49.1-jammy`. `scripts/uv.lock` resolves
`playwright 1.59.0`. The Dockerfile then runs `uv run playwright install chromium` to
re-install Chromium for uv's venv.

This works today but couples three moving parts (base image Playwright, uv-installed
Playwright, Chromium version compatibility). If the gap widens far enough, the renderer
hits browser-launch errors that are reported as "Failed to launch browser".

**Mitigation:** align the lockfile to a Playwright version close to the base image
(`1.49.x`), or upgrade the base image when bumping `playwright`.

## Low impact

### 12. Renderer fails open on missing icons

`scripts/render_excalidraw.py:115-118`:

```python
print(f"WARNING: Failed to embed image {file_path}: {e}", file=sys.stderr)
…
print(f"WARNING: Image file not found: {file_path}", file=sys.stderr)
```

A diagram referencing a missing or renamed icon renders successfully with the image
slot blank or broken. The orchestrator script does not surface these warnings; they
go to stderr and the wrapper exits 0.

**Mitigation:** add a `--strict` flag that turns missing-image warnings into errors.

### 13. No `.gitignore` / `.dockerignore`

When `git init` is eventually run, `__pycache__/`, `.planning/`, generated `*.png`
files, and any local virtualenv would all be picked up. Docker build context will
similarly include everything in `scripts/`. Add both files before initialising git.

### 14. No TODO/FIXME comments in source

A full repo search for `TODO|FIXME|XXX|HACK` (across `.py`, `.sh`, `.md`, `.html`,
`.toml`) returned **zero hits**. The codebase carries no inline reminders of pending
work. This is good hygiene, but it also means latent debt has to be discovered by
reading — none of it is signposted.

### 15. Renderer is single-threaded and starts Chromium per call

Each call to `render_excalidraw.py` boots a fresh browser. For batch rendering of
many diagrams (a common use case during agent iteration), startup overhead dominates.

**Mitigation:** add a batch mode that processes multiple `.excalidraw` files in one
browser session.

### 16. Subprocess / Docker calls in shell scripts

`scripts/render_docker.sh` interpolates `$INPUT_FILE` and `${@:2}` into a `docker run`
command. Filenames with newlines or odd characters could behave unexpectedly. The
script is meant for trusted local input but should be flagged if ever invoked from a
broader pipeline.

## Not actually a concern (closed)

- **MCP tools list out of sync with the implementation.** The 5 tool names listed in
  `excalidraw_specialist.md:4` match what the README documents as the
  `excalidraw/excalidraw-mcp` server contract. If the user upgrades the MCP server, the
  list should be re-verified — but as of the snapshot date, it is consistent.

## Triage summary

| # | Area | Severity | Easy fix? |
|---|---|---|---|
| 1 | No git repo | High | Yes |
| 2 | CDN dependency at runtime | High | Medium (vendor JS) |
| 3 | `uv:latest` unpinned | High | Yes |
| 4 | Hard-coded MCP tool names | High | Medium (add capability probe) |
| 5 | Path traversal in image embed | High | Yes |
| 6 | Container runs as root | Medium | Medium |
| 7 | Bare `python` in shell wrapper | Medium | Yes |
| 8 | Docker rebuild detection | Medium | Yes |
| 9 | Icon duplicates | Medium | Yes (manual audit) |
| 10 | Non-icon PNGs in `icons/` | Medium | Yes |
| 11 | Playwright vs base image drift | Medium | Yes |
| 12 | Renderer fails-open on missing icons | Low | Yes |
| 13 | No `.gitignore` | Low | Yes |
| 14 | No signposted debt | Low | — |
| 15 | Per-call Chromium boot | Low | Medium |
| 16 | Shell-script arg handling | Low | Medium |

## Related

- [[ARCHITECTURE.md]] — where these coupling points sit in the data flow.
- [[STACK.md]] — version pinning and dependency choices.
- [[TESTING.md]] — what would catch these regressions if it existed.
