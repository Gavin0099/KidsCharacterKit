# Character representation contract

**Status: draft v0 (KCK-03A).** Specification only. No images, animations or
3D models are added by this slice.

## 1. Principle

A **character** is an identity. Images, 2D animations and 3D models are
**representations** of that identity. They are never separate characters.

```
Character  (robot-01)
 ├── raster         still image(s)
 ├── animation_2d   frame sequences / sprite sheets / skeletal (future)
 └── model_3d       mesh + rig + animations (future)
```

An app asks for "robot-01"; it does not know or care whether the answer is a PNG,
an animation or a model. A character may have only a raster representation. That
is a complete, valid state.

The contract allows 2D animation and 3D, it does not require them. Animations and
models are made when an app needs them (see §9).

## 2. Identity

- Stable ID: `<character>-NN` — `cat-01`, `cat-02`, `dinosaur-01`, `dinosaur-02`,
  `robot-01`. Defined by [provenance records](../provenance/README.md).
- The ID never changes when a file is replaced, renamed or re-exported.
- The source app's name (e.g. `CatBagKitten`) is not an identity.
- References (`cat-ref-01`, …) are provenance inputs, not characters.

## 3. Capability = what a character actually has

A character's manifest entry states which representations exist. Nothing is
implied: an absent representation is `available: false` / `[]`, and no placeholder
file stands in for it.

```
raster:        available true/false
animation_2d:  available [ "idle", "greeting", … ]   ([] today)
model_3d:      available true/false, formats [ "glb", "usdz" ]   (false today)
```

Schema: [`manifests/character-manifest.schema.json`](../manifests/character-manifest.schema.json).
Instance: [`manifests/characters.json`](../manifests/characters.json).

## 4. Repository layout

```
characters/<id>/
  raster/
    originals/      exact byte copies of the selected source assets (master)
    production/     deterministic delivery variants derived from originals
  animation-2d/     created only when a real animation exists
  model-3d/         created only when a real model exists
    source/         authoring files (e.g. .blend)
    production/     delivery files (.glb, .usdz)
    textures/
```

Empty `animation-2d/` and `model-3d/` directories are intentionally not created.

## 5. Raster: master vs delivery

| Kind | Location | Meaning |
|---|---|---|
| **Master** | `raster/originals/` | Exact byte copy of the selected source-app asset, at its original resolution and canvas. Never resized, cropped or re-encoded. |
| **Delivery** | `raster/production/` | Normalized variant that apps consume. Always derived from the master by a documented, deterministic transform. |

- **`originals/` is not generator raw output.** Raw outputs mostly are not in the
  source repo. `originals/` holds the source app's asset, byte for byte. Its
  SHA-256 must equal `file.sha256` in the asset's provenance record.
- **1024×1024 is a delivery variant, not the character master.** Masters keep
  their native size (e.g. `robot-01`: 1086×1448) so layers, animation and
  textures can be re-made from them later.
- Delivery numbers (canvas, margin, safe box, resampling) are in
  [asset-spec.md](asset-spec.md).
- **Fit and position are separate decisions.** Visible bounds (alpha > 5 %) decide
  *scale* only. *Position* uses the semantic ground anchor in §6.
- Consequence for apps: no per-character `offset`/`scale` corrections should be
  needed to align characters placed on the same ground line.

## 6. Ground anchor / pivot (shared by all representations)

The **ground anchor** is a *semantic* point: where the character stands.

| Anchor type | Meaning |
|---|---|
| `ground-center` | the point on the ground between the character's feet |
| `support-baseline` | for a character with no visible feet (e.g. a cat sitting in a paper bag): the contact point of the character/carrier with the ground |

It is **not** the lowest visible pixel. A tail, a prop or a bag can be lower than the
feet, so "bottom of the alpha bounds" is not guaranteed to be the standing point.
Using it would make a character jump when it switches between raster, animation and
3D.

| Representation | Ground reference |
|---|---|
| raster (delivery) | the semantic ground anchor is placed at a fixed canvas coordinate (asset-spec.md) |
| animation_2d | same anchor, constant across all frames |
| model_3d | origin at ground center |

**The anchor is measured per asset, by looking at the actual image, in KCK-03B**
and recorded as data. It is not guessed here and not computed from alpha.

```json
{
  "anchor": {
    "type": "ground-center",
    "source_x": 0,
    "source_y": 0,
    "delivery_x": 512,
    "delivery_y": 960
  }
}
```

(Placeholder zeros only show the shape; no real value exists yet.)

## 7. Motion: presentation vs authored

Two different things:

| | Presentation motion | Authored character animation |
|---|---|---|
| What | transform-only effects on an existing raster: breathing, bobbing, scale ≈ 0.98→1.02, small rotation, greeting wiggle | new frames, a sprite sheet, or skeletal animation |
| Is it a representation? | **No.** It is app presentation applied to the raster. | **Yes**: an `animation_2d` representation |
| Needs a model sheet? | **No** | **Yes** |
| Lives in | the consuming app | this library (`animation-2d/`) |

