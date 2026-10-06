# Repository Workflow

## Repo Facts

- KidsCharacterKit is a technology-neutral character asset library, not an app.
- Data: PNG candidates/delivery assets, JSON provenance and manifests, Markdown
  contracts, Python image-diagnostic helpers. No platform adapter exists.
- Existing preflight diagnostics use Pillow. JSON schemas use Draft 2020-12.
- Owner approval/provenance/rights/slice boundaries are in `GOVERNANCE.md`.
- Proposed work ordering and bounded current scope are in `PLAN.md`.
- Framework comes from a pinned Git submodule. Initialize with
  `git submodule update --init --recursive` in a fresh checkout.
- Session-derived memory uses the pinned canonical `memory_record.py` writer.
  Run `memory_workflow.py --check --repo . --run-guard` before a completion claim.
- Local static verification commands are in `docs/ai-governance-adoption.md`.
  Do not infer runtime hook installation or art approval from those checks.
