#!/usr/bin/env python3
"""Read-only pose geometry and trial registration; never approve or repair art."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile

import numpy as np
import PIL
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound(path):
    return {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}


def geometry(record):
    eyes = record["eyes"]
    boxes = [e["bbox"] for e in eyes]
    widths = [b[2] - b[0] for b in boxes]
    centers = [((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for b in boxes]
    dx, dy = [centers[1][i] - centers[0][i] for i in (0, 1)]
    return {"eye_bboxes_exclusive": boxes, "mean_eye_width_px": sum(widths) / 2,
            "eye_distance_over_mean_width": math.hypot(dx, dy) / (sum(widths) / 2),
            "eye_width_over_height": [w / (b[3] - b[1]) for w, b in zip(widths, boxes)],
            "eye_pair_roll_degrees": math.degrees(math.atan2(dy, dx)),
            "unchanged_highlight_gates": [e["style_gate"] for e in eyes]}


def diagnose():
    refs = [Path(__file__).resolve()]
    measurements = []
    for i in range(2):
        p = ROOT / f"concepts/kck-03b2/evidence/dinosaur-stumble-01-frame-{i:03d}-measurements.json"
        measurements.append(json.loads(p.read_text()))
        refs.append(p)
    model_geometry = []
    for view in ["front", "three-quarter", "happy", "confused"]:
        p = ROOT / f"concepts/kck-03b2/evidence/dinosaur-{view}-01-measurements.json"
        m = json.loads(p.read_text())
        source = ROOT / f"concepts/kck-03b2/outputs/dinosaur-{view}-01.png"
        provenance = source.with_suffix('.provenance.json')
        assert sha(source) == m['candidate']['raw_sha256']
        assert json.loads(provenance.read_text())['status'] == 'approved_reference'
        refs.extend([p, source, provenance])
        model_geometry.append({"view": view, **geometry(m["candidate"])})
    delivery = ROOT / 'provenance/dinosaur/dinosaur-01-soft-handmade-v1-delivery.json'
    delivery_record = json.loads(delivery.read_text())
    refs.append(delivery)
    master = geometry(measurements[0]['reference'])
    candidate_geometry = [geometry(m['candidate']) for m in measurements]
    mean_width = sum(g['mean_eye_width_px'] for g in candidate_geometry) / 2
    requested = master['mean_eye_width_px'] * delivery_record['parameters']['final_scale'] / mean_width
    scaled_size = round(887 * requested)
    actual = scaled_size / 887
    frames, trials = [], []
    anchors = [[522, 835], [460, 835]]
    for i, anchor in enumerate(anchors):
        p = ROOT / f'artifacts/qa/2026-10-06-dinosaur-stumble-slots/frame-{i:03d}.png'
        assert sha(p) == measurements[i]['candidate']['raw_sha256']
        refs.append(p)
        source = Image.open(p).convert('RGBA')
        scaled = source.resize((scaled_size, scaled_size), Image.Resampling.LANCZOS)
        alpha = np.asarray(scaled)[..., 3]
        offset = [512 - round(anchor[0] * actual), 960 - round(anchor[1] * actual)]
        yy, xx = np.indices(alpha.shape)
        outside = (xx + offset[0] < 0) | (xx + offset[0] >= 1024) | (yy + offset[1] < 0) | (yy + offset[1] >= 1024)
        lost = alpha[outside & (alpha > 0)]
        values, counts = np.unique(lost, return_counts=True)
        trials.append({'frame': i, 'tentative_native_anchor': anchor, 'offset': offset,
                       'scaled_nonzero_bbox_exclusive': list(scaled.getchannel('A').getbbox()),
                       'clipped_nonzero_pixels': int(lost.size), 'clipped_alpha_gt10_pixels': int((lost > 10).sum()),
                       'clipped_alpha_histogram': {str(v): int(c) for v, c in zip(values, counts)}})
        frames.append({'source': str(p.relative_to(ROOT)), 'sha256': sha(p), 'anchor': anchor, 'duration_ms': 150})
    pipeline = ROOT / '.agents/skills/kck-character-pipeline/scripts/pipeline.py'
    refs.append(pipeline)
    before = {str(p): sha(p) for p in refs}
    spec = importlib.util.spec_from_file_location('stumble_qa_pipeline', pipeline)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(pipeline.parent))
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(dir=ROOT / 'artifacts/qa', prefix='.stumble-diagnostic-') as temp:
        temp = Path(temp)
        recipe = temp / 'recipe.json'
        recipe.write_text(json.dumps({'format': 'kck-qa-recipe-v1', 'canvas': [1024, 1024],
                                     'target_anchor': [512, 960], 'scale': requested, 'resampling': 'LANCZOS',
                                     'loop': 1, 'frames': frames}))
        try:
            module.prepare(ROOT, str(recipe.relative_to(ROOT)), str((temp / 'prepared').relative_to(ROOT)))
            result = {'outcome': 'prepared', 'error': None}
        except ValueError as exc:
            result = {'outcome': 'rejected', 'error': str(exc)}
    assert all(sha(Path(p)) == expected for p, expected in before.items())
    assert result == {'outcome': 'rejected', 'error': 'clipping nonzero alpha, including soft edge pixels'}
    return {'format': 'kck-read-only-stumble-diagnostic-v1', 'status': 'HOLD', 'generation_calls': 0,
            'libraries': {'Pillow': PIL.__version__, 'numpy': np.__version__},
            'source_and_tool_hashes': [bound(p) for p in refs], 'sources_unchanged': True,
            'legacy_identity_gates': [m['eye_identity'] for m in measurements],
            'master_facial_geometry': master, 'approved_sheet_facial_geometry': model_geometry,
            'stumble_facial_geometry': candidate_geometry,
            'interpretation': 'Whole-visible-bbox eye metrics change with pose. Facial ratios are near accepted views, but these descriptive measurements define no new acceptance threshold and do not resolve/override either legacy identity FAIL.',
            'trial_registration': {'requested_common_scale': requested, 'actual_uniform_scale': actual,
                                   'scaled_canvas': [scaled_size, scaled_size], 'frames': trials,
                                   'actual_pipeline_result': result, 'anchors_approved': False,
                                   'scope': 'One provisional registration only; not proof all semantic anchors fail. y835 is a hypothesis, not a selected foot-contact measurement. No clipping, alpha cleanup, or delivery was applied.'},
            'not_claimed': ['identity acceptance', 'new tolerance', 'approved anchor', 'motion availability', 'rights', 'consumer-scene QA']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    report = diagnose()
    path = ROOT / args.output
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'report': str(path.relative_to(ROOT)), 'sources_unchanged': True,
                      'legacy_identity': [g['gate'] for g in report['legacy_identity_gates']],
                      'trial_clip_counts': [f['clipped_nonzero_pixels'] for f in report['trial_registration']['frames']],
                      'actual_pipeline': report['trial_registration']['actual_pipeline_result'], 'status': 'HOLD'}))
