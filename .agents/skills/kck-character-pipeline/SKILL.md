---
name: kck-character-pipeline
description: Prepare and review KidsCharacterKit raster candidates and short sprite sequences with source hashes, shared scale, explicit ground anchors and QA previews. Use for KCK asset review and motion preparation; consumer gameplay and procedural motion stay in the app.
---

# KidsCharacterKit character pipeline

Work from the calling checkout. Read `PLAN.md`, `GOVERNANCE.md`, the active exploration brief and `docs/character-representation-contract.md` before choosing the mode. See `docs/character-pipeline.md` for CLI commands, the QA recipe and source/license details. Paths below are relative to the repository root.

## Candidate review

Use `python .agents/skills/kck-character-pipeline/scripts/pipeline.py review` to produce a labeled checker/white/black contact sheet, small-scale view and raw/RGBA hashes. These are QA artifacts; do not feed a comparison sheet back to the generator. Structural QA does not approve identity, style, ownership or rights. Continue using the existing `concepts/kck-03b1/tools/measure_output.py` and separate visual gates for Dinosaur V2.

## Short motion preparation

Once the selected master, Style Bible and required model sheets have the applicable Owner acceptance, use one approved seed and request a short strip in one edit job. Preserve identity, rendering, facing, palette, proportions and required props. State exact frame count and layout. Ground every job in the selected source; retain raw generator output, held-input gate evidence and the exact instruction. Use the installed `imagegen` skill for generation unless the Owner has specified another route.

The current 03B1 exact-input handoff and attempt budget remain authoritative. Check the current ledger; installation of this skill is not a retry or budget reset. Do not substitute a strip canvas for the two frozen 03B1 source objects. A failed hard gate stops that generation sequence. Resolve actual visual decisions with the Owner after preparing a concrete review artifact.

## Existing-frame sequence QA

Use `split-strip` for an existing source-verified horizontal strip with explicit equal-width slots; it preserves each slot's full RGBA rectangle. Use `normalize` only for a candidate QA recipe with supplied source hashes, durations, semantic anchors, one explicit global scale and a target anchor. The tool neither infers standing points from alpha bounds nor fits frames individually. Keep the snack on a separate layer/socket as defined by the later motion contract. It rejects clipping and overwriting, and produces an APNG with declared timing. `check` validates the prepared bundle read-only, including pixel/timing replay.

The recipe is an internal preparation format, not the approved 03C animation representation contract. Outputs stay under `artifacts/qa/` or `concepts/`; no manifest availability or master promotion occurs. Preview contact sheets/APNGs are never delivery assets. Inspect the preview at game scale, then obtain consumer-scene evidence for ground contact, pivot, timing and prop handoff before motion delivery.

## Reuse boundaries

The bundled checker/contact-sheet and animated preview routines adapt OpenAI `hatch-pet` at the commit recorded in `scripts/hatch_pet/SOURCE.json`; retain its Apache-2.0 license and change notices. No pet atlas, fixed state list, chroma key or per-frame auto-fit is used. The strip-first workflow draws on the published `sprite-pipeline` method; its code is not vendored. Do not install ComfyUI, background-removal models or global skills as a side effect.
