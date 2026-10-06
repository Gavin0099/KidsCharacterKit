# KCK-03B2 model-sheet checkpoint

Owner approved [Style Bible v1](../../docs/character-style-bible-v1.md) and the exact
three-character reference set on 2026-10-06. [Approval evidence](evidence/2026-10-06-owner-v1-approval.json)
binds the reviewed draft hash and artwork hashes; Cat/corrected Robot are now
approved references. New model sheets remain candidates, not masters or production.

Six initial built-in `image_gen.imagegen` calls produced six separate **1254×1254
RGBA** PNGs, copied byte-for-byte. No repair/retry/normalization was performed.
The [job ledger](model-sheet-jobs.json) registers one initial call per requested
sheet, exact source/prompt hashes, outcomes and unexecuted jobs. All twelve prompts
are prepared under `instructions/`; a saved prompt does not mean a generation ran.

| Character | Front | Three-quarter | Side | Back / happy / confused |
|---|---|---|---|---|
| Cat | candidate, agent review passes | candidate, agent review passes | **pose continuity FAIL**: tail rises behind instead of resting across front feet | not generated; stopped after side failure |
| Dinosaur | candidate, agent review passes; strict front anatomy Owner pending | candidate; original-pose eye identity + highlight measurements PASS | **view continuity FAIL**: profile head but torso/broad front belly still faces camera | not generated; stopped after side failure |

Agent review is not Owner artwork acceptance. Side failures are preserved as
`candidate`, not assigned the Owner-only `rejected` status. Proposed resolution:
one targeted edit per failed side, preserving approved identity/rendering and
anatomical hand; await Owner disposition before edits or remaining sheets.

## Actual review artifacts

- [Cat normal checker/white/black](../../artifacts/qa/2026-10-06-cat-model-sheets/contact-sheet.png), [64px](../../artifacts/qa/2026-10-06-cat-model-sheets/small-64.png).
- [Dinosaur normal checker/white/black](../../artifacts/qa/2026-10-06-dinosaur-model-sheets/contact-sheet.png), [64px](../../artifacts/qa/2026-10-06-dinosaur-model-sheets/small-64.png).

One common native-canvas factor is used, without independent bbox fit. These views
do not establish semantic ground anchors or approved `visual_scale`.

## Measurement and authority boundaries

Dinosaur three-quarter retains the original pose, so the unchanged eye-identity
comparison is applicable and passes, alongside both highlight gates. The new front
view intentionally levels the original tilted eyes: its original-pose eye-center
comparison reports FAIL and is retained as an **inapplicable pose comparison**, not
a new front-view PASS. Its two actual highlight coordinates independently pass.
Side has one eye by design; its numeric highlight gate passes. Neither a highlight
PASS nor schema validity cures the side torso/pose failure.

The generator-held bytes/internal augmented prompt/model/seed/id are unavailable.
Records preserve the exact local requested inputs/instruction and returned raw PNG;
no generator-side input-hash PASS is claimed. Some faint nonzero alpha pixels reach
source canvas edges; preserve them. These candidate canvases are not delivery-ready,
and any later clipping/transparent-edge cleanup needs explicit transform evidence.

Dinosaur **v2d stays 2/2**, no reset/retry; 03B2 initial jobs are a separate explicitly
authorized scope. All rights remain pending/unknown. No character originals,
manifest availability, production, authored motion or 3D is changed. Style Bible
file acceptance is complete; 03B2 model-sheet acceptance and later slices are not.
