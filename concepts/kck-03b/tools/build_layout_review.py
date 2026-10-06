"""Read-only QA layout proposal. Does not write masters, production or manifests."""
import hashlib
import json
import platform
import zlib
from pathlib import Path

import PIL
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'artifacts/qa/2026-10-06-raster-layout-proposal'
SOURCES = {
    'cat': ('concepts/kck-03b1/outputs/Cat-B1B-attempt-01.png',
            '1ba744b5b7134e22e5881dd58cc87eec55fc517f2a4a69c74bc7f5a242ce704e'),
    'dinosaur': ('concepts/kck-03b1/outputs/A3-v2d-attempt-01-highlight-corrected.png',
                 '16b7db693942c09c7792eb01a4fd8269c4bd8d402b6c0b3b5be29813fd430d27'),
}
# Manually inspected support contacts, not alpha-derived anchor selection.
ANCHORS = {'cat': (705, 1235), 'dinosaur': (650, 1176)}
FOOT_ANCHOR_CAT = (705, 1144)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fit(bounds, anchor):
    l, t, r, b = bounds
    x, y = anchor
    limits = [896 / (r-l), 896 / (b-t)]
    for extent, room in [(x-l, 448), (r-x, 448), (y-t, 896), (b-y, 64)]:
        if extent > 0:
            limits.append(room / extent)
    return min(limits)


def render(source, anchor, scale):
    # Inverse uniform affine in premultiplied alpha avoids dark RGB fringes.
    # Padded replay proves no resampled nonzero alpha gets cropped by 1024.
    pad = 32
    offset = (512 - anchor[0]*scale, 960 - anchor[1]*scale)
    def transformed(padding):
        return source.convert('RGBa').transform(
            (1024+padding*2, 1024+padding*2), Image.Transform.AFFINE,
            (1/scale, 0, -(offset[0]+padding)/scale,
             0, 1/scale, -(offset[1]+padding)/scale),
            resample=Image.Resampling.BICUBIC).convert('RGBA')
    padded = transformed(pad)
    a = padded.getchannel('A')
    for box in [(0,0,pad,1088), (1056,0,1088,1088),
                (pad,0,1056,pad), (pad,1056,1056,1088)]:
        if a.crop(box).getbbox() is not None:
            raise ValueError('resampled nonzero alpha would be clipped')
    result = transformed(0)
    assert result.tobytes() == padded.crop((pad,pad,pad+1024,pad+1024)).tobytes()
    assert result.tobytes() == transformed(0).tobytes()
    return result


