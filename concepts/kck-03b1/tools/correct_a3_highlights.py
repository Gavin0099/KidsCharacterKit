#!/usr/bin/env python3
"""Owner-authorized, source-locked A3 highlight repair; no image generation.

Reflect only the large highlight and its restoration pixels horizontally within
its own eye. Swap RGB from the original image (not a generated/inpainted fill),
keep every alpha byte and all pixels outside the two symmetric patch masks.
The two small highlights remain unchanged. Original input is never overwritten.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from measure_output import fill_holes, label4

SOURCE_SHA = '345b25c5f9b390497d71267b66546dcebd4cb643872ccadf347108072fd03baf'
# Prior independent measurement: exclusive maxima, viewer-left then right.
PATCHES = [
    {'eye_bbox': [445, 497, 582, 647], 'large_bbox': [504, 516, 554, 568], 'reflection_sum_x': 1021},
    {'eye_bbox': [796, 390, 929, 542], 'large_bbox': [850, 407, 899, 459], 'reflection_sum_x': 1717},
]


def repair(raw):
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError('Source hash mismatch: this operation is only approved for exact A3 attempt #1')
    with Image.open(io.BytesIO(raw)) as im:
        if im.mode != 'RGBA' or im.size != (1254, 1254):
            raise ValueError('Expected source RGBA 1254x1254')
        original = np.array(im)
    result = original.copy()
    union = np.zeros(original.shape[:2], dtype=bool)
    details = []
    for patch in PATCHES:
        x0, y0, x1, y1 = patch['large_bbox']
        # Includes the original antialias halo, not just the >235 measurement core.
        rx0, ry0, rx1, ry1 = x0-2, y0-2, x1+2, y1+2
        ex0, ey0, ex1, ey1 = patch['eye_bbox']
        crop = original[ey0:ey1, ex0:ex1]
        dark = (crop[..., 0] < 110) & (crop[..., 1] < 70) & (crop[..., 2] < 60) & (crop[..., 3] > 200)
        labels, _ = label4(dark)
        counts = np.bincount(labels.ravel())
        counts[0] = 0
        support = np.zeros_like(union)
        filled = fill_holes(labels == counts.argmax())
        # Preserve a three-pixel outer eye rim so highlight holes stay enclosed.
        interior = np.array(Image.fromarray(filled.astype(np.uint8)*255).filter(ImageFilter.MinFilter(7))) > 0
        support[ey0:ey1, ex0:ex1] = interior
        yy, xx = np.mgrid[ry0:ry1, rx0:rx1]
        yy, xx = yy.ravel(), xx.ravel()
        mirrored = patch['reflection_sum_x'] - xx
        eligible = support[yy, xx] & support[yy, mirrored]
        yy, xx, mirrored = yy[eligible], xx[eligible], mirrored[eligible]
        mask = np.zeros_like(union)
        mask[yy, xx] = True
        mask[yy, mirrored] = True
        my, mx = np.where(mask)
        ex0, ey0, ex1, ey1 = patch['eye_bbox']
        if not (np.all((mx >= ex0) & (mx < ex1) & (my >= ey0) & (my < ey1))
                and np.all(original[my, mx, 3] > 200)):
            raise ValueError('Repair leaves the opaque eye interior')
        donor_x = patch['reflection_sum_x'] - mx
        # Read all donors from immutable source; do not touch alpha.
        result[my, mx, :3] = original[my, donor_x, :3]
        union |= mask
        details.append({**patch, 'source_roi': [rx0, ry0, rx1, ry1],
                        'mask_pixels': int(mask.sum()),
                        'changed_pixels': int(np.any(result[my, mx] != original[my, mx], axis=1).sum())})
    if not np.array_equal(result[..., 3], original[..., 3]):
        raise AssertionError('Alpha changed')
    if not np.array_equal(result[~union], original[~union]):
        raise AssertionError('Pixels outside authorized patches changed')
    return result, details


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source', type=Path)
    ap.add_argument('output', type=Path)
    ap.add_argument('--record', type=Path, required=True)
    args = ap.parse_args()
    if args.source.resolve() == args.output.resolve() or args.output.exists() or args.record.exists():
        ap.error('Do not overwrite source, output or existing transformation record')
    raw = args.source.read_bytes()
    corrected, patches = repair(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.record.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(corrected).save(args.output, format='PNG', compress_level=9)
    record = {
        'record_type': 'deterministic_candidate_derivation',
        'date': '2026-10-06', 'status': 'candidate',
        'owner_authorization': {
            'statement': '好的 做下去',
            'context': 'Owner accepted proposed programmatic highlight-only correction, retaining V2 and other pixels, separate derivation; remaining generation slot reserved for A4. A3 Balanced texture accepted in the same reply.',
            'does_not_approve': ['corrected image before review', 'style anchor', 'production', 'rights'],
        },
        'input': {'path': str(args.source), 'raw_sha256': SOURCE_SHA},
        'output': {'path': str(args.output), 'raw_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                   'rgba8_sha256': hashlib.sha256(corrected.tobytes()).hexdigest(), 'dimensions': [1254, 1254]},
        'tool': {'name': 'correct_a3_highlights.py', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'method': 'Symmetric RGB swaps of the original large-highlight bounding patch plus two-pixel halo and its reflection, clipped to the filled original eye shape with a three-pixel untouched outer rim on both sides; all donors are original pixels. Alpha untouched. Reflection sums target large centroids near eye x=0.35; y unchanged.',
        'development_validation': 'Initial uncommitted local patch failed left-eye measurement because bounding-box interior included pixels outside the actual eye shape. Added filled-eye support on both source and donor sides before producing this final derivation. No image-generation call or original-byte modification occurred.',
        'patches': patches,
        'budget': {'v2d_generated_attempts_used_before': 1, 'used_after': 1, 'limit': 2,
                   'image_generation_calls': 0, 'derivation_does_not_erase_original_failure': True},
        'original_attempt_record': 'concepts/kck-03b1/evidence/2026-10-06-a3-attempt-01.json',
    }
    args.record.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(record['output'], indent=2))


if __name__ == '__main__':
    main()
