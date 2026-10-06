"""Schema plus semantic/file gates for KCK frame-sequence packs; no promotion."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[3]
VIEWS={'front','three-quarter','side','back','happy','confused'}


def require(ok,message):
    if not ok:raise ValueError(message)


def fingerprint(pack):
    return hashlib.sha256(json.dumps(pack,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def validate_semantics(pack):
    schema=json.loads((ROOT/'manifests/animation-manifest.schema.json').read_text())
    Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(pack)
    require(len({x['path'] for x in pack['model_sheets']})==6,'six distinct model sheets required')
    rights=pack['rights']
    if rights['commercial_use_status']=='confirmed' or rights['rights_review_status']=='reviewed' or rights['ownership_status']=='documented':
        require(bool(rights['evidence']),'upgraded rights require external evidence')
    if pack['status']=='production':require(bool(pack['consumer_scene_evidence']),'production needs consumer-scene evidence')
    for name,clip in pack['actions'].items():
        if clip['type']=='alias':
            require(name=='carry','only carry may alias run in contract v1')
            require(clip['target']=='run','carry must target run')
            require(clip['target'] in pack['actions'],'alias target missing')
            target=pack['actions'][clip['target']]
            require(target['type']=='frame_sequence','alias cannot target an alias')
            require(target['requires_snack_socket'],'carry alias requires target snack socket contract')
            continue
        frames=clip['frames'];require(sum(f['duration_ms'] for f in frames)==clip['duration_ms'],'timing sum mismatch')
        if clip['motion_kind']=='authored':require(len({f['file']['sha256'] for f in frames})>=2,'authored motion needs distinct poses')
        else:require(len(frames)==1,'static hold must have one frame')
        if clip['fps'] is not None:
            require(all(abs(f['duration_ms']-1000/clip['fps'])<=1 for f in frames),'fps/duration mismatch')
        if clip['requires_snack_socket']:
            require(all('snack' in f['sockets'] for f in frames),'required snack socket missing on a frame')
        if pack['character_id'].startswith('cat'):
            for f in frames:
                if 'snack' in f['sockets']:require(f['sockets']['snack']['hand']=='anatomical-left','Cat receiving hand changed')
        if pack['character_id'].startswith('dinosaur'):
            for f in frames:
                if 'snack' in f['sockets']:require(f['sockets']['snack']['hand']=='anatomical-right','Dino snack hand would conflict with magnifier')
        times=[e['time_ms'] for e in clip['events']];require(times==sorted(times),'event order invalid')
        for e in clip['events']:
            require(e['time_ms']<=clip['duration_ms'],'event outside duration')
            if e['type'] in ['prop_attach','prop_release']:
                require(e.get('socket')=='snack' and clip['requires_snack_socket'],'prop event needs declared socket')
            elif e['type']=='foot_contact':require('foot' in e,'foot event requires named foot')
    return pack


def repo_file(root,path):
    p=(root/path).resolve();require(p.is_relative_to(root.resolve()),'path escapes repository')
    require(p.is_file(),'referenced file missing: '+path)
    return p


def validate_motion_frame(rec,root):
    schema=json.loads((ROOT/'manifests/animation-frame-provenance.schema.json').read_text())
    Draft202012Validator(schema).validate(rec)
    def bound(entry):
        p=repo_file(root,entry['path'])
        require(hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],'derivation binding mismatch: '+entry['path'])
        return p
    for name in ['file','split_report','transform_report','recipe','tool']:bound(rec[name])
    strip=bound(rec['source_strip']['file']);source_record=json.loads(bound(rec['source_strip']['provenance']).read_text())
    require(source_record['file']['sha256']==rec['source_strip']['file']['sha256'],'strip provenance mismatch')
    require(source_record['measurements'][0]['results']['agent_hard_gate']=='PASS','source strip not conforming')
    report_path=bound(rec['transform_report']);report=json.loads(report_path.read_text())
    split=json.loads(bound(rec['split_report']).read_text());index=rec['source_slot']
    require(index<len(report['frames']) and index<len(split['frames']),'source slot outside sequence')
    frame=report['frames'][index];slot=split['frames'][index]
    require(split['source_facts']['sha256']==rec['source_strip']['file']['sha256'],'split source mismatch')
    require(str((report_path.parent/frame['path']).relative_to(root))==rec['file']['path'],'frame path not in report')
    require(frame['output_facts']['sha256']==rec['file']['sha256'],'report/frame mismatch')
    require(frame['source_facts']['sha256']==slot['output_facts']['sha256'],'slot/frame source mismatch')
    with Image.open(strip) as image:
        pixels=image.crop(slot['source_slot_exclusive']).tobytes()
    with Image.open(repo_file(root,frame['source'])) as source:
        require(pixels==source.tobytes(),'slot pixels differ from immutable strip')
    with Image.open(bound(rec['file'])) as image:
        require(hashlib.sha256(image.tobytes()).hexdigest()==rec['pixel_sha256'],'frame pixel hash mismatch')
    require(bound(rec['recipe']).read_bytes()==(report_path.parent/'recipe.json').read_bytes(),'recipe not the selected transform')
    sys.path.insert(0,str(ROOT/'.agents/skills/kck-character-pipeline/scripts'))
    import pipeline
    pipeline.check(root,str(report_path.parent.relative_to(root)))
    for ref in rec['evidence_refs']:repo_file(root,ref)


def validate_files(pack,root=ROOT):
    def hashed_file(entry):
        p=repo_file(root,entry['path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],'file hash mismatch: '+entry['path'])
        rec=json.loads(repo_file(root,entry['provenance']).read_text())
        require(rec['file']['sha256']==entry['sha256'] and rec['file']['path']==entry['path'],'provenance/file mismatch')
        with Image.open(p) as im:require(im.mode=='RGBA','RGBA required')
        return p,rec
    _,master=hashed_file(pack['source_master']);require(master['status']=='approved_reference','accepted master required')
    require(master['asset_id']==pack['character_id'] and master['style_version']==pack['style_version'],'master identity/version mismatch')
    found=set()
    for item in pack['model_sheets']:
        _,rec=hashed_file(item);require(rec['status']=='approved_reference','model sheet not accepted')
        require(rec['character']==pack['character_id'].split('-')[0],'wrong model-sheet character')
        # Model view recorded in both the sheet variant and measured evidence.
        view=rec['variant'].split()[0];found.add(view)
    require(found==VIEWS,'model sheet views incomplete')
    for clip in pack['actions'].values():
        if clip['type']=='alias':continue
        for f in clip['frames']:
            p,rec=hashed_file(f['file'])
            with Image.open(p) as im:require(im.size==(1024,1024),'frame canvas mismatch')
            require(rec['status'] in ['candidate','production'],'frame lifecycle not valid')
            require(rec['character_id' if rec.get('record_type')=='motion_frame' else 'asset_id']==pack['character_id'],'wrong frame character')
            require(rec['style_version']==pack['style_version'],'wrong frame style')
            if rec.get('record_type')=='motion_frame':validate_motion_frame(rec,root)
            if pack['status']=='production':
                require(rec['status']=='production','candidate frame cannot be delivered')
                with Image.open(p) as im:require(im.info.get('srgb') is not None,'production requires sRGB metadata')
            for field in ['commercial_use_status','rights_review_status','ownership_status']:
                require(rec['rights'][field]==pack['rights'][field],'frame rights differ from pack')
    for ref in pack['evidence_refs']+pack['rights']['evidence']:repo_file(root,ref)
    if pack['status']=='production':
        evidence=json.loads(repo_file(root,pack['consumer_scene_evidence']).read_text())
        require(evidence.get('format')=='kck-motion-scene-evidence-v1' and evidence.get('actual_run') is True,'actual scene run required')
        require(evidence.get('pack_fingerprint')==fingerprint(pack),'scene evidence belongs to a different pack')
        required={'pivot','scale','ground_contact','timing','loop','transparent_edges','prop_handoff'}
        require(required<=set(evidence.get('checks',{})) and all(evidence['checks'][k] is True for k in required),'scene checks incomplete')
        for key in ['consumer_repository','scene_path','platform']:require(bool(evidence.get(key)),'scene context missing')
        capture=evidence.get('capture');require(isinstance(capture,dict),'scene capture missing')
        p=repo_file(root,capture['path']);require(hashlib.sha256(p.read_bytes()).hexdigest()==capture['sha256'],'scene capture mismatch')
    return {'schema_and_semantics':'PASS','source_and_frame_files':'PASS','status':pack['status'],'availability_promoted':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('pack');args=parser.parse_args()
    pack=json.loads(repo_file(ROOT,args.pack).read_text());validate_semantics(pack);print(json.dumps(validate_files(pack)))


if __name__=='__main__':main()