def plot_pair(cat, dino, title, note):
    panel = Image.new('RGB', (580, 354), '#f5f2eb')
    draw = ImageDraw.Draw(panel)
    draw.text((12,10), title, fill='#202d37')
    for index, (im, name) in enumerate([(cat, 'Cat'), (dino, 'Dinosaur')]):
        tile = Image.new('RGBA', (1024,1024), '#e6eeec')
        tile.alpha_composite(im)
        draw_tile = ImageDraw.Draw(tile)
        draw_tile.line((0,960,1024,960), fill='#ca5050', width=4)
        draw_tile.line((500,960,524,960), fill='#202d37', width=5)
        draw_tile.line((512,948,512,972), fill='#202d37', width=5)
        small = tile.resize((260,260), Image.Resampling.LANCZOS).convert('RGB')
        panel.paste(small,(12+index*290,44))
        draw.text((12+index*290,310),name,fill='#202d37')
    draw.text((12,333),note,fill='#202d37')
    return panel


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    sources = {}
    records = {}
    for char, (path, expected) in SOURCES.items():
        raw = (ROOT/path).read_bytes()
        assert sha(raw) == expected, 'wrong source'
        source = Image.open(ROOT/path)
        assert source.mode == 'RGBA' and source.size == (1254,1254)
        sources[char] = source
        bounds = source.getchannel('A').point(lambda a: 255 if a >= 13 else 0).getbbox()
        records[char] = {'source':path, 'sha256':expected, 'rgba8_sha256':sha(source.tobytes()),
                         'canvas':list(source.size), 'visible_bounds_exclusive':list(bounds),
                         'nonzero_alpha_bounds_exclusive':list(source.getchannel('A').getbbox()),
                         'proposed_anchor':list(ANCHORS[char]),
                         'anchor_type':'support-baseline (proposed seated exception)' if char=='cat' else 'ground-center',
                         'safe_fit_scale':fit(bounds,ANCHORS[char]),
                         'icc_profile_present':bool(source.info.get('icc_profile')),
                         'qa_color_policy':'No profile conversion; candidate preview interprets source samples as sRGB; delivery policy pending'}
        native = Image.new('RGBA',source.size,'#e6eeec');native.alpha_composite(source)
        d = ImageDraw.Draw(native)
        for a, color in [(ANCHORS[char],'#d03939')] + ([(FOOT_ANCHOR_CAT,'#386ed0')] if char=='cat' else []):
            d.line((200,a[1],1100,a[1]),fill=color,width=3)
            d.line((a[0]-16,a[1],a[0]+16,a[1]),fill=color,width=5)
            d.line((a[0],a[1]-16,a[0],a[1]+16),fill=color,width=5)
        native.convert('RGB').save(OUT/(char+'-anchor-annotation.png'))
        box=(350,1030,950,1254);crop=native.crop(box).convert('RGB');d=ImageDraw.Draw(crop)
        for x in range(350,951,50):
            d.line((x-350,0,x-350,crop.height),fill='#91a9b2');d.text((x-348,3),str(x),fill='black')
        for y in range(1050,1254,25):
            d.line((0,y-1030,crop.width,y-1030),fill='#91a9b2');d.text((2,y-1028),str(y),fill='black')
        crop.save(OUT/(char+'-foot-measurement-grid.png'))
    options=[];panels=[]
    for label, cv in [('A - smaller Cat',.75),('B - recommended',.80),('C - larger Cat',.85)]:
        images={};entry={'label':label,'parameters':{}}
        for char,v in [('cat',cv),('dinosaur',.95)]:
            scale=records[char]['safe_fit_scale']*v
            im=render(sources[char],ANCHORS[char],scale);images[char]=im
            name=char+'-option-'+label[0].lower()+'.png';im.save(OUT/name,compress_level=9)
            bounds=im.getchannel('A').point(lambda a:255 if a>=13 else 0).getbbox()
            assert bounds[0]>=64 and bounds[2]<=960 and bounds[1]>=64 and bounds[3]<=1024
            entry['parameters'][char]={'visual_scale':v,'final_scale':scale,'qa_png':name,
                                      'file_sha256':sha((OUT/name).read_bytes()),'rgba8_sha256':sha(im.tobytes()),
                                      'delivery_visible_bounds_exclusive':list(bounds),'visible_height_px':bounds[3]-bounds[1],
                                      'projected_anchor':[512,960], 'clipped_nonzero_alpha_pixels':0}
        hcat=entry['parameters']['cat']['visible_height_px'];hdino=entry['parameters']['dinosaur']['visible_height_px']
        entry['visible_height_ratio_cat_to_dinosaur']=hcat/hdino
        panels.append(plot_pair(images['cat'],images['dinosaur'],label,
                     f'Cat {hcat}px / Dino {hdino}px; ratio {hcat/hdino:.0%}; red = support line'))
        options.append(entry)
    review=Image.new('RGB',(580,354*3),'white')
    for i,p in enumerate(panels):review.paste(p,(0,i*354))
    review.save(OUT/'scale-options.png')
    # Cat original feet versus proposed seated support; use conservative .64 foot scale.
    foot=render(sources['cat'],FOOT_ANCHOR_CAT,.64)
    seated=render(sources['cat'],ANCHORS['cat'],records['cat']['safe_fit_scale']*.80)
    comparison=plot_pair(foot,seated,'Cat anchor choice: feet (left) / seated support (right)',
                         'Left: tail below line; right: feet above projected tail contact')
    # Correct the shared helper labels for this Cat-only diagnostic.
    d=ImageDraw.Draw(comparison);d.rectangle((10,306,579,328),fill='#f5f2eb')
    d.text((12,310),'Cat feet anchor (705,1144)',fill='#202d37')
    d.text((302,310),'Cat seated support (705,1235)',fill='#202d37')
    comparison.save(OUT/'cat-anchor-options.png')
    result={'format':'kck-03b-layout-proposal-v1','status':'candidate_QA_only','owner_approval':'pending',
            'tool':'concepts/kck-03b/tools/build_layout_review.py','tool_sha256':sha(Path(__file__).read_bytes()),
            'versions':{'python':platform.python_version(),'Pillow':PIL.__version__,'zlib':zlib.ZLIB_RUNTIME_VERSION},
            'transform':'Uniform inverse AFFINE BICUBIC on premultiplied RGBa, converted back to RGBA; no artwork retouch, alpha cleanup, independent axis stretch or profile conversion',
            'target_canvas':[1024,1024],'target_anchor':[512,960],'visible_threshold':'alpha>=13 (>5% of 255)',
            'sources':records,'scale_options':options,
            'cat_contact_problem':{'feet_anchor':list(FOOT_ANCHOR_CAT),'proposed_seated_support_anchor':list(ANCHORS['cat']),
                'vertical_difference_source_px':91,'reason':'Resting foreground tail projects lower than feet. Feet anchoring would put tail below a flat ground line. Proposed seated support uses manually inspected tail-contact tangent, not automatic alpha minimum.',
                'requires_contract_decision':'Extend support-baseline to footed seated poses; feet remain about 54 delivery pixels above projected foreground support at option B. Owner must accept the perspective convention or request a new pose.'},
            'checks':['Source raw hashes fixed','Source files rehashed unchanged after preview','Each transform repeated with identical RGBA pixels','Padded affine replay identical inside and zero nonzero-alpha clipping','Visible bounds satisfy left/right/top safe margin and bottom canvas limit'],
            'not_claimed':['Master selection','Approved contract change','Production normalization or availability','Rights clearance','Ground contact in a consumer scene']}
    for char,(path,expected) in SOURCES.items():assert sha((ROOT/path).read_bytes())==expected
    (OUT/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'options':[(x['label'],round(x['visible_height_ratio_cat_to_dinosaur'],3)) for x in options], 'status':result['status']}))


if __name__=='__main__':
    main()
