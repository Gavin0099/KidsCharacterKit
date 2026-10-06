"""Read-only candidate review and explicit-anchor QA bundles. No generation."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import tempfile
from pathlib import Path

import PIL
from PIL import Image
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from hatch_pet.make_contact_sheet import make_sheet
from hatch_pet.render_animation_previews import save_preview

ROOT = Path(__file__).resolve().parents[4]
SCHEMA = Path(__file__).with_name("qa-recipe.schema.json")
MANUAL = ["Owner identity/style acceptance", "semantic ground contact and pivot",
          "relative character visual scale", "consumer-scene timing and prop handoff", "rights evidence"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def within_repo(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path escapes repository")
    return path


def destination(root, value):
    path = within_repo(root, value)
    if not any(path.is_relative_to(root / prefix) and path != root / prefix
               for prefix in ("artifacts/qa", "concepts")):
        raise ValueError("new QA output must be below artifacts/qa or concepts")
    if path.exists():
        raise ValueError("refusing to overwrite existing output")
    return path


def load_png(path, png_only=True):
    data = path.read_bytes()
    with Image.open(path) as opened:
        formats = ("PNG",) if png_only else ("PNG", "WEBP")
        if opened.format not in formats or opened.mode != "RGBA" or getattr(opened, "n_frames", 1) != 1:
            raise ValueError("source must be a single-frame RGBA " + ("PNG" if png_only else "PNG/WebP"))
        frame = opened.copy()
    return frame, facts(frame, data)


def facts(frame, data):
    alpha = frame.getchannel("A")
    counts = alpha.histogram()
    return {"bytes": len(data), "sha256": digest(data), "rgba_sha256": digest(frame.tobytes()),
            "canvas": list(frame.size), "mode": frame.mode,
            "alpha": {"zero": counts[0], "partial": sum(counts[1:255]), "opaque": counts[255]},
            "nonzero_alpha_bbox_exclusive": list(alpha.getbbox()) if alpha.getbbox() else None}


def finish(root, output, build):
    target = destination(root, output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".kck-qa-", dir=target.parent) as temporary:
        stage = Path(temporary) / "bundle"
        stage.mkdir()
        report = build(stage)
        write_json(stage / "report.json", report)
        # No output is published until every source, derivative and preview passes.
        if target.exists():
            raise ValueError("output appeared during preparation; refusing overwrite")
        stage.rename(target)
    return report


def review(root, sources, labels, output):
    if len(sources) != len(labels) or not sources:
        raise ValueError("one explicit label per source required")
    loaded = [load_png(within_repo(root, value), png_only=False) for value in sources]

    def build(stage):
        frames = [entry[0] for entry in loaded]
        layout = make_sheet(frames, labels, stage / "contact-sheet.png")
        small = make_sheet(frames, labels, stage / "small-64.png", extent=64)
        return {"format": "kck-qa-review-v1", "candidate_only": True, "manual_pending": MANUAL,
                "sources": [{"path": str(within_repo(root, path).relative_to(root)), "label": label, **info}
                            for path, label, (_, info) in zip(sources, labels, loaded)],
                "contact_sheet": layout, "small_view": small}

    return finish(root, output, build)


def read_recipe(path):
    recipe = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(recipe)
    return recipe


def split_strip(root, source, sha256, count, output):
    if type(count) is not int or not 2 <= count <= 32:
        raise ValueError("strip requires 2..32 explicit equal-width slots")
    path = within_repo(root, source)
    strip, info = load_png(path)
    if info["sha256"] != sha256:
        raise ValueError("strip source hash mismatch")
    if strip.width % count:
        raise ValueError("strip width must be divisible by slot count")

    def build(stage):
        width = strip.width // count
        cells = []
        for index in range(count):
            bounds = [index * width, 0, (index + 1) * width, strip.height]
            frame = strip.crop(bounds)
            target = stage / f"frame-{index:03d}.png"
            frame.save(target)
            cells.append({"path": target.name, "source_slot_exclusive": bounds,
                          "output_facts": facts(frame, target.read_bytes())})
        return {"format": "kck-qa-strip-v1", "candidate_only": True,
                "source": str(path.relative_to(root)), "source_facts": info,
                "slot_count": count, "frames": cells, "manual_pending": MANUAL}

    return finish(root, output, build)


def prepare(root, recipe_path, output):
    recipe = read_recipe(within_repo(root, recipe_path))
    loaded = []
    for entry in recipe["frames"]:
        frame, info = load_png(within_repo(root, entry["source"]))
        if info["sha256"] != entry["sha256"]:
            raise ValueError("source hash mismatch: " + entry["source"])
        if not frame.getchannel("A").getbbox():
            raise ValueError("empty source frame")
        if any(not 0 <= coordinate <= size for coordinate, size in zip(entry["anchor"], frame.size)):
            raise ValueError("source anchor outside canvas")
        loaded.append((frame, info))
    source_size = loaded[0][0].size
    if any(frame.size != source_size for frame, _ in loaded):
        raise ValueError("sequence sources must share one canvas; no per-frame fit")
    target_size = tuple(recipe["canvas"])
    target_anchor = recipe["target_anchor"]
    if any(coordinate >= size for coordinate, size in zip(target_anchor, target_size)):
        raise ValueError("target anchor outside canvas")
    scaled_size = tuple(round(size * recipe["scale"]) for size in source_size)
    if min(scaled_size) < 1 or scaled_size[0] * source_size[1] != scaled_size[1] * source_size[0]:
        raise ValueError("rounded scale must preserve aspect ratio; choose grid-compatible scale")
    actual_scale = scaled_size[0] / source_size[0]
    resampling = getattr(Image.Resampling, recipe["resampling"])

    def build(stage):
        frames, records = [], []
        for index, (entry, (source, source_info)) in enumerate(zip(recipe["frames"], loaded)):
            scaled = source.copy() if scaled_size == source.size else source.resize(scaled_size, resampling)
            scaled_anchor = [round(v * actual_scale) for v in entry["anchor"]]
            offset = [target_anchor[i] - scaled_anchor[i] for i in range(2)]
            bounds = scaled.getchannel("A").getbbox()
            if bounds is None:
                raise ValueError("frame vanished at requested scale")
            x, y = offset
            if bounds[0] + x < 0 or bounds[1] + y < 0 or bounds[2] + x > target_size[0] or bounds[3] + y > target_size[1]:
                raise ValueError("clipping nonzero alpha, including soft edge pixels")
            frame = Image.new("RGBA", target_size)
            # Unmasked paste preserves RGBA bytes at scale 1, including partial alpha.
            frame.paste(scaled, (x, y))
            path = stage / f"frame-{index:03d}.png"
            frame.save(path)
            records.append({"path": path.name, "source": entry["source"], "source_facts": source_info,
                            "anchor": target_anchor, "source_anchor": entry["anchor"], "offset": offset,
                            "anchor_rounding_error_px": [scaled_anchor[i] - entry["anchor"][i] * actual_scale for i in range(2)],
                            "duration_ms": entry["duration_ms"], "output_facts": facts(frame, path.read_bytes())})
            frames.append(frame)
        write_json(stage / "recipe.json", recipe)
        make_sheet(frames, [f"frame {i}" for i in range(len(frames))], stage / "contact-sheet.png")
        save_preview(frames, [e["duration_ms"] for e in recipe["frames"]], stage / "preview.png", recipe["loop"])
        preview = preview_facts(stage / "preview.png", frames, recipe)
        return {"format": "kck-qa-sequence-v1", "candidate_only": True, "manual_pending": MANUAL,
                "canvas": list(target_size), "target_anchor": target_anchor,
                "requested_scale": recipe["scale"], "actual_uniform_scale": actual_scale,
                "resampling": recipe["resampling"], "tools": {"Pillow": PIL.__version__, "Python": platform.python_version()},
                "recipe_sha256": digest((stage / "recipe.json").read_bytes()), "frames": records, "preview": preview}

    return finish(root, output, build)


def preview_facts(path, frames, recipe):
    # Pillow can coalesce identical adjacent frames. Verify the time-expanded
    # pixel sequence, so coalescing cannot hide altered poses or wrong duration.
    expected = []
    for frame, entry in zip(frames, recipe["frames"]):
        pixels = digest(frame.tobytes())
        if expected and expected[-1][0] == pixels:
            expected[-1][1] += entry["duration_ms"]
        else:
            expected.append([pixels, entry["duration_ms"]])
    actual = []
    with Image.open(path) as preview:
        if preview.info.get("loop") != recipe["loop"] or preview.size != frames[0].size:
            raise ValueError("preview canvas/loop mismatch")
        for index in range(preview.n_frames):
            preview.seek(index)
            actual.append([digest(preview.convert("RGBA").tobytes()), preview.info.get("duration")])
    if actual != expected:
        raise ValueError("preview pixels/timing mismatch")
    return {"path": path.name, "sha256": digest(path.read_bytes()), "encoded_frames": len(actual),
            "duration_ms": sum(item[1] for item in actual), "loop": recipe["loop"], "rgba_and_timing_verified": True}


def check(root, bundle):
    directory = within_repo(root, bundle)
    report = json.loads((directory / "report.json").read_text(encoding="utf-8"))
    if report.get("format") != "kck-qa-sequence-v1" or report.get("candidate_only") is not True:
        raise ValueError("not a candidate sequence bundle")
    recipe = read_recipe(directory / "recipe.json")
    if digest((directory / "recipe.json").read_bytes()) != report["recipe_sha256"]:
        raise ValueError("recipe hash mismatch")
    if len(report["frames"]) != len(recipe["frames"]):
        raise ValueError("frame count mismatch")
    if report["canvas"] != recipe["canvas"] or report["target_anchor"] != recipe["target_anchor"] or report["requested_scale"] != recipe["scale"] or report["resampling"] != recipe["resampling"]:
        raise ValueError("transformation metadata mismatch")
    frames = []
    source_size = None
    for index, (record, entry) in enumerate(zip(report["frames"], recipe["frames"])):
        if record["path"] != f"frame-{index:03d}.png":
            raise ValueError("unexpected frame path")
        source, source_info = load_png(within_repo(root, entry["source"]))
        frame, info = load_png(directory / record["path"])
        if source_info["sha256"] != entry["sha256"] or source_info != record["source_facts"]:
            raise ValueError("source integrity mismatch")
        if source_size is not None and source.size != source_size:
            raise ValueError("source canvas mismatch")
        source_size = source.size
        if info != record["output_facts"]:
            raise ValueError("output integrity mismatch")
        if frame.size != tuple(recipe["canvas"]) or record["anchor"] != recipe["target_anchor"] or record["duration_ms"] != entry["duration_ms"]:
            raise ValueError("canvas/declared anchor/timing mismatch")
        scaled_size = tuple(round(v * recipe["scale"]) for v in source.size)
        scale = scaled_size[0] / source.width
        if min(scaled_size) < 1 or scaled_size[0] * source.height != scaled_size[1] * source.width or report["actual_uniform_scale"] != scale:
            raise ValueError("uniform scale mismatch")
        offset = [recipe["target_anchor"][i] - round(entry["anchor"][i] * scale) for i in range(2)]
        error = [round(entry["anchor"][i] * scale) - entry["anchor"][i] * scale for i in range(2)]
        if record["source"] != entry["source"] or record["source_anchor"] != entry["anchor"] or record["offset"] != offset or record["anchor_rounding_error_px"] != error:
            raise ValueError("anchor transformation mismatch")
        scaled = source.copy() if scaled_size == source.size else source.resize(scaled_size, getattr(Image.Resampling, recipe["resampling"]))
        bounds = scaled.getchannel("A").getbbox()
        if bounds is None or bounds[0] + offset[0] < 0 or bounds[1] + offset[1] < 0 or bounds[2] + offset[0] > frame.width or bounds[3] + offset[1] > frame.height:
            raise ValueError("clipping or empty derivative")
        expected = Image.new("RGBA", frame.size)
        expected.paste(scaled, tuple(offset))
        if expected.tobytes() != frame.tobytes():
            raise ValueError("derivative disagrees with recipe")
        frames.append(frame)
    preview = preview_facts(directory / "preview.png", frames, recipe)
    if preview != report["preview"]:
        raise ValueError("preview integrity mismatch")
    return {"ok": True, "candidate_only": True, "frames": len(frames), "manual_pending": MANUAL}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    review_parser = sub.add_parser("review")
    review_parser.add_argument("--source", action="append", required=True)
    review_parser.add_argument("--label", action="append", required=True)
    review_parser.add_argument("--output", required=True)
    normalize = sub.add_parser("normalize")
    normalize.add_argument("--recipe", required=True)
    normalize.add_argument("--output", required=True)
    strip = sub.add_parser("split-strip")
    strip.add_argument("--source", required=True)
    strip.add_argument("--sha256", required=True)
    strip.add_argument("--frames", type=int, required=True)
    strip.add_argument("--output", required=True)
    verify = sub.add_parser("check")
    verify.add_argument("--bundle", required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    try:
        if args.command == "review":
            report = review(root, args.source, args.label, args.output)
        elif args.command == "normalize":
            report = prepare(root, args.recipe, args.output)
        elif args.command == "split-strip":
            report = split_strip(root, args.source, args.sha256, args.frames, args.output)
        else:
            report = check(root, args.bundle)
    except (ValueError, OSError, KeyError, ValidationError) as error:
        parser.exit(2, f"QA failed: {error}\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
