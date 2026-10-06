# Animation contract v1 (KCK-03C)

Engine-neutral frame sequences for the authorized snack minimum pack. Established
under the [Owner's conformance continuation](../concepts/kck-03b/evidence/2026-10-06-owner-conformance-continuation.json);
it follows the approved representation, style, model-sheet and separate-prop rules.
It adds no gameplay runtime and claims no consumer-scene completion.

## Representation

A pack uses stable `character_id` and `style_version`, a hashed selected master and
six accepted model-sheet references, and exact PNG frames under
`characters/<character>/animation-2d/versions/<style_version>/<action>/` when
finally delivered. Candidate frames stay under `concepts/` or `artifacts/qa/`.
[Schema](../manifests/animation-manifest.schema.json) and semantic/file validator are
both required: schema validity alone cannot prove timing sums or hashes.

Coordinates are source/image pixels, x right / y down. Delivery canvas is 1024²
RGBA sRGB. Root anchor is `(512,960)`, with the same accepted semantic type as the
character raster. Ground reference remains constant during air/raised-foot frames;
never re-anchor to whichever foot or alpha extremum is currently lowest. The Cat
seated support convention retains its recorded perspective offset. All frames use
one scale consistent with the selected character master; do not auto-fit per frame
or silently shrink individual clips to avoid clipping. New pose/foot alignment and
scale must be measured and documented, not inferred from strip edges.

Each frame has a relative PNG path, raw SHA-256, `duration_ms` and fixed anchor.
Frames are ordered explicitly; filenames use zero-based `frame-000.png` etc but
filenames never define the sequence. PNG frames and metadata are authoritative.
A sprite strip is an immutable generation source; retain equal-slot extraction
rectangles and hashes. APNG/contact sheets are QA only. Skeleton, 3D and platform
adapters are deferred.

## Timing and loop

`duration_ms` is the sum of frame durations, with each positive integer duration
1–65535 ms. `fps` is null for variable timing; a numeric nominal FPS must correspond
to each duration within 1 ms of `1000/fps`. The integer durations are authoritative.
Looping returns to frame zero; a one-shot holds its last frame. A single-frame wait
is an explicit static hold, not an authored moving animation. A moving clip needs
at least two distinct frame hashes; repeated stills cannot claim authored motion.

Initial need-driven actions: Dinosaur `idle`, `run`, `stumble`, optional `carry`
alias of a run designed with a free snack hand; Cat `wait`, `receive`, `happy`.
Robot authored motion is blocked until its six-sheet gate passes. Existing `greeting`
vocabulary remains available without promising an actual clip.

## Props, sockets and events

The snack is a separate consumer/library prop; never bake it into character frames.
Dinosaur's identity magnifying glass stays in its anatomical LEFT hand. A carry run
uses a recorded `snack` socket at its RIGHT hand; receiving Cat uses a declared
receiving socket without silently swapping its raised anatomical LEFT paw. Sockets
are delivery-pixel points for each frame, with the anatomical hand recorded. A clip
requiring a snack socket must provide it on every frame. Socket existence does not
prove a prop asset or successful handoff. A prop's independent hash/rights travel
with it when an actual prop is selected.

Events are typed `foot_contact`, `prop_attach`, `prop_release`, `action_complete`,
with integer `time_ms` inside `[0,duration_ms]` and optional socket/hand or foot.
Prop events require an existing socket; attach/release is consumer state, not a baked
image change. Dispatch t=0 when entering a clip; thereafter dispatch events in
`(previous_time,new_time]` once per pass, including complete at duration. For loops,
finish the outgoing pass before firing next pass t=0. Consumer owns interruption,
state transitions, scoring and procedural bob/squash/rotation. `carry` alias shares
run frames/timing/foot events, adds an external prop binding and cannot alias an alias.

## Delivery gate

`candidate` means structural/art checks may be complete but no final motion delivery
is selected. `production` additionally needs exact conformance evidence and actual
consumer-scene validation of pivot, scale, ground contact, timing, loop, transparent
edges and prop handoff. Animation availability remains empty until those checks are
complete; app feel is not established by an APNG. The conformance instruction removes
repeated Owner questions for conforming work, not this evidence requirement.

The pack references the hashed generation/derivation provenance record for each
frame and preserves unresolved input rights. Only implemented actions appear in the
character manifest; an alias is explicit and never counted as extra drawn frames.

The present motion-frame provenance schema records candidate derivations only.
Final frame provenance/status and sRGB encoding must be selected after conformance
and the scene gate; this checkpoint cannot promote QA frames. Scene evidence binds
the canonical pack fingerprint (SHA-256 of sorted compact UTF-8 JSON), includes
actual context/capture and all seven checks. Changing a frame or timing invalidates
that evidence. Dinosaur V2 numeric diagnostics are retained separately; new poses
or Cat sclera/iris must not silently inherit an unqualified measurement PASS.
