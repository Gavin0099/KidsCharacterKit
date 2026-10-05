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
- Consequence for apps: no per-character `offset`/`scale` corrections should be
  needed to align characters placed on the same ground line.

## 6. Anchor / pivot (shared by all representations)

All representations of a character share one ground reference: the point between
its feet at the ground.

| Representation | Ground reference |
|---|---|
| raster (delivery) | anchor `bottom-center` of the **visible bounds**, at a fixed canvas coordinate (asset-spec.md) |
| animation_2d | same anchor, kept constant across all frames |
| model_3d | origin at ground center |

So switching a character between raster, animation and 3D does not make it jump
up or down.

## 7. 2D animation metadata (planned shape, formalized in KCK-03C)

No animation exists yet. When one does, it is described by metadata rather than
guessed from file names:

| Field | Example | Notes |
|---|---|---|
| `animation_id` | `robot-01.idle` | `<character-id>.<name>` |
| `character_id` | `robot-01` | |
| `type` | `frame_sequence` | also `sprite_sheet`, `skeletal`; the format is not fixed by this contract |
| `fps` | `12` | |
| `loop` | `true` | |
| `duration_ms` | `1200` | |
| `anchor` | `bottom-center` | same as §6 |

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
| Texture color | sRGB |
| Alpha | defined per material when a model exists |
| Skeleton / animation naming | defined when the first rig exists; animation names reuse §7 vocabulary |

Coordinate choice follows glTF 2.0 (+Y up, +Z front, meters). Apple's RealityKit
handles either forward axis, so the master is not flipped for Apple.

Delivery formats: **`.glb`** (cross-platform) and **`.usdz`** (Apple). Authoring
source (e.g. `.blend`) is kept under `model-3d/source/`, never only the delivery
file.

A 3D model should be built from the character's 2D model sheet (see the
[style bible](character-style-bible.md)), not generated from a single existing PNG.

## 9. When representations get made

Need-driven. An animation or model is produced when a real app prototype needs it,
and only the poses it needs. Having a 3D model is **not** a completion condition
for v1 of this library.

## 10. Provenance of derived representations

Every file under `production/` (and any future animation or model file) must be
traceable:

```
reference → source-app asset → exact copy (original) → delivery / animation / model
```

Required evidence for a delivery raster (written in KCK-03B):
`asset_id`, source SHA-256, production SHA-256, canvas, anchor, margin, visible-bounds
threshold, scale factor, resampling algorithm and version. This lets a later change
be classified as "artwork replaced" or "normalization changed".

The provenance schema currently has `asset` and `reference` record kinds; a
transformation record kind is added in KCK-03B, with real evidence to model.

## 11. Not decided here

- Animation file format and the formal animation schema (03C).
- 3D skeleton conventions and the formal model schema (03D).
- Per-character relative scale (e.g. whether `dinosaur-02` is rendered smaller than
  `dinosaur-01`): delivery fits each character's largest visible side into the same
  safe box, so a small sibling would currently appear as large as its parent. Known
  trade-off, left for an owner decision.
- Any platform adapter code.
