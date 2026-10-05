# KidsCharacterKit

A small, reusable Swift package that provides shared child-friendly characters
for multiple native iOS apps: the character assets, a stable character identity,
a minimal SwiftUI presentation, and optional basic motion.

Apps should be able to say *"I want the Cat"* without knowing which image file
backs it.

## Status

**KCK-00 — bootstrap.** The package builds and imports; it contains no character
assets and no presentation code yet. See [Roadmap](#roadmap).

## Initial character scope

- Cat
- Dinosaur
- Robot

## What belongs in this package

- Reusable character assets
- Character identity / model
- Minimal reusable SwiftUI presentation
- Basic optional character motion
- Provenance metadata for every asset

## What does NOT belong in this package

- Game logic
- Levels
- Scoring
- Stars / rewards
- Learning progress
- Persistence
- Backend / networking
- App navigation
- A general-purpose UI / design system
- Speculative animation APIs (motion is added only when a real app needs it)

## Layout

```
Package.swift
Sources/KidsCharacterKit/
    Resources/Characters/     character assets (empty until KCK-02)
Tests/KidsCharacterKitTests/
provenance/                   per-asset provenance records
docs/asset-spec.md            asset specification
```

## Development

```
swift build
swift test
```

Requires Swift 5.9+ (iOS 16 / macOS 13 deployment targets).

## Roadmap

| Slice | Goal |
|---|---|
| KCK-00 | Repository bootstrap (this slice) |
| KCK-01 | Asset inventory and provenance |
| KCK-02 | Asset normalization |
| KCK-03 | Character API (`CharacterID`, asset resolver) |
| KCK-04 | SwiftUI `CharacterView`, minimal motion, Reduce Motion |
