# Character style bible

**Status: draft v0 (KCK-03A).** The high-level direction in §2 was **approved by the
owner during the PR #3 review**. The numeric values in §3 are **exploration starting
ranges** for KCK-03B1 and are **not** approved rules. No artwork is produced or
changed by this slice.

The [Owner-approved Style Bible v1](character-style-bible-v1.md) consolidates the
actual three-character exploration and is the active drawing specification. This
v0 remains historical evidence of the originally approved direction and unapproved
exploration ranges; v1 does not waive the representation contract or rights gates.

Purpose: if Cat, Dinosaur and Robot are to look like one world across apps, 2D
animation and later 3D, they need shared visual rules. Normalizing file sizes does
not do that; it only makes differently-styled images the same size.

Applies to new or redrawn art. It does not retroactively invalidate the five
existing assets.

## 1. Baseline: what the current art looks like

Observed by viewing the five selected source assets at the KCK-01 source commit.
Descriptions are my visual reading (inferred, not measured).

| | `cat-01` / `cat-02` | `dinosaur-01` / `dinosaur-02` | `robot-01` |
|---|---|---|---|
| Rendering | soft, painterly, fur-like texture, gradients | flat color, clean vector-like, slight soft shading | crayon / colored-pencil texture, hatching |
| Outline | thin warm-brown line | thick dark-brown, even weight | heavy black, hand-drawn weight |
| Eyes | large brown iris, one or two highlights, expressive brows | very large round dark-brown eyes, two highlights, no brows | small black ovals, one highlight, no brows |
| Proportion | head about the size of the body | head larger than the body (very short, round body) | head smaller than torso, long arms and legs, boxy |
| Main palette | warm orange + cream, pink accents | mint green + cream, soft-yellow spikes | cool gray + saturated blue, small primary accents |
| Face extras | pink cheeks, tongue, whiskers | peach cheeks, small "w" mouth | red cheeks, rectangular mouth with tongue |

Takeaways (inferred):

- The three use **three different rendering languages** (painterly / flat vector /
  crayon). Same-size files would still look like three apps.
- Palette identity is already consistent and worth keeping: **Cat = warm orange,
  Dinosaur = mint, Robot = cool gray + blue**.
- Cheeks, large glossy eyes and a friendly open expression recur in all three.
- Robot is the only one with deliberate handmade texture; Cat has soft texture;
  Dinosaur is flat.

## 2. Approved direction: "Soft Handmade 2.5D"

> Cute but not infantile. Handmade but not rough. Some volume, not plastic.

Approved by the owner (PR #3 review):

- **Soft Handmade 2.5D** as the overall direction: flat shape + hand texture + very
  light volume.
- **Identity palette:** Cat = warm orange, Dinosaur = mint, Robot = cool gray + blue.
  Candy-like but slightly desaturated: not baby-pastel, not neon. Backgrounds in apps
  may change freely; the character stays recognizable by its own palette.
- **Rounded primitive shape language:** the primary masses (head, body, limbs) use
  soft, rounded primitives: sphere, capsule, pear, rounded cube. These map directly to
  3D volumes later. Existing identity-defining protrusions may stay, e.g. the
  Dinosaur's back spikes and the Robot's antennae, provided they are softened at the
  tips, thick enough to read at small sizes, and **not** relied on as fragile
  fine-detail parts of the main silhouette. The goal is a unified style, not removing
  what makes a character recognizable.
- **64 px silhouette:** each character is identifiable from its silhouette alone at
  64 px (app icons, small boards, rhythm-game lanes, distant 3D views).
- **Light and highlight from the upper left**, matching the eye highlight. No cast
  shadows baked into character art.
- **Controlled handmade texture:** handmade, not rough; clean and readable when scaled
  down.
- **One shape language shared by 2D and 3D**, so 3D is built from the 2D model sheet
  (§4).

### What must be shared, and what must not

Shared across all characters (the "same world" part):
rendering language, eye/highlight language, outline language, texture language,
lighting, palette treatment.

**Not** shared: body proportion. The goal is not the same physique.

**Robot exception (explicit):** the Robot keeps its long limbs, box head and
child-crayon character. Forcing it to Dinosaur-like proportions would erase what makes
it recognizable. Any proportion range below applies to it only if exploration shows it
helps.

## 3. Exploration starting ranges (not approved rules)

Starting points for KCK-03B1, to be adjusted after the three characters are viewed
side by side. They are not requirements and not acceptance criteria.

| Parameter | Starting range | Note |
|---|---|---|
| Head : body | ≈ 1 : 1.3 – 1.8 (head ≈ 36–43 % of height) | design judgment, untested; Robot is exempt (§2) |
| Outline weight | ≈ 3–5 % of the character's visual size, ≈ 1–2 % natural wobble | closed and clean |
| Surface texture | ≈ 5–12 % opacity pencil/crayon grain over flat base color | |
| Shadow / highlight | very soft shadow; at most 1–2 highlight shapes | |
| Eye shape | Cat round/large iris, Dinosaur slightly oval, Robot screen-like oval | per-character shape; shared highlight position |
| Expressions | `happy`, `confused` first | more only when an app needs them |

Observation from §1 (inferred): only `cat-02` is near the head:body range;
`dinosaur-*` is shorter and rounder, `robot-01` taller and narrower.

## 4. Model sheet

Per character: turnaround (**front, 3/4, side, back**) and expressions (**happy,
confused**) — six images.

Required before:
- **authored** 2D character animation (new frames, sprite sheet, skeletal), and
- **3D** modeling.

**Not** required for presentation motion. Breathing, bobbing, scale pulses and small
rotations or greeting wiggles applied to an existing raster are app presentation, not
a new representation (see the
[contract](character-representation-contract.md) §7).

3D is built from the model sheet, not generated from a single existing PNG:
single-view conversion tends to drift on side/back views and limb proportions, and the
characters would stop looking like one IP.

### 2D ↔ 3D correspondence (planning, not modeling)

| Character | Primitive plan |
|---|---|
| Cat | round head, pear body, short capsule legs, tube tail |
| Dinosaur | large rounded head, pear body, capsule legs, tapered tube tail |
| Robot | rounded-cube head, rounded-cuboid body, segmented capsule limbs |

## 5. How to check it worked (owner decides)

1. **Same-world test:** the three characters side by side — do they look like they
   live in the same world?
2. **64 px silhouette test:** can each be identified in solid black at 64 px?
3. **Scale test:** do the outline/texture values still read at small sizes?
4. **Palette test:** are the three still distinguishable from each other and from
   typical app backgrounds?

Pass/fail is an owner decision; this document does not claim any artwork passes.

## 6. Open decisions

- Final values for the §3 parameters (after KCK-03B1).
- Relative visual size of related characters, e.g. `dinosaur-02` vs `dinosaur-01`
  (`visual_scale`): **blocking for KCK-03B**; decided after the KCK-03B1 concepts are
  reviewed.
- Design rationale from market or trend research is intentionally not recorded here:
  it has not been verified in this repository's context. Add it with sources if wanted.
