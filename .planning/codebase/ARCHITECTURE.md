# ARCHITECTURE

> Generated: 2026-05-20
> Scope: full repo

## One-line summary

A Claude Code **subagent** that composes Excalidraw diagrams from a named **pattern
library**, references **canonical PNG examples** for style, fetches **brand icons** from
a local asset folder, and emits `.excalidraw` JSON — verified visually via an MCP server
and rendered to PNG by an offline Docker pipeline.

## High-level diagram

```
            user / parent agent
                    │
                    ▼
        ┌───────────────────────────┐
        │ excalidraw_specialist.md  │   ← agent prompt (visual standards,
        │  (system prompt + tools)  │     color palette, JSON templates inlined)
        └────┬──────────┬───────────┘
             │          │
   reads on  │          │ Glob/Read
   demand    ▼          ▼
    ┌──────────┐   ┌──────────┐   ┌──────────────┐
    │  kb/*.md │   │ icons/   │   │ examples/    │
    │ patterns │   │ logos    │   │ PNG ground   │
    │          │   │          │   │ truth        │
    └────┬─────┘   └────┬─────┘   └──────┬───────┘
         │              │                │
         └────────┬─────┴────────────────┘
                  ▼
        compose .excalidraw JSON
                  │
                  ▼
       mcp__excalidraw__create_view ──► visual verification
                  │
                  ▼
       .excalidraw file in CWD
                  │
   (offline)      ▼
       scripts/validate_and_render.sh
       ├─ excalidraw_validator.py    (lint JSON)
       └─ render_docker.sh
            └─ Docker (Playwright + Chromium)
                └─ render_template.html
                     └─ esm.sh/@excalidraw/excalidraw@0.17.3
                          └─ exportToSvg ──► PNG
```

## Layers

| Layer | Responsibility | Key files |
|---|---|---|
| **Agent** | System prompt, visual standards, operational mandates | `excalidraw_specialist.md` |
| **Pattern KB** | Compact, named layout patterns (geometry + JSON skeleton) | `kb/README.md`, `kb/*.md` |
| **Asset library** | Brand / tech logos as PNGs | `icons/*.png` (73 files) |
| **Reference examples** | Canonical-style PNGs the agent reads as visual ground truth | `examples/*.png` |
| **MCP tools** | In-Claude rendering, verification, checkpointing | `mcp__excalidraw__*` |
| **Validator** | Static lint of generated JSON | `scripts/excalidraw_validator.py` |
| **Renderer** | Offline `.excalidraw → .png` via headless Chromium | `scripts/render_excalidraw.py`, `scripts/render_template.html`, `scripts/Dockerfile`, `scripts/render_docker.sh` |
| **Orchestrator** | Validate-then-render pipeline | `scripts/validate_and_render.sh` |

## Data flow — primary generation path

1. User invokes the agent via `/excalidraw` (or by name).
2. Agent decomposes the request into named patterns (`kb/README.md` index).
3. Agent `Read`s the matching `kb/<pattern>.md` for geometry + JSON skeleton.
4. Agent `Read`s the matching `examples/*.png` as visual ground truth.
5. Agent `Glob`s `icons/` to find brand logos for technology nodes.
6. Agent composes Excalidraw JSON in memory, following inlined visual standards
   (roughness 0, fontFamily 3, 20px grid, elbow arrows with `roundness: { type: 2 }`).
7. Agent calls `mcp__excalidraw__create_view` to render-and-verify the layout in the
   MCP canvas; iterates if overlaps or alignment issues are visible.
8. Agent writes the `.excalidraw` file to the **current working directory** (not into
   the agent directory) per `excalidraw_specialist.md:27`.

## Data flow — offline render path

1. User runs `bash scripts/validate_and_render.sh <file.excalidraw>`.
2. **Phase 1 — Validation:** `excalidraw_validator.py` checks:
   - Metadata: `type: "excalidraw"`, `version` present, `elements` present.
   - Anti-pattern: no `label` property on `rectangle`/`ellipse`/`diamond` (must be standalone `text`).
   - Warning: text strokeColor not in `#1e1e1e` / `#000000` / `#000` (low contrast).
   - Warning: no text elements present (probably missing labels).
3. If validation fails (non-zero exit) the pipeline halts.
4. **Phase 2 — Render:** `render_docker.sh` builds the image if missing, then runs:
   - Mounts input dir at `/input` (rw — PNG lands as sibling).
   - Mounts the agent dir at `/excalidraw:ro`.
   - Sets `EXCALIDRAW_ASSETS_DIR=/excalidraw`.
5. Inside the container, `render_excalidraw.py`:
   - Validates JSON structure (`validate_excalidraw`).
   - Walks `elements`, embeds local images by reading `file_path`, base64-encoding into
     `data.files[fileId].dataURL`. Resolution order: absolute → input dir → `EXCALIDRAW_ASSETS_DIR`.
   - Computes a bounding box (`compute_bounding_box`) — counts arrow `points` relative to
     element `x,y`. Pads by 80 px and caps viewport width at `--width` (default 1920).
   - Launches Playwright Chromium headless with `--no-sandbox`, opens
     `render_template.html`, waits for `window.__moduleReady`.
   - The template ES-imports `@excalidraw/excalidraw@0.17.3` from `esm.sh`, exposes
     `window.renderDiagram(json)` that invokes `exportToSvg(...)` and mounts the SVG.
   - Page is screenshotted at the `#root svg` element to the output PNG path.
