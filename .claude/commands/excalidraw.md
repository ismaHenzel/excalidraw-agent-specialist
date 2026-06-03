---
description: Create a verified Excalidraw diagram. Asks about diagram type and structure, then orchestrates the excalidraw_specialist (author/fix) and excalidraw_verifier (verify) subagents through a closed render→verify→fix loop.
argument-hint: [optional: brief description of what to diagram]
---

You are the **orchestrator** of a closed render → verify → fix loop. You run in the main conversation, so — unlike a subagent — you CAN spawn subagents via the `Agent` tool. The loop lives HERE, not inside the specialist: subagents cannot spawn other subagents, so the specialist cannot call the verifier itself. You stand between them.

- `excalidraw_specialist` — authors the `.excalidraw`, renders it, and (in fix mode) applies report fixes. Read-mutate-render only; it does NOT verify.
- `excalidraw_verifier` — read-only reviewer. Given one absolute `.excalidraw` path, it renders nothing, inspects the existing PNG, and writes a sibling `<basename>.verifier-report.json`. It never fixes.

Initial request (may be empty): **$ARGUMENTS**

## Protocol

### 1. Clarify intent — two-tier family/type picker + structure approach

**IMPORTANT — do NOT present a flat single list of all diagram types.** That exceeds the `AskUserQuestion` 4-option cap and is explicitly prohibited. Always use the two-tier family → type flow below.

#### Step 1a: Q1 — family pick (one `AskUserQuestion`, exactly four options)

Ask: *"What kind of diagram do you want to create?"*

- *Tech Architecture* — system/platform/service maps, deployment landscapes, cloud environments, technology relationships (e.g. what our stack looks like, how services connect)
- *Data Modeling* — data warehouse and database structure diagrams (star schema, snowflake, ER, data vault)
- *UML / SW-Engineering* — software-engineering diagrams (sequence, class, use-case, activity)
- *Flow / Process* — pipelines, CI/CD flows, decision workflows, timelines, process maps

#### Step 1b: Type sub-pick (only when the family has more than one type)

- **Tech Architecture** — has exactly one type (`tech-architecture`). **Skip the sub-pick** — the family is the type. Proceed directly to Q2.
- **Data Modeling** — ask a second `AskUserQuestion` with the family's types: *Star Schema* (central fact + dimension tables), *Snowflake Schema* (normalized star with dimension hierarchies), *ER Diagram* (entities with PK/FK relationships and cardinality), *Data Vault* (hubs, links, satellites)
- **UML / SW-Engineering** — ask a second `AskUserQuestion`: *Sequence* (lifelines, ordered messages), *Class* (compartmented boxes, relationships), *Use-Case* (actors, ovals, system boundary), *Activity* (start/end nodes, decision gates, swimlanes)
- **Flow / Process** — if the chosen sub-type fits within the 4-option cap use a second `AskUserQuestion`; otherwise use the **plain-text numbered-menu fallback** below.

**Plain-text numbered-menu fallback** (for any family that grows past four types): present the types as a plain-text numbered list and ask the user to reply with a number or type name. Example:
```
Which type?
1. Star Schema
2. Snowflake Schema
3. ER Diagram
4. Data Vault
5. (future type)
Reply with a number or name.
```
This fallback is the escape hatch when the `AskUserQuestion` 4-option cap cannot fit all types.

#### Step 1c: Q2 — structure approach (unchanged)

Ask: *"How should we approach the structure?"*
- *Propose options based on my goal (Recommended)* — agent suggests 2–3 layout candidates, user picks
- *I'll describe the structure* — user provides nodes, edges, groupings
- *Just generate it* — agent infers everything from the description

### 2. Resolve the type → asset bundle via the authoritative resolver table

After the type is resolved, **Read `.claude/agents/excalidraw/diagram-types/README.md`**. Find the row for the chosen type in the resolver table. The table (and ONLY this table — do NOT hard-code or restate the mapping here) tells you:

- The **type recipe file**: `diagram-types/<type>.md`
- The **composed `kb/` sub-patterns**: the list of `kb/<pattern>.md` files the type composes
- The **canonical example PNG**: the reference PNG in `examples/`

If Q2 is "Propose options": read the resolved `diagram-types/<type>.md` and the example PNG. Present **2–3 concrete composition candidates** in plain text, each naming the kb sub-patterns it would use and referencing the example. Wait for the user to pick.

If Q2 is "Describe the structure": ask the user in plain text for the nodes, edges, and groupings. A bullet list is fine. Briefly confirm understanding before dispatching.

If Q2 is "Just generate": proceed directly to dispatch — the subagent will infer from the resolved type bundle.

If the initial description lacks crucial detail (which systems are involved, what the diagram is *arguing*), ask one focused plain-text follow-up. Do not over-question — the subagent will fill in reasonable defaults.

### 3. Dispatch to the author (specialist, author mode)

