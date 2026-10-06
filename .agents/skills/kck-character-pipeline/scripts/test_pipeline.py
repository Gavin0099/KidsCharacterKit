"""Spec fixtures: neutral geometry only, never generated character motion."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from PIL import Image
from jsonschema.exceptions import ValidationError

sys.path.insert(0, str(Path(__file__).parent))
import pipeline
from hatch_pet.render_animation_previews import save_preview


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        (self.root / "concepts/fixtures").mkdir(parents=True)
        self.inputs = []
        for index in range(2):
            frame = Image.new("RGBA", (12, 12))
            # Body and standing point stay fixed while a tail/prop changes bbox.
            for x in range(5, 8):
                for y in range(5, 9):
                    frame.putpixel((x, y), (23, 101, 200, 253))
            frame.putpixel((1 if index == 0 else 10, 7), (220, 11, 51, 128))
            path = self.root / f"concepts/fixtures/{index}.png"
            frame.save(path)
            self.inputs.append(path)
        self.before = [path.read_bytes() for path in self.inputs]
        self.recipe = {"format": "kck-qa-recipe-v1", "canvas": [24, 24],
                       "target_anchor": [12, 18], "scale": 1, "resampling": "NEAREST", "loop": 0,
                       "frames": [{"source": str(path.relative_to(self.root)),
                                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                   "anchor": [6, 9], "duration_ms": duration}
                                  for path, duration in zip(self.inputs, (80, 175))]}

    def prepare(self, recipe=None, output="artifacts/qa/sequence"):
        path = self.root / "recipe.json"
        path.write_text(json.dumps(recipe or self.recipe))
        return pipeline.prepare(self.root, "recipe.json", output)

    def test_shared_anchor_ignores_changed_tail_bbox_and_preserves_soft_alpha(self):
        report = self.prepare()
        self.assertEqual([record["offset"] for record in report["frames"]], [[6, 9], [6, 9]])
        for index in range(2):
            with Image.open(self.root / f"artifacts/qa/sequence/frame-{index:03d}.png") as frame:
                self.assertEqual(frame.getpixel((11, 14)), (23, 101, 200, 253))
                self.assertEqual(frame.getpixel((7 if index == 0 else 16, 16)), (220, 11, 51, 128))
            self.assertEqual(self.inputs[index].read_bytes(), self.before[index])
        self.assertTrue(pipeline.check(self.root, "artifacts/qa/sequence")["ok"])

    def test_one_scale_for_whole_sequence(self):
        self.recipe["scale"] = 2
        self.recipe["canvas"] = [32, 32]
        self.recipe["target_anchor"] = [16, 24]
        report = self.prepare()
        self.assertEqual(report["actual_uniform_scale"], 2)
        for index in range(2):
            with Image.open(self.root / f"artifacts/qa/sequence/frame-{index:03d}.png") as frame:
                # Scale 2 expands a 3x4 body into 6x8 with identical placement.
                body = [(x, y) for y in range(32) for x in range(32)
                        if frame.getpixel((x, y)) == (23, 101, 200, 253)]
                self.assertEqual(len(body), 48)
                self.assertEqual((min(x for x, _ in body), min(y for _, y in body)), (14, 16))

    def test_wrong_source_hash_fails_without_publishing(self):
        self.recipe["frames"][1]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.prepare()
        self.assertFalse((self.root / "artifacts/qa/sequence").exists())

    def test_alpha_one_pixel_clipping_is_rejected_atomically(self):
        with Image.open(self.inputs[1]) as source:
            frame = source.copy()
        frame.putpixel((0, 0), (12, 12, 12, 1))
        frame.save(self.inputs[1])
        self.recipe["frames"][1]["sha256"] = hashlib.sha256(self.inputs[1].read_bytes()).hexdigest()
        self.recipe["target_anchor"] = [5, 8]  # Shift left/up by 1.
        with self.assertRaisesRegex(ValueError, "clipping"):
            self.prepare()
        self.assertFalse((self.root / "artifacts/qa/sequence").exists())
        self.assertEqual(self.inputs[0].read_bytes(), self.before[0])

    def test_overwrite_and_production_destination_rejected(self):
        self.prepare()
        before = (self.root / "artifacts/qa/sequence/report.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "overwrite"):
            self.prepare()
        self.assertEqual((self.root / "artifacts/qa/sequence/report.json").read_bytes(), before)
        with self.assertRaisesRegex(ValueError, "QA output"):
            self.prepare(output="characters/dinosaur-01/raster/production/test")

    def test_symlink_escape_and_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / "concepts/escape").symlink_to(outside, target_is_directory=True)
            for output in ("concepts/escape/bundle", "../outside"):
                with self.assertRaisesRegex(ValueError, "escapes"):
                    self.prepare(output=output)

    def test_missing_anchor_invalid_duration_and_unknown_recipe_keys(self):
        for mutation in ("anchor", "duration", "unknown"):
            recipe = copy.deepcopy(self.recipe)
            if mutation == "anchor":
                del recipe["frames"][0]["anchor"]
            elif mutation == "duration":
                recipe["frames"][0]["duration_ms"] = 0
            else:
                recipe["auto_fit"] = True
            with self.subTest(mutation=mutation), self.assertRaises(ValidationError):
                self.prepare(recipe)

    def test_canvas_mismatch_and_non_rgba_rejected(self):
        for size, mode in (((11, 12), "RGBA"), ((12, 12), "RGB")):
            Image.new(mode, size, "red").save(self.inputs[1])
            self.recipe["frames"][1]["sha256"] = hashlib.sha256(self.inputs[1].read_bytes()).hexdigest()
            with self.subTest(size=size, mode=mode), self.assertRaises(ValueError):
                self.prepare()

    def test_apng_pixels_explicit_timing_and_once_loop(self):
        self.recipe["loop"] = 1
        report = self.prepare()
        self.assertEqual(report["preview"]["duration_ms"], 255)
        self.assertEqual(report["preview"]["loop"], 1)
        with Image.open(self.root / "artifacts/qa/sequence/preview.png") as preview:
            self.assertEqual(preview.n_frames, 2)
            for index, duration in enumerate((80, 175)):
                preview.seek(index)
                self.assertEqual(preview.info["duration"], duration)
                self.assertEqual(preview.getpixel((11, 14)), (23, 101, 200, 253))

    def test_identical_frames_can_coalesce_without_losing_time(self):
        repeat = copy.deepcopy(self.recipe["frames"][0])
        repeat["duration_ms"] = 120
        self.recipe["frames"].insert(1, repeat)
        report = self.prepare()
        self.assertEqual(report["preview"]["duration_ms"], 375)
        self.assertTrue(pipeline.check(self.root, "artifacts/qa/sequence")["ok"])

    def test_identical_only_sequence_rejected_without_silent_timing_loss(self):
        self.recipe["frames"][1]["source"] = self.recipe["frames"][0]["source"]
        self.recipe["frames"][1]["sha256"] = self.recipe["frames"][0]["sha256"]
        with self.assertRaisesRegex(ValueError, "all frames identical"):
            self.prepare()
        self.assertFalse((self.root / "artifacts/qa/sequence").exists())

    def test_check_detects_pixel_tampering_even_with_replaced_output_hash(self):
        self.prepare()
        path = self.root / "artifacts/qa/sequence/frame-001.png"
        frame, _ = pipeline.load_png(path)
        frame.putpixel((12, 14), (255, 0, 0, 253))
        frame.save(path)
        report_path = path.parent / "report.json"
        report = json.loads(report_path.read_text())
        report["frames"][1]["output_facts"] = pipeline.facts(frame, path.read_bytes())
        pipeline.write_json(report_path, report)
        with self.assertRaisesRegex(ValueError, "disagrees with recipe"):
            pipeline.check(self.root, "artifacts/qa/sequence")

    def test_check_rejects_changed_preview_timing(self):
        self.prepare()
        folder = self.root / "artifacts/qa/sequence"
        frames = [pipeline.load_png(folder / f"frame-{i:03d}.png")[0] for i in range(2)]
        save_preview(frames, [81, 175], folder / "preview.png", 0)
        with self.assertRaisesRegex(ValueError, "timing mismatch"):
            pipeline.check(self.root, "artifacts/qa/sequence")

    def test_real_canonical_review_is_read_only_and_reports_known_hash(self):
        source = pipeline.ROOT / "concepts/kck-03b1/inputs/dinosaur-01_DinosaurResearcher.png"
        before = source.read_bytes()
        report = pipeline.review(pipeline.ROOT, [str(source)], ["canonical source"],
                                 "artifacts/qa/test-review-" + Path(self.temporary.name).name)
        output = pipeline.ROOT / ("artifacts/qa/test-review-" + Path(self.temporary.name).name)
        import shutil
        self.addCleanup(shutil.rmtree, output)
        self.assertEqual(report["sources"][0]["sha256"], "1515f5860c6f497c5a9a84da11b9e125b05aa63ead4e08ffe8142899872dbb76")
        self.assertEqual(source.read_bytes(), before)
        self.assertFalse(report["contact_sheet"]["anchor_alignment"])

    def test_packaged_skill_and_vendor_license_ledger(self):
        skill = Path(__file__).parents[1] / "SKILL.md"
        metadata = yaml.safe_load(skill.read_text().split("---")[1])
        self.assertEqual(metadata["name"], skill.parent.name)
        self.assertTrue(metadata["description"])
        vendor = Path(__file__).parent / "hatch_pet"
        ledger = json.loads((vendor / "SOURCE.json").read_text())
        for name, record in ledger["files"].items():
            actual = hashlib.sha256((vendor / name).read_bytes()).hexdigest()
            self.assertEqual(actual, record.get("adapted_sha256", record["upstream_sha256"]))
        self.assertIn("Apache License", (vendor / "LICENSE.txt").read_text())

    def test_strip_slots_preserve_exact_rgba_without_bbox_fitting(self):
        strip = Image.new("RGBA", (24, 12))
        originals = [pipeline.load_png(path)[0] for path in self.inputs]
        for index, frame in enumerate(originals):
            strip.paste(frame, (index * 12, 0))
        path = self.root / "concepts/fixtures/strip.png"
        strip.save(path)
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        report = pipeline.split_strip(self.root, str(path), sha, 2, "artifacts/qa/slots")
        self.assertEqual(report["source_facts"]["sha256"], sha)
        for index, frame in enumerate(originals):
            extracted, _ = pipeline.load_png(self.root / f"artifacts/qa/slots/frame-{index:03d}.png")
            self.assertEqual(extracted.tobytes(), frame.tobytes())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), sha)

    def test_strip_bad_hash_and_nondivisible_width_rejected(self):
        source = self.inputs[0]
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            pipeline.split_strip(self.root, str(source), "0" * 64, 2, "artifacts/qa/bad")
        with self.assertRaisesRegex(ValueError, "divisible"):
            pipeline.split_strip(self.root, str(source), sha, 5, "artifacts/qa/bad")
        self.assertFalse((self.root / "artifacts/qa/bad").exists())


if __name__ == "__main__":
    unittest.main()
