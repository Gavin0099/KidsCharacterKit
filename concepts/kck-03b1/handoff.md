# KCK-03B1 B1-A generation handoff

How the Owner starts one generation, under the **v2d pre-flight gate, rev. 4** in
[`docs/kck-03b1-brief.md`](../../docs/kck-03b1-brief.md). If this file and the brief differ,
the brief decides. Rev. 4 is proposed in PR #12; Owner acceptance is pending.
The image gate is unchanged; do not start a formal attempt while the upload mismatch remains unresolved.

## Source objects (exactly two per generation)

| Object | Where | Gate (full 64-hex) |
|---|---|---|
| Source image | [`inputs/dinosaur-01_DinosaurResearcher.png`](inputs/dinosaur-01_DinosaurResearcher.png) | decodes to 1448x1086; decoded RGBA8 pixel SHA-256 = `5b9b014e0347ec89aab3fe896ae7a94d76202d92adb24aefce404533b71aeab8`. The canonical/source file SHA-256 `1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76` is provenance; the actual held raw SHA is reported separately and may differ (pixel-identical re-encode). |
| Instruction A2 | [`instructions/A2_instruction_v2d.txt`](instructions/A2_instruction_v2d.txt) | canonical-content SHA-256 `b1b54564a7b6b5e4a8ee0420a9d52c7053eb2edf7d108561493a913a51a668d1` |
| Instruction A3 | [`instructions/A3_instruction_v2d.txt`](instructions/A3_instruction_v2d.txt) | canonical-content SHA-256 `53e34cde5ec972a98347dd8e808f49a4ac3fb831621ddd3f1acf33c85eeaff09` |
| Instruction A4 | [`instructions/A4_instruction_v2d.txt`](instructions/A4_instruction_v2d.txt) | canonical-content SHA-256 `99679d30a86d32be6555e1071babecf50aa25233feff69ab3db9c0b923c522ee` |

`inputs/dinosaur-01_DinosaurResearcher.png` is a byte-exact copy of `dinosaur-01` (source
repo commit `dc9435962b056af66be7cbf201802f691d0ab322`, file SHA-256 above, the same hash as
[`provenance/dinosaur/dinosaur-01.json`](../../provenance/dinosaur/dinosaur-01.json)). It is
a generation input, not the character master and not under `characters/`.

Algorithms (fixed; reference implementation `tools/preflight_hash.py`):

- **Image pixel hash:** decode, convert to RGBA8, row-major top to bottom, SHA-256 of the raw
  RGBA bytes; no color management, no alpha premultiplication.
- **Instruction canonical hash:** UTF-8, drop a leading BOM, CRLF/CR to LF, remove all empty
  lines, join the remaining lines with LF and append exactly one LF, SHA-256. Empty means
  zero characters; preserve spaces and tabs. Do not hash the execution or verification
  message as part of the instruction.

## The one Owner message (fresh conversation, nothing sent before it)

Upload the two objects (download them from this directory) into a brand-new conversation. Then
send **only** this message (A3 shown; replace the file name and the instruction hash for another
variant). A repository-fetch route was tried on 2026-10-06 and does not work: the image tool
would not accept the fetched PNG as the image reference.

```text
Use the provided dinosaur image as the only image reference. Follow A3_instruction_v2d.txt exactly and generate exactly one image.

Before generating, verify the content you actually hold for dinosaur-01_DinosaurResearcher.png and A3_instruction_v2d.txt (not a preview, display name or metadata) and report the full 64-hex values you computed:
1. Image (gate): decode to RGBA8, confirm 1448x1086, and compute the SHA-256 of the raw RGBA bytes read row by row from the top. It must equal 5b9b014e0347ec89aab3fe896ae7a94d76202d92adb24aefce404533b71aeab8.
2. Instruction (gate): take the UTF-8 text you hold, drop a leading BOM, convert CRLF/CR to LF, remove all empty lines (zero characters; preserve spaces and tabs), join remaining lines with LF and append exactly one LF, and compute the SHA-256. It must equal 53e34cde5ec972a98347dd8e808f49a4ac3fb831621ddd3f1acf33c85eeaff09. Say whether you hold it as an attachment, a fetched file, or expanded text.
3. Provenance (not a gate): if you hold the raw file bytes of either object, also report their SHA-256; if you only see expanded text, write "raw bytes not exposed".
Only if both gates PASS, generate exactly one image following A3_instruction_v2d.txt. If a gate fails, or you cannot access the content or cannot compute a gate hash, stop: report PRE-FLIGHT FAILED or INCONCLUSIVE and do not call image generation.
```

The sentence says "provided" on purpose; it is transport-neutral.

## After the generation (does not count as generation input)

Ask the generation side for: generation id (or `not exposed`); the original artifact's format,
dimensions and SHA-256; the SHA-256 of any delivered copy; the pre-flight gate values it computed and its raw-SHA provenance (or `raw bytes not exposed`);
the highlight coordinates and the five gate results by its own measurement. The measuring
agent then re-measures independently and records each actor and copy separately.