An app that only wants a character to breathe needs nothing beyond the raster. This
library does not gate that on new artwork.

### 7.1 Authored 2D animation metadata (planned shape, formalized in KCK-03C)

No authored animation exists yet. When one does, it is described by metadata rather
than guessed from file names:

| Field | Example | Notes |
|---|---|---|
| `animation_id` | `robot-01.idle` | `<character-id>.<name>` |
| `character_id` | `robot-01` | |
| `type` | `frame_sequence` | also `sprite_sheet`, `skeletal`; the format is not fixed by this contract |
| `fps` | `12` | |
| `loop` | `true` | |
| `duration_ms` | `1200` | |
| `anchor` | `ground-center` | same semantic anchor as §6, kept constant |

Initial vocabulary: **`idle`, `greeting`, `happy`**. Other names (`walk`, `run`,
`jump`, `hurt`, …) are added only when an app needs them. The current PNGs have no
layer structure and do not support skeletal animation without new artwork.

## 8. 3D conventions (fixed now, applied when a model exists)

Fixed now because import problems from inconsistent units/axes are expensive later.

| Item | Value |
|---|---|
| Units | meters |
| Up axis | +Y |
| Front (forward) | +Z (a character faces +Z) |
| Handedness | right-handed |
| Origin | ground center (between the feet, on the ground) |
| Scale | each character has a `canonical_height_m` in its manifest entry; `null` until a model exists. No value is invented before then. |
| Texture color space | `baseColor` and `emissive` textures: **sRGB**. `normal`, `metallic-roughness` and `occlusion` textures: **linear / non-color data** (never sRGB-decoded). |
| Alpha | defined per material when a model exists |
| Skeleton / animation naming | defined when the first rig exists; animation names reuse §7 vocabulary |

Coordinate choice follows glTF 2.0 (+Y up, +Z front, meters). Apple's RealityKit
handles either forward axis, so the master is not flipped for Apple.

Delivery formats: **`.glb`** (cross-platform) and **`.usdz`** (Apple). Authoring
source (e.g. `.blend`) is kept under `model-3d/source/`, never only the delivery
file.

A 3D model should be built from the character's 2D model sheet (see the
[style bible](character-style-bible.md)), not generated from a single existing PNG.
The same applies to authored 2D animation (§7). Presentation motion does not need a
model sheet.

## 9. When representations get made

Need-driven. An animation or model is produced when a real app prototype needs it,
and only the poses it needs. Having a 3D model is **not** a completion condition
for v1 of this library.

## 10. Provenance and determinism of derived representations

Every file under `production/` (and any future animation or model file) must be
traceable:

```
reference → source-app asset → exact copy (original) → delivery / animation / model
```

**Determinism.** The same master and the same transformation parameters must produce
the same **decoded RGBA pixels**. Identical *file bytes* are not promised by default:
different PNG encoder, library or zlib versions can give different bytes for identical
pixels. Byte-identical output may be claimed only if 03B pins and records the encoder,
its settings and versions.

Required evidence for a delivery raster (written in KCK-03B):

- `asset_id`
- source SHA-256, **`pixel_sha256`** and **`file_sha256`** of the output
- canvas, safe margin, visible-bounds threshold and resulting bounds
- the semantic ground anchor record (§6) and the resulting scale factor
- `tool`, `tool_version`, resampling algorithm, color-conversion policy and PNG
  encoder settings

This lets a later change be classified as "artwork replaced" or "normalization
changed".

The provenance schema currently has `asset` and `reference` record kinds; a
transformation record kind is added in KCK-03B, with real evidence to model.

## 11. Decisions

### Blocking decision for KCK-03B

**Relative visual scale of related characters.** Normalization must not fit
`dinosaur-01` and `dinosaur-02` both to the maximum size: that would make the
"junior" as large as its parent. Before 03B produces delivery files, the owner
decides each character's relative visual size (after the KCK-03B1 concepts are
reviewed). It is stored in the manifest as `visual_scale` (`null` until decided).

Definition: `final_scale = safe_fit_scale × visual_scale`, where `safe_fit_scale` is the
largest anchor-aware scale that keeps the visible content within the delivery
constraints ([asset-spec.md](asset-spec.md)), and `0 < visual_scale ≤ 1`. `1.0` means
the maximum allowed visual size; smaller values intentionally keep a character
relatively smaller. (A junior might later be 0.7; that number is illustrative, not
decided.) `visual_scale` is an art/layout ratio and is separate from
`canonical_height_m`, which is the 3D world-space height.

### Not decided here

- Animation file format and the formal animation schema (03C).
- 3D skeleton conventions and the formal model schema (03D).
- Per-asset ground anchors (measured in 03B).
- Any platform adapter code.