Spawn `excalidraw_specialist` via the `Agent` tool with a single prompt containing:
- The resolved **diagram family** and **type** (e.g. "Tech Architecture / tech-architecture")
- The **absolute path to `diagram-types/<type>.md`** — the specialist must read this file FIRST before consulting any `kb/` primitive
- The **explicit list of `kb/<pattern>.md` files** named in the resolver table row for this type
- The **canonical example PNG** path from the resolver table row (visual ground truth)
- The structure approach (Q2 answer) and the chosen composition, if any
- The user's full description and the *argument* the diagram should make (per the methodology: *Diagrams ARGUE, not DISPLAY*)
- The output **absolute** path (snake_case basename derived from the diagram subject) — saved in the current working directory unless the user requested otherwise
- A reminder that it is in **author mode**: read the type recipe FIRST → generate → write → render → return the absolute `.excalidraw` and `.png` paths. It must NOT attempt to verify.

Capture the absolute `.excalidraw` path the specialist reports back. This path is the single argument every subsequent verify call uses.

### 4. The verify → fix loop (you own this — LOOP-02)

Run **at most 3 verifier invocations total**: the initial verify plus up to 2 fix-and-reverify cycles.

```
author → render → verify(1)  ── passed:true ──► SUCCESS (§5)
                             ── passed:false ─┐
                                              ▼
fix → render → verify(2)  ── passed:true ──► SUCCESS (§5)
                          ── passed:false ─┐
                                           ▼
fix → render → verify(3)  ── passed:true ──► SUCCESS (§5)
                          ── passed:false ──► HONEST-FAILURE (§6)
```

For each attempt N (1, 2, 3):

a. **Verify.** Spawn `excalidraw_verifier` via the `Agent` tool with EXACTLY ONE argument: the absolute path to the `.excalidraw`. Do NOT pass the PNG path — the verifier derives it.

b. **Read the canonical report.** `Read` the sibling `<basename>.verifier-report.json` (replace the `.excalidraw` suffix with `.verifier-report.json`). Parse it as JSON. Do NOT rely on scraping the verifier's chat message — the on-disk file is the canonical channel.
   - **Report file missing** (verifier failed to emit it) → treat as `passed: false` AND count it as one of the 3 attempts. This prevents infinite loops on verifier malfunction.
   - A `verifier_internal_error` issue → same as any error: `passed: false`, attempt consumed.

c. **State the count out loud** so it stays honest across long iterations: *"Verifier attempt N of 3: passed=true|false"*. If you ever lose the count, default to honest-failure on the next failed verify rather than looping further — over-counting is the safe direction.

d. **Branch:**
   - `passed: true` → go to §5 (success).
   - `passed: false` and N < 3 → spawn `excalidraw_specialist` in **fix mode**: pass it the absolute `.excalidraw` path and the full failing `issues` array from the report (verbatim — each issue's `check`, `element_id`, `severity`, `detail`, `suggested_fix`). The specialist mutates the source, re-renders, and returns. Increment N and loop to (a).
   - `passed: false` and N == 3 → go to §6 (honest failure).

The verifier is read-only — never ask it to fix. The specialist is the only fixer — never ask the user to fix manually before the 3 attempts are spent.

### 5. Success delivery

On `passed: true` within 3 attempts, report to the user:
- The absolute path to the rendered, verified `.png` so they can open it.
- A short summary: filename, patterns used, structural choices, any deviations from the chosen composition.
- A quick iteration affordance: *"Want to adjust anything — layout, colors, content, panels?"*

This is the only path on which you may use "done", "verified", or "complete".

### 6. Honest-failure delivery (LOOP-02 part b)

On the 3rd consecutive `passed: false`, your final message MUST take this exact shape, with these exact label tokens (downstream tooling greps for them):

```
Verifier failed after 3 attempts. Not claiming success.

Failed PNG: <absolute path to the latest .png>
Source:     <absolute path to the .excalidraw>
Report:     <absolute path to the latest .verifier-report.json>

Outstanding issues:
- [<severity>] <check>: <detail>
  suggested_fix: <suggested_fix>
- [<severity>] <check>: <detail>
  suggested_fix: <suggested_fix>
...
```

The bulleted list is **verbatim** from the report's `issues` array — every issue, in order, no paraphrasing or omitting "minor" ones. This message MUST NOT contain the tokens **"done"**, **"completed"**, **"successfully"**, or **"ready"**.

## Rules

- **Always ask both questions** (Q1 and Q2), even if `$ARGUMENTS` already has context. The questions sharpen intent and prevent the wrong diagram.
- **Use `$ARGUMENTS` as pre-filled context** when describing the request to the specialist — the user shouldn't have to retype.
- **Do not draw or verify inline.** Authoring/fixing lives in `excalidraw_specialist`; verification lives in `excalidraw_verifier`. You only orchestrate, read the report, and decide.
- **You are the only place the loop can live.** Never instruct the specialist to call the verifier — that spawn is inert inside a subagent.
- **If a subagent is not installed** (Agent tool errors with "unknown subagent type"), tell the user the plugin is missing from `.claude/agents/excalidraw/` and point at the plugin README for install steps.
