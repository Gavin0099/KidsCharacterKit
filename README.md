# KidsCharacterKit

A technology-neutral library of shared child-friendly character assets
(Cat, Dinosaur, Robot) that multiple apps can reuse from one source of truth.

It is an **asset library**, not a framework. There is no Swift (or any other
language) code here. A platform adapter is added only when a real app shows
repeated lookup code worth extracting.

## Questions this repo answers

- Which images are the official assets?
- Where is the original of each, and where did it come from?
- Is there any open question about commercial-use rights?
- Are names, canvas, transparency and padding consistent?
- Can different apps use the same file without per-app adjustment?
- When an asset changes, what changed?

## Layout

```
assets/originals/<character>/    untouched source images
assets/production/<character>/   normalized images apps consume
provenance/<character>/          per-asset source and rights records
manifests/characters.json        language-neutral character → asset map
docs/asset-spec.md               canvas / transparency / anchor / padding
docs/naming.md                   file naming convention
```

## Rules

- Unknown provenance or rights is recorded as `pending` / `unknown`, never inferred.
- Originals are never overwritten; production files are derived from them.
- Not in scope: game logic, levels, scoring, rewards, learning progress,
  persistence, networking, navigation, UI/design system, animation APIs.

## Roadmap

| Slice | Goal |
|---|---|
| KCK-01 | Read-only inventory of existing Cat / Dinosaur / Robot assets |
| KCK-02 | Provenance records and schema |
| KCK-03 | Normalize: copy originals, produce production assets, asset spec, naming |
| KCK-04 | Language-neutral manifest |
| later | Platform adapter (e.g. Swift) only once an app needs it |

## Status

Skeleton only. No assets or provenance records yet.
