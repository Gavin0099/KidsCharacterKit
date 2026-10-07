# Governance (Lite)

How AI-generated work, approvals and rights are handled in this repository. Kept
deliberately short: this is an asset library, not a product with a release process.

**Roles.** The **Owner** decides. **Agents** (AI assistants, including Claude) propose,
produce candidates, and record evidence. An agent never approves its own work.

## The four rules

### 1. AI produces candidates; only the Owner approves

Anything an agent creates is a **candidate**: concepts, style translations, model
sheets, redrawn characters, text changes to approved docs. It becomes an approved
baseline only when the Owner explicitly accepts it.

- Agents do not independently approve or promote anything (approved, official,
  preferred, selected, final, or any status change). An agent may record an explicit
  Owner approval and update the corresponding status only when that Owner decision is
  cited as evidence in the record. "The agent judged it good enough" is never
  sufficient; "the Owner said they approve this version" is.
- The "Approved direction" in the [style bible](docs/character-style-bible.md) and the
  decisions in the [contract](docs/character-representation-contract.md) are changed
  only with Owner approval. Agents may propose edits in a PR; they do not move
  exploration values into approved rules.
- An approval given in chat is not durable. The agent records it in the next PR as the
  cited evidence ("Owner decision, stated in session, date") so it exists in the repo.
- A merge performed by the Owner, or explicitly authorized by the Owner, accepts the
  repository changes as submitted. A merge event itself never promotes a `candidate`
  to `approved_reference` or `production`; that needs an explicit, cited Owner decision
  (see Statuses). An automated or agent-initiated merge without Owner authorization
  accepts nothing.

### 2. Provenance is a hard gate

When an agent creates or modifies an asset, the record must contain: input assets and
their SHA-256, the tool (and version if known), the prompt or a reference to it, and
the output's SHA-256 (see [provenance](provenance/README.md)).

If any of that is missing, the asset stays a `candidate` and may not be called a
production asset. A file being committed does not make it a character.

### 3. Agents do not upgrade rights status

`commercial_use_status`, `rights_review_status` and `ownership_status` stay
`pending` / `unknown` until the Owner records them with **external evidence** (for
example the generator's written terms for the plan used, or documented authorship).
"AI generated", "owner provided", "the app already ships it" and "it looks original"
are not evidence. This applies to new and derived assets, which inherit the unresolved
status of their inputs.

`production` status says the work is complete, not that it is cleared for release. Use
in a released app of any asset whose `commercial_use_status` is not `confirmed` is the
Owner's decision, made in that app.

### 4. A slice boundary is an authority boundary

Each slice (see the README roadmap) has a stated scope, e.g. `KCK-03B1 = style
exploration`. Work outside that scope, even if obviously useful, needs a new slice the
Owner opens. Finishing a slice does not authorize the next one.

At a gate, the agent stops and reports. Examples: B1 may not continue into raster
normalization (03B), animation (03C) or 3D (03D); 03B may not start while the
`visual_scale` decision is open.

## Statuses

For candidate artwork and derived representations:

```
candidate
   │  Owner explicitly approves
   ▼
approved_reference
   │  production work done + evidence complete + Owner approves
   ▼
production
```

Side states, set by the Owner: `rejected`, `deferred`, `superseded` (names its successor).

| Status | Meaning | Not implied |
|---|---|---|
| `candidate` | Produced or proposed; under review | usable by apps; rights; identity |
| `approved_reference` | Owner accepted it as a baseline for further work (e.g. style anchor, model sheet) | production-ready; rights |
| `production` | Delivered representation: `available: true` in the manifest, provenance and transformation evidence complete, Owner approved | rights cleared (rule 3) |
| `rejected` | Owner decided not to use it; kept for history | |
| `deferred` | Not now | |
| `superseded` | Replaced; points to the successor | |

Example: a unified-style concept `cat-style-concept-v2` is a `candidate` even though it
is committed. After the Owner reviews the three characters side by side and accepts it,
it becomes `approved_reference`.

Existing records use `selection.status: selected_core_candidate` for the five
owner-selected core assets. That means "selected for processing", i.e. stage
`candidate`. Concept records (`record_type: concept`, KCK-03B1) carry the formal `status`
field defined above, and a `status_evidence` list quoting the Owner decision that set it;
the five asset records are not changed.

## Consumers

Apps and games use this repo as a **versioned, external dependency**. They do not edit
character definitions, assets or the manifest locally; changes come through this repo.

## When unsure

Stop and ask the Owner. Do not resolve an approval, rights or scope question by
choosing the likeliest answer.

## AI governance integration

The pinned framework and repo-specific [AGENTS.md](AGENTS.md) support execution
discipline, evidence and memory. [PLAN.md](PLAN.md) records bounded work and
proposed future slices; [adoption notes](docs/ai-governance-adoption.md) describe
what is installed and what remains unverified. These surfaces do not replace
the four rules above. Framework installation or a static check cannot approve
artwork, waive a model-sheet requirement, upgrade rights or open another slice.
