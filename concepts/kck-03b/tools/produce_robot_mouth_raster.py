"""Owner-authorized mouth-fixed Robot static delivery; reuses the checked uniform raster transform."""
import copy
import io
import json
import platform
import zlib
from pathlib import Path

import PIL
from PIL import Image
from jsonschema import Draft202012Validator

import produce_raster as raster

ROOT=raster.ROOT
AUTH='concepts/kck-03b2/evidence/2026-10-06-owner-robot-local-mouth-continuation.json'
SOURCE='concepts/kck-03b2/outputs/robot-mouth-01-local-corrected.png'
SOURCE_RECORD=SOURCE.replace('.png','.provenance.json')
BASE='characters/robot/raster/versions/soft-handmade-v1-mouthfix'
MASTER=BASE+'/originals/robot-01.png'
DELIVERY=BASE+'/production/robot-01-1024.png'
MASTER_RECORD='provenance/robot/robot-01-soft-handmade-v1-mouthfix-master.json'
DELIVERY_RECORD='provenance/robot/robot-01-soft-handmade-v1-mouthfix-delivery.json'


def prepare():
    auth=json.loads((ROOT/AUTH).read_text());raw=(ROOT/SOURCE).read_bytes();source_record_raw=(ROOT/SOURCE_RECORD).read_bytes();src=json.loads(source_record_raw)
    if src['status']!='approved_reference' or raster.sha(raw)!=src['file']['sha256']:
        raise ValueError('Robot source not approved/hash bound')
    source=Image.open(io.BytesIO(raw));source.load()
    anchor=(560,1420);v=.95
    image,safe,scale,bounds,visible=raster.normalize(source,anchor,v)
    tool={'path':str(Path(__file__).relative_to(ROOT)),'sha256':raster.sha(Path(__file__).read_bytes()),
          'python':platform.python_version(),'Pillow':PIL.__version__,'zlib':zlib.ZLIB_RUNTIME_VERSION,
          'helpers':[{'path':str(p.relative_to(ROOT)),'sha256':raster.sha(p.read_bytes())} for p in [ROOT/'concepts/kck-03b/tools/produce_raster.py',raster.HELPER_PATH]]}
    common={'schema_version':1,'asset_id':'robot-01','character':'robot','style_version':'soft-handmade-v1-mouthfix','tool':tool,'rights':src['rights'],
            'evidence':[{'path':AUTH,'sha256':raster.sha((ROOT/AUTH).read_bytes()),'supports':'Owner contextual continuation of the exact bounded mouth-only composite proposal'},
                        {'path':'artifacts/qa/2026-10-06-robot-static/foot-measurement-grid.png','supports':'Manually inspected native foot-contact baseline; no alpha-derived anchor'}]}
    master={**common,'record_type':'master','id':'robot-01-soft-handmade-v1-mouthfix-master','status':'approved_reference',
            'status_evidence':[{'decision':'Select existing Owner-approved corrected Robot under continuing conformance authority; no source-app overwrite','date':auth['date'],'stated_in':AUTH,'quote':auth['quote']}],
            'file':raster.facts(MASTER,raw,source),'pixel_sha256':raster.sha(source.tobytes()),'input':{'path':SOURCE,'sha256':raster.sha(raw)},
            'source_provenance':{'path':SOURCE_RECORD,'sha256':raster.sha(source_record_raw)},'copy_policy':'Exact source bytes; no resize/re-encoding/pixel edits',
            'unresolved_questions':['Inherited rights pending/unknown']}
    master_bytes=raster.dump(master);encoded=raster.encode(image)
    parameters=copy.deepcopy(json.loads((ROOT/'provenance/dinosaur/dinosaur-01-soft-handmade-v1-delivery.json').read_text())['parameters'])
    parameters.update(source_visible_bounds=list(bounds),safe_fit_scale=safe,visual_scale=v,final_scale=scale,
                      anchor={'type':'ground-center','source_x':560,'source_y':1420,'delivery_x':512,'delivery_y':960})
    record={**common,'record_type':'transformation','id':'robot-01-soft-handmade-v1-mouthfix-delivery','status':'candidate',
            'status_evidence':[{'decision':'Create Robot static candidate under conditional Owner acceptance; verify actual output before delivery selection','date':auth['date'],'stated_in':AUTH,'quote':auth['quote']}],
            'file':raster.facts(DELIVERY,encoded,image),'pixel_sha256':raster.sha(image.tobytes()),'input':{'path':MASTER,'sha256':raster.sha(raw)},
            'master_provenance':{'path':MASTER_RECORD,'sha256':raster.sha(master_bytes)},'parameters':parameters,
            'qa':{'delivery_visible_bounds':list(visible),'clipped_nonzero_alpha_pixels':0,'padded_replay_equal':True,'repeat_pixel_equal':True,'srgb_chunk':raster.has_srgb(encoded)},
            'unresolved_questions':['Conditional actual visual conformance check','Inherited rights pending/unknown','Consumer scene not validated']}
    validator=Draft202012Validator(json.loads((ROOT/'provenance/schema/provenance.schema.json').read_text()))
    validator.validate(master);validator.validate(record)
    return {MASTER:raw,DELIVERY:encoded,MASTER_RECORD:master_bytes,DELIVERY_RECORD:raster.dump(record)}


def main():
    files=prepare()
    if any((ROOT/path).exists() for path in files):raise ValueError('refuse overwrite')
    written=[]
    try:
        for path,raw in files.items():
            p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as stream:written.append(p);stream.write(raw)
    except Exception:
        for p in written:p.unlink()
        raise
    print(json.dumps({'Robot':'candidate','native_anchor':[560,1420],'visual_scale':.95,'files':list(files)}))


if __name__=='__main__':main()
