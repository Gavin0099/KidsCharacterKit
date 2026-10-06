# Provenance

Technology-neutral provenance records. Goal: any asset in this library can be
traced back to its source and its current rights status.

Records are JSON, validated by [`schema/provenance.schema.json`](schema/provenance.schema.json)
(JSON Schema 2020-12).

## Rules

- **Unknown stays unknown.** `commercial_use_status` must remain `pending`,
  and `rights_review_status` / `ownership_status` must remain `unknown`, unless
  a record cites evidence. The schema sets no defaults: every record states
  these fields explicitly, and it rejects `confirmed` / `reviewed` /
  `documented` without `evidence_for_confirmation`.
- **No inference.** "AI-generated", "owner provided" or "app uses it" are not
  rights evidence. Statements found in the source repo are quoted under
  `rights.statements` with their path.
- **Stable IDs, not app names.** IDs are `cat-01`, `dinosaur-02`, `robot-01`
  (assets) and `cat-ref-01`, … (references). The source app's name
  (e.g. `CatBagKitten`) lives in `source_asset_name` and is not an identity.

## Record types

| Type | ID shape | Meaning |
|---|---|---|
| `asset` | `<character>-NN` | A selected core candidate image |
| `reference` | `<character>-ref-NN` | Source/reference artwork or an earlier output used as a generation input |

Each `asset` points at the references it was derived from (`derivation.inputs`);
each `reference` lists the assets that use it (`used_by`). A reference can be
`in_source_working_tree`, `not_in_source_working_tree` (only a recorded hash) or
`external_missing` (not in git at all).

## What is observed vs source-stated

- `file` (format, dimensions, color type, bytes, SHA-256) — computed from the
  file bytes at the source commit. For references that are not in the working
  tree, the hash is marked `sha256_basis: source_stated`.
- `generation`, `derivation`, `origin`, `rights.statements` — taken from
  source-repo records and not independently verified. Prompts are referenced by
  path + JSON Pointer, not copied.

All records were written against `Gavin0099/english-vocab-trainer` at commit
`dc9435962b056af66be7cbf201802f691d0ab322` (the commit inspected in
[KCK-01](../docs/asset-inventory.md)).

## Records

### Assets (selected core candidates)

| ID | Source app name | Inventory ID | Record |
|---|---|---|---|
| `cat-01` | `CatBagKitten` | CAT-A1 | [cat/cat-01.json](cat/cat-01.json) |
| `cat-02` | `CatRaisedPaw` | CAT-A2 | [cat/cat-02.json](cat/cat-02.json) |
| `dinosaur-01` | `DinosaurResearcher` | DINO-A1 | [dinosaur/dinosaur-01.json](dinosaur/dinosaur-01.json) |
| `dinosaur-02` | `DinosaurJunior` | DINO-A3 | [dinosaur/dinosaur-02.json](dinosaur/dinosaur-02.json) |
| `robot-01` | `RobotSkinMascot` | ROBOT-A1 | [robot/robot-01.json](robot/robot-01.json) |

`DinosaurWorldThumbnail` (DINO-A2) is recorded only as a `byte_identical_copy`
note on `dinosaur-01`; it is not a separate asset.

### References and chains

```
cat-ref-01 (owner reference, JPEG)
 ├─ cat-01
 └─ cat-02

dinosaur-ref-02 (owner-selected concept; origin Unknown)
 ├─ dinosaur-01
 └─ dinosaur-02 ── also edits ── dinosaur-ref-03 (superseded DINO-01 junior; hash only)
                                  └─ derived from dinosaur-ref-01 (owner reference, PNG)

robot-ref-01 (child's drawing; external_missing, hash only)
 └─ robot-01
```

| ID | Availability |
|---|---|
| `cat-ref-01` | in source working tree |
| `dinosaur-ref-01` | in source working tree |
| `dinosaur-ref-02` | in source working tree |
| `dinosaur-ref-03` | not in source working tree (hash/size/dimensions source-stated) |
| `robot-ref-01` | external_missing (only SHA-256 recorded) |

### Inventoried but not selected for the core set (no records)

`CatEmptyBag`, `CatCompletionHeart`, `CatWorldThumbnail`,
`DinosaurWorldThumbnail`, `DinosaurFamily`.

This means *not selected for the core reusable set now*. It does not mean
rejected or unusable; they remain in [the inventory](../docs/asset-inventory.md)
and can get records later.

## Status

All five assets and all five references have `commercial_use_status: pending`.
Nothing here clears any asset for any use.

## Versioned style master and delivery records (03B)

`master` records bind an exact approved concept PNG copy to a stable asset identity
and style version, citing the Owner selection and a hashed source provenance record.
`transformation` records bind that master/record to the 1024 delivery, both output
hashes, semantic anchor, visible fit, visual scale, uniform resampling, color policy,
encoder/tool/helper versions and no-clipping/replay evidence. Old source-app records
retain their original hashes. Both kinds inherit unresolved input rights.

Delivery is `candidate` until the Owner accepts the exact output; merely placing a
file under `production/` does not promote it. The manifest stays unavailable until
acceptance. Versioned raster metadata is optional for old manifest consumers, but
when selected it includes style version, both evidence pointers and the anchor.

See [selected pack candidate index](../concepts/kck-03b/raster-candidate-set.json)
and [Owner master/layout decision](../concepts/kck-03b/evidence/2026-10-06-owner-master-layout-approval.json).
