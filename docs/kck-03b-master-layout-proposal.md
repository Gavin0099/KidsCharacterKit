# KCK-03B master and layout proposal

**Owner accepted this proposal and option B, 2026-10-06.**
[Exact decision and pre-update document hash](../concepts/kck-03b/evidence/2026-10-06-owner-master-layout-approval.json). Both Cat and Dinosaur
six-sheet sets are accepted references. The accepted rules are now applied to the active representation contract.
This decision authorizes delivery candidates; it does not accept unseen output
or set manifest availability.

## Versioned master selection

Recommend the already approved original Cat style translation (`cat-concept-01`)
and corrected Dinosaur style key (`dinosaur-concept-03`) as this pack's default
three-quarter still masters. The six-sheet sets define the other views and new
expressions; they do not replace these defaults. Exact source paths and SHA-256
are in the [layout report](../artifacts/qa/2026-10-06-raster-layout-proposal/report.json).

Owner-approved contract §5/§10 addition:

> An Owner-selected style pack can derive from a hash-bound approved concept
> instead of a source-app asset. Preserve its complete reference/source/generation
> and local-derivative provenance chain. Its selected master is an exact byte copy
> of the approved concept output, never resized, re-encoded or retouched. Put it
> under `characters/<character>/raster/versions/<style_version>/originals/<asset_id>.png`;
> delivery lives in that version's `production/`. Existing source-app originals,
> provenance records and hashes are retained unchanged. Record stable character
> identity (`cat-02`, `dinosaur-01`) and style version (`soft-handmade-v1`) separately.
> A manifest version selection references both selected-master and transformation
> evidence. Selection does not imply production acceptance or rights clearance.

After acceptance, add the smallest schema extension for these real records and
validate backward compatibility. Do not overload existing asset provenance hashes
with concept hashes. Robot, bag Cat and junior Dinosaur remain unavailable/deferred.

## The Cat ground-contact decision

[Measured contacts](../artifacts/qa/2026-10-06-raster-layout-proposal/cat-foot-measurement-grid.png)
show that Cat's resting foreground tail projects below both feet. Manually inspected
foot anchor `(705,1144)` and tail-contact support baseline `(705,1235)` differ by
91 source pixels. Alpha bounds were not used to select either semantic point.
The [comparison](../artifacts/qa/2026-10-06-raster-layout-proposal/cat-anchor-options.png)
shows the consequence: foot anchoring puts the resting tail below a flat ground line;
tail-support anchoring leaves the feet higher, retaining the drawn perspective.

Owner accepted the seated support convention, with this explicit §6 addition:

> `support-baseline` also applies to a seated pose with visible feet when a resting
> tail or carrier defines its projected foreground support. Measure that contact
> manually; document the foot-contact offset. A standing or running pose uses
> `ground-center` between the feet. Do not infer either anchor from alpha extrema.
> All normalized representations share the delivery anchor `(512,960)`; native
> anchors are pose-specific. A consumer scene must verify the actual ground contact.

This is an art/layout decision. In recommended option B, Cat feet remain approximately
54 px above the tail-support line on the 1024 canvas because of the source perspective.
It cannot be fixed by changing scale. If that convention is unsuitable for Snack,
a separately authorized new resting/standing pose is needed; no silent pixel edit
or generation retry is proposed.

Dinosaur proposed native `ground-center` is `(650,1176)`, manually measured between
the two rounded foot contact regions. The [annotation](../artifacts/qa/2026-10-06-raster-layout-proposal/dinosaur-anchor-annotation.png)
and [measurement grid](../artifacts/qa/2026-10-06-raster-layout-proposal/dinosaur-foot-measurement-grid.png)
show the chosen point. These coordinates were separately accepted in the cited layout decision.

## Relative size

[Three actual layout options](../artifacts/qa/2026-10-06-raster-layout-proposal/scale-options.png)
use the proposed seated Cat and standing Dinosaur anchors. Recommend **B**:
Cat `visual_scale=0.80`, Dinosaur `visual_scale=0.95`. Cat's visible total height
is approximately 84% of Dinosaur's. A/C give approximately 79%/90%. These are
measured preview ratios; `visual_scale` itself is not the height ratio.

All proposals obey the existing 1024 canvas, alpha>5% visible fit, side/top safe
margin and bottom exception. Values below 1 also leave room for faint nonzero alpha:
no source alpha is threshold-cleaned, and padded replay verifies no resampled alpha
is clipped. Other characters' scales remain `null`; no junior/parent equality is inferred.

## Review evidence and next authorized work

The [read-only builder](../concepts/kck-03b/tools/build_layout_review.py) source-hashes
both inputs, writes only QA previews, uses a uniform inverse affine BICUBIC transform
in premultiplied alpha, and verifies deterministic pixels, padded no-clipping replay
and visible bounds. Its library/tool hashes, parameters and preview hashes are saved
in the report. Source artwork, approved Bible, manifest and existing originals are
unchanged. Color-profile conversion and production schema/transform implementation
remain explicit 03B work; the QA builder is not the production pipeline.

The Owner decision accepts the versioned concept-master rule, two exact masters,
seated support exception, native anchors and option B. Implement
and validate the immutable master copies and deterministic delivery candidates, obtain
actual production review, and continue 03C. No remote merge or rights approval follows.
