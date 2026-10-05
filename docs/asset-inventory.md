# Asset inventory (KCK-01)

Read-only inventory of Cat, Dinosaur and Robot visual assets found in
`Gavin0099/english-vocab-trainer`, listed as **candidates** for reuse.

**This document does not select anything.** No asset here is marked official,
preferred, selected or recommended. Which assets (if any) enter this library is
an owner decision, made after this slice.

## Scope and method

| Item | Value |
|---|---|
| Source repo | `Gavin0099/english-vocab-trainer` (read-only; not modified) |
| Source commit inspected | `dc9435962b056af66be7cbf201802f691d0ab322` (`main`, shallow clone, depth 1) |
| Inspected | working tree at that commit only; git history and other branches were **not** inspected |
| Files copied into this repo | none |

### Evidence labels

- **Observed** — read directly from a file or computed from the file bytes.
- **Source-stated** — written in a source-repo document or manifest; I did not independently verify it.
- **Inferred** — my reading; may be wrong.
- **Unknown** — no evidence found.

What I computed myself from the files: byte size, SHA-256, PNG/JPEG pixel
dimensions and PNG color type (header only). Alpha statistics and "visible
bounds" below are **source-stated** (from the source repo's manifests) and were
not recomputed. Every SHA-256 computed here matches the hash recorded in the
corresponding source manifest.

## Summary

| Character | Asset candidates | Reference / source images | Notes |
|---|---|---|---|
| Cat | 5 | 1 (JPEG, no alpha) | 2 of the 5 are non-character elements (a paper bag, a heart) |
| Dinosaur | 4 paths, **3 unique files** | 2 (one RGBA, one RGB) | `DinosaurWorldThumbnail` is byte-identical to `DinosaurResearcher` |
| Robot | 1 | 0 in repo | the child's original drawing is not in the repo |

Total: **10 asset paths** (9 unique files) plus **3 reference images**.

## Cat

All five were produced with `image_gen.imagegen` from one owner-provided
reference image (source-stated). Delivered at the tool's native canvas with no
post-generation pixel edits or scaling (source-stated).

Common observed facts: PNG, 8-bit RGBA, 1254×1254.
Source manifest: `resources/skin-art/cat/cat-02-assets-20261003.json`.

| ID | Current filename / asset name | Source path | Bytes | SHA-256 | Depicts | Role stated by source |
|---|---|---|---|---|---|---|
| CAT-A1 | `CatBagKitten` / `artwork.png` | `ios/App/App/Assets.xcassets/CatBagKitten.imageset/artwork.png` | 1,332,012 | `034c6f9a11348f42abdf0005506e491183f9f82ce9088ca4f8639e57bd4ad179` | Orange tabby kitten in a paper bag (from generation prompt) | welcome/home only |
| CAT-A2 | `CatRaisedPaw` / `artwork.png` | `…/CatRaisedPaw.imageset/artwork.png` | 1,255,317 | `9d77b5ba7b6174a0f4a5bec9849ea8fd47e67f407de00e66642a6f0107792f30` | Seated orange tabby raising a front paw (from prompt) | post-answer encouragement / confirmed completion |
| CAT-A3 | `CatEmptyBag` / `artwork.png` | `…/CatEmptyBag.imageset/artwork.png` | 1,101,570 | `cefa041afdeb91efa2bedb2eefd2eb4d74278c074eba5a0a4366e17fd087e2e6` | **Empty kraft paper bag — no character** (from prompt) | non-question empty state only |
| CAT-A4 | `CatWorldThumbnail` / `artwork.png` | `…/CatWorldThumbnail.imageset/artwork.png` | 1,644,273 | `3f7817c9f18c638558856902b1a716e1c56dcf8016f40f28149ca85af0420ab1` | Composite of the cats; generated with CAT-A1 and CAT-A2 as extra inputs | world chooser / welcome only |
| CAT-A5 | `CatCompletionHeart` / `artwork.png` | `…/CatCompletionHeart.imageset/artwork.png` | 431,364 | `bcc0c9c110974ac95abd310c55017cb3ab59412d6ffa5a5bc0356ce521b585ca` | **Coral-pink heart — no character** (from prompt) | completion feedback |

Transparency (source-stated alpha stats; color type RGBA is observed): all five
have real transparency, with 147–934 fully opaque pixels and 244k–893k
partially transparent pixels. "Visible bounds" (alpha > 5%) per source:

