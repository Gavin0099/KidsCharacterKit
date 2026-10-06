# KCK-03B2 model-sheet checkpoint

Owner approved [Style Bible v1](../../docs/character-style-bible-v1.md) and three
exact character references. [Cat six-sheet acceptance](evidence/2026-10-06-owner-cat-sheets-and-dino-repair.json)
now accepts front/three-quarter/corrected side/back/happy/confused, including newly
proposed back patterns, tail continuity and expressions. Cat sheets are
`approved_reference`, not production. [Exact review set](model-sheet-review-set.json)
binds every selected view to its PNG hash and provenance.

[Dinosaur six-sheet acceptance](evidence/2026-10-06-owner-dinosaur-sheets-approval.json)
records the contextual Owner reply 「Ok 再往下」 after the exact six-sheet review,
including back spike/foot anatomy, hand/prop continuity and new expressions. Both
sets are now approved references; production and rights remain separate. See the
[03B master/layout proposal](../../docs/kck-03b-master-layout-proposal.md) for the
next distinct decisions.

- [Cat six views on checker/white/black](../../artifacts/qa/2026-10-06-cat-six-sheets/contact-sheet.png), [64px](../../artifacts/qa/2026-10-06-cat-six-sheets/small-64.png).
- [Dinosaur six views on checker/white/black](../../artifacts/qa/2026-10-06-dinosaur-six-sheets/contact-sheet.png), [64px](../../artifacts/qa/2026-10-06-dinosaur-six-sheets/small-64.png).

All PNGs are 1254×1254 RGBA. Source canvases use a common preview factor without
independent bbox fit or invented ground anchors. Raw generated outputs are exact
copies; the one separate local repair has documented RGB derivation.

## Failures and authorized continuation

First side jobs failed: Cat reposed its grounded forward tail into an upright
rear curl; Dinosaur kept a front-facing torso under a profile head. Owner
[authorized one targeted edit per side](evidence/2026-10-06-owner-side-correction.json).
Cat side corrected, passing checks; its back/happy/confused were then completed.
Dino torso improved but acquired three belly-line ends instead of two. Stop and
[before/after evidence](../../artifacts/qa/2026-10-06-dinosaur-side-correction/contact-sheet.png)
are retained; the extra line was never waived as acceptable identity.

Owner then explicitly authorized removal of only the upper extra line locally.
[Transformation](evidence/dinosaur-side-belly-correction.json) fixes the exact
source hash and records bounded cream-interior RGB copy, donor offset, encoder
and library versions. All alpha/outside pixels, outer contour and remaining two
strokes are exact; four real-image regressions check these invariants, removal,
reproducibility, wrong-source refusal and overwrite refusal. This made zero new
generation calls. Dino back/happy/confused resumed only after repair validation.
The [completed checkpoint](evidence/2026-10-06-complete-model-sheet-checkpoint.json)
records eight new calls this continuation and fourteen total 03B2 generation
outputs (twelve initial sheets + two authorized side edits), plus one local
RGB derivative. All three failed side originals remain unchanged candidates.
Historical [first side correction checkpoint](evidence/2026-10-06-side-correction-checkpoint.json)
records the intermediate stop before local-repair authorization.

## Measurement and authority boundaries

Unchanged original-pose eye-identity and highlight gates pass for Dino
three-quarter/happy/confused. New front intentionally levels originally tilted
eyes: its old-pose eye-center comparison FAIL is preserved as inapplicable to a
front-view camera change, never relabeled numeric PASS. Front/side actual highlight
coordinates pass. Back has no visible eyes; no eye test is claimed for that view.
Highlight/schema/hash validity alone does not approve anatomy or expressions.

[Job ledger](model-sheet-jobs.json) preserves registered call limits, exact source
and instruction hashes, older unsubmitted prompt versions, conditional resumes
and zero-call derivation. Input images are individual approved references, never
QA collages. Generated tool-held hashes/internal model prompt/model/seed/id are
not exposed, so local requested input hashes are not a generator-side gate PASS.
Some faint alpha reaches raw source canvas edges; preserve it, and require actual
transform/transparent-edge evidence before delivery.

Dinosaur v2d budget remains **2/2**. 03B2 is a separate explicitly authorized
scope, with no reset. Rights remain pending/unknown. Source-app masters and manifest
availability remain untouched. Production/master/visual_scale/semantic anchors,
authored motion and consumer-scene delivery remain later gated work.
