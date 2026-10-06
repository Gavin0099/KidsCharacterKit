"""KCK-03B immutable selected masters and deterministic delivery candidates.

Requires the hash-bound Owner layout decision. Never sets manifest availability.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import math
import platform
import struct
import tempfile
import zlib
from pathlib import Path

import PIL
from PIL import Image, PngImagePlugin
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
HELPER_PATH = ROOT / 'concepts/kck-03b/tools/build_layout_review.py'
spec = importlib.util.spec_from_file_location('layout_review', HELPER_PATH)
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)
DECISION = 'concepts/kck-03b/evidence/2026-10-06-owner-master-layout-approval.json'
STYLE = 'soft-handmade-v1'
SOURCE_RECORDS = {'cat':'concepts/kck-03b1/outputs/Cat-B1B-attempt-01.provenance.json',
                  'dinosaur':'concepts/kck-03b1/outputs/A3-v2d-attempt-01-highlight-corrected.provenance.json'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')


def repo_file(path):
    target = (ROOT/path).resolve()
    if not target.is_relative_to(ROOT.resolve()):
        raise ValueError('outside repository')
    return target


def normalize(source, anchor, visual_scale):
    if source.mode != 'RGBA' or source.getchannel('A').getbbox() is None:
        raise ValueError('nonempty RGBA source required')
    if source.info.get('icc_profile'):
        raise ValueError('profiled source needs an explicitly reviewed color conversion')
    if not math.isfinite(visual_scale) or not 0 < visual_scale <= 1:
        raise ValueError('invalid visual scale')
    if len(anchor)!=2 or any(not math.isfinite(v) or not 0 <= v < source.size[i] for i,v in enumerate(anchor)):
        raise ValueError('invalid semantic anchor')
    bounds = source.getchannel('A').point(lambda a:255 if a>=13 else 0).getbbox()
    if bounds is None:
        raise ValueError('no visible content')
    safe_fit = layout.fit(bounds,anchor)
    scale = safe_fit*visual_scale
    # Preflight full nonzero support, plus interpolation support. This protects
    # faint edge pixels outside the >5% scale box, not just visible content.
    l,t,r,b = source.getchannel('A').getbbox()
    ox,oy = 512-anchor[0]*scale,960-anchor[1]*scale
    halo = 2*scale
    if min(ox+l*scale-halo,oy+t*scale-halo) < 0 or max(ox+r*scale+halo,oy+b*scale+halo) > 1024:
        raise ValueError('full alpha extent/halo would clip; review a smaller visual_scale')
    result = layout.render(source,anchor,scale)
    visible = result.getchannel('A').point(lambda a:255 if a>=13 else 0).getbbox()
    if visible is None or visible[0]<64 or visible[2]>960 or visible[1]<64 or visible[3]>1024:
        raise ValueError('delivery visible content violates safe bounds')
    return result, safe_fit, scale, bounds, visible


def encode(image):
    metadata = PngImagePlugin.PngInfo()
    metadata.add(b'sRGB',b'\x00')
    buf=io.BytesIO()
    image.save(buf,format='PNG',pnginfo=metadata,compress_level=9,optimize=False)
    return buf.getvalue()


def has_srgb(raw):
    offset=8
    while offset<len(raw):
        size=struct.unpack('>I',raw[offset:offset+4])[0]
        if raw[offset+4:offset+8]==b'sRGB':
            return raw[offset+8:offset+8+size]==b'\x00'
        offset+=size+12
    return False


def facts(path, raw, image):
    return {'path':path,'format':'png','width':image.width,'height':image.height,
            'color_type':image.mode,'bytes':len(raw),'sha256':sha(raw)}


def prepare():
    decision_raw=repo_file(DECISION).read_bytes();decision=json.loads(decision_raw)
    if decision['quote']!='核准整份提案，採 B 尺寸':
        raise ValueError('expected exact Owner layout decision')
    report_ref=decision['review_report'];report_raw=repo_file(report_ref['path']).read_bytes()
    if sha(report_raw)!=report_ref['sha256']:
        raise ValueError('reviewed report changed')
    files={};records=[]
    tools={'path':str(Path(__file__).relative_to(ROOT)),'sha256':sha(Path(__file__).read_bytes()),
           'python':platform.python_version(),'Pillow':PIL.__version__,'zlib':zlib.ZLIB_RUNTIME_VERSION,
           'helpers':[{'path':str(HELPER_PATH.relative_to(ROOT)),'sha256':sha(HELPER_PATH.read_bytes())}]}
    for char, asset_id in [('cat','cat-02'),('dinosaur','dinosaur-01')]:
        approved=decision['approved_masters_and_anchors'][char]
        source_path=approved['source'];raw=repo_file(source_path).read_bytes()
        if sha(raw)!=approved['sha256']:
            raise ValueError('selected source hash mismatch')
        source_record_path=SOURCE_RECORDS[char];source_record_raw=repo_file(source_record_path).read_bytes();source_record=json.loads(source_record_raw)
        if source_record['status']!='approved_reference' or source_record['file']['sha256']!=sha(raw):
            raise ValueError('selected concept not accepted/hash bound')
        source=Image.open(io.BytesIO(raw));source.load()
        v=decision['approved_scale_option']['parameters'][char]['visual_scale'];anchor=approved['proposed_anchor']
        result,safe,scale,bounds,visible=normalize(source,anchor,v)
        base=f'characters/{char}/raster/versions/{STYLE}'
        master_path=f'{base}/originals/{asset_id}.png';delivery_path=f'{base}/production/{asset_id}-1024.png'
        master_rec_path=f'provenance/{char}/{asset_id}-{STYLE}-master.json'
        delivery_rec_path=f'provenance/{char}/{asset_id}-{STYLE}-delivery.json'
        common={'schema_version':1,'asset_id':asset_id,'character':char,'style_version':STYLE,'tool':tools,
                'rights':source_record['rights'],'evidence':[{'path':DECISION,'sha256':sha(decision_raw),'supports':'Exact Owner-selected master/anchor/scale/versioned-copy and seated support decisions'}]}
        selected={**common,'record_type':'master','id':f'{asset_id}-{STYLE}-master','status':'approved_reference',
                  'status_evidence':[{'decision':'Owner selected exact approved concept as versioned immutable master, not production/rights','date':decision['date'],'stated_in':DECISION,'quote':decision['quote']}],
                  'input':{'path':source_path,'sha256':sha(raw)},'source_provenance':{'path':source_record_path,'sha256':sha(source_record_raw)},
                  'file':facts(master_path,raw,source),'pixel_sha256':sha(source.tobytes()),
                  'copy_policy':'Exact source bytes; no resize/re-encoding/pixel edits','unresolved_questions':['Production acceptance and inherited rights unresolved']}
        master_record_bytes=dump(selected)
        encoded=encode(result)
        assert has_srgb(encoded)
        reopened=Image.open(io.BytesIO(encoded));assert reopened.mode=='RGBA' and reopened.size==(1024,1024) and reopened.tobytes()==result.tobytes()
        derived={**common,'record_type':'transformation','id':f'{asset_id}-{STYLE}-delivery','status':'candidate',
                 'status_evidence':[{'decision':'Owner authorized delivery candidate creation; unseen production output not yet accepted','date':decision['date'],'stated_in':DECISION,'quote':decision['quote']}],
                 'input':{'path':master_path,'sha256':sha(raw)},'master_provenance':{'path':master_rec_path,'sha256':sha(master_record_bytes)},
                 'file':facts(delivery_path,encoded,result),'pixel_sha256':sha(result.tobytes()),
                 'parameters':{'canvas':[1024,1024],'safe_margin':64,'alpha_threshold':13,'source_visible_bounds':list(bounds),
                               'anchor':{'type':'support-baseline' if char=='cat' else 'ground-center','source_x':anchor[0],'source_y':anchor[1],'delivery_x':512,'delivery_y':960},
                               'safe_fit_scale':safe,'visual_scale':v,'final_scale':scale,
                               'resampling':'uniform inverse affine BICUBIC, premultiplied RGBa',
                               'color_policy':'Unprofiled selected source samples interpreted as sRGB; preserve samples before resampling; write PNG sRGB intent 0',
                               'encoder':{'name':'Pillow PNG','compress_level':9,'optimize':False}},
                 'qa':{'delivery_visible_bounds':list(visible),'clipped_nonzero_alpha_pixels':0,'padded_replay_equal':True,'repeat_pixel_equal':True,'srgb_chunk':True},
                 'unresolved_questions':['Owner actual production acceptance','Inherited rights pending/unknown','Consumer scene ground contact not validated']}
        validator=Draft202012Validator(json.loads((ROOT/'provenance/schema/provenance.schema.json').read_text()))
        validator.validate(selected);validator.validate(derived)
        files.update({master_path:raw,delivery_path:encoded,master_rec_path:master_record_bytes,delivery_rec_path:dump(derived)})
        records.append({'asset_id':asset_id,'style_version':STYLE,'status':'candidate','master':{'path':master_path,'sha256':sha(raw),'provenance':master_rec_path},
                        'delivery':{'path':delivery_path,'sha256':sha(encoded),'pixel_sha256':sha(result.tobytes()),'provenance':delivery_rec_path},
                        'visual_scale':v,'anchor':derived['parameters']['anchor']})
    index={'format':'kck-raster-candidate-set-v1','style_version':STYLE,'status':'candidate','owner_production_acceptance':'pending',
           'selection_decision':DECISION,'records':records,'manifest_available':False,'generation_calls':0}
    files['concepts/kck-03b/raster-candidate-set.json']=dump(index)
    return files


def build():
    files=prepare()
    targets=[repo_file(path) for path in files]
    if any(p.exists() or p.is_symlink() for p in targets):
        raise ValueError('refusing overwrite; use --check for an existing pack')
    # Compute/validate everything before publication; exclusive writes prevent
    # replacing a file introduced after the preflight. Roll back only own files.
    written=[]
    try:
        with tempfile.TemporaryDirectory(prefix='kck-raster-') as tmp:
            stage=Path(tmp)
            for i,(path,raw) in enumerate(files.items()):(stage/str(i)).write_bytes(raw)
            for i,path in enumerate(files):
                p=repo_file(path);p.parent.mkdir(parents=True,exist_ok=True)
                with p.open('xb') as stream:written.append(p);stream.write((stage/str(i)).read_bytes())
    except Exception:
        for p in written:p.unlink()
        raise
    return {'files_written':len(written),'status':'candidate','availability':False}


def check():
    expected=prepare()
    for path,raw in expected.items():
        actual=repo_file(path).read_bytes()
        # Encoder bytes are pinned for this environment; pixels checked above too.
        if actual!=raw:
            raise ValueError('bundle differs from replay: '+path)
    return {'files_checked':len(expected),'pixel_and_file_replay':'PASS','status':'candidate','availability':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check() if args.check else build(),ensure_ascii=False))


if __name__=='__main__':main()