| ID | Visible bounds `[x0, y0, x1, y1]` |
|---|---|
| CAT-A1 | 258, 79, 1050, 1183 |
| CAT-A2 | 227, 39, 1045, 1235 |
| CAT-A3 | 204, 218, 1073, 1092 |
| CAT-A4 | 76, 119, 1223, 1173 |
| CAT-A5 | 319, 359, 945, 940 |

Margins differ per asset; the source itself notes they differ from the prompt's
requested values.

Reference image:

| ID | Path | Format | SHA-256 | Notes |
|---|---|---|---|---|
| CAT-R1 | `resources/skin-art/cat/owner-reference-20261003.jpg` | JPEG 1254×1254, no alpha (observed) | `ba50f18b43e6cf1d26ed50b9eff0be1a5088bed94cc8f5f2f36dbce3d0b66c6c` | Owner-provided visual reference; source says it is not a formal transparent asset and is not in the app resource directory |

Usage in the source app:

- **Observed:** asset names are mapped in `ios/App/App/GardenNative/GardenTheme.swift`
  (`CatArtworkRole`, lines ~1383–1392) and rendered by `CatSkinIllustration`,
  `CatCompanionPortrait` and `CatStudyScene`. Those views are called from
  `TodayGardenView`, `SessionCompleteView`, `PracticeTaskRouter`,
  `PracticeCardView`, `PhonicsLessonView`, `OralPASegmentingView`,
  `OralPASoundIsolationView` and `NativeSettingsView`.
- **Observed:** all five names are also referenced in DEBUG-only preview
  fixtures and in `ios/App/AppTests/ContractSmokeTests.swift`.
- **Unknown:** which role (and therefore which asset) each individual call
  site passes, and whether each is reachable in a shipped build. Not traced.
- **Source-stated:** Cat is one of the selectable skins (Garden / Robot / Cat /
  Dinosaur).

Source-stated usage restrictions exist (e.g. no character artwork in
pre-answer question cards; see `resources/skin-art/cat/README.md` and
`docs/design/cat-02-independent-assets-20261003.md`). These are app-level
rules and are recorded here for awareness, not evaluated.

## Dinosaur

Produced with `image_gen.imagegen` (source-stated). The current set is the
"baby" revision (DINO-09, 2026-10-04) that replaced an earlier DINO-01 set;
source says no post-generation pixel edits. Source manifest:
`resources/skin-art/dinosaur/dino-09-assets-20261004.json`.

All PNG, 8-bit RGBA (observed).

| ID | Current asset name | Source path | Dimensions | Bytes | SHA-256 | Depicts (source-stated) |
|---|---|---|---|---|---|---|
| DINO-A1 | `DinosaurResearcher` | `ios/App/App/Assets.xcassets/DinosaurResearcher.imageset/artwork.png` | 1448×1086 | 770,614 | `1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76` | Large mint dinosaur holding a magnifying glass |
| DINO-A2 | `DinosaurWorldThumbnail` | `…/DinosaurWorldThumbnail.imageset/artwork.png` | 1448×1086 | 770,614 | **identical to DINO-A1** | Same bytes as DINO-A1; source calls it a byte-for-byte copy |
| DINO-A3 | `DinosaurJunior` | `…/DinosaurJunior.imageset/artwork.png` | 1320×1191 | 647,813 | `028277f689c17ef9aadc5166f5f71ee50dc6479d692db45a375a4f31e93c13ed` | Small baby dinosaur, no props |
| DINO-A4 | `DinosaurFamily` | `…/DinosaurFamily.imageset/artwork.png` | 1448×1086 | 955,186 | `50e9fc6f561cd35ee32e16e73e2ce7dd7bcfbcfa82a3d96ab1d49809522d23fb` | Group: large dinosaur, egg, small dinosaur |

Visible bounds (source-stated): A1/A2 `[57, 52, 1346, 1061]`, A3
`[85, 21, 1264, 1091]`, A4 `[89, 40, 1392, 1035]`.

Reference images (neither is loaded by the app, per source):

| ID | Path | Format | SHA-256 | Notes |
|---|---|---|---|---|
| DINO-R1 | `resources/skin-art/dinosaur/approved-baby-reference-20261004.png` | PNG 1448×1086 RGBA (observed) | `cc6a77dde05609b2f0068e38cd3deacb7577e0234c56eacf5164fbfd9f77bb0c` | Concept image the owner selected; source says it still contains a white residue patch that the shipped version corrected |
| DINO-R2 | `resources/skin-art/dinosaur/owner-reference-20261004.png` | PNG 1448×1086 **RGB, no alpha** (observed) | `54eed7f9c18c26dcde6d8fda505230be972b34b6435298135dcd4620186c8293` | Owner-provided colored drawing used as input for the first (DINO-01) generation; opaque white background |

