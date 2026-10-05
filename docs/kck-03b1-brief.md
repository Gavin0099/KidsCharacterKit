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
  only: `dinosaur-01`, the current canonical prompt (v2d from Round 2d on), and that
  variant's single line. The words `A3`, `A4`, `comparison` and `three variants` must not
  appear in that context.
- **Clarification (Owner, 2026-10-05):** the fresh-context exclusion applies to surrounding
  task/context content and additional variant instructions. Literal words appearing inside
  the canonical prompt solely as negative output constraints (for example "variants",
  "side-by-side comparisons") are exempt.
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
   in Round 2c, then split into eye identity and eye style gates in Round 2d.)*
4. **Identity:** still recognizably `dinosaur-01` (silhouette, proportions, anatomy).
5. **Variant intensity:** texture/line variation matches the variant line and visibly
   differs from the other variants. *(Reported and Owner-judged, not an automated hard gate,
   from Round 2d on.)*

Any failure is recorded as a `rejected` attempt (generation id, SHA-256, reason).

### Round 2b attempt 1 (A2 Clean): `rejected`

One generation, made in a fresh context with only `dinosaur-01`, prompt v2b and the A2
line (the instruction is exactly the canonical v2b text followed by the A2 line; checked
against the pasted instruction). Decision (Owner, 2026-10-05): **`rejected`**.

