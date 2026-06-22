---
type: seed
status: open
created: 2026-06-07
source: /gsd-explore session
related_milestone: v1.1 (or later)
---

# Seed: Replace author-path example PNGs with composition-spec text

## The idea

Replace the `examples/*.png` references in the **author path** (excalidraw_specialist)
with a structured **composition-spec `.md` per example**. Keep the `.excalidraw` sources
as exact ground truth. Drop the rastered PNGs from what the *author* reads.

Chosen approach: **composition-spec text per example** (one `.md` describing layout,
density, palette-in-use, labeling rhythm, and which kb patterns combine).

## Why — the findings that motivated it

Explored five questions: are the example PNGs useful, what do they cost, what can the
model learn from them, would text be better, and how the model "looks" before writing.

1. **Token cost is real but capped.** Anthropic auto-resizes any image >~1.15 MP before
   the model sees it. The example PNGs are 4.8–18.7 MP (e.g. data_pipeline_flow is
   6000×3120). Each Read lands at **~1,500 tokens** regardless of original size. The
   author may Read 1–2 per diagram.

2. **At the capped resolution, fine detail is unreadable.** A 6000×3120 diagram becomes
   ~1480×770 by the time the model sees it. The author gets **composition / color /
   arrow-style gestalt** but CANNOT read most labels or extract coordinates. The detail
   the diagrams were authored with is literally downsampled away.

3. **The verifier never uses the examples.** `excalidraw_verifier.md` lines 44 & 54
   explicitly forbid cross-referencing any canonical render: "Apply per-diagram absolute
   judgment ONLY." Its 5 visual checks (text_overflow_visual, arrow_disconnected_visual,
   icon_blank, missing_glyph_box, layout_collision) are self-contained defect detection on
   the diagram-under-review's own PNG. So the examples benefit ONLY the author — the
   initial intuition that "the verifier needs the visual ground truth" was backwards.

4. **Redundancy is partial.** `kb/*.md` already encode geometry + JSON skeletons;
   `examples_excalidraw/*.excalidraw` already hold exact coordinates, labels, structure.
   The PNG's *only* unique contribution is the composition gestalt — which a text spec can
   encode at full fidelity, greppable, and cheaper.

## Conclusion

Replacing author-path PNGs with text loses little and the verifier loses nothing (it never
read them). The one genuinely vision-ish thing — "match layout density and labeling
rhythm" (specialist mandate #2) — can be made *explicit* in a composition spec rather than
left implicit in a raster, which arguably improves the house style by documenting it.

## Proposed scope (when promoted to a phase)

1. Author `examples/<name>.md` composition-spec per example. Shape:
   ```
   ---
   layout: 3 panels side-by-side + evidence strip on top + persona example below
   density: ~5 nodes/panel, depth 2-3
   palette: primary blue panels, violet trace across facets
   rhythm: icon+title top-left per container
   composes: multi-zoom-overview, group-container, icon-block, tree-hierarchy, evidence-card
   ---
   <prose elaborating the gestalt the PNG used to convey>
   ```
2. Update `kb/README.md` reference-example index, `kb/*.md` "See in examples" sections,
   `diagram-types/*.md` "Ground truth" links, and specialist mandate #2 + `<asset_paths>`
   to point at the `.md` spec (and optionally the `.excalidraw` source for exact coords)
   instead of the PNG.
3. Decide the fate of the PNGs: keep on disk as human reference / for refreshing specs, but
   remove from the *author's read path*. Verifier already ignores them.

## Open questions before promoting

- Keep PNGs on disk (human reference) or delete entirely?
- Author the composition specs by hand, or have a one-time agent pass generate a draft
  from each `.excalidraw` source + its PNG, then hand-edit?
- Does this fit inside v1.1 or land as a v1.2 cleanup phase? (v1.1 is mid-execution at
  Phase 06.)
