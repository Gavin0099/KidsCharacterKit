# KCK-03B raster checkpoint

Owner accepted the [master/layout proposal](../../docs/kck-03b-master-layout-proposal.md),
including versioned concept masters, seated Cat support, semantic anchors and B size.
[Exact decision](evidence/2026-10-06-owner-master-layout-approval.json) retains the
reviewed document/report hashes and direct answer.

The [candidate index](raster-candidate-set.json) binds three immutable master copies
and three actual 1024 RGBA sRGB files. Cat/Dinosaur are production under the
[Owner conditional acceptance](evidence/2026-10-06-owner-conformance-continuation.json);
Robot now uses an accepted [mouthfix amendment](../../docs/character-reference-amendments.md)
after [tongue feedback](evidence/2026-10-06-owner-robot-tongue-feedback.json). Its
previous version remains a withdrawn candidate in `retired_records`. Sources remain byte-exact;
old source-app records and all failed exploration outputs are unchanged. New
master/transformation record kinds retain full provenance and pending rights.

[Actual background review](../../artifacts/qa/2026-10-06-raster-delivery/contact-sheet.png)
and [64px review](../../artifacts/qa/2026-10-06-raster-delivery/small-64.png) use a common
canvas factor. Their generic pending list is not a reversal of accepted scale/anchor
decisions; actual production acceptance and consumer-scene evidence remain separate.

`tools/produce_raster.py` builds a candidate pack from the fixed Owner decision:
source hash/status gates; exact-copy master; uniform inverse affine BICUBIC in
premultiplied RGBa; source samples interpreted as sRGB (no ICC profile present);
explicit output sRGB chunk; pinned encoder/library metadata; immutable no-overwrite
publication. It rejects unreviewed profiles and full nonzero alpha/halo clipping,
replays on a padded canvas and checks repeated pixels. No threshold alpha cleanup
or new artwork is performed. `--check` replays the complete candidate bundle
read-only; it is a candidate-checkpoint verifier, not a lifecycle promotion command.

Five regressions cover actual masters/repeated pixels+encoder, independent anchor
and uniform geometry, faint-alpha/profile/input rejection, overwrite/source gates,
and negative provenance/manifest schemas. Use `tools/validate_raster.py` for current lifecycle/status verification after
acceptance. The original builder's `--check` replays the historical candidate stage
and cannot byte-compare later status evidence/index additions. Cat/Dinosaur
and new Robot-mouthfix availability is true; all old/failed outputs are retained. A4 stays 2/2; this checkpoint made no
generation calls. Rights remain pending/unknown; PR merge and app release separate.
