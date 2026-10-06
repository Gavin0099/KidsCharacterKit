"""Owner-authorized RGB swaps for the exact Robot B1-B original; no generation.

Only two large highlight patches and their reflected donor patches change.
All alpha, the eye rims and every outside pixel are retained. Original is immutable.
"""
import argparse
import hashlib
import io
import json
import platform
from pathlib import Path

import numpy as np
import PIL
from PIL import Image, ImageFilter
from measure_output import fill_holes, label4

SOURCE_SHA = '03ef900a89866cef4b163deb7c7a303e3f496c07b26b1efe74e30b62aecd1cd7'
# Read-only source measurement, exclusive maxima, viewer-left then right.
PATCHES = [
    {'eye_bbox': [432, 261, 508, 339], 'large_bbox': [472, 272, 492, 292], 'reflection_sum_x': 939},
    {'eye_bbox': [659, 275, 733, 352], 'large_bbox': [698, 287, 717, 306], 'reflection_sum_x': 1391},
]


def eye_support(original, bbox):
    x0, y0, x1, y1 = bbox
    crop = original[y0:y1, x0:x1]
    dark = (crop[..., 0] < 125) & (crop[..., 1] < 85) & (crop[..., 2] < 75) & (crop[..., 3] > 200)
    labels, _ = label4(dark)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    if not counts.any():
        raise ValueError('No dark eye support')
    filled = fill_holes(labels == counts.argmax())
    interior = np.array(Image.fromarray(filled.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(7))) > 0
    support = np.zeros(original.shape[:2], dtype=bool)
    support[y0:y1, x0:x1] = interior
    return support


def repair(raw):
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError('Source hash mismatch: approved only for exact Robot B1-B attempt #1')
    with Image.open(io.BytesIO(raw)) as image:
        if image.mode != 'RGBA' or image.size != (1086, 1448):
            raise ValueError('Expected RGBA 1086x1448 source')
        original = np.array(image)
    output = original.copy()
    union = np.zeros(original.shape[:2], dtype=bool)
    details = []
    for patch in PATCHES:
        support = eye_support(original, patch['eye_bbox'])
        x0, y0, x1, y1 = patch['large_bbox']
        yy, xx = np.mgrid[y0-2:y1+2, x0-2:x1+2]
        yy, xx = yy.ravel(), xx.ravel()
        mirrored = patch['reflection_sum_x'] - xx
        eligible = support[yy, xx] & support[yy, mirrored]
        yy, xx, mirrored = yy[eligible], xx[eligible], mirrored[eligible]
        mask = np.zeros_like(union)
        mask[yy, xx] = True
        mask[yy, mirrored] = True
        my, mx = np.where(mask)
        if not len(mx) or not np.all(original[my, mx, 3] > 200):
            raise ValueError('Invalid eye-interior patch')
        output[my, mx, :3] = original[my, patch['reflection_sum_x'] - mx, :3]
        union |= mask
        details.append({**patch, 'source_roi': [x0-2, y0-2, x1+2, y1+2],
                        'mask_pixels': int(mask.sum()),
                        'changed_pixels': int(np.any(output[my, mx] != original[my, mx], axis=1).sum())})
    if not np.array_equal(output[..., 3], original[..., 3]) or not np.array_equal(output[~union], original[~union]):
        raise AssertionError('Unauthorized alpha/outside change')
    return output, details


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args()
    if len({p.resolve() for p in (args.source, args.output, args.record)}) != 3 or args.output.exists() or args.record.exists():
        parser.error('Do not overwrite source, output or transformation record')
    raw = args.source.read_bytes()
    corrected, patches = repair(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.record.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(corrected).save(args.output, format='PNG', compress_level=9)
    record = {
        'record_type': 'deterministic_candidate_derivation', 'date': '2026-10-06', 'status': 'candidate',
        'owner_authorization': {
            'quote': '好的 可以這樣做',
            'stated_in': 'current Owner session, reply to the specific Robot programmatic-repair proposal',
            'scope': 'Only move the two large eye highlights to upper left; retain all alpha and other pixels, preserve original, verify and update lineup/PR. No generation.',
            'does_not_approve': ['unseen corrected artwork', 'Cat/Robot shared-world lineup', 'Style Bible v1', 'production', 'rights'],
        },
        'input': {'path': str(args.source), 'raw_sha256': SOURCE_SHA},
        'output': {'path': str(args.output), 'raw_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                   'rgba8_sha256': hashlib.sha256(corrected.tobytes()).hexdigest(), 'dimensions': [1086, 1448]},
        'tool': {'name': Path(__file__).name, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 'Python': platform.python_version(), 'Pillow': PIL.__version__, 'numpy': np.__version__},
        'method': 'Symmetric immutable-source RGB swaps within large-highlight bbox plus two-pixel halo and its horizontal reflection, clipped on both sides to filled eye interior with untouched three-pixel rim; alpha unchanged. No new pixels synthesized. Primary highlight count and height retained; horizontal eye-axis reflection moves it from right to left.',
        'patches': patches,
        'image_generation_calls': 0, 'dinosaur_v2d_budget': {'used': 2, 'limit': 2, 'remaining': 0},
        'original_failure_retained': 'concepts/kck-03b1/outputs/Robot-B1B-attempt-01.provenance.json',
    }
    args.record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(record['output'], indent=2))


if __name__ == '__main__':
    main()
