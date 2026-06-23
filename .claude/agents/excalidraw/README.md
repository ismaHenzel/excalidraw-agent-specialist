# Excalidraw Visual Architect Plugin

A Claude Code plugin that produces professional, architectural-grade technical diagrams in Excalidraw, each one rendered and independently verified before it's called done. Ships as three pieces:

- **Author subagent** (`excalidraw_specialist`) at `.claude/agents/excalidraw/` — the visual standards, the two-layer knowledge base (`kb/`), and icon library. Authors and fixes the `.excalidraw`, and renders it. It does **not** verify.
- **Verifier subagent** (`excalidraw_verifier`) — a read-only fresh-eyes reviewer that inspects the rendered PNG and emits a structured pass/fail report. It never edits or re-renders.
- **Orchestrator slash command** at `.claude/commands/excalidraw.md` — the `/excalidraw` entry point. It gathers intent, then drives the closed **render → verify → fix** loop, spawning the author and verifier in turn (capped at 3 verify attempts).

### Why the orchestrator owns the loop

Claude Code subagents **cannot spawn other subagents**. So the author cannot call the verifier itself — the loop has to live one level up, in the `/excalidraw` command, which runs in the main conversation and *can* spawn both. The command verifies after each render, hands any failing report back to the author to fix, and only declares success on a passing verifier report (or surfaces an honest failure after 3 attempts).

## Style: Architect's Precision

- **Zero Roughness** — `roughness: 0` on every element. No hand-drawn effects.
- **Monospace Typography** — `fontFamily: 3` for all text.
- **20px Grid Alignment** — no arbitrary positions.
- **90° Elbow Arrows** — structured connectors instead of diagonals.
- **Brand Consistency** — built-in icon library and semantic color palette.

## Folder layout

```
.claude/agents/excalidraw/
├── excalidraw_specialist.md   ← author/fixer agent + inlined visual standards + style principles
├── excalidraw_verifier.md     ← read-only verifier agent (structural + visual checks → report)
├── excalidraw_icon_fetcher.md ← icon resolver agent (local-first, then downloads + converts)
├── README.md                  ← this file
├── kb/                        ← the knowledge base — everything the agent reads on demand
│   ├── README.md              ← KB hub: the map + reading order
│   ├── patterns/              ← PRIMITIVE layer: reusable layout sub-patterns
│   │   ├── README.md          ← primitive index (macro / flow / decision / structure)
│   │   └── group-container.md, fan-out.md, tree-hierarchy.md, …  (15 files)
│   └── diagram-types/         ← TYPE layer: one SUBFOLDER per diagram type, WITH its example assets
│       ├── README.md          ← type index + authoritative resolver table
│       ├── compartmented-box.md, notation-conventions.md  ← shared cross-type files
│       └── tech-architecture/ ← one folder per type (star-schema/, er/, sequence/, …)
│           ├── tech-architecture.md          ← recipe file
│           ├── architecture_overview.png     ← canonical render (visual ground truth)
│           └── architecture_overview.excalidraw  ← editable source, beside its render
├── icons/                     ← brand/tech PNG logos
└── scripts/
    ├── render/                ← specialist's render pipeline (validator + Playwright + Docker)
    ├── verifier/              ← verifier subagent's structural pre-check helper + self-test
    └── e2e/                   ← operator-side end-to-end check runner
```

The agent prompt always carries the visual standards (colors, rules, JSON templates) and style principles. The KB under `kb/` is read on demand: `kb/diagram-types/<type>/<type>.md` recipes name which `kb/patterns/` primitives to compose, and each type's canonical PNG (plus its editable `.excalidraw` source) sits **right beside the recipe in that type's subfolder** under `kb/diagram-types/` — the agent Reads the PNG as ground truth before producing similar diagrams. Start at `kb/README.md` for the full map.

## Installation

### 1. Place the plugin files

Choose a scope and copy **both** pieces:

| Piece | Project scope | User scope |
|---|---|---|
| Agent bundle | `<project>/.claude/agents/excalidraw/` | `~/.claude/agents/excalidraw/` |
| `/excalidraw` command | `<project>/.claude/commands/excalidraw.md` | `~/.claude/commands/excalidraw.md` |

The slash command is optional — the agent works standalone if invoked by name. The command makes invocation feel native (`/excalidraw a CI/CD pipeline`) instead of *"please use the excalidraw_specialist agent to…"*.

All paths inside the agent are relative to the project working directory (`.claude/agents/excalidraw/...`), so no edits are needed when cloning into a new project.

### 2. Register the Excalidraw MCP server
The agent calls `mcp__excalidraw__*` tools. Install the MCP server from [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp), then register it with Claude Code **under the server name `excalidraw`**:

```bash
claude mcp add excalidraw -- <command to launch the excalidraw-mcp server>
```

If your MCP server uses a different name or different tool names, update the `tools:` line in `excalidraw_specialist.md` accordingly.

## Usage

### Via `/excalidraw` (recommended)

Type `/excalidraw [optional description]` at the prompt. The command will:

1. Ask **what kind of diagram** (architecture overview / pipeline / hierarchy / process-decision).
2. Ask **how much structure you have in mind**:
   - *Propose options based on my goal (Recommended)* — agent reads the kb + examples and suggests 2–3 concrete layout candidates, you pick.
   - *I'll describe the structure* — you give the nodes, edges, and groupings.
   - *Just generate it* — agent infers everything from your description.
3. Optionally ask one follow-up if crucial detail is missing (which systems, what's it arguing).
4. **Dispatch to `excalidraw_specialist`** (author mode) to generate, write, and render the `.excalidraw`.
5. **Run `excalidraw_verifier`** on the result; on a failing report, hand the issues back to the specialist (fix mode) and re-verify — up to 3 verify attempts.
6. **Report back** the verified PNG path, filename, patterns used, and structural choices — or an honest failure if 3 attempts didn't pass.

This is the recommended entry point precisely because the verify-fix loop only works when something orchestrates it. See *"Why the orchestrator owns the loop"* above.

### Via direct invocation (no verification)

You can invoke `excalidraw_specialist` by name. It will identify the matching `kb/patterns/` pattern, read the relevant `kb/diagram-types/*.png` as ground truth, Glob `icons/` for logos, generate the JSON, and render it via `scripts/render/validate_and_render.sh`.

**Caveat:** invoked directly, the specialist is a subagent and **cannot spawn the verifier** — so you get a rendered PNG but no independent verification or auto-fix loop. For a verified diagram, always go through `/excalidraw` (or otherwise drive the loop from the main conversation: author → verify → fix).

## Extending the pattern KB

To add a new pattern (e.g., swim-lane, hub-and-spoke):

1. Create `kb/patterns/<pattern>.md` with sections: *When*, *Geometry*, *JSON skeleton*, *Notes*.
2. Add a row to `kb/patterns/README.md`'s pattern index.
3. If a diagram type composes it, add a `> Used by types: <type>` back-ref so the two-layer link stays bidirectional.

The agent will discover it automatically.

## Reference examples (`kb/diagram-types/`)

The canonical PNGs are **the visual style guide**. They live **inside each type's subfolder under `kb/diagram-types/`, beside the recipe that owns each one**, together with the editable `.excalidraw` source (same basename) — so the diagram type and its image stay together. Every pattern in `kb/patterns/` links to the example(s) that demonstrate it, and the agent is instructed to Read them as ground truth before producing a similar diagram. Every connector in these examples is a sharp **elbow arrow** (`elbowed: true`, `roundness: null`, orthogonal points) — never a curved `roundness:{type:2}` arrow.

The authoritative type → example mapping is the resolver table in [`kb/diagram-types/README.md`](kb/diagram-types/README.md); the pattern → example mapping is the reference example index in [`kb/patterns/README.md`](kb/patterns/README.md). A few cross-pattern reference renders (not tied to a single type) also live there:

| File (under `kb/diagram-types/`) | Use as reference for |
|---|---|
| `tech-architecture/architecture_overview.png` | Multi-zoom architecture overview · group containers · folder tree inside a panel · evidence cards with real data · persona-anchored worked example with a cross-facet trace |
| `tech-architecture/data_pipeline_flow.png` | Left-to-right linear pipeline · color-coded fan-out · convergence into a single sink · inline ✗/✓ decision markers · feedback loop routed outside the forward flow |
| `tech-architecture/process_decision.png` | Vertical task-list runbook · side I/O to external resources · labeled-condition decision-branch diamond · binary ✗/✓ gate · timeline axis · restart feedback loop |
| `star-schema/example_star_schema.png` | Legacy user-authored star schema (**de-indexed** — see `star-schema/star_schema_v2.png` for the current canonical) |

To add or refresh an example: edit (or create) the source `kb/diagram-types/<type>/<name>.excalidraw`, re-render it with `scripts/render/validate_and_render.sh` so the `<name>.png` beside it updates, and add/update the relevant row in the resolver table ([`kb/diagram-types/README.md`](kb/diagram-types/README.md)) and/or the reference example index ([`kb/patterns/README.md`](kb/patterns/README.md)).

---
*Adapted from the Gemini-CLI Excalidraw Visual Architect; restructured for Claude Code.*
