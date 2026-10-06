from pathlib import Path
import sys,json,hashlib,shutil,os
from PIL import Image
import numpy as np
r=Path(__file__).resolve().parents[3];b=r/'concepts/kck-03b2';p=b/os.environ.get('KCK_ROBOT_LEDGER','robot-model-sheet-jobs.json');d=json.loads(p.read_text());j=next(x for x in d['jobs'] if x['job_id']==sys.argv[2])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
if sys.argv[1]=='register':
 assert j['calls']==0 and j['status']=='planned';assert sha(r/j['reference'])==j['reference_sha256'];assert sha(r/j['instruction'])==j['instruction_sha256'];
 if j.get('edit_target'):assert sha(r/j['edit_target'])==j['edit_target_sha256'] and (r/j['authorization']).is_file()
 elif j.get('requires_pass'):assert next(x for x in d['jobs']+d.get('derivations',[]) if x['job_id']==j['requires_pass']).get('agent_hard_gate')=='PASS'
 else:assert not any(x.get('agent_hard_gate')=='FAIL' for x in d['jobs'] if x['character']==j['character'])
 j.update(status='submitted',calls=1);put(p,d);print((r/j['instruction']).read_text(),end='');sys.exit()
assert sys.argv[1]=='save' and j['calls']==1 and j['status']=='submitted'
source=Path(sys.argv[3]);out=b/'outputs'/f"{j['job_id']}.png";assert not out.exists();out.parent.mkdir(exist_ok=True);shutil.copyfile(source,out);assert sha(source)==sha(out)
with Image.open(out) as im:
 a=np.array(im);mode=im.mode;w,h=im.size;fmt=im.format
assert mode=='RGBA' and fmt=='PNG';alpha=a[:,:,3];ys,xs=np.where(alpha>10);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
ep=b/'evidence'/f"{j['job_id']}-qa.json";eprel=str(ep.relative_to(r));gate=sys.argv[4];notes=sys.argv[5]
struct={'canvas':[w,h],'mode':mode,'raw_sha256':sha(out),'rgba8_sha256':hashlib.sha256(a.tobytes()).hexdigest(),'bytes':out.stat().st_size,'alpha_zero':int((alpha==0).sum()),'alpha_partial':int(((alpha>0)&(alpha<255)).sum()),'alpha_opaque':int((alpha==255).sum()),'alpha_gt10_bbox_exclusive':bounds,'corners':[int(alpha[y,x]) for y,x in [(0,0),(0,-1),(-1,0),(-1,-1)]]}
put(ep,{'job_id':j['job_id'],'copy':'Exact byte copy of built-in saved output; no image editing','structural':struct,'agent_hard_gate':gate,'agent_visual_review':notes,'owner_acceptance':'pending','not_proven':['Generator-held input hashes','Unseen anatomy correctness','Production scale or semantic ground anchor','Rights']})
views=['front','three-quarter','side','back','happy','confused'];cid=j.get('concept_id_reserved') or f"{j['character']}-concept-{(2 if j['character']=='cat' else 5)+views.index(j['view']):02d}"
file={'path':str(out.relative_to(r)),'format':'png','width':w,'height':h,'color_type':mode,'bytes':out.stat().st_size,'sha256':sha(out),'relationship_to_original':'Exact byte copy of built-in saved output; no post-generation pixel edits'}
inputs=[{'name':j['reference'],'role':'Only Owner-approved identity/rendering reference','sha256':j['reference_sha256'],'bytes':(r/j['reference']).stat().st_size},{'name':j['instruction'],'role':'Exact text passed as built-in tool prompt','sha256':j['instruction_sha256'],'bytes':(r/j['instruction']).stat().st_size},{'name':d['specification']['path'],'role':'Owner-approved drawing specification informing saved instruction; not separately mounted','sha256':d['specification']['sha256'],'bytes':(r/d['specification']['path']).stat().st_size}]
rec={'schema_version':1,'record_type':'concept','id':cid,'character':j['character'],'slice':d.get('slice','KCK-03B2'),'stage':j.get('stage','model-sheet'),'variant':j['view']+' initial individual model-sheet candidate','status':'candidate','status_evidence':[{'decision':'Owner authorizes scoped asset preparation with conditional acceptance only after actual conformance checks','date':'2026-10-06','stated_in':d['authorization'],'quote':d['authorization_quote']}],'file':file,'original_artifact':{k:v for k,v in file.items() if k not in ['path','relationship_to_original']},'inputs':{'requested':inputs,'actually_mounted':[],'canonical_match':False},'generation':{'tool':'image_gen.imagegen','model':None,'generation_id':None,'prompt':{'version':'model-sheet v1','path':j['instruction'],'locator':'Entire UTF-8 file passed as prompt','instruction_file':{'name':Path(j['instruction']).name,'bytes':inputs[1]['bytes'],'sha256':j['instruction_sha256'],'attached_in_generation':False}},'execution_message':{'text':(r/j['instruction']).read_text(),'certified_sole_message':False},'fresh_context':'unknown','post_generation_pixel_edit':False},'registration':{'status':'registered','valid_attempt_number':1,'counts_toward_budget':False,'basis':'Separate authorized 03B2 initial job; 1 call per sheet. Does not consume or reset exhausted Dinosaur v2d 2/2 ledger; no retry inferred.'},'deviations':['Generator-held input hashes/internal augmented prompt/model/seed/id not exposed; canonical_match=false means match not established, not mismatch.','Unseen side/back anatomy is proposed for Owner review, never inferred as previously approved.'],'measurements':[{'actor':'Codex structural and visual review','copy':{'description':'Exact saved tool PNG','format':'png','sha256':sha(out)},'reference_for_comparison':j['reference'],'method':'Direct visual review plus decoded RGBA8/alpha measurements; source canvases not fit independently','results':{'structural':struct,'agent_hard_gate':gate,'visual_review':notes,'owner_acceptance':'pending'}}],'owner_review':{'variant_intensity':'pending','overall_identity':'pending','note':'Approval of input reference/v1 does not approve this new sheet'},'rights':{'commercial_use_status':'pending','rights_review_status':'unknown','ownership_status':'unknown','statements':[]},'evidence':[{'path':d['authorization'],'supports':'Model-sheet preparation authorization and exact approved references'}, {'path':str(p.relative_to(r)),'supports':'Registered initial job, bounded calls and immutable prompt/source hashes'}, {'path':eprel,'supports':'Structural facts and independent agent review; Owner acceptance pending'}],'unresolved_questions':['Conditional conformance evidence including 64px required before reference acceptance','Unseen anatomy/side and pose continuity','Production, visual_scale, anchors and rights unresolved']}

