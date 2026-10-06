"""Owner-authorized local upper-stroke removal on the exact Dino side #2.

Copy neighboring cream RGB into one bounded interior patch. All alpha and every
outside pixel remain unchanged. No new generation, blur or source overwrite.
"""
import argparse
import hashlib
import io
import json
import platform
from pathlib import Path

import numpy as np
import PIL
from PIL import Image

SOURCE_SHA = 'c864809df3793c82d46462bdee953d1b1928b7d3aea538072071b4ff40ead0ef'
AUTHORITY = 'concepts/kck-03b2/evidence/2026-10-06-owner-cat-sheets-and-dino-repair.json'


def repair(raw):
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError('Source hash mismatch: only exact Dinosaur side #2 authorized')
    with Image.open(io.BytesIO(raw)) as image:
        if image.mode != 'RGBA' or image.size != (1254, 1254):
            raise ValueError('Expected RGBA 1254x1254')
        source = np.array(image)
    # Border follows the observed sloping cream-interior edge. The brown outer
    # contour to its left and both lower belly strokes stay outside this patch.
    yy, xx = [], []
    for y in range(851, 864):
        for x in range(472 - (y - 850) // 2, 493):
            yy.append(y)
            xx.append(x)
    yy, xx = np.array(yy), np.array(xx)
    donor_y, donor_x = yy + 28, xx + 14
    donor = source[donor_y, donor_x]
    if not (np.all(source[yy, xx, 3] > 200) and np.all(donor[:, 3] > 200)
            and np.all(donor[:, 0] > 230) and np.all(donor[:, 1] > 210)
            and np.all(donor[:, 2] > 180)):
        raise ValueError('Patch/donor must be interior cream, never contour or transparent edge')
    output = source.copy()
    output[yy, xx, :3] = donor[:, :3]
    mask = np.zeros(source.shape[:2], dtype=bool)
    mask[yy, xx] = True
    if not np.array_equal(output[..., 3], source[..., 3]) or not np.array_equal(output[~mask], source[~mask]):
        raise AssertionError('Unauthorized alpha/outside change')
    return output, {'patch_bbox_exclusive': [466, 851, 493, 864],
                    'patch_pixels': int(mask.sum()),
                    'changed_pixels': int(np.any(output != source, axis=2).sum()),
                    'donor_offset': [14, 28],
                    'protected_lower_strokes': [[445, 912, 500, 947], [450, 977, 508, 1011]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--record', type=Path, required=True)
    a = parser.parse_args()
    if len({p.resolve() for p in [a.source, a.output, a.record]}) != 3 or a.output.exists() or a.record.exists():
        parser.error('Do not overwrite source/output/record')
    output, patch = repair(a.source.read_bytes())
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.record.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(output).save(a.output, format='PNG', compress_level=9)
    record = {'record_type': 'deterministic_candidate_derivation', 'date': '2026-10-06',
              'status': 'candidate', 'owner_authorization': AUTHORITY,
              'input': {'path': str(a.source), 'raw_sha256': SOURCE_SHA},
              'output': {'path': str(a.output), 'raw_sha256': hashlib.sha256(a.output.read_bytes()).hexdigest(),
                         'rgba8_sha256': hashlib.sha256(output.tobytes()).hexdigest(), 'dimensions': [1254, 1254]},
              'method': 'Bounded cream-interior RGB copy from immutable neighboring cream (dx=14,dy=28); alpha and outside unchanged',
              'patch': patch, 'image_generation_calls': 0,
              'tool': {'name': Path(__file__).name, 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                       'Python': platform.python_version(), 'Pillow': PIL.__version__, 'numpy': np.__version__},
              'dinosaur_v2d_budget': {'used': 2, 'maximum': 2, 'remaining': 0},
              'original_failure_retained': 'concepts/kck-03b2/outputs/dinosaur-side-02.provenance.json'}
    a.record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(record['output'], indent=2))


if __name__ == '__main__':
    main()
