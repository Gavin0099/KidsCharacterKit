# Naming

**Status: draft v0 (KCK-03A).**

## Identity

`<character>-NN` — `cat-01`, `cat-02`, `dinosaur-01`, `dinosaur-02`, `robot-01`.
Identity never encodes a pose, size, file type or source app name.

## Paths

| Kind | Path |
|---|---|
| Raster master | `characters/<id>/raster/originals/<id>.<ext>` — `<ext>` as in the source file (all current sources are `.png`) |
| Raster delivery | `characters/<id>/raster/production/default.png` |
| 2D animation | `characters/<id>/animation-2d/…` — IDs are `<id>.<name>`, e.g. `robot-01.idle` |
| 3D source | `characters/<id>/model-3d/source/<id>.<ext>` (e.g. `.blend`) |
| 3D delivery | `characters/<id>/model-3d/production/<id>.glb`, `<id>.usdz` |
| Provenance | `provenance/<character>/<id>.json` |

`default` is the only raster delivery name today. Additional named raster variants
are added only when an app needs one.

## Rules

- Lowercase, ASCII, hyphen-separated; no spaces.
- A replaced file keeps its path; the manifest hash and provenance change instead.
- Source-app names (`CatBagKitten`, …) appear only in provenance as `source_asset_name`.
