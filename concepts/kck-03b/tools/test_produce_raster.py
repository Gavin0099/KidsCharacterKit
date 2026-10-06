"""Actual-master and independent geometry regressions for the 03B transform."""
import copy
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from jsonschema import Draft202012Validator, ValidationError

import produce_raster as tool


class RasterDelivery(unittest.TestCase):
    def test_actual_masters_layout_pixels_and_alpha(self):
        # Independently calculated from reviewed bounds/semantic contacts.
        expected={'cat':(.7472894078398665,(705,1235),.80),
                  'dinosaur':(.8064806480648065,(650,1176),.95)}
        for char,(safe,anchor,v) in expected.items():
            with Image.open(tool.ROOT/tool.layout.SOURCES[char][0]) as source:
                before=source.tobytes()
                result,computed,scale,bounds,visible=tool.normalize(source,anchor,v)
                self.assertAlmostEqual(computed,safe,places=12)
                self.assertAlmostEqual(scale,safe*v,places=12)
                self.assertEqual(source.tobytes(),before)
                self.assertEqual(result.size,(1024,1024))
                self.assertEqual(result.mode,'RGBA')
                self.assertGreater(result.getchannel('A').histogram()[0],0)
                self.assertEqual(result.getpixel((0,0))[3],0)
                self.assertGreaterEqual(visible[0],64)
                self.assertGreaterEqual(visible[1],64)
                self.assertLessEqual(visible[2],960)
                encoded=tool.encode(result);decoded=Image.open(io.BytesIO(encoded))
                self.assertTrue(tool.has_srgb(encoded))
                self.assertEqual(decoded.tobytes(),result.tobytes())
                again,*_=tool.normalize(source,anchor,v)
                self.assertEqual(again.tobytes(),result.tobytes())
                self.assertEqual(tool.encode(again),encoded)

    def test_semantic_anchor_keeps_independent_uniform_geometry(self):
        # A plus mark around a non-bounds anchor must land at (512,960).
        source=Image.new('RGBA',(200,200))
        for x in range(65,96):
            for y in range(155,166):source.putpixel((x,y),(255,20,10,255))
        for x in range(75,86):
            for y in range(145,176):source.putpixel((x,y),(255,20,10,255))
        result,_,scale,_,_=tool.normalize(source,(80,160),.10)
        self.assertGreater(result.getpixel((512,960))[3],200)
        box=result.getchannel('A').getbbox()
        self.assertLessEqual(abs((box[2]-box[0])-(box[3]-box[1])),1)
        self.assertGreater(scale,0)

    def test_faint_nonzero_alpha_is_not_silently_cropped(self):
        source=Image.new('RGBA',(100,100))
        for x in range(20,80):
            for y in range(10,80):source.putpixel((x,y),(50,80,90,255))
        source.putpixel((99,99),(40,70,80,1))
        with self.assertRaisesRegex(ValueError,'clip'):
            tool.normalize(source,(50,80),1)
        with self.assertRaisesRegex(ValueError,'scale'):
            tool.normalize(source,(50,80),float('nan'))
        with self.assertRaisesRegex(ValueError,'anchor'):
            tool.normalize(source,(-1,80),.5)
        source.info['icc_profile']=b'unreviewed'
        with self.assertRaisesRegex(ValueError,'profile'):
            tool.normalize(source,(50,80),.5)

    def test_refuses_wrong_source_and_overwrite(self):
        original=tool.repo_file
        def altered(path):
            if path==tool.layout.SOURCES['cat'][0]:
                return tool.ROOT/'docs/asset-spec.md'
            return original(path)
        with patch.object(tool,'repo_file',side_effect=altered):
            with self.assertRaisesRegex(ValueError,'hash mismatch'):tool.prepare()
        # Publication checks happen before a single write, with a cheap fixture.
        with patch.object(tool,'prepare',return_value={'docs/asset-spec.md':b'bad'}):
            before=(tool.ROOT/'docs/asset-spec.md').read_bytes()
            with self.assertRaisesRegex(ValueError,'overwrite'):tool.build()
            self.assertEqual((tool.ROOT/'docs/asset-spec.md').read_bytes(),before)
        with self.assertRaisesRegex(ValueError,'outside'):tool.repo_file('../escape')

    def test_record_and_manifest_schema_negative_cases(self):
        provenance=Draft202012Validator(json.loads((tool.ROOT/'provenance/schema/provenance.schema.json').read_text()))
        files=tool.prepare()
        delivery=next(json.loads(raw) for path,raw in files.items() if path.endswith('-delivery.json'))
        provenance.validate(delivery)
        for key in ['input','master_provenance','rights','parameters','status_evidence']:
            bad=copy.deepcopy(delivery);del bad[key]
            with self.assertRaises(ValidationError):provenance.validate(bad)
        bad=copy.deepcopy(delivery);bad['qa']['clipped_nonzero_alpha_pixels']=1
        with self.assertRaises(ValidationError):provenance.validate(bad)
        manifest=json.loads((tool.ROOT/'manifests/characters.json').read_text())
        validator=Draft202012Validator(json.loads((tool.ROOT/'manifests/character-manifest.schema.json').read_text()))
        validator.validate(manifest)
        raster=manifest['characters']['cat-02']['representations']['raster']
        raster['style_version']='soft-handmade-v1'
        with self.assertRaises(ValidationError):validator.validate(manifest)


if __name__=='__main__':unittest.main()
