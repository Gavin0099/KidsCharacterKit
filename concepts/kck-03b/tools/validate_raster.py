"""Read-only lifecycle-aware raster verification after Owner status decisions."""
import hashlib
import json
from PIL import Image
import produce_raster as transform

ROOT=transform.ROOT

def require(ok,message):
    if not ok:raise ValueError(message)

def bound(entry):
    p=transform.repo_file(entry['path']);raw=p.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'binding mismatch: '+entry['path'])
    return p

def validate(manifest=None,index=None):
    if manifest is None:manifest=json.loads((ROOT/'manifests/characters.json').read_text())
    if index is None:index=json.loads((ROOT/'concepts/kck-03b/raster-candidate-set.json').read_text())
    checked=[]
    for item in index['records']:
        master=json.loads(transform.repo_file(item['master']['provenance']).read_text())
        rec=json.loads(transform.repo_file(item['delivery']['provenance']).read_text())
        require(master['status']=='approved_reference','master not accepted')
        require(master['file']['path']==item['master']['path'] and rec['file']['path']==item['delivery']['path'],'index path mismatch')
        require(item['anchor']==rec['parameters']['anchor'],'index anchor mismatch')
        require(master['asset_id']==rec['asset_id']==item['asset_id'],'record identity mismatch')
        for record in [master,rec]:
            bound(record['file']);bound(record['input']);bound(record['tool'])
            for helper in record['tool']['helpers']:bound(helper)
            for evidence in record['evidence']:
                transform.repo_file(evidence['path']).read_bytes()
                if 'sha256' in evidence:bound(evidence)
        with Image.open(bound(master['file'])) as image:
            require(hashlib.sha256(image.tobytes()).hexdigest()==master['pixel_sha256'],'master pixel hash mismatch')
        source_record=json.loads(bound(master['source_provenance']).read_text())
        require(source_record['status']=='approved_reference','source not accepted')
        require(master['rights']==source_record['rights']==rec['rights'],'rights were changed')
        require(bound(master['file']).read_bytes()==bound(master['input']).read_bytes(),'master is not an exact copy')
        require(bound(rec['master_provenance'])==transform.repo_file(item['master']['provenance']),'wrong master provenance')
        require(rec['input']=={'path':master['file']['path'],'sha256':master['file']['sha256']},'transform input mismatch')
        params=rec['parameters'];a=params['anchor']
        with Image.open(bound(rec['input'])) as image:
            expected,safe,scale,bounds,visible=transform.normalize(image,(a['source_x'],a['source_y']),params['visual_scale'])
        with Image.open(bound(rec['file'])) as output:
            require(output.tobytes()==expected.tobytes(),'delivery pixels differ from replay')
            require(hashlib.sha256(output.tobytes()).hexdigest()==rec['pixel_sha256']==item['delivery']['pixel_sha256'],'pixel hash mismatch')
        require(transform.has_srgb(bound(rec['file']).read_bytes()),'sRGB metadata missing')
        require(safe==params['safe_fit_scale'] and scale==params['final_scale'],'geometry scale mismatch')
        require(list(bounds)==params['source_visible_bounds'] and list(visible)==rec['qa']['delivery_visible_bounds'],'bounds mismatch')
        require(item['master']['sha256']==master['file']['sha256'] and item['delivery']['sha256']==rec['file']['sha256'],'index hash mismatch')
        require(item['status']==rec['status'],'index lifecycle mismatch')
        asset=manifest['characters'][item['asset_id']];raster=asset['representations']['raster']
        require(asset['visual_scale']==params['visual_scale']==item['visual_scale'],'manifest scale mismatch')
        require(raster['available']==(rec['status']=='production'),'availability/lifecycle mismatch')
        if raster['available']:
            require(raster['master']=={'path':master['file']['path'],'sha256':master['file']['sha256']},'manifest master mismatch')
            require(raster['delivery']['default']=={'path':rec['file']['path'],'sha256':rec['file']['sha256']},'manifest delivery mismatch')
            require(raster['transformation_provenance']==item['delivery']['provenance'],'manifest transformation mismatch')
            require(raster['anchor']=={'type':a['type'],'x':512,'y':960},'manifest anchor mismatch')
            require(any(x['stated_in']==index['owner_production_acceptance'] for x in rec['status_evidence']),'conditional authority missing')
        checked.append({'asset_id':item['asset_id'],'status':rec['status'],'available':raster['available'],'pixel_replay':'PASS'})
    available={key for key,value in manifest['characters'].items() if value['representations']['raster']['available']}
    require(available=={x['asset_id'] for x in checked if x['available']},'available asset absent from verified index')
    return {'records':checked,'originals_replaced':False}

if __name__=='__main__':print(json.dumps(validate()))