6. **Phase 3 — Visual analysis:** The script instructs the agent to `Read` the PNG and
   verify visually.

## Key abstractions

### Pattern
A named, compact layout recipe (`kb/<slug>.md`) with sections **When · Geometry · JSON
skeleton · Notes** and an optional **See in examples** pointer. Diagrams are *compositions
of patterns*, never freeform. The pattern catalogue is categorized in `kb/README.md`:

- **Macro:** `group-container`, `multi-zoom-overview`
- **Flow:** `linear-pipeline`, `fan-out`, `convergence`, `task-list`, `feedback-loop`, `timeline`
- **Decision:** `decision-branch`, `decision-marker`
- **Structure:** `icon-block`, `tree-hierarchy`, `evidence-card`

### Icon Block
The atomic node (`kb/icon-block.md`): a `180×80` rectangle with a `24×24` icon at
`(x+8, y+8)` and a label `text` element at `(x+40, y+28)`. Every higher-level pattern
treats nodes as Icon Blocks.

### Group Container
A bordered scope with brand icon + title at top-left inset. House-style convention:
nesting depth 2–3 levels (Environment → Technology → Operation). Outermost container
carries the brand identification; innermost typically omits the title.

### Evidence Card
Pattern for displaying real data — cost figures, metrics, output samples. Story over
abstraction; real numbers, not placeholders.

### Semantic color role
Colors encode meaning, not decoration. Palette is inlined in the agent prompt
(`excalidraw_specialist.md:42-55`): Primary, Secondary, Start/Trigger, End/Success,
Warning, Decision, AI/LLM, Inactive, Error — each with a fill + stroke pair.

## Entry points

| Entry | Trigger | What happens |
|---|---|---|
| `/excalidraw` slash command | User in Claude Code | Two-question intent gather → dispatch to subagent (command file lives outside this directory; see `README.md:5-6`) |
| Direct subagent invocation | Parent agent calls `excalidraw_specialist` by name | Same pipeline, no intent gather |
| `bash scripts/validate_and_render.sh <file>` | Shell | Validate + render `.excalidraw` to PNG |
| `bash scripts/render_docker.sh <file>` | Shell | Render only (skips validator) |
| `uv run python scripts/render_excalidraw.py <file>` | Shell, no Docker | Render directly on host (requires uv + Playwright Chromium installed locally) |

## Architectural constraints

- **Path portability.** Asset paths inside the agent are always
  `.claude/agents/excalidraw/...` relative to the project working directory. The agent is
  drop-in for any project that vendors `.claude/agents/excalidraw/`. (`README.md:66`,
  `excalidraw_specialist.md:21-22`)
- **MCP coupling.** The agent name-binds to `mcp__excalidraw__*` tools; the MCP server must
  be registered with prefix `excalidraw`.
- **Visual standards are non-negotiable** (`excalidraw_specialist.md:30`): `roughness: 0`,
  `fontFamily: 3`, 20 px grid, elbow arrows only, brand stroke colors per table.
- **No `label` property on shapes.** Labels are always standalone `text` elements
  (enforced by `excalidraw_validator.py:32-37`).
- **Output is local.** Diagrams are written to the *current working directory*, not into
  the agent folder.

## Anti-patterns the agent must avoid

| Don't | Do instead |
|---|---|
| Diagonal arrows | 90° elbow with `points` array of ≥ 3 entries and `roundness: { type: 2 }` |
| Diamonds for binary pass/fail | Inline ✗/✓ circles (`kb/decision-marker.md`) — diamonds only for ≥ 2 labeled-condition branches (`kb/decision-branch.md`) |
| Feedback arrows crossing forward flow | Route around bounding box with wide-arc elbow (`kb/feedback-loop.md`) |
| `label` field inside a shape element | Separate `text` element with own `x, y` |

## Error handling strategy

| Layer | Strategy |
|---|---|
| Validator | Exit non-zero with `[X]` errors / `[!]` warnings printed to stdout |
| Render orchestrator | `set -e`; halts pipeline at first failure; propagates exit code |
| Renderer (Python) | Print to stderr, `sys.exit(1)` on bad JSON / missing template / Playwright import / module load timeout / failed `renderDiagram` / missing SVG |
| Embed-images | Warns on missing files (`scripts/render_excalidraw.py:118`) but continues — diagram renders with broken image refs |
| Agent | Operational mandate "No Chitchat" — produce diagram or ask for missing technical detail |

## Related

- [[STACK.md]] — language & dependency choices.
- [[STRUCTURE.md]] — where each layer lives on disk.
- [[CONVENTIONS.md]] — how to extend patterns, KB rules.
- [[CONCERNS.md]] — fragile coupling points in this architecture.
