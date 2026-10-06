# Character preparation and QA tools

The repository-local skill is `.agents/skills/kck-character-pipeline/SKILL.md`.
Codex discovers repository skills from `.agents/skills`; this installation is
local to this checkout. It adds preparation tools, not a generator or runtime.
Use Python 3.12 and `Pillow==12.3.0`, `jsonschema==4.26.0` (the CI pins);
tests also use the existing `PyYAML==6.0.3` dependency.

## Review existing candidates

```sh
python .agents/skills/kck-character-pipeline/scripts/pipeline.py review \
  --source concepts/kck-03b1/inputs/dinosaur-01_DinosaurResearcher.png \
  --label 'A1 source' \
  --source concepts/kck-03b1/outputs/A3-v2d-attempt-01-highlight-corrected.png \
  --label 'A3 corrected' --output artifacts/qa/my-review
```

`review` accepts static RGBA PNG/WebP without altering sources. It writes raw and
decoded RGBA SHA-256, alpha counts, alpha bounds and labeled checker/white/black
contact sheets at normal and 64px canvas extent. One common preview factor is
used for all source canvases. Canvas centering is only a review layout: it neither
aligns semantic anchors nor compares approved relative character heights. Do not
use the sheet as a generation reference. WebP texture measurements remain
codec-confounded; review decoding does not restore its original PNG.

The current [A1/A2/A3/A4 review](../artifacts/qa/2026-10-06-dinosaur-lineup/contact-sheet.png)
uses exact A1, repaired A3 and failed A4 files. A2 is a byte-exact review copy from
PR #10 at `01053171c8d6c815415df1a8c0bfc37441fd7423`; its
[source ledger](../artifacts/qa/references/SOURCE.json) records the candidate,
pending rights and transport limitations. This copy does not merge that PR.

## Extract an existing short strip

After the applicable art/model-sheet gates and generation authorization, use a
single approved seed, one edit job, explicit pose order and 2–4 poses on equal
horizontal slots. Preserve palette, facing, anatomy and the magnifying glass.
Keep the snack separate. The current 03B1 two-object handoff and budget are
unaffected by this later workflow.

```sh
python .agents/skills/kck-character-pipeline/scripts/pipeline.py split-strip \
  --source concepts/my-motion/raw-strip.png --sha256 ACTUAL_64_HEX_SHA256 \
  --frames 4 --output artifacts/qa/my-slots
```

The tool requires a static RGBA PNG with a matching raw hash and width divisible
by the explicit slot count. Every slot is cropped at its full fixed rectangle;
RGBA pixels, transparent RGB and empty margins are preserved. The extraction
report records source hash and exclusive slot rectangles. It does not infer
frames, remove chroma/backgrounds or calculate anchors. Retain this report as
the link from extracted frame hashes to the immutable strip.

## Normalize an existing sequence for candidate QA

The internal [recipe schema](../.agents/skills/kck-character-pipeline/scripts/qa-recipe.schema.json)
is deliberately separate from the future KCK-03C delivery contract. Paths in
recipes resolve from the repository root, not the recipe's directory.

```json
{
  "format": "kck-qa-recipe-v1",
  "canvas": [1024, 1024],
  "target_anchor": [512, 960],
  "scale": 0.5,
  "resampling": "LANCZOS",
  "loop": 0,
  "frames": [
    {"source": "concepts/my-motion/pose-0.png", "sha256": "REPLACE_WITH_RAW_SHA256", "anchor": [800, 1500], "duration_ms": 120},
    {"source": "concepts/my-motion/pose-1.png", "sha256": "REPLACE_WITH_RAW_SHA256", "anchor": [800, 1500], "duration_ms": 180}
  ]
}
```

This is an illustrative recipe, not measured Dinosaur data. Supply measured
semantic anchors and the approved sequence scale before using real art. The
example hash placeholders intentionally fail schema validation.

```sh
python .agents/skills/kck-character-pipeline/scripts/pipeline.py normalize \
  --recipe concepts/my-motion/qa-recipe.json --output artifacts/qa/my-sequence
python .agents/skills/kck-character-pipeline/scripts/pipeline.py check \
  --bundle artifacts/qa/my-sequence
```

All source frames must have the same canvas. A single requested scale produces
one shared resized canvas; rounded dimensions must preserve aspect ratio.
The actual uniform scale and each anchor's pixel-grid rounding error are
recorded. Choose a compatible scale if rounding would distort aspect ratio.
`LANCZOS` serves soft raster art; `NEAREST` is available for pixel fixtures.
Positions come from supplied anchors, never from alpha bbox center/bottom.
Any clipping of nonzero alpha, including faint edge pixels and resampling halos,
fails. Sources are unchanged and outputs are new candidate bundles under
`artifacts/qa/` or `concepts/`; existing destinations, production paths and
repository escapes are rejected. Preparation is staged before publication.

The bundle contains lossless PNG frames, source/output raw and RGBA hashes,
parameters/tool versions, recipe hash, contact sheet and APNG preview. APNG
uses declared millisecond durations, replace blending, no disposal, and `loop=0`
for repeat or `loop=1` for one play. Adjacent identical poses may coalesce;
their combined time and decoded pixels are verified. An entirely identical
sequence is rejected because Pillow would drop animation timing; use a static
raster plus consumer presentation timing for a hold. PNG frames and recipe
remain authoritative; preview files are QA artifacts, not delivery assets.

`check` verifies source/output/recipe/preview hashes, replays the transformation,
and checks canvas, declared anchor, actual uniform scale, pixel sequence, timing
and loop. It is read-only. It cannot infer whether a supplied anchor really is a
foot contact, approve identity/relative visual scale, clear rights, verify prop
sockets or prove game feel. Those require Owner review and consuming-app scene
evidence. No manifest availability changes or production promotions occur.

## Sources and verification

The contact-sheet checker/layout and Pillow preview-save routines adapt
[OpenAI hatch-pet](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet),
pinned at `49f948faa9258a0c61caceaf225e179651397431`. The bundled
[Apache-2.0 license](../.agents/skills/kck-character-pipeline/scripts/hatch_pet/LICENSE.txt)
and [source ledger](../.agents/skills/kck-character-pipeline/scripts/hatch_pet/SOURCE.json)
retain upstream paths, original hashes, adapted hashes and change notices.
The CLI, recipe and tests are KCK-specific integration code.

The strip-first method references `sprite-pipeline`; its code is not copied.
No fixed pet atlas/states, auto-fit, chroma removal, ComfyUI, model downloads or
global skill installation is included. See the [reuse analysis](character-pipeline-reuse-review.md).

```sh
python .agents/skills/kck-character-pipeline/scripts/test_pipeline.py
```

Tests use neutral geometric sequence fixtures and a real canonical read-only
review. They cover shared scale/anchors despite moving props, exact RGBA strip
extraction, soft alpha preservation, timing/loop/coalescing, tampered derivatives,
wrong hashes, clipping, missing metadata, incompatible canvases, path escapes
and overwrite rejection. CI runs them alongside the existing identity,
measurement, repair, provenance and governance checks.
