# Visuals and media

Before drafting, review every substantive section: **which part would become easier to understand if the learner could see it?** Identify multiple distinct visual opportunities throughout the file—concept, difficulty, required labels, format, and placement. A visually rich substantial note often offers **4–8** useful image opportunities as a starting point; a full lab often offers **7–10** substantive visuals, or **10–15** for complex investigations. These are planning guides, not forced quotas or ceilings.

Count downloaded web images separately from native Mermaid diagrams, Markdown tables, and video frames. Several Mermaid diagrams or tables do not satisfy a need for downloaded web figures. A long, visually rich note with zero downloaded web images must receive explicit review before completion. Never use decorative photos, logos, repeated icons, or unrelated screenshots to satisfy visual coverage.

Choose native Mermaid for flows, dependencies, decisions, sequences, and states; an inspected local raster image for geometry, function curves, distributions, apparatus, molecular structures, architectures, decision boundaries, and empirical plots; and a Markdown table for exact values, traces, comparisons, and measurements. Do not create or download SVG assets, export Mermaid to SVG, generate pictures, or build HTML viewers or rendering programs.

## Native Mermaid

Write fenced `mermaid` blocks. Use `flowchart TD` or `flowchart LR` for flows, and sequence or state diagrams when they fit. Name the question, select components, define arrow meaning, then draw one clear relationship. Quote node labels, use meaningful edge labels and direction, and use Unicode notation instead of raw LaTeX. Explain the main path, important branch or loop, and connection to the lesson in prose after the diagram. Split crowded diagrams into overview and detail. Do not use Mermaid to replace a numerical plot, photograph, or geometry figure it cannot represent accurately. Check syntax manually; report rendering unverified until observed.

## External raster image: completion workflow

An image-search result, source-page URL, planned filename, or remote Markdown embed is not a completed image. Track `Needed → Candidate found → Source checked → Downloaded → Local image inspected → Embedded → Saved embed checked`; only the last state completes the local-image requirement.

1. **Identify purpose & find candidate.** Name the teaching question the figure answers, then use available web or image-search tools.
2. **Open source & inspect actual figure.** Open the source page and inspect the actual figure. Prefer identifiable educational, scientific, institutional, documentation, or creator sources. Check relevance, notation, labels, and reuse/attribution information; do not infer rights or a file URL from a thumbnail. Honor source-only limits.
3. **Confirm acquisition & download.** Download a supported raster file (`.png`, `.jpg`, `.jpeg`, `.webp`) using an available download tool or standard file-download command where permitted; do not write a custom downloader, inline program, or script. If acquisition fails, try another suitable source rather than silently abandoning the visual; if no tool can save the asset, report the precise limitation.
4. **Save in authorized local asset directory.** Use a descriptive, non-colliding filename beneath `assets/scriptorium/<collection-slug>/` in the authorized vault or preview. Keep actual format and extension aligned; never accidentally overwrite an existing asset.
5. **Inspect the saved file.** Open the local file with an image-inspection tool (`read_file` or viewer). Confirm it is a valid image (not an HTML error page), complete and readable, matches the intended concept, and retains legible axes, units, arrows, and legends.
6. **Embed and teach around the image.** Embed the actual vault-relative path `![[assets/scriptorium/<collection-slug>/<descriptive-name>.png]]` (or matching extension) near its first point of need, with a descriptive caption, source link, and appropriate attribution. Compose the surrounding explanation **after** inspecting the saved image using **Orient → Show → Explain → Work through → Connect**:
   - **Orient:** Introduce the question the image helps answer.
   - **Show:** Embed the inspected image near the first point of need.
   - **Explain:** Decode its labels, axes, components, and relationships; align explanation with the figure's actual notation (or explain notation differences explicitly rather than mislabeling it).
   - **Work through:** Walk through a concrete example using what is visible in the figure, then state the conclusion.
   - **Connect:** Bridge to the next concept or step.
   Never insert an image between unrelated paragraphs or write "as shown above" without explaining what matters. Keep external reference figures distinct from a lab's own experimental evidence.
7. **Reopen the saved note.** Check the saved Markdown to confirm the embed, existing local target, caption, source, explanation, and placement. Inspect Obsidian rendering when available; otherwise report only local-file and Markdown checks, with rendering unverified.

Never create a fake local asset, insert uninspected remote embeds, or claim an image was inspected when it was not. For video, distinguish transcript access from inspected frames, attach timestamps only to locatable segments, and report narrower access states honestly.
