# KidsCharacterKit AI governance adoption

## Scope and authority

KCK-GOV-02 is an initial static adoption of the Owner's canonical framework,
not a full runtime rollout. The Owner requested this adoption in the current
session on 2026-10-06. This PR also records the proposed snack-motion slices;
it does not authorize their execution or change approved artwork gates.

- Source: <https://github.com/Gavin0099/ai-governance-framework.git>
- Pinned commit: `fb8f6abb09d6419923247183a2ce744d75e65b29` (release 1.3.0).
- Interface: `1`, compatible with `>=1.0.0,<2.0.0`.
- [GOVERNANCE.md](../GOVERNANCE.md) retains Owner approval, provenance, rights
  and slice boundaries. [PLAN.md](../PLAN.md) is planning, not approval.
- Framework copies remain a baseline; `AGENTS.md` and `contract.yaml` calibrate
  it to this asset library. Do not edit protected `AGENTS.base.md`.

The official adopter provides the shared pack rather than a new custom
policy hierarchy. Existing failed input transport gates and the absent motion
content motivate recording evidence and work boundaries using that pack.
No new domain runtime validator or app framework is introduced. Re-evaluate
runtime rollout only as a separate Owner-opened scope after this PR review.

## Installed surfaces and claim boundary

| Surface | Scope |
|---|---|
| Git submodule and consumer lock | Reproducible framework source; not correctness proof |
| Protected baseline and repo AGENTS | Framework discipline plus asset-specific constraints |
| PLAN and domain contract | Current bounded scope, future proposals, existing Owner gates |
| Governance pack and payload config | Official adopter defaults, not automatic session wiring |
| Memory scaffold and canonical writer | Repo-local records; placement does not make them approved |
| Strict framework evidence policy | Official minimal strict policy; does not alter artwork gates |
| GitHub workflow | Drift, existing preflight tests and JSON record validation; CI execution is separate evidence |

Runtime hooks are **not installed**. No `.governance/version_manifest.yaml` is
written claiming installed runtime/hook components, and no agent claims
`hooks_ready` or full adoption. The direct quickstart diagnostic may expose
missing runtime components; retain its actual result. Domain runtime validators
are unregistered (`validators: []`), although existing JSON schemas/tests are
run. Branch protection and required checks are not changed by this PR.

PR #12 contains the proposed rev5 input rules and the A3 attempt evidence; this
PR starts from main and does not import that pending implementation. The
session's execution hold (A3 output gate 4 failed, budget 1/2) remains in PLAN.
Do not resume generation using an older main brief simply because it is present.

## Verification

Use Python 3.12 with PyYAML 6.0.3, Pillow 12.3.0 and jsonschema 4.26.0. In a fresh
checkout first run `git submodule update --init --recursive`. These packages
are check dependencies, not product runtime dependencies. The workflow pins
those direct versions and runs the same static checks.

From the repository root:

```sh
python ai-governance-framework/governance_tools/governance_drift_checker.py --repo . --framework-root ./ai-governance-framework --format human
python concepts/kck-03b1/tools/test_preflight_hash.py
python ai-governance-framework/governance_tools/external_repo_readiness.py --repo . --framework-root ./ai-governance-framework --format human
python ai-governance-framework/governance_tools/quickstart_smoke.py --project-root . --plan PLAN.md --contract contract.yaml --task-text 'KCK-GOV-02 initial static adoption' --format json
python ai-governance-framework/governance_tools/memory_workflow.py --check --repo . --run-guard
```

JSON record validation uses the existing Draft 2020-12 schemas; its exact
command is in `.github/workflows/governance-drift.yml`. Retained local evidence
is under [`.governance/evidence/kck-gov-02/`](../.governance/evidence/kck-gov-02/).
A static PASS does not prove runtime enforcement, asset pixels, Owner visual
approval or commercial-use clearance. Maturity/readiness are diagnostic reports,
not human approval.

After intentional repo extension edits, refresh baseline with the official tool:

```sh
python ai-governance-framework/governance_tools/adopt_governance.py --target . --framework-root ./ai-governance-framework --refresh
```

Never change the protected baseline or weaken a rule to manufacture a PASS.
Future requests to update governance to latest follow the imported F-7 update
protocol; this initial adoption is not an F-7 full-update completion claim.

## Observed initial results (2026-10-06)

- Governance drift: PASS (18 checks), including protected baseline identity.
- Existing main-based preflight regressions: PASS (4 tests). Pending PR #12 has
  different tests/rules and is not included in that count.
- Manifest plus provenance: PASS (11 JSON records against the existing schemas).
- Readiness: `ready=true`, separately `hooks_ready=false`; the aggregate is not
  proof of hook installation.
- Quickstart/external runtime smoke: FAIL. Session start refuses with
  `version_compatibility_unsupported` because the installed-component version
  manifest is absent; pre-task check succeeds. This is retained evidence of the
  runtime rollout gap, not a successful runtime or artwork gate.
- Canonical memory and final maturity reports are separate retained evidence.

## Delivery and reversibility

Keep implementation and its canonical memory companion on one PR. Record
local checks before delivery; report remote ref/CI separately. Owner review
and merge remain pending. Reverting the adoption PR removes this integration;
it does not rewrite pending PR #12 or any original assets. No global hooks,
consumer app configuration or existing artwork bytes are modified.
