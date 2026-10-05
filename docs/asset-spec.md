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
| Visible bounds | bounding box of pixels with alpha > 5 % (the threshold the source repo uses for its own bounds; recorded in the evidence) |
| Fit | scale so the **larger side of the visible bounds fits the safe box** (`scale = min(896 / w, 896 / h)`); the content is not cropped |
| Anchor | **bottom-center**: the bottom edge of the visible bounds sits at **y = 960** (canvas height − margin) and its horizontal center at **x = 512**. Normalized anchor: (0.5, 0.9375) |
| Upscaling | allowed in principle; any scale factor > 1 must be recorded. No limit is set in v0. |
| Resampling | one fixed algorithm chosen and recorded in KCK-03B so output is reproducible |
| Added content | none: no new shadow, background, border or glow |
| Determinism | same master + same parameters ⇒ identical bytes |

## What "same canvas" does and does not mean

Fitting the larger visible side into the same box gives every character the same
layout contract (same canvas, same ground line, same margins). It does **not** give
every character the same visual height: a wide character ends up shorter than a tall
one. That is intended; forcing equal heights would make wide characters look
oversized and tall ones small.

Relative size between related characters (e.g. a small sibling) is not modeled in
v0; see contract §11.

## Layout sketch

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

`asset_id`, source SHA-256, production SHA-256, canvas, anchor, safe margin,
visible-bounds threshold and resulting bounds, scale factor, resampling algorithm
and version. See contract §10.
