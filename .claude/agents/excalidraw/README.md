# Excalidraw Visual Architect Plugin

A Claude Code plugin that produces professional, architectural-grade technical diagrams in Excalidraw, each one rendered and independently verified before it's called done. Ships as three pieces:

- **Author subagent** (`excalidraw_specialist`) at `.claude/agents/excalidraw/` — the visual standards, pattern KB, reference examples, and icon library. Authors and fixes the `.excalidraw`, and renders it. It does **not** verify.
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
├── README.md                  ← this file
├── kb/                        ← compact layout patterns (13 files, categorized)
│   ├── README.md              ← pattern index + example index
│   │
│   │   Macro:
│   ├── group-container.md
│   ├── multi-zoom-overview.md
│   │   Flow:
│   ├── linear-pipeline.md
│   ├── fan-out.md
│   ├── convergence.md
│   ├── task-list.md
│   ├── feedback-loop.md
│   ├── timeline.md
│   │   Decision:
│   ├── decision-branch.md
│   ├── decision-marker.md
│   │   Structure:
│   ├── icon-block.md
│   ├── tree-hierarchy.md
│   └── evidence-card.md
├── examples/                  ← canonical reference PNGs (visual ground truth)
│   ├── architecture_overview.png  ← multi-zoom · group-container · tree · evidence-cards · persona
│   ├── data_pipeline_flow.png     ← linear-pipeline · fan-out · convergence · feedback-loop · ✗/✓ markers
│   ├── process_decision.png       ← decision-branch · decision-marker · task-list · timeline · feedback-loop
│   ├── repo_tree_hierarchy.png    ← tree-hierarchy · group-container · icon-block
│   └── example_star_schema.png    ← user-authored data-model (star schema)
├── examples_excalidraw/       ← editable .excalidraw sources for the reference PNGs
├── icons/                     ← brand/tech PNG logos
└── scripts/
    ├── render/                ← specialist's render pipeline (validator + Playwright + Docker)
    ├── verifier/              ← verifier subagent's structural pre-check helper + self-test
    └── e2e/                   ← operator-side end-to-end check runner
```

The agent prompt always carries the visual standards (colors, rules, JSON templates) and style principles. Pattern files in `kb/` are read on demand when a diagram matches the pattern. The PNGs in `examples/` are **canonical visual references** — the agent Reads them as ground truth before producing similar diagrams.

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

You can invoke `excalidraw_specialist` by name. It will identify the matching `kb/` pattern, read the relevant `examples/*.png` as ground truth, Glob `icons/` for logos, generate the JSON, and render it via `scripts/render/validate_and_render.sh`.

**Caveat:** invoked directly, the specialist is a subagent and **cannot spawn the verifier** — so you get a rendered PNG but no independent verification or auto-fix loop. For a verified diagram, always go through `/excalidraw` (or otherwise drive the loop from the main conversation: author → verify → fix).

## Extending the pattern KB

To add a new pattern (e.g., swim-lane, hub-and-spoke):

1. Create `kb/<pattern>.md` with sections: *When*, *Geometry*, *JSON skeleton*, *Notes*.
2. (Optional) Add `kb/<pattern>.png` rendered from a real Excalidraw example.
3. Add a row to `kb/README.md`'s pattern index.

The agent will discover it automatically.

## Reference examples (`examples/`)

The PNGs in `examples/` are **the visual style guide**. Every pattern in `kb/` links to the example(s) that demonstrate it, and the agent is instructed to Read them as ground truth before producing a similar diagram. Their editable sources live in `examples_excalidraw/` (one `.excalidraw` per PNG) so you can tweak a reference by hand. Every connector in these examples is a sharp **elbow arrow** (`elbowed: true`, `roundness: null`, orthogonal points) — never a curved `roundness:{type:2}` arrow.

Current images (one per diagram kind):

| File | Use as reference for |
|---|---|
| `architecture_overview.png` | Multi-zoom architecture overview · group containers · folder tree inside a panel · evidence cards with real data · persona-anchored worked example with a cross-facet trace |
| `data_pipeline_flow.png` | Left-to-right linear pipeline · color-coded fan-out · convergence into a single sink · inline ✗/✓ decision markers · feedback loop routed outside the forward flow |
| `process_decision.png` | Vertical task-list runbook · side I/O to external resources · labeled-condition decision-branch diamond · binary ✗/✓ gate · timeline axis · restart feedback loop |
| `repo_tree_hierarchy.png` | Folder / namespace tree · brand-titled group container · folders mapped to technology icon blocks · thin elbow tree connectors |
| `example_star_schema.png` | User-authored dimensional / star-schema data model |

To add or refresh an example: edit (or create) the source under `examples_excalidraw/<name>.excalidraw`, re-render it with `scripts/render/validate_and_render.sh`, copy the resulting `<name>.png` into `examples/`, and add/update a row in `kb/README.md`'s reference example index pointing to the patterns it demonstrates.

---
*Adapted from the Gemini-CLI Excalidraw Visual Architect; restructured for Claude Code.*
