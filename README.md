# KidsCharacterKit

A technology-neutral library of shared child-friendly character assets
(Cat, Dinosaur, Robot) that multiple apps can reuse from one source of truth.

It is an **asset library**, not a framework. There is no Swift (or any other
language) code here. A platform adapter is added only when a real app shows
repeated lookup code worth extracting.

## Questions this repo answers

- Which images are the official assets?
- Where is the original of each, and where did it come from?
- Is there any open question about commercial-use rights?
- Are names, canvas, transparency and padding consistent?
- Can different apps use the same file without per-app adjustment?
- When an asset changes, what changed?

## Layout

```
characters/<id>/raster/originals/   exact byte copies of selected source assets (master)
characters/<id>/raster/production/  deterministic delivery variants
provenance/                          schema + per-asset and per-reference records
manifests/                           language-neutral character manifest + schema
docs/                                inventory, contracts, specs, style bible
```

`<id>` is `cat-01`, `cat-02`, `dinosaur-01`, `dinosaur-02`, `robot-01`.
`animation-2d/` and `model-3d/` are added per character only when real content exists.

Start with the [representation contract](docs/character-representation-contract.md).

## Rules

- Unknown provenance or rights is recorded as `pending` / `unknown`, never inferred.
- Originals are never overwritten; delivery files are derived from them. A character is an identity; images, animations and 3D models are its representations.
- Not in scope: game logic, levels, scoring, rewards, learning progress,
  persistence, networking, navigation, UI/design system, animation APIs.

## Roadmap

| Slice | Goal | State |
|---|---|---|
| KCK-01 | Read-only inventory of existing Cat / Dinosaur / Robot assets | done |
| KCK-02 | Provenance schema and records for the five core candidates | done |
| KCK-03A | Character representation contract, manifest schema, raster delivery spec, style bible (specification only) | this slice |
| KCK-03B1 | Style exploration: one unified concept per character, reviewed side by side (needs an illustration workflow outside this repo; proposed, owner decides whether it precedes 03B) | proposed |
| KCK-03B | Raster assets: exact-copy originals, deterministic 1024×1024 delivery variants, transformation evidence | planned |
| KCK-03C | 2D animation contract (schema only; no animations) | planned |
| KCK-03D | 3D contract (schema only; no models) | planned |
| later | Platform adapter (e.g. Swift) only once an app needs it | — |

## Status

Specification stage. [Inventory](docs/asset-inventory.md), [provenance](provenance/README.md), the [contract](docs/character-representation-contract.md) and the [style bible](docs/character-style-bible.md) exist. No image files have been copied in yet; every character has `raster.available: false`, no animations and no 3D model. Rights status of every asset is `pending`.
