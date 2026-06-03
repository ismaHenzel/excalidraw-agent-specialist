# TESTING

> Generated: 2026-05-20
> Scope: full repo

## Headline

**There is no automated test suite.** No `tests/` directory, no `pytest`, no CI workflow,
no fixtures. Quality is enforced by a **static validator → render → visual review** loop
plus a small library of canonical PNGs used as visual ground truth.

## The QA loop

The closest thing to a test runner is `scripts/validate_and_render.sh`:

```bash
bash scripts/validate_and_render.sh <path-to-file.excalidraw>
```

Three phases:

1. **Phase 1 — Technical Validation** (`scripts/excalidraw_validator.py`).
   Lints the JSON for the rules in [[CONVENTIONS.md]] (`type`/`version`/`elements`
   present, no `label` on shapes, low-contrast warnings, missing-text warnings).
   Non-zero exit halts the pipeline.
2. **Phase 2 — Visual Rendering** (`scripts/render_docker.sh`). Builds the
   `excalidraw-renderer` Docker image if missing, mounts the input directory and the agent
   directory, runs `scripts/render_excalidraw.py` to produce a PNG via Playwright +
   headless Chromium.
3. **Phase 3 — Visual Analysis.** Script prints an instruction telling the calling agent
   to `Read` the resulting PNG and verify visually. This step is performed by the LLM,
   not by code.

This is the only quality gate. There is no diff against a golden image, no pixel
comparison, no schema diff against published Excalidraw versions.

## What the validator covers (`scripts/excalidraw_validator.py`)

| Check | Severity | Code reference |
|---|---|---|
| Top-level `type` is `"excalidraw"` | Error | `excalidraw_validator.py:21-22` |
| Top-level `version` present | Error | `excalidraw_validator.py:23-24` |
| Top-level `elements` present | Error | `excalidraw_validator.py:25-26` |
| Shape elements (`rectangle`/`ellipse`/`diamond`) must NOT carry a `label` field | Error | `excalidraw_validator.py:32-37` |
| Diagrams with >2 elements should have at least one `text` element | Warning | `excalidraw_validator.py:40-42` |
| Text `strokeColor` should be in `{#1e1e1e, #000000, #000}` | Warning | `excalidraw_validator.py:45-52` |

Report format: `[X]` errors, `[!]` warnings, `[✓]` pass. Errors fail the script with exit 1.

## What the renderer revalidates (`scripts/render_excalidraw.py:18-32`)

A stricter pre-render check than the static validator:

- `type == "excalidraw"`.
- `elements` is a `list`.
- `elements` is non-empty.

Failures here return errors to stderr and exit 1 *before* a browser is launched, so
malformed input is cheap to reject.

## What is NOT tested

- Pattern files in `kb/*.md` — no schema or example check.
- The agent prompt — no regression check that visual standards remain consistent across
  edits.
- Icon library — no audit for missing PNGs or duplicate-of-different-bytes variants.
- Renderer behaviour — no integration test that a known input produces the expected
  output. `scripts/render_template.html` loading `@excalidraw/excalidraw@0.17.3` from
  `esm.sh` is unverified each run.
- Shell scripts — no `shellcheck` integration, no script-level tests.
- `scripts/render_docker.sh` image freshness — once `excalidraw-renderer` exists locally
  it is reused indefinitely (see [[CONCERNS.md]]).

## Visual regression reference

`examples/*.png` serve as canonical visual baselines:

| Image | Patterns it certifies in canonical style |
|---|---|
| `examples/governance.png` | 3-level nested `group-container`, inline `decision-marker`, outside-routed `feedback-loop`, container-level branding |
| `examples/orchestrator.png` | `tree-hierarchy` on the left, colour-coded `fan-out`, `convergence` into a single sink |
| `examples/refresh_bi.png` | Vertical `task-list`, side I/O through container border, async badge |
| `examples/dlt.png` | `multi-zoom-overview`, `evidence-card` with real data, persona-anchored worked example |

The agent is instructed (in `excalidraw_specialist.md` operational mandate #2) to `Read`
the matching PNG as ground truth *before* drawing a similar diagram. There is no
automated diffing — visual fidelity is enforced by the LLM matching layout density and
labeling rhythm.

## Running the full QA loop manually

```bash
# 1. Generate or hand-edit a .excalidraw file
# 2. Validate + render + visually verify
bash scripts/validate_and_render.sh path/to/diagram.excalidraw

# Or skip the validator (not recommended):
bash scripts/render_docker.sh path/to/diagram.excalidraw

# Or skip Docker (requires uv + Playwright Chromium installed locally):
cd scripts
uv run python render_excalidraw.py path/to/diagram.excalidraw
```

The resulting PNG lands next to the input as `<name>.png`.

## Gaps and recommendations

- **No structural test of the kb/icon-block geometry rules** — a mistyped coordinate in
  a kb file won't be caught until a diagram visibly misaligns.
- **No CI** — every check is local and on-demand.
- **No diff coverage** for Excalidraw schema changes when the CDN moves the pinned
  version pointer; the renderer can break silently if `@excalidraw/excalidraw@0.17.3`
  is yanked from `esm.sh`.

See [[CONCERNS.md]] for the full risk list.

## Related

- [[CONVENTIONS.md]] — the rules the validator enforces.
- [[ARCHITECTURE.md]] — where the QA loop sits in the data flow.
- [[CONCERNS.md]] — what fails silently today.
