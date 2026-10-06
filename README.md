# KidsCharacterKit

A technology-neutral library of shared child-friendly character assets
(Cat, Dinosaur, Robot) that multiple apps can reuse from one source of truth.

It is an **asset library**, with Python preparation/QA tools and no app runtime.
A platform adapter is added only when a real app shows
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
.agents/skills/                      repo-local character preparation/QA skill
artifacts/qa/                        labeled candidate reviews and QA bundles
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
| KCK-03B1 | Dinosaur style key → Cat / Robot translation → lineup; [brief](docs/kck-03b1-brief.md), [lineup review](artifacts/qa/2026-10-06-b1c-corrected-lineup/contact-sheet.png) | Three-character references/lineup approved; Dino v2d budget remains 2/2 |
| KCK-03B2 | [Style Bible v1](docs/character-style-bible-v1.md), Cat/Dinosaur formal model sheets plus Robot continuation | Cat/Dinosaur six-sheet sets approved; Robot incomplete |
| KCK-03B | Raster assets: exact-copy originals, delivery variants, per-asset ground anchors, transformation evidence. Master/version/scale/anchor approved; [1024 delivery review](artifacts/qa/2026-10-06-raster-delivery/contact-sheet.png) | Cat/Dinosaur available; Robot mouthfix static available |
| KCK-03C | [Neutral animation contract](docs/animation-contract-v1.md), schema, timing/events/sockets and file validator | implemented; validation covered |
| KCK-03C1 | [Snack minimum pack checkpoint](concepts/kck-03c1/README.md) | Cat/Dinosaur minimum action candidates prepared; consumer QA pending |
| KCK-03C2 | Actual consumer-scene pivot, scale, ground, timing, loop, alpha and prop handoff | pending |
| KCK-03D | 3D contract (schema only; no models) | planned |
| later | Platform adapter (e.g. Swift) only once an app needs it | — |

The authorized snack-motion path and its dependencies are in [PLAN.md](PLAN.md).
Conditional Owner acceptance applies only to output with real conformance evidence.

## Status

Exploration and preparation tooling stage. Concept originals and the separately
authorized A3 derivative are preserved under `concepts/`. The
[character pipeline](docs/character-pipeline.md) provides read-only review,
fixed-slot extraction and explicit-anchor sequence QA. Cat/Dinosaur and the [mouth-fixed Robot](docs/character-reference-amendments.md)
have accepted static deliveries; Robot sheets remain incomplete.
No delivered animations or 3D model are available. Asset rights
remain `pending`. These changes are on the review branch, not merged main.
