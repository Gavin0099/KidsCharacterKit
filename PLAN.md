# PLAN.md
<!-- governance-baseline: overridable -->
<!-- baseline_version: 1.0.0 -->

> **最後更新**: 2026-10-06
> **Owner**: repository owner (Gavin0099)
> **Freshness**: Sprint (7d)

## Current Phase

- **KCK-GOV-02 — AI governance initial adoption**: local static implementation
  validated; governance proposal awaiting Owner review. Authorized by Owner in the
  current session (「然後可以倒入ai goverance了」). Done condition: pinned canonical
  framework, official adoption baseline, calibrated repo rules and contract,
  proposed slice plan, honest local evidence, canonical memory and one reviewable
  PR. Initial adoption is distinct from runtime/hook rollout and full adoption.
- **KCK-03B1 — style exploration** remains active. Owner approved deterministic
  A3 highlight-only repair and accepted A3 Balanced texture. The preserved A3
  derivative passes all five independent output gates; corrected-art and style
  anchor approval remain pending. Original A3 gate-4 failure remains recorded.
- Fresh-chat A4 passed both input hashes and generated exactly one candidate.
  Independent output gates 3 (eye identity) and 4 (highlights) failed. The shared
  v2d generation budget is now **2/2**; no further generation is permitted under
  the current budget. Record failure and await Owner disposition.
- This review branch locally combines pending PR #14 governance and PR #12
  rev5 inputs/evidence. It does not establish remote merge or main availability.
- No production raster, authored motion or 3D is available on this baseline.
  Manifest availability is false/empty and asset rights remain pending.

## Active Sprint

- [x] Identify canonical `Gavin0099/ai-governance-framework` and pin source.
- [x] Run official dry-run/adopter; retain protected baseline and repo extensions.
- [x] Define asset-library authority/risk boundaries and proposed slice ordering.
- [x] Run static checks, existing tests, readiness and runtime diagnostic smoke;
  record actual PASS/FAIL/UNKNOWN separately.
- [x] Commit validated static implementation; record canonical milestone for
  its separate memory companion. Delivery uses one draft PR; remote publication
  and ref/CI status are reported separately without a post-push memory loop.
- [ ] Owner review/merge of the governance PR (not agent-authorized).
- [x] Owner disposition of A3: source-locked deterministic repair; texture accepted.
- [ ] Owner disposition of failed A4 and review/merge of pending PR #12, separately.
- [x] Record Owner's continuous-execution instruction (2026-10-06):
  「導入後按照slice 做下去 除非有問題 不然就做到完」.
  Proceed through the snack critical path without re-asking about routine steps;
  report actual gate failures, conflicting specifications and visual decisions.
- [x] Repair only A3 large eye highlights; preserve all alpha, small highlights,
  original bytes and unrelated pixels. Independent five gates PASS; 18 tests PASS.
- [x] Execute the remaining A4 slot with unchanged original inputs and handoff.
  Input gates PASS; output eye identity/highlight gates FAIL. Budget 2/2.
- [x] Search GitHub reuse options at Owner request; save source-linked analysis in
  `docs/character-pipeline-reuse-review.md`. No external skill installed or run.
- [ ] Owner disposition of A4 failure and review of corrected A3 before advancing
  visual selection; no budget reset, broad correction or production promotion.

## Backlog

Owner has now authorized continuous execution of the snack critical path
**03B1 → 03B2 → 03B → 03C → 03C1 → 03C2**, subject to actual problems and existing
acceptance gates. Routine work within that path need not be separately opened
again. Scope authorization does not approve unseen artwork, waive a hard gate,
reset the shared attempt budget, or attest to merge of an exact PR head.
03D/04 remain deferred. The consumer-app SNACK-01 scene remains a distinct repo
scope; this instruction does not identify a consumer checkout.