if j.get('edit_target'):
 inputs.append({'name':j['edit_target'],'role':'Failed side image edit target, retained unchanged','sha256':j['edit_target_sha256'],'bytes':(r/j['edit_target']).stat().st_size})
 rec['variant']=j['view']+' Owner-authorized targeted correction candidate'
 rec['status_evidence'].append({'decision':'Owner explicitly authorizes one side correction, not output acceptance','date':'2026-10-06','stated_in':j['authorization'],'quote':'ok沒問題 往下做'})
 rec['evidence'].append({'path':j['authorization'],'supports':'Explicit bounded side correction and conditional continuation'})
 rec['registration']['basis']='One Owner-authorized side correction call; failed original kept. Separate 03B2 scope, no Dino v2d reset.'

rec['original_artifact'].update(held_in_repo=True,basis=f'Exact byte copy of built-in saved PNG {source.name}; output filename is not a model generation id')
rp=out.with_suffix('.provenance.json');put(rp,rec);j.update(status='candidate_recorded',agent_hard_gate=gate,output=str(out.relative_to(r)),output_sha256=sha(out),provenance=str(rp.relative_to(r)),concept_id=cid,qa=eprel)
if gate=='PASS' and j.get('kind')=='authorized_targeted_correction':
 for x in d['jobs']:
  if x.get('requires_pass')==j['job_id'] and x['status']=='blocked_after_hard_failure':
   x['status_history']=[{'status':'blocked_after_hard_failure','reason':'Original side failure'},{'status':'planned','reason':'Owner-authorized correction passed agent checks','evidence':j['authorization']}]
   x['status']='planned'
if gate=='FAIL':
 for x in d['jobs']:
  if x['character']==j['character'] and x['status']=='planned':x['status']='blocked_after_hard_failure'
put(p,d);print(json.dumps({'saved':str(out),'sha256':sha(out),'dimensions':[w,h],'agent_hard_gate':gate}))
