# Concepts

Style-exploration outputs (KCK-03B1). Kept outside `characters/` so that a concept is
never mistaken for a character master. Every concept is a `candidate` until the Owner
approves it ([GOVERNANCE.md](../GOVERNANCE.md)); committing a file here promotes nothing.

Each file has a record in [`provenance/`](../provenance/README.md) (`record_type: concept`).
A committed file may be a **platform-delivered copy** (e.g. WebP) of the tool's original
artifact (e.g. PNG); the record states both, with hashes, and says which one is held here.

| File | Record | Status |
|---|---|---|
| [`kck-03b1/a2-dinosaur-v01.webp`](kck-03b1/a2-dinosaur-v01.webp) | [`dinosaur-concept-01`](../provenance/dinosaur/dinosaur-concept-01.json) | `candidate` |

`kck-03b1/evidence/` holds the unmodified generation-side report and the agent's
measurement scripts used for the record. Rejected and unregistered samples without an
Owner acceptance are not committed; the brief records their hashes and the reasons.
