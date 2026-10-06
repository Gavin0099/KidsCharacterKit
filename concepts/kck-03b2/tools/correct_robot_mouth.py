"""Owner-authorized, hash-bound mouth-only composite into the full original Robot.

The generated donor failed full-body crop QA. Its body is never used. RGB is
registered locally at one uniform scale and feathered inside the mouth ROI;
every original alpha and every RGBA pixel outside that ROI stays exact.
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

SOURCE_SHA='6865f582ac502ecd73574c06aa1328e574712a63175beaba8662cb575bd85216'
DONOR_SHA='3a0c3799d4ebf861c685aad3e8e948ca9ffa1a2251ac5a9202a01628726e3387'
ROI=(512,392,650,520)
SCALE=116/121
# Observed mouth contour bounds: original [523,403,639,508], donor [529,412,650,511].
OFFSET=(523-SCALE*529,403-SCALE*412)
AUTH='concepts/kck-03b2/evidence/2026-10-06-owner-robot-local-mouth-continuation.json'

def decode(raw,expected):
    if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('Source/donor hash mismatch')
    with Image.open(io.BytesIO(raw)) as im:
        if im.mode!='RGBA' or im.size!=(1086,1448):raise ValueError('Expected native RGBA 1086x1448')
        return im.copy()

def repair(source_raw,donor_raw):
    source=decode(source_raw,SOURCE_SHA);donor=decode(donor_raw,DONOR_SHA)
    x0,y0,x1,y1=ROI;width,height=x1-x0,y1-y0
    matrix=(1/SCALE,0,(x0-OFFSET[0])/SCALE,0,1/SCALE,(y0-OFFSET[1])/SCALE)
    registered=donor.transform((width,height),Image.Transform.AFFINE,matrix,Image.Resampling.BICUBIC)
    src=np.array(source);insert=np.array(registered);local=src[y0:y1,x0:x1]
    if np.any(local[:,:,3]<200) or np.any(insert[:,:,3]<200):raise ValueError('Mouth patch must stay inside opaque head interior')
    yy,xx=np.indices((height,width));distance=np.minimum.reduce([xx,width-1-xx,yy,height-1-yy])
    weight=np.minimum(distance/8,1)[:,:,None]
    # Match cold-gray background using the inspected mouth-free outer border.
    border=distance<8
    offset=np.median(local[border,:3].astype(float)-insert[border,:3].astype(float),axis=0)
    matched=np.clip(insert[:,:,:3].astype(float)+offset,0,255)
    out=src.copy();out[y0:y1,x0:x1,:3]=np.rint(local[:,:,:3]*(1-weight)+matched*weight).astype(np.uint8)
    changed=np.any(out!=src,axis=2);mask=np.zeros(changed.shape,bool);mask[y0:y1,x0:x1]=True
    if not np.array_equal(src[:,:,3],out[:,:,3]) or np.any(changed&~mask):raise AssertionError('Alpha/outside violation')
    ys,xs=np.where(changed)
    return Image.fromarray(out),{'allowed_roi_exclusive':list(ROI),'changed_bbox_exclusive':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'changed_pixels':int(changed.sum()),'uniform_donor_scale':SCALE,'donor_translation':list(OFFSET),'rgb_border_median_offset':offset.tolist(),'feather_width_px':8,'all_alpha_equal':True,'outside_roi_rgba_equal':True,'body_and_boots_equal':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('donor',type=Path);parser.add_argument('output',type=Path);parser.add_argument('--record',type=Path,required=True);a=parser.parse_args()
    if len({p.resolve() for p in [a.source,a.donor,a.output,a.record]})!=4 or a.output.exists() or a.record.exists():parser.error('No overwrites or shared source/output paths')
    image,patch=repair(a.source.read_bytes(),a.donor.read_bytes())
    raw=io.BytesIO();image.save(raw,format='PNG',compress_level=9);encoded=raw.getvalue()
    record={'record_type':'deterministic_candidate_derivation','date':'2026-10-06','status':'candidate','owner_authorization':AUTH,'input':{'path':str(a.source),'raw_sha256':SOURCE_SHA},'donor':{'path':str(a.donor),'raw_sha256':DONOR_SHA,'failure':'Full-body cropped right boot; mouth RGB only is sampled'},'output':{'path':str(a.output),'raw_sha256':hashlib.sha256(encoded).hexdigest(),'rgba8_sha256':hashlib.sha256(image.tobytes()).hexdigest(),'dimensions':list(image.size)},'method':'One uniform BICUBIC donor registration; cold-gray border RGB match; bounded feathered mouth composite. All original alpha and outside RGBA exact.','patch':patch,'tool':{'path':str(Path(__file__).relative_to(Path.cwd())),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'Python':platform.python_version(),'Pillow':PIL.__version__,'numpy':np.__version__},'image_generation_calls':0,'dinosaur_v2d_budget':{'used':2,'maximum':2,'remaining':0}}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.record.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('xb') as stream:stream.write(encoded)
    try:
        with a.record.open('x') as stream:json.dump(record,stream,ensure_ascii=False,indent=2);stream.write('\n')
    except Exception:
        a.output.unlink();raise
    print(json.dumps(record['output']))

if __name__=='__main__':main()