Historical versions: source says the DINO-01 set had different bytes
(e.g. Researcher `2217b0a1…`, Junior `40485705…` per
`dino-01-assets-20261004.json`). Those files are **not** in the inspected
working tree; whether they are recoverable from git history was not checked.

Usage in the source app:

- **Observed:** names mapped in `GardenTheme.swift` (`DinosaurArtworkRole`,
  lines ~1146–1155); rendered by `DinosaurSkinIllustration` and
  `DinosaurResearchScene`, called from `TodayGardenView`, `SessionCompleteView`,
  `PracticeTaskRouter`, `PracticeCardView`, `PhonicsLessonView`,
  `OralPASegmentingView`, `OralPASoundIsolationView` and `NativeSettingsView`.
- **Observed:** all four names appear in DEBUG fixtures and `ContractSmokeTests.swift`;
  a test asserts A1 and A2 have identical PNG data.
- **Unknown:** per-call-site role mapping and shipped-build reachability.
- **Source-stated:** `dino-09-assets-20261004.json` records
  `static_render_qualification: "PENDING"`, and the dinosaur README says the
  concept home screen is not device-verified.

## Robot

Single asset. Produced with `image_gen.imagegen` as an identity-preserving
cutout of a child's crayon robot drawing (source-stated).

| ID | Current filename | Source path | Format | Bytes | SHA-256 |
|---|---|---|---|---|---|
| ROBOT-A1 | `robot.png` (asset name `RobotSkinMascot`) | `ios/App/App/Assets.xcassets/RobotSkinMascot.imageset/robot.png` | PNG 1086×1448, 8-bit RGBA (observed) | 1,534,882 | `2a7b4b8c8c75aa0f1ec98337e94b42b9dd94a39bfe2c87dff38f6388f0d69b51` |

- Observed: portrait orientation (the Cat/Dinosaur assets are square or landscape).
- Observed: the filename (`robot.png`) does not follow the `artwork.png`
  convention used by the Cat and Dinosaur imagesets.
- Source-stated alpha: min 0 / max 255; 935,838 transparent, 636,611 partial,
  79 opaque pixels.
- Provenance record: `docs/design/robot-skin-provenance.json`. Its
  `output_sha256` matches the computed hash.
- Reference drawing: **not in the repo** — the record says it is "local
  reference retained outside this commit". Only its SHA-256
  (`ce901872d608305ba52cd5c18f2872189cca8f17171980c73c1533494febdac7`) is recorded.

Usage in the source app:

- **Observed:** rendered by the `RobotSkinMascot` view (`GardenTheme.swift:166`),
  called from `TodayGardenView`, `SessionCompleteView`, `PracticeTaskRouter`,
  `PracticeCardView` and `NativeSettingsView` at heights from 36 to 220 pt.
  Also asserted in `ContractSmokeTests.swift`.
- Observed: a `missing-robot-fixture` DEBUG case tests the fallback when the
  asset is absent.

## Other files that matched but are not character artwork candidates

Listed so nothing is silently dropped. No judgment is made beyond category.

| Group | Path | What it is | Evidence |
|---|---|---|---|
| Vocabulary word illustrations | `ios/App/App/Assets.xcassets/WordIllustrations/word-illustration-*-{cat,dinosaur,robot}.imageset/image.png` (5 files: cambridge-flyers-dinosaur 512×468, elementary-800-cat 512×512, elementary-800-robot 512×512, general-vocab-cat 512×512, general-vocab-dinosaur 474×512) | Per-word teaching pictures for the words "cat", "dinosaur", "robot" | Observed names/dimensions. **Inferred** that they are word-teaching illustrations, not recurring characters. Their provenance lives under `resources/word-illustrations/provenance/` and was **not reviewed** here. |
| Brand mascot SVGs | `public/assets/brand/mascot/mascot_{celebrate,encourage,happy,idle,sleep,water}.svg` | A different mascot (not Cat/Dinosaur/Robot) | **Inferred** from the SVG content (face + sprout gradients). No literal reference to these paths found in source/docs by text search. Provenance: Unknown. |
| App screenshots | `artifacts/evidence/design/garden-ios-ux/**/today-robot-*.png` | Screenshots of the app showing the Robot skin | Observed filenames only; evidence images, not source art. |

## Provenance evidence found in the source repo

