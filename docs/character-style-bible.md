# Character style bible

**Status: draft v0 (KCK-03A) — proposals pending owner approval.** No artwork is
produced or changed by this slice. Everything under "Proposed direction" is a
proposal, not an approved rule, and the numbers have not been tested against any
artwork.

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

## 2. Proposed direction: "Soft Handmade 2.5D"

> Cute but not infantile. Handmade but not rough. Some volume, not plastic.

Intent: one visual language that survives being a still image, a 2D animation and,
later, a 3D model.

### 2.1 Shape language
- Built from rounded primitives (sphere, capsule, pear, rounded cube). No sharp,
  spiky or thin forms.
- Primitives map directly to 3D volumes later (§2.8).

### 2.2 Proportion
- Proposed target: head : body ≈ **1 : 1.3 – 1.8** (head about 36–43 % of height).
- Rationale (design judgment, not tested): readable as cute, but not as baby-like as
  a very short chibi body, because the apps target roughly 6–12-year-olds.
- Observed: only `cat-02` is near this; `dinosaur-*` is shorter and rounder,
  `robot-01` is taller and narrower. The Robot may stay a robot; the rule needs an
  owner decision on how strictly it applies per character.

### 2.3 Eye language (shared rules, per-character shape)
Shared across all three: highlight at upper-left, large pupil/iris, clearly
readable expression (including brows or equivalent), a defined blink.
Per-character shape: Cat = round / large iris, Dinosaur = slightly oval,
Robot = screen-like oval.

### 2.4 Silhouette
- Each character must be identifiable **at 64 px**, from the silhouette alone,
  without internal detail.
- Used for: app icons, small game boards, rhythm-game lanes, distant 3D views.

### 2.5 Outline and texture ("controlled imperfection")
Proposed starting values, to be tuned on real art:
- Outline weight ≈ 3–5 % of the character's visual size, slight natural variation
  (≈ 1–2 % wobble), closed and clean.
- Surface texture (pencil / crayon grain) at ≈ 5–12 % opacity over flat base color.
- Shadow: very soft. Highlight: at most 1–2 shapes.
- Must remain clean when scaled down: no noisy edges, no mixed resolutions.

### 2.6 Palette
- Keep the identity colors from §1. Candy-like but slightly desaturated: not
  baby-pastel, not neon.
- Backgrounds in apps may change freely; the character must stay recognizable
  because of its own palette.

### 2.7 Lighting
- One soft key light from upper-left, matching the eye highlight. No cast shadows
  baked into character art (delivery adds none; see [asset-spec.md](asset-spec.md)).

### 2.8 2D ↔ 3D correspondence (planning, not modeling)
| Character | Primitive plan |
|---|---|
| Cat | round head, pear body, short capsule legs, tube tail |
| Dinosaur | large rounded head, pear body, capsule legs, tapered tube tail |
| Robot | rounded-cube head, rounded-cuboid body, segmented capsule limbs |

3D is built from the 2D model sheet (§3), not generated from a single existing PNG:
single-view conversion tends to drift on side/back views and limb proportions, and
the three characters would stop looking like one IP.

### 2.9 Expressions
Initial vocabulary: **happy**, **confused**. More only when an app needs them.

## 3. Model sheet (required before any animation or 3D work)

Per character: turnaround (**front, 3/4, side, back**) and expressions
(**happy, confused**) — six images. Animation (`idle`, `greeting`, `happy`) and 3D
modeling start from these, not from the existing single poses.

## 4. How to check it worked (owner decides)

1. **Same-world test:** the three characters side by side — do they look like they
   live in the same world?
2. **64 px silhouette test:** can each be identified in solid black at 64 px?
3. **Scale test:** do the proposed outline/texture values still read at small sizes?
4. **Palette test:** are the three still distinguishable from each other and from
   typical app backgrounds?

Pass/fail is an owner decision; this document does not claim any artwork passes.

## 5. Open decisions

- Approve, change or drop the proposed numbers (§2.2, §2.5).
- Whether Robot is allowed to differ from the proportion target.
- Whether the new style should be explored on new concept art before the existing
  five assets go through raster normalization (the order of KCK-03B1 and KCK-03B in
  the README roadmap).
- Design rationale from market or trend research is intentionally not recorded
  here: it has not been verified in this repository's context. Add it with sources
  if wanted.