| Slice | Minimal delivery and completion gate | Snack dependency |
|---|---|---|
| KCK-03B1 Style Exploration | Dino style key → Cat/Robot static translation → lineup; Owner accepts shared world and preserved identity | Final art yes; Robot static lineup remains required by current brief |
| KCK-03B2 Style Bible v1 | Owner-approved outline, lighting, materials, eyes, palette, proportions/exceptions and required model sheets | Final authored assets yes |
| KCK-03B Raster Production | Versioned selected-master provenance; exact-copy originals; deterministic transparent 1024 delivery; agreed visual scale and semantic ground anchors; Owner production approval | Final static assets yes |
| KCK-03C Animation Contract | Engine-neutral action/timing/loop/anchor/event schema; distinguish authored frames from procedural motion; prop socket/layer/handoff semantics | Final motion pack yes; keep lightweight |
| KCK-03C1 Snack Motion Minimum Pack | Dino idle/run/stumble; carry may reuse run plus separate snack; Cat wait and receive/happy; 2–4 key poses only if applicable model-sheet gate is satisfied | Final motion prototype yes |
| KCK-03C2 Motion QA & Delivery | Test fixed canvas/sequence scale, pivot/ground contact, timing, transparency and prop handoff in consumer scene; deliver manifest | Final motion delivery yes |
| KCK-03D 3D Contract | Future neutral 3D representation contract; no models in this slice | No; defer |
| KCK-04 Extended Motion Library | Additional expressions/actions/Robot motion/variants only against an actual consumer need | No; defer |

Asset delivery order: **03B1 → 03B2 → 03B → 03C → 03C1 → 03C2**.
A **SNACK-01 placeholder motion/test scene can begin in the consuming app in
parallel**, under that app's own authorization. It can test bob/squash/timing
before final art and later provide 03C2 integration evidence. Final delivery and
placeholder experiments have different dependencies; QA must not wait for a
scene that is itself blocked on QA.

Keep the target to Cat + Dinosaur sufficient for a snack-delivery prototype.
Robot motion, all poses, full expression packs, skins and 3D are deferred.
Do not interpret equal canvas/anchor as equal character height.

## Decision Log

- 2026-10-06: Owner requested initial governance adoption. Canonical source is
  `https://github.com/Gavin0099/ai-governance-framework.git`, pinned at
  `fb8f6abb09d6419923247183a2ce744d75e65b29` (release 1.3.0, interface 1).
  Existing `GOVERNANCE.md` Owner/provenance/rights/slice rules remain authoritative.
- 2026-10-06: Owner opened continuous execution of the snack critical path
  (quoted above). Owner subsequently approved the proposed programmatic A3 repair
  (「好的 做下去」), leaving the remaining generation slot for A4. The A4 output
  failure and exhausted budget are actual problems; pause generation, preserve
  evidence and continue the explicitly requested tool-reuse analysis.
- Pending Owner decisions, **no approved contract changes in this PR**:
  1. Current style bible requires full model sheets before authored animation.
     A single-view shortcut for 2–4 poses would require explicit gate change;
     Robot motion/model-sheet production may wait, static lineup may not.
  2. Define how Owner-selected new style art becomes a versioned master without
     losing source/output hashes or overwriting existing originals. The current
     representation contract identifies selected source-app assets as masters.
  3. Resolve junior/parent `visual_scale`, per-character semantic ground anchors
     and Dinosaur's locked magnifying-glass identity when carrying a snack.
  4. Decide failed A4 disposition and corrected-A3 visual acceptance. The current
     branch includes PR #12 inputs/evidence without claiming remote merge;
     installing governance does not decide artwork acceptance or reset budget.

## Known Risks

- Planning cannot silently waive model-sheet, identity or selected-master rules.
- Main and pending PR #12 have different input-gate revisions; always identify
  the branch/commit used for a hash/test/attempt claim.
- This adoption includes static files and a CI workflow. Global/local runtime
  hooks are not installed; no version manifest claims installed hook components.
  Retain readiness/smoke gaps rather than manufacturing a full-adoption PASS.
- Schema validity does not prove asset hashes, style quality, ownership or rights.
- Framework update and hook rollout are separate bounded scopes. Re-evaluate the
  adoption gaps after Owner review; do not expand governance speculatively.
