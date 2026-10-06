# KCK-03B1 B1-A generation handoff

How the Owner starts one generation, under the **v2d pre-flight gate, rev. 3** in
[`docs/kck-03b1-brief.md`](../../docs/kck-03b1-brief.md). If this file and the brief differ,
the brief decides.

## Source objects (exactly two per generation)

| Object | Where | Gate (full 64-hex) |
|---|---|---|
| Source image | [`inputs/dinosaur-01_DinosaurResearcher.png`](inputs/dinosaur-01_DinosaurResearcher.png) | decodes to 1448x1086; decoded RGBA8 pixel SHA-256 = `5b9b014e0347ec89aab3fe896ae7a94d76202d92adb24aefce404533b71aeab8`. The canonical/source file SHA-256 `1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76` is provenance; the actual held raw SHA is reported separately and may differ (pixel-identical re-encode). |
| Instruction A2 | [`instructions/A2_instruction_v2d.txt`](instructions/A2_instruction_v2d.txt) | canonical-content SHA-256 `12c67216741b4bf308d61cdf4390bb773080e9eb5fb5398e9627e49df9a47e1e` |
| Instruction A3 | [`instructions/A3_instruction_v2d.txt`](instructions/A3_instruction_v2d.txt) | canonical-content SHA-256 `c93b136768f35baf12e9c55da09571cd6a86ab307221abbe875ff511555c9884` |
| Instruction A4 | [`instructions/A4_instruction_v2d.txt`](instructions/A4_instruction_v2d.txt) | canonical-content SHA-256 `d667795522e258351cb0686230fba66d829698057404c86738ba32d5fba4bf34` |

`inputs/dinosaur-01_DinosaurResearcher.png` is a byte-exact copy of `dinosaur-01` (source
repo commit `dc9435962b056af66be7cbf201802f691d0ab322`, file SHA-256 above, the same hash as
[`provenance/dinosaur/dinosaur-01.json`](../../provenance/dinosaur/dinosaur-01.json)). It is
a generation input, not the character master and not under `characters/`.

Algorithms (fixed; reference implementation `tools/preflight_hash.py`):

- **Image pixel hash:** decode, convert to RGBA8, row-major top to bottom, SHA-256 of the raw
  RGBA bytes; no color management, no alpha premultiplication.
- **Instruction canonical hash:** UTF-8, drop a leading BOM, CRLF/CR to LF, exactly one trailing
  LF, SHA-256.

## The one Owner message (fresh conversation, nothing sent before it)

Provide the two objects either as uploaded files, or by naming the repository files at a
pinned commit for the generation side to fetch. Then send **only** this message (A3 shown;
replace the file name and the instruction hash for another variant; replace `<COMMIT>`):

```text
Use the provided dinosaur image as the only image reference. Follow A3_instruction_v2d.txt exactly and generate exactly one image.

Before generating, verify the content you actually hold for dinosaur-01_DinosaurResearcher.png and A3_instruction_v2d.txt (not a preview, display name or metadata) and report the full 64-hex values you computed:
1. Image (gate): decode to RGBA8, confirm 1448x1086, and compute the SHA-256 of the raw RGBA bytes read row by row from the top. It must equal 5b9b014e0347ec89aab3fe896ae7a94d76202d92adb24aefce404533b71aeab8.
2. Instruction (gate): take the UTF-8 text you hold, drop a leading BOM, convert CRLF/CR to LF, keep exactly one trailing LF, and compute the SHA-256. It must equal c93b136768f35baf12e9c55da09571cd6a86ab307221abbe875ff511555c9884. Say whether you hold it as an attachment, a fetched file, or expanded text.
3. Provenance (not a gate): if you hold the raw file bytes of either object, also report their SHA-256; if you only see expanded text, write "raw bytes not exposed".
Only if both gates PASS, generate exactly one image following A3_instruction_v2d.txt. If a gate fails, or you cannot access the content or cannot compute a gate hash, stop: report PRE-FLIGHT FAILED or INCONCLUSIVE and do not call image generation.

(Source objects, if fetched: Gavin0099/KidsCharacterKit at commit <COMMIT>, paths concepts/kck-03b1/inputs/dinosaur-01_DinosaurResearcher.png and concepts/kck-03b1/instructions/A3_instruction_v2d.txt.)
```

The last paragraph is only for the fetched-from-repository route; delete it when uploading. The
sentence says "provided" on purpose so that it is true for both routes.

## After the generation (does not count as generation input)

Ask the generation side for: generation id (or `not exposed`); the original artifact's format,
dimensions and SHA-256; the SHA-256 of any delivered copy; the pre-flight gate values it computed and its raw-SHA provenance (or `raw bytes not exposed`);
the highlight coordinates and the five gate results by its own measurement. The measuring
agent then re-measures independently and records each actor and copy separately.