| | |
|---|---|
| Generation id | `91d29f39-c8ee-4693-8302-4e17c26fd4e9` |
| Input | `dinosaur-01` only (no Cat, Robot or other reference) |
| Original generation artifact | PNG, RGBA, 1254×1254, SHA-256 `5d5df835d1b8a8d72bf0e35e6d42dcd3c906cf3f06f9e1a33b492489d2f2aa9e`. Format, size and hash were re-checked on the generation side (the Owner's assistant, which holds the file) and match the earlier report. The file was not supplied to this repository's session, so this session did **not** verify it itself. Not committed (the attempt is rejected). |
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

   **Re-measurement on the original PNG** (done on the generation side, same method):
   left eye large highlight x ≈ 0.562, y ≈ 0.272; right eye x ≈ 0.537, y ≈ 0.264. This
   matches the delivered-WebP result to within about 0.001. Conclusion: the highlight
   failure is present in the generation artifact itself; PNG → WebP re-encoding did not
   move it.
2. **Provenance gap, fixed by a rule (below):** the original generation artifact and the
   delivered copy are different encodings, and at first only the delivered copy had been
   measured. **Resolved:** the geometry was then re-measured on the original PNG (on the
   generation side) and matches the delivered WebP result (below), so the failure is in the
   generation artifact itself, not introduced by platform re-encoding. The rule stays so
   the question never has to be re-argued.

The other four checks passed:

- **One character:** single 1:1 canvas (1254×1254), one connected figure, no text or labels.
- **True alpha:** corners fully transparent; character interior alpha 251–254 (not 255).
- **Identity:** visible-bounds aspect 0.886 vs 0.890 for `dinosaur-01`; mint body, cream
  belly with two lines, yellow back spikes, peach cheeks, magnifying glass, tail and feet kept.
- ~~**Variant intensity:** surface texture is nearly absent~~ **INVALID MEASUREMENT /
  codec-confounded** (corrected 2026-10-05, see Round 2d). The comparison used a lossy WebP
  copy against the lossless PNG source; lossy re-encoding alone lowers the metric.

Correction: the statement "the only uncontrolled factor left is the highlight position" is
withdrawn. Variant intensity was not actually established, and the highlight failure is
explained by a specification conflict (Round 2d). The attempt stays `rejected`.

### Round 2c: measurable eye-highlight rule

The approved direction (large highlight at the upper left) is **unchanged**. "Upper-left"
and "visibly left of the centerline" were too loose to generate or check, so the rule is
restated as coordinates. This is an implementation precision, not a style change.

**Generation target (replaces the v2b highlight bullet):**

> Treat the dark eye shape as a box from 0% to 100%. The center of the large white highlight should be around 35% from the left edge and 25% from the top edge. Acceptable generation target: x=30–40%, y=20–35%. It must remain clearly left of the eye centerline. The smaller highlight must be lower and to the right of it. Do not place the large highlight at top-center or upper-right.

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

#### Canonical prompt v2c (shared part) — SUPERSEDED BEFORE ANY VALID ATTEMPT (specification conflict); use v2d

```text
Use the attached `dinosaur-01` image as the identity reference and strict character reference. Preserve the same dinosaur identity, proportions, silhouette, mint-green body, cream belly with two curved lines, softened yellow back spikes, peach cheeks, large brown eyes, tail, feet, and magnifying glass. Do not redesign the character, do not chibify it further, and do not change its anatomy.

Goal: explore a shared Soft Handmade 2.5D rendering language that can later be translated to Cat and Robot without changing their anatomy.

Shared rendering rules:
- clean dark warm-brown outline with slight controlled hand-drawn variation
- flat base colors
- one soft shadow layer, primarily lower-right
- one restrained soft highlight, primarily upper-left
- very light colored-pencil / paper grain; texture is subtle seasoning, not the rendering method
- Treat the dark eye shape as a box from 0% to 100%. The center of the large white highlight should be around 35% from the left edge and 25% from the top edge. Acceptable generation target: x=30–40%, y=20–35%. It must remain clearly left of the eye centerline. The smaller highlight must be lower and to the right of it. Do not place the large highlight at top-center or upper-right.
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
- A validation or measurement states **which copy it was run on and who ran it**. The
  geometric gates are binding on the original artifact; a result on a delivered copy is
  indicative. The party that holds the original may run the measurement (same method) and
  report it. If only a delivered copy reaches the repository, the record says no original
  is verifiable here, and a hash or measurement reported from the generation side is
  recorded as reported, not as verified by this repository.
- **Rejected attempts keep evidence, not images:** generation id, original-artifact and
  delivered-copy hashes, measurements and reasons are enough. The image files are not
  committed, so the repository does not accumulate failed outputs.
- A conversion made inside this repository is a derived copy with its own record. It never
  replaces the generation-output hash.
- Per output, the Owner brings: generation id, original artifact format and SHA-256, the
  exact instruction, and the input SHA-256.

### Round 2d: resolve the specification conflict

#### Owner decision (stated in session, 2026-10-05)

The position of the eye highlights is a **style override, not a dinosaur identity feature.**
Stated rationale: A2 exists to find a shared Soft Handmade 2.5D rendering language for
Dinosaur, Cat and Robot. Eye shape, size, spacing, dark-brown color and placement on the face
can be identity; where the specular highlight sits on the eyeball is lighting/rendering
language. Locking it as identity would forbid A2 from changing it, which contradicts the
purpose of a shared rendering rule.

#### Evidence: the base already has the "wrong" highlight position

Large-highlight center as a fraction of each dark eye shape (0 = left/top edge), same
method as Round 2c:

| Image | Left eye (x, y) | Right eye (x, y) | Copy measured |
|---|---|---|---|
| `dinosaur-01` (base) | 0.596, 0.293 | 0.576, 0.285 | original PNG |
| Round 2b A2 attempt | 0.562, 0.272 | 0.538, 0.264 | delivered WebP |
| unregistered attempt (below) | 0.586, 0.284 | 0.549, 0.275 | delivered WebP (non-binding) |

The generator moved the highlight only slightly left of the base. The best-supported reading
is a **prompt conflict**: the instruction told it to treat `dinosaur-01` as a strict
identity reference and also to move that reference's highlight to x = 0.30–0.40. The earlier
hypothesis that the generator has a persistent right/center bias is **withdrawn**; it is not
supported until the conflict is removed.

#### Status of earlier items

| Item | Status |
|---|---|
| Prompt v2c | **SUPERSEDED BEFORE VALID ATTEMPT / specification conflict.** Not a failure and not a protocol deviation. v2c attempts consumed: **0 of 2**. |
| Generation `e1acb811-2a91-46fc-8fe9-9f60d2a2856f` | **UNREGISTERED / protocol deviation.** Does not consume budget. |
| Texture "PASS" on delivered WebP copies (both A2 images) | **INVALID MEASUREMENT / codec-confounded.** Not a FAIL. |
| Round 2b A2 attempt (v2b) | stays `rejected`; cause note: the same specification conflict. |

The unregistered generation `e1acb811…`, as reported from the generation side:

- Not a fresh context (made inside an existing project conversation).
- Input image attached was SHA-256 `332e8c94af3ff582230bfbf9b0fcb16c02a8f77273489206fb7bead6afa3ea01`
  (PNG 1269×952), **not** `dinosaur-01`.
- `A2_instruction_v2c.txt` was not attached; the text was paraphrased and re-ordered.
- Original generation artifact: PNG, RGBA, 1254×1254, SHA-256
  `4277e5316e9b14f94a6e7d8fc19c25c4aaa8e8d57c6aeb094b8facddf5056a35` (generation-side
  report; not supplied to this repository, not verified here).
- Delivered copy: WebP, 1254×1254, SHA-256
  `6e0d0689f67ae909e0e091e1c2f44868b4a43110aa41d026418015ca1b85a8c9`.
- The official gate script was not run on the original at generation time.
- Measurements on the delivered copy are non-binding and are **not** used as evidence about
  generator behavior.

Why the texture result is invalid: re-encoding `dinosaur-01` itself as lossy WebP (quality
75, 80, 90) drops the forehead high-frequency measure from 1.514 to 0.39–0.43; lossless
WebP leaves it at 1.514. The two A2 images measured 0.22 and 0.51 on lossy WebP. Those
values are not inside 0.39–0.43 and are therefore **not explained by that control alone**.
The demonstrated point is narrower: codec choice materially changes this proxy, so a
cross-encoding comparison (lossy WebP output vs lossless PNG base) cannot isolate texture
change.

#### Canonical prompt v2d (shared part)

v2d is v2c plus one sentence at the start of the eye-highlight bullet (verified by script).
No other word changes.

```text
Use the attached `dinosaur-01` image as the identity reference and strict character reference. Preserve the same dinosaur identity, proportions, silhouette, mint-green body, cream belly with two curved lines, softened yellow back spikes, peach cheeks, large brown eyes, tail, feet, and magnifying glass. Do not redesign the character, do not chibify it further, and do not change its anatomy.

Goal: explore a shared Soft Handmade 2.5D rendering language that can later be translated to Cat and Robot without changing their anatomy.

Shared rendering rules:
- clean dark warm-brown outline with slight controlled hand-drawn variation
- flat base colors
- one soft shadow layer, primarily lower-right
- one restrained soft highlight, primarily upper-left
- very light colored-pencil / paper grain; texture is subtle seasoning, not the rendering method
- Preserve the eye shape, size, spacing, placement, and dark-brown eye color as identity features. The white eye highlights are not identity features. Their positions are an intentional style override: do not copy their positions from the reference image. Treat the dark eye shape as a box from 0% to 100%. The center of the large white highlight should be around 35% from the left edge and 25% from the top edge. Acceptable generation target: x=30–40%, y=20–35%. It must remain clearly left of the eye centerline. The smaller highlight must be lower and to the right of it. Do not place the large highlight at top-center or upper-right.
- clean silhouette and edges suitable for a 64 px character
- no cast shadow, no background scene, no text, labels, UI, color palette, model sheet, turnaround, or extra characters

Keep the dinosaur recognizably the same character. Reduce the overly polished digital-sticker feeling while preserving clarity.

Produce one isolated full-body character on a true transparent background.

Output exactly ONE dinosaur, centered on ONE square 1:1 canvas. There must be exactly one full-body character in the entire image. Do not show alternatives, variants, panels, side-by-side comparisons, duplicated characters, labels, captions, headings, UI, or text of any kind.

This output is a style exploration candidate, not production artwork and not an approved character master.
```

The variant lines (A2 Clean, A3 Balanced, A4 Handmade) are unchanged. `A2_instruction_v2c.txt`
(2088 bytes, SHA-256 `0cfb46b4876ec06c207d0b334d1c7449acd00007da7e56bce1b7363c8de2285a`) is **retired** and must not be used.

#### Instruction artifact `A2_instruction_v2d.txt`

v2d prompt, a blank line, then the A2 line (`Use almost no visible surface texture; prioritize clean graphic readability.`), with a trailing newline.

- Size: **2342 bytes**
- SHA-256: `12c67216741b4bf308d61cdf4390bb773080e9eb5fb5398e9627e49df9a47e1e`

Execution message (the only text sent, verbatim):

```text
Use the attached dinosaur image as the only image reference. Follow A2_instruction_v2d.txt exactly and generate exactly one image.
```

#### Gates, split into identity and style

All five hard gates must PASS, and the Owner must separately judge variant intensity
acceptable, before A2 can be accepted:

| # | Gate | Rule |
|---|---|---|
| 1 | One character | one full-body character on one 1:1 canvas; no text, labels, panels or duplicates |
| 2 | True alpha | transparent background (corners alpha 0), no matte |
| 3 | **Eye identity** (highlights masked out) | the dark eye shapes keep the base's size, shape, placement, spacing and color; see tolerances below |
| 4 | **Eye style** | per eye: large highlight center x ∈ [0.30, 0.40], y ∈ [0.20, 0.35] of the dark eye shape; small highlight x > large.x and y > large.y |
| 5 | Overall identity | silhouette, proportions, anatomy, mint body, cream belly with two lines, yellow back spikes, peach cheeks, magnifying glass, tail and feet still read as `dinosaur-01` |

Required Owner acceptance check, **not** an automated hard gate: **variant intensity**
(A2 = almost no visible surface texture). A texture proxy is reported with its measurement
conditions, but it is not used to auto-pass or auto-fail until it is shown to track human
judgment of texture strength. Passing the five hard gates alone is therefore necessary but
not sufficient for A2 acceptance.

The base's own highlight positions (table above) are recorded as **original-state evidence,
not as a pass target**. A highlight that moves does not fail the identity gates.

**Eye-identity tolerances (Owner-confirmed, 2026-10-05).** Measured as fractions of the
visible-bounds width (size, x) or height (y), highlights masked out. For scale, the largest
deviation seen between the base and the two generated images so far was 0.007 (size), 0.011
(center x), 0.009 (center y), 0.007 (spacing) and 8 RGB units; the confirmed tolerances are
about twice that:

| Metric | Observed range (base / v2b attempt / unregistered) | Confirmed tolerance vs base |
|---|---|---|
| eye width (L / R) | 0.142 / 0.135, 0.142 / 0.136, 0.139 / 0.132 | ± 0.015 |
| eye height (L / R) | 0.155 / 0.157, 0.150 / 0.152, 0.148 / 0.148 | ± 0.015 |
| eye center (L) x, y | 0.314, 0.439 / 0.325, 0.430 / 0.324, 0.435 | ± 0.02 |
| eye center (R) x, y | 0.674, 0.348 / 0.677, 0.347 / 0.681, 0.352 | ± 0.02 |
| eye spacing (centers, x) | 0.360 / 0.353 / 0.357 | ± 0.02 |
| eye color (each RGB channel) | about (69, 28, 1) / (68, 26, 2) / (76, 30, 6) | ± 15 |

#### Texture measurement validity

A texture or surface-detail proxy is only meaningful if the comparison is controlled:

1. Prefer the lossless / original artifact. Never compare files in different encodings.
2. Define the same forehead ROI by normalized facial landmarks, not by pixel coordinates.
3. Resize both ROIs to identical pixel dimensions.
4. Use the same color space and the same alpha handling.
5. Only then compute the high-frequency measure.
6. Call it a **texture proxy** until it is shown to correlate with human texture ratings; do
   not use it alone as a production gate.

#### Retry budget and attempt definition (v2d)

- v2d attempts: **0 of 2** used.
- **An attempt is consumed only when all four pre-flight checks pass and the generation
  request is actually sent.** Tool/transport failures that produce no reviewable generated
  artifact do not consume it.
- v2d permits at most two valid generation attempts. After the second valid generated
  artifact, any failed hard gate stops prompt-only retry; an Owner decision is then needed.
- If both eyes' large highlight stays at x > 0.45 in two valid attempts, record it
  additionally as "highlight position stays at a reference-like location". That is a
  diagnostic of what the generator did under v2d, not by itself a conclusion about generator
  ability.
- Fallbacks if prompt-only stops: accept the observed highlight position and revisit the
  style rule, or treat the highlight as a deterministic post-process by the image tool with a
  transformation record. Either is an Owner decision.

#### A2 v2d pre-flight gate (hard; before calling the generator)

All four must PASS. Any FAIL: do not generate, do not consume an attempt.

1. **Fresh context.** A brand-new conversation, not the current project conversation. Before
   generation it contains only the two attachments and one execution message.
2. **Source image identity.** The attached file is canonical `dinosaur-01`. Its bytes hash to
   the full SHA-256 `1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76`. Compare full 64-hex values, never abbreviations.
3. **Instruction artifact identity.** `A2_instruction_v2d.txt` is actually attached (not
   pasted, retyped or paraphrased): 2342 bytes, full SHA-256 `12c67216741b4bf308d61cdf4390bb773080e9eb5fb5398e9627e49df9a47e1e`.
4. **Execution message exact match.** The only text sent is the execution message above,
   verbatim: no preamble, no extra rules, no restated instruction, no gate script.

#### Post-generation provenance capture

Recorded after generation (a generation id does not exist before it):

- attempt number (v2d attempt N);
- generation id, or `not exposed` if the product does not expose one;
- source image SHA-256 and instruction file SHA-256 (full);
- the exact execution message;
- original generation artifact: format, dimensions, SHA-256;
- measurement actor and tool version for each measurement (generation-side measurement, and
  any independent measurement recorded separately; never overwrite);
- the five hard gates and the highlight coordinates;
- which copy was measured;
- if the delivered file was re-encoded: delivery format and SHA-256, recorded separately and
  never replacing the original artifact.

#### Reservation

Even if v2d succeeds on the Dinosaur, `x ∈ [0.30, 0.40]` is **not** yet a shared style rule.
It still has to be validated on the Cat and the Robot. Until then it only shows that the
coordinate suits this dinosaur's eyes.

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