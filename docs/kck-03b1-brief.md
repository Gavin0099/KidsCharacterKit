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

**Status: `rejected`** (Owner decision, 2026-10-05): output-contract violation,
eye-highlight violation, distorted comparison, incomplete provenance. Not `superseded`:
it never became an approved baseline. The image itself is not committed; this record,
its SHA-256 and the reason are the evidence that it was tested and rejected.

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

### Canonical prompt v2 (shared part) — superseded by v2b for new generations

This text was the generation instruction used for the first Round 2 attempts. It is kept
unchanged for the record. New generations use v2b below.

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

### Round 2 attempts (all `rejected`)

Four generation attempts were made for A2 Clean. All are `rejected` (Owner decision,
2026-10-05) for **output-contract violation** (the tool produced a three-figure board
instead of one character) **and eye-highlight violation** (large highlight at top-center
or slightly right, not upper-left). Not `superseded`: none became a baseline. The images
are **not committed**; the SHA-256 and reason are the record.

All four: WebP, 2000×667 (about 3:1), RGBA with real transparency. The true-alpha result
is the one requirement they met.

| # | Generation id | External instruction (Owner's intent, not verbatim) | SHA-256 | Result |
|---|---|---|---|---|
| 3 | `a31db5ab-60e9-40c3-add1-a9e012d5c7fa` | full canonical v2 shared prompt + A2 Clean line | `35892949f79f921b5abb3147bd0b4214ba32742bbd23ff9470f8ce8fba7116c8` | three figures + labels |
| 4 | `7f3a42af-3afb-4320-ae2c-2accbe9051a3` | only A2, one dinosaur, transparent, no A3/A4, no text or comparison board | `1a0c0c5cb4137411db8867edd9b7c0868c2bebcd6da6d2a2c007f4f1d1b7e658` | three figures + labels |
| 5 | `de636c4c-93c8-4d95-a044-29240f9468d7` | again: one dinosaur only; no text, labels, columns or other characters | `d844e1564bceef7e96f7661e6fd1b285bb046445637f55ab1c1c54acbd11b476` | three figures, no labels |
| 6 | `4501f2a1-18c7-46ac-bcfd-65c7373dfb46` | retry of single-character A2; no new A3/A4 instruction | `11fcaf4737c99a25765311f264f86ab9bff9847cc45af6d09828bfae87184d45` | three figures, no labels |

Provenance notes:

- The tool call is derived automatically from the conversation. The internal prompt sent
  to the image model is not exposed, so the column above records the instruction given
  *to the tool* as the Owner remembers it, not the text the model received.
- **Attempts 5 and 6 must not be split into A2/A3/A4.** The left, middle and right figures
  visibly look like Clean, Balanced and Handmade, but the three variant lines were never
  supplied separately for those attempts, so labeling the figures A2/A3/A4 afterwards
  would claim provenance that does not exist. No cropped derivative of these images is
  made.

### Round 2b: amended canonical instruction

Round 2b is a precision change. The approved direction (large highlight at the upper
left) is **unchanged**; the instruction is rewritten so it implements the rule
unambiguously, and the composition is locked to one character on a square canvas. Two
changes to canonical prompt v2:

1. **Composition (added after "Produce one isolated full-body character on a true
   transparent background."):**

   > Output exactly ONE dinosaur, centered on ONE square 1:1 canvas. There must be exactly one full-body character in the entire image. Do not show alternatives, variants, panels, side-by-side comparisons, duplicated characters, labels, captions, headings, UI, or text of any kind.

2. **Eye highlight (replaces the bullet "large eye highlight must be visibly at the upper-left of each eye; secondary highlight smaller"):**

   > In each iris/pupil, place the large white highlight clearly inside the **upper-left quadrant**, close to the upper-left edge of the dark eye shape. It must be visibly left of the eye's vertical centerline. Place the smaller secondary highlight below and to the right of the large highlight. Do not place the large highlight at top-center or upper-right.

#### Canonical prompt v2b (shared part) — superseded by v2c for new generations

```text
Use the attached `dinosaur-01` image as the identity reference and strict character reference. Preserve the same dinosaur identity, proportions, silhouette, mint-green body, cream belly with two curved lines, softened yellow back spikes, peach cheeks, large brown eyes, tail, feet, and magnifying glass. Do not redesign the character, do not chibify it further, and do not change its anatomy.

Goal: explore a shared Soft Handmade 2.5D rendering language that can later be translated to Cat and Robot without changing their anatomy.

Shared rendering rules:
- clean dark warm-brown outline with slight controlled hand-drawn variation
- flat base colors
- one soft shadow layer, primarily lower-right
- one restrained soft highlight, primarily upper-left
- very light colored-pencil / paper grain; texture is subtle seasoning, not the rendering method
- In each iris/pupil, place the large white highlight clearly inside the upper-left quadrant, close to the upper-left edge of the dark eye shape. It must be visibly left of the eye's vertical centerline. Place the smaller secondary highlight below and to the right of the large highlight. Do not place the large highlight at top-center or upper-right.
- clean silhouette and edges suitable for a 64 px character
- no cast shadow, no background scene, no text, labels, UI, color palette, model sheet, turnaround, or extra characters

Keep the dinosaur recognizably the same character. Reduce the overly polished digital-sticker feeling while preserving clarity.

Produce one isolated full-body character on a true transparent background.

Output exactly ONE dinosaur, centered on ONE square 1:1 canvas. There must be exactly one full-body character in the entire image. Do not show alternatives, variants, panels, side-by-side comparisons, duplicated characters, labels, captions, headings, UI, or text of any kind.

This output is a style exploration candidate, not production artwork and not an approved character master.
```

The variant lines (A2 Clean, A3 Balanced, A4 Handmade) are unchanged.

#### Generation order and context rule

- **One variant per fresh context.** Each generation starts in a new context that contains
  only: `dinosaur-01`, prompt v2b, and that variant's single line. The words `A3`, `A4`,
  `comparison` and `three variants` must not appear in that context.
- Order: A2 Clean → validate → (new context) A3 Balanced → validate → (new context) A4
  Handmade → validate. A failed validation stops the sequence; the next variant is not
  started.
- Keep the generation id of every attempt, including failures.

#### Validation after each generation

Each output is checked before the next variant starts:

1. **One character** in the whole image (no board, panels or duplicates; no text).
2. **True alpha** (transparent background, no matte).
3. **Eye highlight:** large highlight in the upper-left quadrant of each eye, left of its
   vertical centerline; smaller one lower-right of it. *(Replaced by the measurable gate
   in Round 2c below.)*
4. **Identity:** still recognizably `dinosaur-01` (silhouette, proportions, anatomy).
5. **Variant intensity:** texture/line variation matches the variant line and visibly
   differs from the other variants.

Any failure is recorded as a `rejected` attempt (generation id, SHA-256, reason).

### Round 2b attempt 1 (A2 Clean): `rejected`

One generation, made in a fresh context with only `dinosaur-01`, prompt v2b and the A2
line (the instruction is exactly the canonical v2b text followed by the A2 line; checked
against the pasted instruction). Decision (Owner, 2026-10-05): **`rejected`**.

| | |
|---|---|
| Generation id | `91d29f39-c8ee-4693-8302-4e17c26fd4e9` |
| Input | `dinosaur-01` only (no Cat, Robot or other reference) |
| Original generation artifact | PNG, RGBA, 1254×1254, SHA-256 `5d5df835d1b8a8d72bf0e35e6d42dcd3c906cf3f06f9e1a33b492489d2f2aa9e` (reported by the Owner; not in this repo; not verified here) |
| Platform-delivered copy | WebP, 1254×1254, SHA-256 `7393a0672eb5b069e4163547de30855aa796931dd1d1af20862210e785810887` (the file that was measured) |

Reasons for rejection:

1. **Eye-highlight geometry gate failed.** Measured on the delivered copy, as fractions of
   each dark eye shape's bounding box (0 = left/top edge, 1 = right/bottom edge):

   | Eye | Large highlight (x, y) | Small highlight (x, y) |
   |---|---|---|
   | left | 0.562, 0.272 | 0.644, 0.617 |
   | right | 0.538, 0.264 | 0.627, 0.604 |

   The large highlight sits at the center-top, slightly right of the vertical centerline
   (target x ∈ [0.30, 0.40], measured 0.54–0.56). The vertical position (y) is within
   range and the small highlight is below and to the right of the large one in both eyes.
2. **Provenance gap, fixed by a rule (below):** the original generation artifact and the
   delivered copy are different encodings, and only one of them was measured.

The other four checks passed:

- **One character:** single 1:1 canvas (1254×1254), one connected figure, no text or labels.
- **True alpha:** corners fully transparent; character interior alpha 251–254 (not 255).
- **Identity:** visible-bounds aspect 0.886 vs 0.890 for `dinosaur-01`; mint body, cream
  belly with two lines, yellow back spikes, peach cheeks, magnifying glass, tail and feet kept.
- **Variant intensity:** surface texture is nearly absent, as A2 requires (forehead
  high-frequency energy 0.22 vs 1.51 in the source).

So the only uncontrolled factor left is the highlight position.

### Round 2c: measurable eye-highlight rule

The approved direction (large highlight at the upper left) is **unchanged**. "Upper-left"
and "visibly left of the centerline" were too loose to generate or check, so the rule is
restated as coordinates. This is an implementation precision, not a style change.

**Generation target (replaces the v2b highlight bullet):**

> Treat the dark eye shape as a box from 0% to 100%. The center of the large white highlight should be around 35% from the left edge and 25% from the top edge. Acceptable generation target: x=30–40%, y=20–35%. It must remain clearly left of the eye centerline. The smaller highlight must be lower and to the right of it.

**Validation (replaces check 3), applied to each eye:**

```text
large highlight center:   x in [0.30, 0.40] of eye width
                          y in [0.20, 0.35] of eye height
small highlight:          x > large.x   and   y > large.y
```

Both eyes must pass.

**Measurement method (so it is reproducible):** the eye is the filled connected dark-brown
region; its bounding box is the 0–1 frame; the highlights are near-white blobs inside it;
a highlight's center is its centroid. State which copy (original or delivered) was
measured.

#### Canonical prompt v2c (shared part)

```text
Use the attached `dinosaur-01` image as the identity reference and strict character reference. Preserve the same dinosaur identity, proportions, silhouette, mint-green body, cream belly with two curved lines, softened yellow back spikes, peach cheeks, large brown eyes, tail, feet, and magnifying glass. Do not redesign the character, do not chibify it further, and do not change its anatomy.

Goal: explore a shared Soft Handmade 2.5D rendering language that can later be translated to Cat and Robot without changing their anatomy.

Shared rendering rules:
- clean dark warm-brown outline with slight controlled hand-drawn variation
- flat base colors
- one soft shadow layer, primarily lower-right
- one restrained soft highlight, primarily upper-left
- very light colored-pencil / paper grain; texture is subtle seasoning, not the rendering method
- Treat the dark eye shape as a box from 0% to 100%. The center of the large white highlight should be around 35% from the left edge and 25% from the top edge. Acceptable generation target: x=30–40%, y=20–35%. It must remain clearly left of the eye centerline. The smaller highlight must be lower and to the right of it.
- clean silhouette and edges suitable for a 64 px character
- no cast shadow, no background scene, no text, labels, UI, color palette, model sheet, turnaround, or extra characters

Keep the dinosaur recognizably the same character. Reduce the overly polished digital-sticker feeling while preserving clarity.

Produce one isolated full-body character on a true transparent background.

Output exactly ONE dinosaur, centered on ONE square 1:1 canvas. There must be exactly one full-body character in the entire image. Do not show alternatives, variants, panels, side-by-side comparisons, duplicated characters, labels, captions, headings, UI, or text of any kind.

This output is a style exploration candidate, not production artwork and not an approved character master.
```

The variant lines (A2 Clean, A3 Balanced, A4 Handmade) and the one-variant-per-fresh-context
rule are unchanged. v2c differs from v2b only in the highlight bullet.

### Original generation artifact vs platform-delivered copy

The platform can re-encode what it shows (here PNG → WebP). A hash of the delivered copy is
not the hash of what the generator produced. Rules:

- **Generation output** = the original artifact the tool produced. Record its format and
  SHA-256 as reported by the Owner (the Owner's side holds it), and note that the
  repository did not verify it unless the original file is supplied.
- **Delivered copy** = any re-encoded or re-exported copy (for example the WebP shown in
  chat). It is a separate record with its own SHA-256 and says how it was obtained.
- A validation or measurement states **which copy it was run on**. The geometric gates are
  binding on the original artifact; a result on a delivered copy is indicative. If only a
  delivered copy reaches the repository, the record says no original is verifiable here.
- A conversion made inside this repository is a derived copy with its own record. It never
  replaces the generation-output hash.
- Per output, the Owner brings: generation id, original artifact format and SHA-256, the
  exact instruction, and the input SHA-256.

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