| File | Covers | What it says |
|---|---|---|
| `resources/skin-art/cat/README.md` | Cat | Reference is an owner-provided visual baseline (2026-10-03) with SHA-256; CAT-02 assets are untouched tool outputs |
| `resources/skin-art/cat/cat-02-assets-20261003.json` | CAT-A1…A5, CAT-R1 | Tool, full prompts, input/output SHA-256, generated filenames, pixel metadata, allowed role |
| `docs/design/cat-02-independent-assets-20261003.md` | Cat | Allowed roles and inspection notes |
| `resources/skin-art/dinosaur/README.md` | Dinosaur | Owner reference, owner selection of the baby revision, thumbnail is a copy of Researcher |
| `resources/skin-art/dinosaur/generation-record-20261004.json` | DINO-01 (historical) | Prompts incl. one unselected revision |
| `resources/skin-art/dinosaur/generation-record-baby-20261004.json` | DINO-A1…A4 | Prompts for the baby revision |
| `resources/skin-art/dinosaur/dino-09-assets-20261004.json` | DINO-A1…A4 | Current hashes and pixel metadata |
| `resources/skin-art/dinosaur/dino-01-assets-20261004.json` | historical DINO-01 | Superseded hashes; source says not current |
| `docs/design/robot-skin-provenance.json` | ROBOT-A1 | Generator, prompt, reference/output SHA-256, alpha stats, review status, `rights_note` |

Generation records contain absolute paths on the original author's machine
(under `/Users/…/.codex/generated_images/`). The raw generator outputs are
therefore **outside the repo**; only hashes remain.

## Unresolved provenance and rights questions

Nothing below is resolved by this inventory. Each is recorded as pending.

1. **Rights to the underlying reference artwork — Unknown (all three).**
   - Robot: the only explicit statement is in `robot-skin-provenance.json`:
     *"Owner selected the supplied drawing as reference. No independent
     rights/licence audit is claimed."* It also describes the reference as a
     child's drawing; who made it is not stated.
   - Cat and Dinosaur: the references are described as "owner-provided"
     (Cat JPEG, Dinosaur PNG). No statement about who created them, or about
     any rights audit, was found.
2. **Rights status of AI-generated outputs — Unknown.** All ten asset paths
   were generated with a built-in image-generation tool (`image_gen.imagegen`).
   No license terms or commercial-use determination was found in the repo.
   Robot provenance states model name/version/seed were not returned by the
   tool; the Cat and Dinosaur records contain no model field at all.
3. **Commercial-use status — `pending` for every asset.** A text search of
   `docs/design`, `resources/skin-art` and `docs/product` for commercial /
   license / copyright terms found nothing about Cat/Dinosaur/Robot artwork
   (the hits concern TTS audio providers and unrelated items).
4. **Raw originals and robot reference not in repo.** Generator outputs and the
   robot drawing are outside git; only hashes are recorded.
5. **Who the "owner" is for each reference.** Not stated beyond the word
   "owner" in source docs.
6. **Dinosaur DINO-01 historical bytes.** Recoverability from git history not
   checked.

## Ambiguities and duplicates

- **Exact duplicate:** `DinosaurResearcher` = `DinosaurWorldThumbnail` (same
  SHA-256, same bytes).
- **Derived composites:** `CatWorldThumbnail` was generated using the other Cat
  assets as inputs; `DinosaurFamily` was composited from the Researcher and
  Junior art plus an egg. They overlap in content with the single-character files.
- **Non-character Cat elements:** `CatEmptyBag` and `CatCompletionHeart` are
  props, not characters; whether they belong in a character library is for the
  owner to decide.
- **Group vs single:** `CatWorldThumbnail` and `DinosaurFamily` contain
  multiple figures.
- **Canvas inconsistency (observed):** 1254×1254 (Cat), 1448×1086 and 1320×1191
  (Dinosaur), 1086×1448 (Robot); visible bounds differ widely. Not evaluated
  here — normalization is a later slice.
- **Superseded art:** an earlier Dinosaur set exists only in history; the
  current files are the DINO-09 revision.
- **Pose naming:** no asset carries a pose name like idle/greeting; the roles
  above come from source docs, not filenames.
- **Reference vs asset in the same folder:** `approved-baby-reference-…png` is
  RGBA but is a concept image with a known flaw (source-stated), not an app asset.

## Not covered

- Git history and branches of `english-vocab-trainer` other than `main` at the
  inspected commit.
- Per-call-site mapping of artwork role to asset, and whether each is reachable
  in a release build.
- Review of the `resources/word-illustrations/` pipeline and its provenance.
- Pixel-level verification of alpha statistics and visible bounds.
- Any rights or license assessment.
