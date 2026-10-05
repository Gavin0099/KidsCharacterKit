# Raster delivery specification

**Status: draft v0 (KCK-03A).** Defines the delivery variant described in the
[representation contract](character-representation-contract.md) §5. Implemented in
KCK-03B; nothing is produced by KCK-03A.

Masters (`raster/originals/`) are exact byte copies of the source assets and are
never changed. Everything below applies to `raster/production/`.

## Delivery variant

| Item | Value |
|---|---|
| Canvas | **1024 × 1024 px** |
| Format | PNG, RGBA |
| Color space | sRGB |
| Aspect ratio | preserved; never stretched |
| Safe margin | **64 px** on every side (6.25 %) |
| Safe box | 896 × 896 px (canvas inset by the margin) |
| Visible bounds | bounding box of pixels with alpha > 5 % (the threshold the source repo uses for its own bounds; recorded in the evidence). **Used for scale only.** |
| Fit (scale) | the **larger side of the visible bounds** is fitted to the safe box: `scale ≤ min(896 / w, 896 / h)`. Visible content is never cropped: if placing by the anchor would push visible content outside the safe box (left, right, top) or outside the canvas (bottom), the scale is reduced until it fits and the resulting scale is recorded. |
| Position (anchor) | the **semantic ground anchor** (`ground-center` or `support-baseline`, see contract §6) is placed at canvas **(512, 960)**, i.e. horizontally centered, 64 px above the bottom edge (normalized (0.5, 0.9375)). The anchor is **not** the lowest visible pixel. |
| Per-asset anchor | measured by looking at each actual image in KCK-03B and recorded as `source_x`, `source_y` (source pixels) and `delivery_x`, `delivery_y`. Not guessed and not computed from alpha. |
| Upscaling | allowed in principle; any scale factor > 1 must be recorded. No limit is set in v0. |
| Resampling | one fixed algorithm chosen and recorded in KCK-03B so output is reproducible |
| Added content | none: no new shadow, background, border or glow |
| Determinism | same master + same parameters ⇒ identical **decoded RGBA pixels**. Identical PNG *file bytes* are claimed only if KCK-03B pins and records encoder, settings and versions. |

## What "same canvas" does and does not mean

Fitting the larger visible side into the same box and placing the ground anchor at
the same point gives every character the same layout contract (same canvas, same
ground line, same margins). It does **not** give
every character the same visual height: a wide character ends up shorter than a tall
one. That is intended; forcing equal heights would make wide characters look
oversized and tall ones small.

Relative size between related characters (e.g. a small sibling) is **not** handled
by the fit rule: fitting both `dinosaur-01` and `dinosaur-02` to the maximum would
make the junior as large as its parent. Each character's `visual_scale` (manifest) is
a **blocking owner decision for KCK-03B**; see contract §11.

## Layout sketch (anchor shown at the standing point)

```
1024 × 1024
┌────────────────────────────┐
│          64 px             │
│   ┌────────────────────┐   │
│   │                    │   │
│   │     character      │   │
│   │                    │   │
│   └─────────┬──────────┘   │
│             ▲ anchor (512, 960)
│          64 px             │
└────────────────────────────┘
```

## Evidence required per delivery file (KCK-03B)

`asset_id`; source SHA-256; output `pixel_sha256` and `file_sha256`; canvas, safe
margin; visible-bounds threshold and resulting bounds; the semantic anchor record
(`type`, `source_x`, `source_y`, `delivery_x`, `delivery_y`); scale factor
(including `visual_scale`); `tool`, `tool_version`, resampling algorithm,
color-conversion policy and PNG encoder settings. See contract §10.
