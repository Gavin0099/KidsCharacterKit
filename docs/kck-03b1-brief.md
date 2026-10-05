# KCK-03B1 brief: unified-style concept exploration

**Status: brief for the owner-run generation work (KCK-03B1).** It records decisions
the Owner stated in session on 2026-10-05 so they exist in the repo
([GOVERNANCE.md](../GOVERNANCE.md) rule 1). Everything produced under this brief is a
`candidate`. No artwork is added by this PR.

## Question this slice answers

> After Cat, Dinosaur and Robot are redrawn in the shared rendering language, are they
> still recognizably themselves, and do they look like they live in the same world
> (same IP)?

It does not produce production assets, model sheets, animations or 3D. It ends at the
lineup gate (B1-C); the next step needs a new Owner decision.

## Owner decisions recorded here (stated in session)

- Run B1 as **three checkpoints**, not one generation of all three characters
  (image models tend to contaminate characters with each other: a chubby Robot, Cat
  with Dinosaur eyes, Dinosaur with Cat texture).
- The **Dinosaur is the style anchor**: used as the **rendering reference**, not as an
  identity reference. Reason: reads well small, animates easily, clear silhouette,
  converts to 3D easily, lower production cost than the Cat's fur detail, more
  "product" than the pure-crayon Robot.
- The Dinosaur itself is also adjusted a little (see B1-A), so the anchor is a new
  shared style, not the current Dinosaur art unchanged.
- **Unify rendering language, not anatomy.** Do not make everyone big-head/short-limb.

These do not change the approved direction in the
[style bible](character-style-bible.md) ("Soft Handmade 2.5D", Robot proportion
exception). The values below are a starting brief and may be adjusted after B1-A.

## Checkpoints

### B1-A: Dinosaur style key
Input: `dinosaur-01` (rendering and identity).
Goal: soften the digital polish; add a little controlled handmade texture; keep the
current silhouette and proportions; avoid over-glossy, sticker-like finish.
Output: the new shared style anchor (candidate).

### B1-B: Cat and Robot translation (one character per generation)
- **Cat:** inputs = `cat-02` (identity) + B1-A output (rendering reference). Keep Cat
  identity and anatomy; adopt the anchor's rendering system.
- **Robot:** inputs = `robot-01` (identity) + B1-A output (rendering reference).
  **Do not chibify the robot.**

### B1-C: lineup gate
The three side by side. One question for the Owner: *does it look like the same IP?*
Pass → formal turnaround/model sheets can start (a new slice). Fail → iterate B1-A/B.
Pass/fail is the Owner's decision.

## B1-A round 2: canonical generation brief

### Round 1 (not committed)

A first B1-A sheet was generated on 2026-10-05 (single composite image, 1536×1024 WebP,
SHA-256 `19e3b7889ddaec05d361e9e0756eb9036ac82382ceea685c3d39e6b954e12095`). It is
**not in this repository** and is not a style anchor. Why:

- The large eye highlight was drawn at the upper right although labeled "upper-left", so
  it contradicts the approved direction and rule 4.
- The four variants (A1–A4) were nearly indistinguishable, so it did not test a style
  range. Its "A1 Current Reference" was a regenerated copy, not the repository file.
- It was a presentation board (labels, palette, tagline, turnaround, expressions), not
  clean art, and its "Recommended" label has no governance effect.
- Provenance was incomplete (see Provenance limitation).

Whether this sheet is later marked `rejected` or `superseded` is decided by the Owner
after round 2.

### Owner decisions for round 2 (stated in session, 2026-10-05)

1. **Eye highlight rule is unchanged**: large highlight at the upper left, smaller
   secondary highlight. The style bible is not edited to fit a wrong output; the image is
   redone.
2. **Spread the variants on purpose**: three candidates that differ visibly even at
   thumbnail size.
3. **A1 is the repository file**: `dinosaur-01` (SHA-256
   `1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76`), used directly. No
   regenerated stand-in.
4. **No variant is selected.** Everything from round 1 and round 2 stays `candidate`.

### Inputs and outputs

- Input (only): `dinosaur-01` / DinosaurResearcher, SHA-256 above.
- Output: **one isolated full-body character per variant, as its own transparent PNG.** No
  comparison board, turnaround, expressions, palette, tagline or "Recommended" text.
- If the tool cannot return true alpha, record how the background was removed: that is a
  modification with its own provenance entry, not a silent step.
- Lineup review after generation: A1 (repo original) + A2 + A3 + A4. Only then does the
  Owner consider choosing a style anchor.

### Canonical prompt (shared part)

This text is the generation instruction given to the image generator. It is recorded in
full as the canonical brief.

