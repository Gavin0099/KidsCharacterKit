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

Governance (who approves what, asset statuses, rights): see [GOVERNANCE.md](GOVERNANCE.md).

- Unknown provenance or rights is recorded as `pending` / `unknown`, never inferred.
- Originals are never overwritten; delivery files are derived from them. A character is an identity; images, animations and 3D models are its representations.
- Not in scope: game logic, levels, scoring, rewards, learning progress,
  persistence, networking, navigation, UI/design system, animation APIs.

## Roadmap

| Slice | Goal | State |
|---|---|---|
| KCK-01 | Read-only inventory of existing Cat / Dinosaur / Robot assets | done |
| KCK-02 | Provenance schema and records for the five core candidates | done |
| KCK-03A | Character representation contract, manifest schema, raster delivery spec, style bible (specification only) | done |
| KCK-GOV-01 | Lite governance: AI proposes / Owner approves, provenance gate, rights not auto-upgraded, slice boundaries, asset statuses ([GOVERNANCE.md](GOVERNANCE.md)) | done |
| KCK-GOV-02 | Initial AI governance adoption: pinned framework, repo rules, PLAN, static checks and explicit runtime gaps ([adoption](docs/ai-governance-adoption.md)) | proposed in this PR |
| KCK-03B1 | Style exploration: a unified concept for the three characters, reviewed side by side. Three checkpoints: B1-A Dinosaur style key → B1-B Cat / Robot translation → B1-C lineup gate. Brief: [docs/kck-03b1-brief.md](docs/kck-03b1-brief.md). Done by the owner outside this repo (needs an illustration workflow); outputs are `candidate`s and come back for a Style Bible v1 decision | execution hold; pending PR #12 |
| — | Style Bible v1 approved, then formal model sheets | after B1 |
| KCK-03B | Raster assets: exact-copy originals, delivery variants, per-asset ground anchors, transformation evidence. **Blocked until `visual_scale` (e.g. junior vs parent) is decided** | planned |
| KCK-03C | Authored 2D animation contract (schema only; no animations) | planned |
| KCK-03D | 3D contract (schema only; no models) | planned |
| later | Platform adapter (e.g. Swift) only once an app needs it | — |

The proposed snack-motion slices (03B2, 03C1, 03C2) and their dependencies are in
[PLAN.md](PLAN.md). They do not authorize production or waive existing gates.

## Status

Specification stage. [Inventory](docs/asset-inventory.md), [provenance](provenance/README.md), the [contract](docs/character-representation-contract.md) and the [style bible](docs/character-style-bible.md) exist. No image files have been copied in yet; every character has `raster.available: false`, no animations and no 3D model. Rights status of every asset is `pending`.
