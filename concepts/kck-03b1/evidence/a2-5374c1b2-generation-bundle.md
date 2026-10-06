# A2 v2d generation bundle — UNREGISTERED / PRE-FLIGHT NOT ESTABLISHED

Generated: 2026-10-05 (Asia/Taipei)

## Status

- registration_status: UNREGISTERED
- valid_attempt_number: NONE
- reason: strict pre-flight cannot be certified for this run

## Requested canonical inputs (as stated by Owner)

- source filename: dinosaur-01_DinosaurResearcher.png
- expected source SHA-256: 1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76
- instruction filename: A2_instruction_v2d.txt
- expected instruction size: 2342 bytes
- expected instruction SHA-256: 12c67216741b4bf308d61cdf4390bb773080e9eb5fb5398e9627e49df9a47e1e
- requested execution message: Use the attached dinosaur image as the only image reference. Follow A2_instruction_v2d.txt exactly and generate exactly one image.

## Inputs actually verifiable in this run

- mounted image filename: image(5).png
- mounted image format: PNG RGB
- mounted image dimensions: 1269 x 952
- mounted image size: 441868 bytes
- mounted image SHA-256: 332e8c94af3ff582230bfbf9b0fcb16c02a8f77273489206fb7bead6afa3ea01
- canonical source hash match: FAIL / cannot certify canonical bytes as generation input
- A2_instruction_v2d.txt as separate attachment: NOT PRESENT in the conversation file surface available to this run
- instruction-file SHA-256 independently verified: NO
- fresh-context status: NOT VERIFIABLE from generation metadata
- exact requested execution message as the sole generation-side text: NOT CERTIFIABLE; generation was invoked from the current chat context rather than from a separately verified instruction-file-only handoff

## Generation metadata

- generation id: 5374c1b2-6064-4b10-8345-06cea98f0ef2
- original generation artifact format: PNG RGBA
- original dimensions: 1254 x 1254
- original size: 1140257 bytes
- original SHA-256: fd172d05af4d800e80bc10441834f828db5167ad9152114cc41ddcd5234077b9

## Generation-side measurements on original PNG

### Gate 1 — one character
- connected foreground components (>10 alpha, >10 px): 1
- visible foreground bbox (alpha > 10): x=186..1173, y=64..1193
- visible bbox size: 988 x 1130
- visible bbox width/height ratio: 0.874336
- result: PASS for one connected isolated character

### Gate 2 — true transparency
- canvas: 1254 x 1254 RGBA
- corner alpha (TL, TR, BL, BR): 0, 0, 1, 0
- alpha==0 fraction: 0.507488 (50.7488%)
- dominant nonzero alpha: 253 (89.92% of nonzero-alpha pixels)
- result: PASS

### Gate 3 — eye identity, geometry relative to visible character bbox
Brown-eye segmentation bboxes:
- left eye: x=429, y=484, w=143, h=151
- right eye: x=799, y=388, w=134, h=151

Normalized generated eye geometry vs mounted reference copy:
- left center x: 0.318320 vs 0.314136, delta +0.004184
- left center y: 0.438496 vs 0.438084, delta +0.000411
- left width: 0.144737 vs 0.138743, delta +0.005993
- left height: 0.133628 vs 0.137850, delta -0.004222
- right center x: 0.688259 vs 0.672775, delta +0.015484
- right center y: 0.353540 vs 0.347547, delta +0.005993
- right width: 0.135628 vs 0.133508, delta +0.002120
- right height: 0.133628 vs 0.139019, delta -0.005390

Representative dark-brown eye-color difference by simple RGB segmentation:
- left mean RGB Euclidean delta: 2.38
- right mean RGB Euclidean delta: 2.05

Note: these geometry/color measurements are against the mounted 1269x952 reference copy, not a byte-verified canonical source file.

### Gate 4 — eye highlight style
Coordinates are centers normalized to each segmented dark-eye bbox.
- left large highlight: (x=0.3616, y=0.3003)
- left small highlight: (x=0.4853, y=0.5936), lower-right of large highlight
- right large highlight: (x=0.3434, y=0.3071)
- right small highlight: (x=0.4643, y=0.6018), lower-right of large highlight
- target for large highlight: x=0.30..0.40, y=0.20..0.35
- result: PASS

### Gate 5 — overall identity
- visible bbox width/height ratio: 0.874336
- mounted reference visible bbox ratio: 0.892523 (thresholding white background at >5 RGB distance from white)
- required motifs visually present: back spikes, cream belly with two curved lines, magnifying glass, peach cheeks, tail, feet
- result: visually consistent, but no formal numeric acceptance threshold was provided for this gate

## Conclusion

This artifact is useful as an unregistered measurement sample, but it should NOT be recorded as A2 v2d attempt #1. A valid attempt still requires a run where the source image and instruction file are independently available as attachments and their exact canonical hashes are verified before generation, plus the requested execution message is the only execution message used for the generation handoff.