```text
Use the attached `dinosaur-01` image as the identity reference and strict character reference. Preserve the same dinosaur identity, proportions, silhouette, mint-green body, cream belly with two curved lines, softened yellow back spikes, peach cheeks, large brown eyes, tail, feet, and magnifying glass. Do not redesign the character, do not chibify it further, and do not change its anatomy.

Goal: explore a shared Soft Handmade 2.5D rendering language that can later be translated to Cat and Robot without changing their anatomy.

Shared rendering rules:
- clean dark warm-brown outline with slight controlled hand-drawn variation
- flat base colors
- one soft shadow layer, primarily lower-right
- one restrained soft highlight, primarily upper-left
- very light colored-pencil / paper grain; texture is subtle seasoning, not the rendering method
- large eye highlight must be visibly at the upper-left of each eye; secondary highlight smaller
- clean silhouette and edges suitable for a 64 px character
- no cast shadow, no background scene, no text, labels, UI, color palette, model sheet, turnaround, or extra characters

Keep the dinosaur recognizably the same character. Reduce the overly polished digital-sticker feeling while preserving clarity.

Produce one isolated full-body character on a true transparent background.

This output is a style exploration candidate, not production artwork and not an approved character master.
```

### Variant line (the only part that changes)

| Variant | Appended line |
|---|---|
| A2 Clean | `Use almost no visible surface texture; prioritize clean graphic readability.` |
| A3 Balanced | `Use subtle visible handmade grain and slight line variation, balanced with clean mobile-game readability.` |
| A4 Handmade | `Push the handmade pencil/paper character noticeably further than A3, while keeping edges clean and avoiding dense crayon hatching.` |

### Provenance limitation (honest record)

The tool is ChatGPT's built-in image generation (`image_gen`). Per the Owner, it returns a
generation id but **no model name, version or seed**, and it does not expose the internal
prompt it actually sends to the image model; it derives that from the conversation. So an
"exact full internal prompt" cannot be recorded. What this repository records instead is
the **user-provided generation instruction** above (verbatim), the tool name, the
generation id, the input SHA-256 and the output SHA-256, with the limitation stated in
each record. Records say "instruction given to the tool", never "the prompt the model
saw".

## Shared rendering rules (starting brief)

1. **Outline:** all three dark warm brown, similar weight (not Cat light brown, Dinosaur
   dark brown, Robot black).
2. **Coloring:** flat base + one soft shadow + one soft highlight. No multi-layer fur
   gradients, no all-over crayon hatching, no smooth full gradients mixed together.
3. **Texture:** only a very light colored-pencil / paper grain. Texture is seasoning,
   not the rendering method.
4. **Eye system:** same rules, per-character shape: large upper-left highlight, small
   secondary highlight, dark warm pupil, same gloss treatment. Cat may keep an iris,
   Dinosaur large round eyes, Robot black ovals (slightly larger than now, not
   Dinosaur-sized).
5. **Lighting:** from the upper left: soft highlight upper-left, very soft shadow
   lower-right. No ambient scene lighting, no cast shadow.
6. **Edge quality:** clean silhouette with controlled hand-drawn character, not vector
   vs watercolor vs crayon scan.

## Identity locks (what must not change)

| Character | Keep |
|---|---|
| Cat (`cat-02`) | orange tabby, round face, large round eyes, raised paw, pink paw pad, long tail |
| Dinosaur (`dinosaur-01`) | mint body, cream belly with curved lines, soft-yellow back spikes, magnifying glass, peach cheeks |
| Robot (`robot-01`) | rectangular head, long arms and legs, antennae, blue mitten hands and boots, four-shape chest panel, tongue, gray body |

Cat changes (translation): thicker dark-brown outline; fur rendered as shapes, not
strands; tabby stripes as larger color blocks; much less fur texture; simplified volume;
Dinosaur-style highlight treatment; the shared peach/coral cheeks; one soft shadow layer.

Robot changes (translation): keep a slightly imperfect, hand-drawn feel (a little
wobble, not perfectly symmetric) but outline dark brown instead of black, clean base
color plus very light grain instead of dense hatching.

## Pass criteria for the lineup (Owner judges)

- Same-world test: do they look like one illustrator's toys?
- All-black silhouette test: each still identifiable at 64 px.
- Identity test: each still clearly the original character.
- Palette: Cat warm orange, Dinosaur mint, Robot cool gray + blue stay distinct.

## Provenance and status requirements

Per [GOVERNANCE.md](../GOVERNANCE.md): every output is a `candidate` until the Owner
approves it, and is not a character master.

Where the tool hides its internal prompt, see "Provenance limitation" above for what is recorded instead.

For each output, record: the input assets with their SHA-256 (the repo records for
`cat-02`, `dinosaur-01`, `robot-01` already hold these), the generation tool
(and version if known), the full prompt, and the output file's SHA-256. Rights status is
`pending`; derived artwork inherits the unresolved status of its inputs
(`dinosaur-ref-02` origin Unknown; all commercial-use statuses `pending`).

A formal `status` field is added to the provenance schema in the PR that brings the
first concept record into the repo, not before.

Proposed location (to confirm when the first output arrives):
`concepts/kck-03b1/<stage>-<character>-vNN.png` with a matching record, kept outside
`characters/` so a concept is never mistaken for a character master.

## Out of scope

No raster normalization (03B), no animation (03C), no 3D (03D), no turnaround or model
sheets, no changes to `characters/`, the manifest or the five existing records, no
claim that any output is approved.

## Handoff: what to bring back per checkpoint

1. The output image(s).
2. The exact prompt and the tool used.
3. Which input images were attached (cat-02 / dinosaur-01 / robot-01 / B1-A output).
4. Anything rejected and why (kept as `rejected` history if useful).
