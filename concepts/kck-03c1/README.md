# Snack motion checkpoint (partial)

[Owner conditional continuation](../kck-03b/evidence/2026-10-06-owner-conformance-continuation.json)
authorizes work that satisfies the accepted spec. This checkpoint is **candidate**.
No animation availability is added to the character manifest.

- Dinosaur `idle`: explicit static hold of accepted raster, no authored movement.
- Dinosaur `run`: two distinct key poses, 100 ms each / 200 ms loop. One common
  eye-width registration to the accepted master; manual semantic root y835,
  native x475/x449. Earlier y842 recipe remains historical QA. Actual contact
  phase is LEFT then RIGHT, opposite the requested starting phase, recorded as-is.
- Dinosaur `carry`: explicit alias of run with separate snack at anatomical RIGHT
  hand. Magnifier remains LEFT. No additional frames or snack asset are invented.
- Dinosaur `stumble`: immutable raw two-pose output and whole-slot extraction;
  eye-style checks PASS but the existing position/size comparator FAILs. Lean can
  affect screen-space metrics, but no qualified assessment has resolved the result.
  [Read-only follow-up](evidence/dinosaur-stumble-read-only-diagnostic.json) records
  facial ratios against accepted views without inventing a new gate. One provisional
  shared registration also clips 37 alpha=1 pixels and is rejected by the actual
  pipeline. Anchors remain unapproved; no cleanup, acceptance or retry occurred.
- Cat `receive`: two distinct poses, 150/200 ms, 350 ms one-shot; grounded tail
  support, one global registration, anatomical LEFT hand socket and attach event.
  Dinosaur diagnostics remain FAIL because they include white sclera, which also
  happens in the accepted master; qualified Cat visual/glint evidence is separate.
- Cat `wait`: accepted raster static hold; `happy`: second receive pose static hold,
  not newly authored motion. Minimum-pack completeness waits for Dinosaur stumble.

[Partial pack](dinosaur-snack-partial-pack.json) references the six accepted Dinosaur
sheets, exact frame hashes and candidate derivation records. [Run preview](../../artifacts/qa/2026-10-06-dinosaur-run-normalized-v2/preview.png)
is QA APNG only. Fixed canvas/alpha/no-clipping/pixel/timing replay is verified;
source-held inputs are not exposed by the built-in tool and rights stay unresolved.
No game-scene pivot/contact/scale/loop/edge/prop-handoff evidence is available.

Run `python concepts/kck-03c/tools/validate_animation.py concepts/kck-03c1/dinosaur-snack-partial-pack.json`.
A schema-only PASS cannot select production; the validator checks source/model
lifecycle, sockets, events, timing, hashes, extraction and derivative replay.

[Cat candidate pack](cat-snack-candidate-pack.json), [qualified Cat art evidence](evidence/cat-receive-art-conformance.json) and [Cat QA preview](../../artifacts/qa/2026-10-06-cat-receive-normalized/preview.png) preserve the same delivery boundaries.

Master/pose comparison on a common canvas scale is saved under `artifacts/qa/2026-10-06-motion-master-comparison/`. Pose height changes are visible; equal eye registration and anchors do not establish a consumer-scene no-jump result.

[Bounded retry proposal](retry-proposal/README.md) has exact inputs/instructions
for one Dino stumble call and a six-view mouthfix Robot sheet set. All calls are
zero and execution requires the Owner's explicit failed-sequence decision.
